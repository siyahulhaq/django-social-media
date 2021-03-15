from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from userprofile.models import Profile
from .models import Like, Tweet, Comment
from .serializers import TweetSerializer
# Create your views here.
#constants
invalid_input = "Invalid Inputs"


class Tweets(APIView):
    def get(self, request, *args, **kwargs):
        tweet = Tweet.objects.all()
        serializers = TweetSerializer(
            tweet, many=True, context={'test': 'test'})
        return Response(serializers.data)


class GetATweet(APIView):
    def get(self, request, pk):
        tweet = Tweet.objects.get(pk=pk)
        serializer = TweetSerializer(tweet)
        return Response(serializer.data)


class UserTweets(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        tweets = Tweet.objects.filter(owner=profile)
        serializer = TweetSerializer(data=tweets, many=True)
        serializer.is_valid()
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        if 'text' in data:
            text = data['text']
            owner = Profile.objects.get(user=request.user)
            tweet = Tweet(text=text, owner=owner)
            tweet.save()
            serializer = TweetSerializer(tweet)
            return Response(serializer.data)
        return Response({'error': invalid_input}, status=301)


class UpdateTweets(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, pk):
        tweet = None
        try:
            tweet = Tweet.objects.get(pk=pk)
        except Tweet.DoesNotExist:
            tweet = None
        if tweet is not None:
            if (request.user.id == tweet.owner.id):
                tweet.delete()
                return Response({"message": "deleted"})
            else:
                Response({"error": "You can not delete this tweet"}, status=401)
        else:
            return Response({"error": "Tweet is not found"}, status=404)

    def post(self, request, pk):
        text = ""
        data = request.data
        if 'text' in data:
            text = data['text']
        tweet = None
        print(text)
        try:
            tweet = Tweet.objects.get(pk=pk)
        except Tweet.DoesNotExist:
            tweet = None
        if tweet is not None:
            if (request.user.id == tweet.owner.id):
                tweet.text = text
                tweet.save()
                serializer = TweetSerializer(tweet)
                return Response(serializer.data)
            else:
                Response({"error": "You can not delete this tweet"}, status=401)
        else:
            return Response({"error": "Tweet is not found"}, status=404)


class Comments(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request,):
        data = request.data
        if ('body' and 'tweetId') in data:
            tweet_id = data['tweetId']
            tweet = Tweet.objects.get(pk=tweet_id)
            body = data['body']
            profile = Profile.objects.get(user=request.user)
            comment = Comment.objects.create(
                tweet=tweet, body=body, user=profile)
            comment.save()
            serializer = TweetSerializer(tweet)
            return Response(serializer.data)
        else:
            return Response({'error': invalid_input}, status=400)


class Likes(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request,):
        data = request.data
        profile = Profile.objects.get(user=request.user)
        like = None
        try:
            like = Like.objects.get(user=profile)
        except Like.DoesNotExist:
            like = None
        if like is None:
            if 'tweetId' in data:
                tweet_id = data['tweetId']
                tweet = Tweet.objects.get(pk=tweet_id)
                like = Like.objects.create(tweet=tweet, user=profile)
                like.save()
                serializer = TweetSerializer(tweet)
                return Response(serializer.data)
            else:
                return Response({'error': invalid_input}, status=400)
        else:
            return Response({'error': "You have already liked"}, status=405)

    def delete(self, request):
        data = request.data
        if 'likeId' in data:
            like_id = data['likeId']
            profile = Profile.objects.get(user=request.user)
            like = Like.objects.get(pk=like_id)
            tweet = like.tweet
            if (like.user.id == profile.id):
                like.delete()
                serializer = TweetSerializer(tweet)
                return Response(serializer.data)
            else:
                return Response({'error': "You can not unlike"}, status=401)
        return Response({'error': invalid_input}, status=400)