"""Format structured recipe data as markdown."""


def format_recipe(recipe: dict) -> str:
    """Convert a parsed recipe dict into a formatted markdown string.

    Args:
        recipe: A dict with keys: dish_name, ingredients, steps.

    Returns:
        A markdown-formatted string.
    """
    lines = [f"# {recipe['dish_name']}", ""]

    lines.append("## Ingredients")
    lines.append("")
    for ingredient in recipe["ingredients"]:
        lines.append(f"- {ingredient}")

    lines.append("")
    lines.append("## Steps")
    lines.append("")
    for i, step in enumerate(recipe["steps"], 1):
        lines.append(f"{i}. {step}")

    lines.append("")
    return "\n".join(lines)
