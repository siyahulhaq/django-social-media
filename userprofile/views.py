from django.contrib.auth import login, models
from .models import Profile
from rest_framework import permissions, generics, response, views
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken
from .serializers import OwnerSerializer, RegisterSerializer, UserSerializer
from .models import Profile
# Create your views here.


class ProfileView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = Profile.objects.get(user=request.user)
        print(user)
        serializer = OwnerSerializer(user)
        return response.Response(serializer.data)


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        profile = Profile(user=user)
        profile.save()
        token = AuthToken.objects.create(user)
        return response.Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token details": {'token': token[1], 'expiry': token[0].expiry}
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class Follow(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            destination_user_id = request.data['profileId']
            my_profile = Profile.objects.get(user=request.user)
            try:
                destination_profile = Profile.objects.get(id=destination_user_id)
                destination_profile.followers.add(request.user)
                my_profile.followings.add(destination_profile.user)
                serialized = OwnerSerializer(my_profile)
                return response.Response(serialized.data, status=200)
            except Profile.DoesNotExist:
                print(Profile.DoesNotExist)
                return response.Response({'error': 'Not Found The Destination User'}, status=404)
        except KeyError:
            return response.Response({'error': 'Invalid input'}, status=400)

    def delete(self, request):
        try:
            destination_user_id = request.data['profileId']
            my_profile = Profile.objects.get(user=request.user)
            try:
                destination_profile = Profile.objects.get(id=destination_user_id)
                destination_profile.followers.remove(request.user)
                my_profile.followings.remove(destination_profile.user)
                serialized = OwnerSerializer(my_profile)
                return response.Response(serialized.data, status=200)
            except Profile.DoesNotExist:
                return response.Response({'error': 'Not Found The Destination User'}, status=404)
        except KeyError:
            return response.Response({'error': 'Invalid input'}, status=400)