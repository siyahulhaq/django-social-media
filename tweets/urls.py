from django.urls import path
from . import views
urlpatterns=[
    path('get', views.Tweets.as_view(), name='get_tweets')
]