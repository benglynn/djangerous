from django.db import models

class Post(models.Model):
    """
    Store post details returned by posterous api.
    """
    title = models.CharField(max_length=180)
    date = models.DateTimeField()
    link = models.URLField(verify_exists=False)
    body = models.TextField(null=True, blank=True)
    xml = models.XMLField()
