from django.db import models

class Post(models.Model):
    """
    Store post details returned by posterous api.
    """
    title = models.CharField(max_length=180)
    body = models.TextField(null=True, blank=True)
