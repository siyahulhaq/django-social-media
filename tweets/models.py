from django.db import models
# Create your models here.
from userprofile.models import Profile


class Tweet(models.Model):
    text = models.CharField(max_length=2555, null=True, blank=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.FileField(upload_to="images/tweets", null=True, blank=True)
    def __str__(self) -> str:
        return self.text

class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE,null=True)
    def __str__(self) -> str:
        return self.user.user.username

class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    body = models.CharField(max_length=1024, null=True)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE,null=True)
    def __str__(self) -> str:
        return self.body