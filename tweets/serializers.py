from django.db.models import fields
from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",)


class OwnerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = models.Subscriber
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    user = OwnerSerializer()

    class Meta:
        model = models.Like
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = OwnerSerializer()

    class Meta:
        model = models.Comment
        fields = ('id', 'body', 'user')


class TweetSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer()
    comment = serializers.SerializerMethodField('_get_comments')
    likes = serializers.SerializerMethodField('_get_likes')

    def _get_comments(self, tweet_object):
        tweet_id = getattr(tweet_object, 'id')
        comment = models.Comment.objects.filter(tweet=tweet_id)
        serialized = CommentSerializer(data=comment, many=True)
        serialized.is_valid()
        return serialized.data

    def _get_likes(self, tweet_object):
        tweet_id = getattr(tweet_object, 'id')
        like = models.Like.objects.filter(tweet=tweet_id)
        serialized = LikeSerializer(data=like, many=True)
        serialized.is_valid()
        return serialized.data

    class Meta:
        model = models.Tweet
        fields = ('id', 'text', 'image', 'owner', 'comment', 'likes')
