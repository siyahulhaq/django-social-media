from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Subscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(
        User,related_name="followers", blank=True)
    followings = models.ManyToManyField(
        User,related_name="followings", blank=True)
    display_pic = models.FileField(
        upload_to="images/display_pic", null=True, blank=True)
    def __str__(self):
        return self.user.username

class Tweet(models.Model):
    text = models.CharField(max_length=2555, null=True, blank=True)
    owner = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    image = models.FileField(upload_to="images/tweets", null=True, blank=True)
    def __str__(self) -> str:
        return self.text

class Like(models.Model):
    user = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE,null=True)
    def __str__(self) -> str:
        return self.user.user.username

class Comment(models.Model):
    user = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    body = models.CharField(max_length=1024, null=True)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE,null=True)
    def __str__(self) -> str:
        return self.body