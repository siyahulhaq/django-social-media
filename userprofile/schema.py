import graphene
import graphql_jwt
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from graphql import GraphQLError
from userprofile import models, serializers

User = get_user_model()


class UserType(graphene.ObjectType):
    username = graphene.String()
    email = graphene.String()


class Profile(graphene.ObjectType):
    user = graphene.Field(UserType)
    display_pic = graphene.String()
    followers = graphene.List(UserType)
    followings = graphene.List(UserType)


class CreateUser(graphene.Mutation):
    profile = graphene.Field(Profile)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        try:
            user = User(
                username=username,
                email=email,
            )
            user.set_password(password)
            user.save()
            profile = models.Profile(user=user)
            profile.save()
            serializer = serializers.OwnerSerializer(data=profile)
            serializer.is_valid()
            return CreateUser(profile=serializer.data)
        except IntegrityError:
            raise GraphQLError("Username is already existing")

class Query(graphene.ObjectType):
    get_all_profiles = graphene.List(Profile)
    get_me = graphene.Field(Profile)

    def resolve_get_all_profiles(self, info):
        users = models.Profile.objects.all()
        serializer = serializers.OwnerSerializer(data=users, many=True)
        serializer.is_valid()
        serializer = serializer.data
        return serializer

    def resolve_get_me(self, info):
        user = info.context.user
        if not user.is_anonymous:
            user = models.Profile.objects.get(user=user)
            serializer = serializers.OwnerSerializer(user)
            serializer = serializer.data
            return serializer
        else:
            raise GraphQLError('No Authorization Token Found')


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    create_user = CreateUser.Field()
    
