from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(
        User, related_name="followers",blank=True)
    followings = models.ManyToManyField(
        User, related_name="followings",blank=True)
    display_pic = models.FileField(
        upload_to="images/display_pic", null=True, blank=True)

    def __str__(self):
        return self.user.username
