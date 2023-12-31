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

    def __str__(self):
        if self.title is None:
            self._fetch_title()
        return self.title

    def _fetch_title(self):
        video_response = youtube.videos().list(
            part='snippet',
            id=self.video_id
        ).execute()
        self.title = video_response['items'][0]['snippet']['title']


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __str__(self):
        if self.title is None:
            self._fetch_title()
        return self.title


video1 = Video('AWX4JnAnjBE')  # 'AWX4JnAnjBE' - это id видео из ютуб
video2 = PLVideo('4fObz_qw9u4', 'PLv_zOGKKxVph_8g2Mqc3LMhj0M_BfasbC')
