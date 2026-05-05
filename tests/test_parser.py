"""Tests for the LLM recipe parser module."""

import json

import pytest

from recipe_extractor.parser import parse_recipe, get_client, SYSTEM_PROMPT


class TestGetClient:
    def test_raises_without_token(self, monkeypatch):
        monkeypatch.delenv("GITHUB_TOKEN", raising=False)
        with pytest.raises(EnvironmentError, match="GITHUB_TOKEN"):
            get_client()

    def test_creates_client_with_token(self, monkeypatch):
        monkeypatch.setenv("GITHUB_TOKEN", "test-token")
        client = get_client()
        assert client.api_key == "test-token"


class TestParseRecipe:
    def test_extracts_recipe(self, mocker):
        recipe_response = json.dumps({
            "is_recipe": True,
            "dish_name": "Pasta Carbonara",
            "ingredients": ["200g spaghetti", "100g pancetta", "2 eggs"],
            "steps": ["Boil pasta.", "Fry pancetta.", "Mix eggs and cheese."],
        })

        mock_message = mocker.Mock()
        mock_message.content = recipe_response
        mock_choice = mocker.Mock()
        mock_choice.message = mock_message
        mock_response = mocker.Mock()
        mock_response.choices = [mock_choice]

        mock_client = mocker.Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mocker.patch("recipe_extractor.parser.get_client", return_value=mock_client)

        result = parse_recipe("today we're making carbonara...")

        assert result["is_recipe"] is True
        assert result["dish_name"] == "Pasta Carbonara"
        assert len(result["ingredients"]) == 3
        assert len(result["steps"]) == 3

    def test_detects_non_recipe(self, mocker):
        non_recipe_response = json.dumps({
            "is_recipe": False,
            "reason": "This video is a tech review, not a cooking tutorial.",
        })

        mock_message = mocker.Mock()
        mock_message.content = non_recipe_response
        mock_choice = mocker.Mock()
        mock_choice.message = mock_message
        mock_response = mocker.Mock()
        mock_response.choices = [mock_choice]

        mock_client = mocker.Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mocker.patch("recipe_extractor.parser.get_client", return_value=mock_client)

        result = parse_recipe("hey guys today we're reviewing the new iPhone...")

        assert result["is_recipe"] is False
        assert "reason" in result

    def test_handles_code_fenced_response(self, mocker):
        fenced = "```json\n" + json.dumps({"is_recipe": False, "reason": "Not food"}) + "\n```"

        mock_message = mocker.Mock()
        mock_message.content = fenced
        mock_choice = mocker.Mock()
        mock_choice.message = mock_message
        mock_response = mocker.Mock()
        mock_response.choices = [mock_choice]

        mock_client = mocker.Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mocker.patch("recipe_extractor.parser.get_client", return_value=mock_client)

        result = parse_recipe("some transcript")
        assert result["is_recipe"] is False

    def test_raises_on_invalid_json(self, mocker):
        mock_message = mocker.Mock()
        mock_message.content = "This is not JSON at all"
        mock_choice = mocker.Mock()
        mock_choice.message = mock_message
        mock_response = mocker.Mock()
        mock_response.choices = [mock_choice]

        mock_client = mocker.Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mocker.patch("recipe_extractor.parser.get_client", return_value=mock_client)

        with pytest.raises(ValueError, match="Failed to parse LLM response"):
            parse_recipe("some transcript")
