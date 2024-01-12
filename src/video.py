import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

api_key = os.environ.get('API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        self.title = None
        self.like_count = None

    def __str__(self):
        if self.title is None:
            self._fetch_title()
        return self.title

    def _fetch_title(self):
        try:
            video_response = youtube.videos().list(
                part='snippet, statistics',  # Add statistics part to fetch like count
                id=self.video_id
            ).execute()

            self.title = video_response['items'][0]['snippet']['title']
            self.like_count = video_response['items'][0]['statistics']['likeCount']
        except:
            self.title = None
            self.like_count = None


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __str__(self):
        if self.title is None:
            self._fetch_title()
        return self.title
