from django.db import models

class YouTubeVideo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video_id = models.CharField(max_length=255)
    published_at = models.DateTimeField()
    thumbnail_url = models.URLField()
    video_url = models.URLField()
   
    class Meta:
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['title', 'description']),
        ]
