from django.contrib import admin
from django.urls import path,include
from graphene_django.views import GraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/tweets/',include('tweets.urls')),
    path('api/profile/',include('userprofile.urls')),
    path("graphql", GraphQLView.as_view(graphiql=True)),
]
