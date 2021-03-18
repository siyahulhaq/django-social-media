import graphene
from graphql import GraphQLError
from userprofile.schema import Profile
from . import models
from . import serializers

class Comment(graphene.ObjectType):
    body =graphene.String()
    user = graphene.Field(Profile)
    created_at = graphene.String()
    updated_at = graphene.String()

class Like(graphene.ObjectType):
    user = graphene.Field(Profile)
    created_at = graphene.String()

class Tweet(graphene.ObjectType):
    text = graphene.String()
    owner = graphene.Field(Profile)
    comment = graphene.List(Comment)
    created_at = graphene.String()
    updated_at = graphene.String()
    likes = graphene.List(Like)


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
