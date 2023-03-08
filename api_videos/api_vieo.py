from googleapiclient.discovery import build
from requests import HTTPError
from rest_framework import generics, pagination
from api_videos.serializers import VideoSerializer
from api_videos.models import YouTubeVideo
from django.db.models import Q

class VideoPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class VideoList(generics.ListAPIView):
    serializer_class = VideoSerializer
    pagination_class = VideoPagination

    api_keys = ['AIzaSyAUsp-ZS_d1N0llAv5Dl-XBOg27Nid6PH8', 'AIzaSyAUsp-ZS_d1N0llAv5Dl-XBOg27Nid6PH8']
    
    def get_queryset(self):
        for api_key in self.api_keys:
            try:
                youtube = build('youtube', 'v3', developerKey=api_key)
                request = youtube.search().list(
                    part='id,snippet',
                    q=self.request.query_params.get('q', ''),
                    type='video',
                    order='date',
                    maxResults=10
                )
                response = request.execute()
                video_ids = [video['id']['videoId'] for video in response['items']]
                videos = YouTubeVideo.objects.filter(video_id__in=video_ids)
                return videos
            except HTTPError as exception:
                if exception.resp.status == 403 and 'quota' in str(exception):
                    continue
                else:
                    raise exception
    
class SearchApi(generics.ListAPIView):
    serializer_class = VideoSerializer

    def get_queryset(self):
        query_param = self.request.query_params.get('q', '')
        you_tube_videos = YouTubeVideo.objects.filter(Q(title__icontains=query_param) | Q(description__icontains=query_param)).order_by('-published_at')

        if len(query_param.split()) > 1:
            query_params = query_param.split()
            for param in query_params:
                you_tube_videos = you_tube_videos.filter(Q(title__icontains=param) | Q(description__icontains=param)).distinct()
        
        return you_tube_videos
            