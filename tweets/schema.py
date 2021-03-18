import graphene
from graphql import GraphQLError
from userprofile.schema import Profile
from . import models
from . import serializers


class Tweet(graphene.ObjectType):
    text = graphene.String()
    owner = graphene.Field(Profile)


class Query(graphene.ObjectType):
    get_all_tweets = graphene.List(Tweet)
    get_my_tweets = graphene.List(Tweet)

    def resolve_get_all_tweets(self, info):
        tweets = models.Tweet.objects.all()
        serializer = serializers.TweetSerializer(data=tweets, many=True)
        serializer.is_valid()
        return serializer.data

    def resolve_get_my_tweets(self, info):
        if info.context.user.is_anonymous:
            raise GraphQLError('No Authorization Token Found')
        else:
            owner = models.Profile.objects.get(user=info.context.user)
            tweets = models.Tweet.objects.filter(owner=owner)
            serializer = serializers.TweetSerializer(
                data=tweets, many=True)
            serializer.is_valid()
            return serializer.data
