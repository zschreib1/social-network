from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE) # user who posted the post
    content = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True) # date and time at which the post was made
    likes = models.ManyToManyField(User, related_name="post_likes")

    def __str__(self):
        return f"{self.content} posted by {self.posted_by} at {self.posted_at}"
    
    def serialize(self):

        return {
            "id": self.id,
            "posted_by": self.posted_by.username,
            "content": self.content,
            "posted_at": self.posted_at.strftime("%b %d %Y, %I:%M %p"),
            "likes": [user.username for user in self.likes.all()]
        }

class FollowersCount(models.Model):
    profile = models.ForeignKey(User, on_delete=models.CASCADE) # user being followed
    follower = models.CharField(max_length=1000) # user that follows 
    
    def __str__(self):
        return f'{self.profile} is followed by {self.follower}'

class FollowingCount(models.Model):
    following =  models.CharField(max_length=1000) # user that follows
    profile = models.ForeignKey(User, on_delete=models.CASCADE) # user being followed

    def __str__(self):
        return f'{self.following} follows {self.profile}'

