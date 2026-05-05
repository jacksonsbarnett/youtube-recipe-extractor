"""CLI entry point for the recipe extractor."""

import sys

import click
from openai import APIConnectionError, AuthenticationError, RateLimitError
from youtube_transcript_api import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
)

from recipe_extractor.formatter import format_recipe
from recipe_extractor.parser import parse_recipe
from recipe_extractor.transcript import fetch_transcript


@click.command()
@click.argument("url")
@click.option("--output", "-o", type=click.Path(), help="Output file path (default: print to stdout)")
def main(url: str, output: str | None) -> None:
    """Extract a recipe from a YouTube cooking video.

    URL is the YouTube video link to extract a recipe from.
    """
    click.echo(f"Fetching transcript from: {url}")

    try:
        transcript = fetch_transcript(url)
    except ValueError as e:
        click.echo(f"Invalid URL: {e}", err=True)
        sys.exit(1)
    except TranscriptsDisabled:
        click.echo(
            "Error: Transcripts are disabled for this video. "
            "The video owner has not enabled captions.",
            err=True,
        )
        sys.exit(1)
    except NoTranscriptFound:
        click.echo(
            "Error: No English transcript found for this video. "
            "Only videos with English captions are supported.",
            err=True,
        )
        sys.exit(1)
    except VideoUnavailable:
        click.echo(
            "Error: Video is unavailable. It may be private, deleted, or region-locked.",
            err=True,
        )
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error fetching transcript: {e}", err=True)
        sys.exit(1)

    click.echo("Extracting recipe with AI...")

    try:
        recipe = parse_recipe(transcript)
    except EnvironmentError as e:
        click.echo(f"Configuration error: {e}", err=True)
        click.echo("Hint: Make sure GITHUB_TOKEN is set in your .env file.", err=True)
        sys.exit(1)
    except AuthenticationError:
        click.echo(
            "Error: Authentication failed. Your GitHub token may be invalid or expired.\n"
            "Regenerate it at: https://github.com/settings/tokens",
            err=True,
        )
        sys.exit(1)
    except RateLimitError:
        click.echo(
            "Error: Rate limit exceeded. GitHub Models free tier has usage limits.\n"
            "Wait a moment and try again.",
            err=True,
        )
        sys.exit(1)
    except APIConnectionError:
        click.echo(
            "Error: Could not connect to GitHub Models API. Check your internet connection.",
            err=True,
        )
        sys.exit(1)
    except ValueError as e:
        click.echo(f"Error: Failed to parse AI response: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error parsing recipe: {e}", err=True)
        sys.exit(1)

    if not recipe["is_recipe"]:
        click.echo(f"This doesn't appear to be a recipe video: {recipe['reason']}")
        sys.exit(0)

    markdown = format_recipe(recipe)

    if output:
        with open(output, "w") as f:
            f.write(markdown)
        click.echo(f"Recipe saved to: {output}")
    else:
        click.echo("")
        click.echo(markdown)
