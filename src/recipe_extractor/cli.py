"""CLI entry point for the recipe extractor."""

import sys

import click

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
    except Exception as e:
        click.echo(f"Error fetching transcript: {e}", err=True)
        sys.exit(1)

    click.echo("Extracting recipe with AI...")

    try:
        recipe = parse_recipe(transcript)
    except EnvironmentError as e:
        click.echo(f"Configuration error: {e}", err=True)
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
