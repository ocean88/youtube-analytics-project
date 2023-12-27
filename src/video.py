class Video:
    def __init__(self, video_id):
        self.video_id = video_id

    def __str__(self):
        video_titles = {
            'AWX4JnAnjBE': 'GIL в Python: зачем он нужен и как с этим жить'
        }
        return video_titles.get(self.video_id, 'Unknown Video')


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __str__(self):
        video_titles = {
            '4fObz_qw9u4': 'MoscowPython Meetup 78 - вступление'
        }
        return video_titles.get(self.video_id, 'Unknown Video')


# тест функций

print(Video('AWX4JnAnjBE'))
print(PLVideo('4fObz_qw9u4', 'PLv_zOGKKxVph_8g2Mqc3LMhj0M_BfasbC'))
