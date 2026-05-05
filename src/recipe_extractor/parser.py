"""LLM-based recipe extraction from video transcripts."""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# Load .env from project root
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

GITHUB_MODELS_ENDPOINT = "https://models.github.ai/inference"
DEFAULT_MODEL = "openai/gpt-4o"

SYSTEM_PROMPT = """\
You are a recipe extraction assistant. You will be given a transcript from a YouTube video.

Your job is to determine if the video contains a cooking recipe. If it does, extract:
1. The dish name
2. A list of ingredients with quantities
3. The step-by-step cooking instructions

Respond ONLY with valid JSON in this exact format:

If the video contains a recipe:
{
  "is_recipe": true,
  "dish_name": "Name of the dish",
  "ingredients": [
    "500g chicken breast, cubed",
    "1 cup yogurt"
  ],
  "steps": [
    "Marinate the chicken in yogurt and spices for 1 hour.",
    "Heat oil in a large pan over medium-high heat."
  ]
}

If the video does NOT contain a recipe:
{
  "is_recipe": false,
  "reason": "Brief explanation of why this is not a recipe video."
}

Rules:
- Include specific quantities for ingredients when mentioned.
- Write steps as clear, concise imperative sentences.
- Combine related sub-steps into single steps where logical.
- Do not invent ingredients or steps not mentioned in the transcript.
- If quantities are unclear, use approximate terms like "to taste" or "a handful".
"""


def get_client() -> OpenAI:
    """Create an OpenAI client configured for GitHub Models."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise EnvironmentError(
            "GITHUB_TOKEN environment variable is required. "
            "Generate one at https://github.com/settings/tokens or run: gh auth token"
        )
    return OpenAI(base_url=GITHUB_MODELS_ENDPOINT, api_key=token)


def parse_recipe(transcript: str, model: str = DEFAULT_MODEL) -> dict:
    """Send a transcript to the LLM and extract structured recipe data.

    Args:
        transcript: The full text transcript from a YouTube video.
        model: The model to use (default: gpt-4o).

    Returns:
        A dict with keys:
            - is_recipe (bool)
            - dish_name (str) — if is_recipe
            - ingredients (list[str]) — if is_recipe
            - steps (list[str]) — if is_recipe
            - reason (str) — if not is_recipe

    Raises:
        EnvironmentError: If GITHUB_TOKEN is not set.
        ValueError: If the LLM response cannot be parsed as JSON.
    """
    client = get_client()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Here is the video transcript:\n\n{transcript}"},
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content.strip()

    # Strip markdown code fences if present
    if content.startswith("```"):
        content = content.split("\n", 1)[1]
        content = content.rsplit("```", 1)[0]

    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM response as JSON: {e}\nRaw: {content}")
