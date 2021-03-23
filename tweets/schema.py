import graphene
from graphql import GraphQLError
from userprofile.schema import Profile
from userprofile import models
from . import models
from . import serializers


class Comment(graphene.ObjectType):
    body = graphene.String()
    user = graphene.Field(Profile)
    created_at = graphene.String()
    updated_at = graphene.String()


class Like(graphene.ObjectType):
    user = graphene.Field(Profile)
    created_at = graphene.String()


class Tweet(graphene.ObjectType):
    id = graphene.String()
    text = graphene.String()
    owner = graphene.Field(Profile)
    comment = graphene.List(Comment)
    created_at = graphene.String()
    updated_at = graphene.String()
    likes = graphene.List(Like)


class DeleteTweet(graphene.Mutation):
    deleted = graphene.Boolean()

    class Arguments:
        tweetid = graphene.String()

    def mutate(self, info, tweetid):
        if info.context.user.is_anonymous:
            raise GraphQLError('No Authorization Token Found')
        else:
            try:
                owner = models.Profile.objects.get(user=info.context.user)
                tweet = models.Tweet.objects.get(id=tweetid, owner=owner)
                tweet.delete()
                return DeleteTweet(deleted=True)
            except models.Tweet.DoesNotExist:
                raise GraphQLError('Tweet does not exist')


class CreateTweet(graphene.Mutation):
    tweet = graphene.Field(Tweet)

    class Arguments:
        text = graphene.String()

    def mutate(self, info, text):
        if info.context.user.is_anonymous:
            raise GraphQLError('No Authorization Token Found')
        else:
            owner = models.Profile.objects.get(user=info.context.user)
            tweet = models.Tweet(text=text, owner=owner)
            tweet.save()
            return CreateTweet(tweet=tweet)

class UpdateTweet(graphene.Mutation):
    tweet = graphene.Field(Tweet)

    class Arguments:
        text = graphene.String()
        tweet_id = graphene.String()
    def mutate(self, info, text,tweet_id):
        if info.context.user.is_anonymous:
            raise GraphQLError('No Authorization Token Found')
        else:
            owner = models.Profile.objects.get(user=info.context.user)
            tweet = models.Tweet.objects.get(id = tweet_id)
            tweet.text = text
            tweet.save()
            return UpdateTweet(tweet=tweet)


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


class Mutation(graphene.ObjectType):
    create_tweet = CreateTweet.Field()
    update_tweet = UpdateTweet.Field()
    delete_tweet = DeleteTweet.Field()
