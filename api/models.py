from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    # Add other fields as needed, e.g. profile_picture = models.ImageField(...)

    def __str__(self):
        return self.username