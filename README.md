# YouTube Recipe Extractor

A CLI tool that extracts recipes from YouTube cooking videos and formats them as clean markdown. Simply paste a YouTube URL and get a structured list of ingredients and steps — no need to watch the entire video.

## How It Works

1. Fetches the video transcript (captions) from YouTube
2. Sends the transcript to GPT-4o-mini via GitHub Models to identify and extract the recipe
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

This tool uses [GitHub Models](https://github.com/marketplace/models) (free) for AI-powered recipe extraction. You'll need a GitHub Personal Access Token (PAT) with model permissions.

### Creating your token

1. Go to [github.com/settings/tokens?type=beta](https://github.com/settings/tokens?type=beta) (Fine-grained tokens)
2. Click **"Generate new token"**
3. Give it a name (e.g., `recipe-extractor`)
4. Set an expiration (e.g., 90 days)
5. Under **Account permissions**, set **"Models"** to **"Read"**
6. Click **"Generate token"** and copy the value

> ⚠️ The `models:read` permission is required. Without it, you'll get a `403 no_access` error.

### Setting up the `.env` file

Create a `.env` file in the project root:

```
GITHUB_TOKEN=github_pat_xxxxx...
```

The token is used to access GitHub Models (GPT-4o-mini) for recipe extraction — no billing required.

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
- A fine-grained PAT with `models:read` permission (see [Configuration](#configuration))
- YouTube videos must have English captions/subtitles available

## Troubleshooting

| Error | Solution |
|-------|----------|
| `403 no_access` | Your token is missing the `models:read` permission. Edit it at [github.com/settings/tokens](https://github.com/settings/tokens). |
| `Authentication failed` | Your token may be expired. Regenerate it. |
| `Transcripts are disabled` | The video owner hasn't enabled captions. Try a different video. |
| `No English transcript found` | The video only has non-English captions. |
| `Connection error` | Check your internet connection. |

## License

MIT
