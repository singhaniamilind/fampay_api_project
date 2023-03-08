from rest_framework import serializers
from api_videos.models import YouTubeVideo

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = YouTubeVideo
        fields = ('title', 'description','id' , 'video_url','thumbnail_url', 'published_at')