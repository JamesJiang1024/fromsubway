from django.db import models


class UserPicData(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    user_open_id = models.CharField(max_length=100, default='')
    to_username = models.TextField()
    media_id = models.TextField()
    pic_url = models.TextField()

    class Meta:
        ordering = ('created_time',)
