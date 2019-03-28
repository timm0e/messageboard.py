from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Board(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=280, blank=True, null=True)

    # posts: Post[]

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    board = models.ForeignKey(Board, models.CASCADE, related_name="posts")
    user = models.ForeignKey(User, models.CASCADE, related_name="posts")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = (("delete_this_post", "Delete this post"),)
