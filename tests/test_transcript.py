"""Tests for the transcript fetcher module."""

import pytest

from recipe_extractor.transcript import extract_video_id, fetch_transcript


class TestExtractVideoId:
    def test_standard_url(self):
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        assert extract_video_id(url) == "dQw4w9WgXcQ"

    def test_short_url(self):
        url = "https://youtu.be/dQw4w9WgXcQ"
        assert extract_video_id(url) == "dQw4w9WgXcQ"

    def test_embed_url(self):
        url = "https://www.youtube.com/embed/dQw4w9WgXcQ"
        assert extract_video_id(url) == "dQw4w9WgXcQ"

    def test_url_with_extra_params(self):
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=120"
        assert extract_video_id(url) == "dQw4w9WgXcQ"

    def test_invalid_url_raises(self):
        with pytest.raises(ValueError):
            extract_video_id("https://www.example.com/not-a-video")


class TestFetchTranscript:
    def test_returns_joined_text(self, mocker):
        mock_snippet_1 = mocker.Mock()
        mock_snippet_1.text = "Hello everyone"
        mock_snippet_2 = mocker.Mock()
        mock_snippet_2.text = "today we're making pasta"

        mock_api_instance = mocker.Mock()
        mock_api_instance.fetch.return_value = [mock_snippet_1, mock_snippet_2]

        mocker.patch(
            "recipe_extractor.transcript.YouTubeTranscriptApi",
            return_value=mock_api_instance,
        )

        result = fetch_transcript("https://www.youtube.com/watch?v=abc12345678")

        assert result == "Hello everyone today we're making pasta"
        mock_api_instance.fetch.assert_called_once_with("abc12345678", languages=["en"])
