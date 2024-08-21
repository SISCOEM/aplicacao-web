from django.db import models

# Create your models here.
class Notification(models.Model):
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=100)
    data = models.CharField(max_length=100)
    to = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title