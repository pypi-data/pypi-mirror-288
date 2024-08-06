from youtube_data_api import YouTubeDataAPI
from youtube_transcript_api import YouTubeTranscriptApi

class YouTubeClient:
    """
    A client to interact with both the YouTube Data API and YouTube Transcript API.
    """

    def __init__(self, api_key):
        """
        Initializes the YouTubeClient with an API key.
        :param api_key: str - YouTube Data API key.
        """
        self.data_api = YouTubeDataAPI(api_key)
        self.transcript_api = YouTubeTranscriptApi()

    def get_video_details(self, video_id):
        """
        Retrieves video details using the YouTube Data API.
        :param video_id: str - The YouTube video ID.
        :return: dict - The video details.
        """
        return self.data_api.get_video_details(video_id)

    def get_transcript(self, video_id, languages=['en']):
        """
        Retrieves the transcript of a video using the YouTube Transcript API.
        :param video_id: str - The YouTube video ID.
        :param languages: list - Preferred languages for the transcript.
        :return: list - A list of dictionaries containing transcript information.
        """
        return self.transcript_api.get_transcript(video_id, languages=languages)
