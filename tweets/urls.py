from django.urls import path
from . import views
urlpatterns=[
    path('', views.UserTweets.as_view(),name="create_tweets"),
    path('get', views.Tweets.as_view(), name='get_tweets'),
    path('comment',views.Comments.as_view(), name='comments'), 
    path('like',views.Likes.as_view(), name='likes'), 
    path('<str:pk>', views.UpdateTweets.as_view(),name="update_tweets"),
    path('get/<str:pk>', views.Tweets.as_view(), name='get_tweets'),
]