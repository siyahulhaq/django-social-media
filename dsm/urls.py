from django.contrib import admin
from django.urls import path,include
from graphene_django.views import GraphQLView
from graphene_file_upload.django import FileUploadGraphQLView
from .schema import schema
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/tweets/',include('tweets.urls')),
    path('api/profile/',include('userprofile.urls')),
    path("graphql",csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True,schema=schema))),
]