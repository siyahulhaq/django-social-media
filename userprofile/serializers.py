from rest_framework import serializers
from.models import Profile
from django.contrib.auth.models import User

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "id")


class OwnerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    followers = serializers.SerializerMethodField('_get_followers')
    followings = serializers.SerializerMethodField('_get_followings')

    def _get_followers(self,profile_obj):
        followers = getattr(profile_obj,'followers')
        serialized = UserSerializer(data=followers,many=True)
        serialized.is_valid()
        return serialized.data

    def _get_followings(self,profile_obj):
        followings = getattr(profile_obj,'followings')
        serialized = UserSerializer(data=followings,many=True)
        serialized.is_valid()
        return serialized.data

    class Meta:
        model = Profile
        fields = '__all__'

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user