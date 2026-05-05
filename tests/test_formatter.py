"""Tests for the markdown formatter module."""

from recipe_extractor.formatter import format_recipe


class TestFormatRecipe:
    def test_formats_complete_recipe(self):
        recipe = {
            "dish_name": "Pasta Carbonara",
            "ingredients": ["200g spaghetti", "100g pancetta", "2 eggs", "50g parmesan"],
            "steps": [
                "Boil pasta in salted water until al dente.",
                "Fry pancetta until crispy.",
                "Mix eggs and parmesan in a bowl.",
                "Toss hot pasta with pancetta, then stir in egg mixture.",
            ],
        }

        result = format_recipe(recipe)

        assert result.startswith("# Pasta Carbonara\n")
        assert "## Ingredients" in result
        assert "- 200g spaghetti" in result
        assert "- 50g parmesan" in result
        assert "## Steps" in result
        assert "1. Boil pasta in salted water until al dente." in result
        assert "4. Toss hot pasta with pancetta, then stir in egg mixture." in result

    def test_single_ingredient_and_step(self):
        recipe = {
            "dish_name": "Toast",
            "ingredients": ["1 slice bread"],
            "steps": ["Toast the bread."],
        }

        result = format_recipe(recipe)

        assert "# Toast" in result
        assert "- 1 slice bread" in result
        assert "1. Toast the bread." in result

    def test_output_ends_with_newline(self):
        recipe = {
            "dish_name": "Test",
            "ingredients": ["item"],
            "steps": ["Do thing."],
        }
        result = format_recipe(recipe)
        assert result.endswith("\n")
