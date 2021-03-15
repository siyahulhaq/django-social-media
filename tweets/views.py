from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Tweet
from .serializers import TweetSerializer
# Create your views here.

class Tweets(APIView):
    def get(self,request, *args, **kwargs):
        tweet = Tweet.objects.all()
        serializers = TweetSerializer(tweet,many=True,context={'test':'test'})
        return Response(serializers.data)