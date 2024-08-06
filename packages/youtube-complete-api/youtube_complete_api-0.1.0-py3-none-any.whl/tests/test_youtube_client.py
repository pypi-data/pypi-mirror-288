import pytest
from unittest.mock import patch
from youtube_complete_api import YouTubeClient

@pytest.fixture
def youtube_client():
    """Fixture to create a YouTubeClient instance with a dummy API key."""
    return YouTubeClient(api_key="dummy_api_key")

@patch('youtube_complete_api.YouTubeDataAPI.get_video_details')
def test_get_video_details(mock_get_video_details, youtube_client):
    """Test getting video details."""
    # Setup the mock to return a specific value
    expected_details = {'title': 'Test Video', 'description': 'A test video description'}
    mock_get_video_details.return_value = expected_details

    # Call the function
    details = youtube_client.get_video_details('dummy_video_id')

    # Assert that the returned details match the expected details
    mock_get_video_details.assert_called_once_with('dummy_video_id')
    assert details == expected_details, "The details should match the mock response"

@patch('youtube_complete_api.YouTubeTranscriptApi.get_transcript')
def test_get_transcript(mock_get_transcript, youtube_client):
    """Test getting video transcripts."""
    # Setup the mock to return a specific value
    expected_transcript = [{'text': 'Hello, world!', 'start': 5, 'duration': 10}]
    mock_get_transcript.return_value = expected_transcript

    # Call the function
    transcript = youtube_client.get_transcript('dummy_video_id')

    # Assert that the returned transcript match the expected transcript
    mock_get_transcript.assert_called_once_with('dummy_video_id', languages=['en'])
    assert transcript == expected_transcript, "The transcript should match the mock response"
