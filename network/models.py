from typing import Callable
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE


class User(AbstractUser):
    followers = models.ManyToManyField("User",default=None,related_name="user")
    following = models.ManyToManyField("User",default=None,related_name="follower")


class PostManager(models.Manager):
    def create_Post(self,user,content):
        post=self.create(user=user,content=content)
        post.save()
        return post


class Post(models.Model):
    user= models.ForeignKey("User",on_delete=models.CASCADE,related_name="posts")
    content=models.TextField(max_length=255)
    like=models.PositiveIntegerField(default=0)
    unlike=models.PositiveIntegerField(default=0)
    timeStamp=models.DateTimeField(auto_now_add=True)
    
    objects=PostManager()

    def __str__(self):
        return str(self.content)
