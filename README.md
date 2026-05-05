# YouTube Recipe Extractor

A CLI tool that extracts recipes from YouTube cooking videos and formats them as clean markdown. Simply paste a YouTube URL and get a structured list of ingredients and steps — no need to watch the entire video.

## How It Works

1. Fetches the video transcript (captions) from YouTube
2. Sends the transcript to OpenAI GPT-4o to identify and extract the recipe
3. Outputs a formatted markdown file with the dish name, ingredients, and steps

## Installation

```bash
# Clone the repo
git clone https://github.com/jacksonsbarnett/youtube-recipe-extractor.git
cd youtube-recipe-extractor

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install the package
pip install -e .
```

## Configuration

Create a `.env` file in the project root with your GitHub token:

```bash
# Get your token (requires gh CLI to be authenticated)
gh auth token

# Create the .env file
echo "GITHUB_TOKEN=$(gh auth token)" > .env
```

Or manually create `.env`:

```
GITHUB_TOKEN=your-github-token-here
```

The token is used to access GitHub Models (GPT-4o) for recipe extraction — no billing required.

## Usage

```bash
# Basic usage — prints markdown to stdout
recipe-extractor https://www.youtube.com/watch?v=VIDEO_ID

# Save to a file
recipe-extractor https://www.youtube.com/watch?v=VIDEO_ID --output recipe.md
```

## Example Output

```markdown
# Chicken Tikka Masala

## Ingredients

- 500g chicken breast, cubed
- 1 cup plain yogurt
- 2 tbsp tikka masala paste
- 1 can (400ml) crushed tomatoes
- 1 cup heavy cream
- 1 large onion, diced
- 3 cloves garlic, minced
- Salt and pepper to taste

## Steps

1. Marinate the chicken in yogurt and spices for at least 1 hour.
2. Heat oil in a large pan over medium-high heat and cook the chicken until browned.
3. In the same pan, sauté onion and garlic until softened.
4. Add crushed tomatoes and simmer for 10 minutes.
5. Stir in heavy cream and return the chicken to the pan.
6. Simmer for another 10 minutes until the sauce thickens. Season to taste.
```

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## Requirements

- Python 3.11+
- A GitHub account (for free access to GitHub Models)
- `gh` CLI authenticated (`gh auth login`)
- YouTube videos must have captions/subtitles available

## License

MIT
