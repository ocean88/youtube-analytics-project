import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
import datetime
import isodate

load_dotenv()

api_key = os.environ.get('API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Playlist:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.youtube = youtube

    @property
    def title(self):
        playlist_response = self.youtube.playlists().list(
            part="snippet",
            id=self.playlist_id
        ).execute()
        return playlist_response['items'][0]['snippet']['title']

    @property
    def url(self):
        return f"https://www.youtube.com/playlist?list={self.playlist_id}"

    @property
    def total_duration(self):
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=5,
                                                       ).execute()

        # получить все id видеороликов из плейлиста
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        # printj(video_response)

        total_duration = datetime.timedelta()  # Initialize the total duration

        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration

        return total_duration

    def show_best_video(self):
        # Получение списка видео в плейлисте
        playlist_items = self.youtube.playlistItems().list(
            part="snippet",
            maxResults=50,  # Максимальное количество видео для получения
            playlistId=self.playlist_id
        ).execute()

        # Инициализация переменных для хранения информации о видео с наибольшим количеством лайков
        best_video_id = ""
        best_video_likes = 0

        # Перебор каждого видео в плейлисте
        for item in playlist_items['items']:
            video_id = item['snippet']['resourceId']['videoId']

            # Получение подробной информации о видео
            video_details = self.youtube.videos().list(
                part="snippet,statistics",
                id=video_id
            ).execute()

            # Получение количества лайков для видео
            video_likes = int(video_details['items'][0]['statistics']['likeCount'])

            # Обновление информации о видео с наибольшим количеством лайков, если текущее видео имеет больше лайков
            if video_likes > best_video_likes:
                best_video_id = video_id
                best_video_likes = video_likes

        # Формирование ссылки на видео с наибольшим количеством лайков
        best_video_url = f"https://youtu.be/{best_video_id}"

        return best_video_url
