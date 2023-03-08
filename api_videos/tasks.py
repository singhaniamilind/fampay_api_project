from datetime import datetime, timedelta
from googleapiclient.discovery import build
from django.conf import settings
from celery import shared_task
from .models import Video


@shared_task
def fetch_latest_videos():
    search_query = 'your_predefined_search_query_here'
    youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
    response = youtube.search().list(
        q=search_query,
        type='video',
        part='id,snippet',
        order='date',
    ).execute()
    videos = response.get('items', [])
    video_data = []
    for video in videos:
        video_data.append({
            'title': video['snippet']['title'],
            'description': video['snippet']['description'],
            'thumbnail_url': video['snippet']['thumbnails']['default']['url'],
            'publish_date': video['snippet']['publishedAt'],
            'video_id': video['id']['videoId'],
        })
    Video.objects.bulk_create([
        Video(
            title=video['title'],
            description=video['description'],
            thumbnail_url=video['thumbnail_url'],
            publish_date=datetime.fromisoformat(video['publish_date'].replace('Z', '+00:00')),
            video_id=video['video_id'],
        )
        for video in video_data
    ])


@shared_task
def cleanup_old_videos():
    Video.objects.filter(publish_date__lt=datetime.now() - timedelta(days=7)).delete()