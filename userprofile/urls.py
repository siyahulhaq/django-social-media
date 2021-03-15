from knox import views as knox_views
from django.urls import path
from . import views

urlpatterns = [
    path('',views.ProfileView.as_view(),name='profile'),
    path('login', views.LoginAPI.as_view(), name='login'),
    path('register',views.RegisterAPI.as_view(), name='register'),
    path('logout', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall', knox_views.LogoutAllView.as_view(), name='logoutall'),
]
