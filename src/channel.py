import json
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build


load_dotenv()

# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key = os.environ.get('API_KEY')

# создать специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.title = None
        self.description = None
        self.video_count = None
        self.view_count = None
        self.subscriber_count = None
        self.url = None
        self._fetch_channel_info()

    def _fetch_channel_info(self) -> None:
        """Заполняет атрибуты экземпляра данными о канале."""
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        channel_info = channel['items'][0]['snippet']
        statistics = channel['items'][0]['statistics']

        self.title = channel_info['title']
        self.description = channel_info['description']
        self.video_count = statistics['videoCount']
        self.view_count = statistics['viewCount']
        self.subscriber_count = statistics['subscriberCount']
        self.url = f"https://www.youtube.com/channel/{self.channel_id}"

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API."""
        return youtube

    def to_json(self, filename: str) -> None:
        """Сохраняет значения атрибутов экземпляра Channel в файл."""
        data = {
            'channel_id': self.channel_id,
            'title': self.title,
            'description': self.description,
            'video_count': self.video_count,
            'view_count': self.view_count,
            'subscriber_count': self.subscriber_count,
            'url': self.url
        }

        with open(filename, 'w') as file:
            json.dump(data, file, indent=2)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel_info = {
            'Channel ID': self.channel_id,
            'Title': self.title,
            'Description': self.description,
            'Video Count': self.video_count,
            'View Count': self.view_count,
            'Subscriber Count': self.subscriber_count,
            'URL': self.url
        }
        print(json.dumps(channel_info, indent=2, ensure_ascii=False))