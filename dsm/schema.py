from django.contrib.auth.models import User
import graphene
from graphene_django import DjangoObjectType
from userprofile import models,serializers
from tweets import models as tweets_models,serializers as tweets_serializers


class User(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    email = graphene.String()

class Profile(graphene.ObjectType):
    user = graphene.Field(User)
    display_pic = graphene.String()
    followers = graphene.List(User)
    followings = graphene.List(User)

class Tweet(graphene.ObjectType):
    text = graphene.String()
    owner = graphene.Field(Profile)

class Query(graphene.ObjectType):
    get_all_profiles = graphene.List(Profile)
    get_all_tweets = graphene.List(Tweet)

    def resolve_get_all_profiles(self, info):
        users = models.Profile.objects.all()
        serializer = serializers.OwnerSerializer(data=users,many=True)
        serializer.is_valid()
        serializer = serializer.data
        return serializer
        
    def resolve_get_all_tweets(self, info):
        tweets = tweets_models.Tweet.objects.all()
        serializer = tweets_serializers.TweetSerializer(data=tweets, many=True)
        serializer.is_valid()
        return serializer.data

schema = graphene.Schema(query=Query)
