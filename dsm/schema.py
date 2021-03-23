import graphene
from userprofile import schema as user_schema
from tweets import schema as tweet_schema

class Query(user_schema.Query,tweet_schema.Query):
    pass

class Mutation(user_schema.Mutation,tweet_schema.Mutation):
    pass

schema = graphene.Schema(query=Query,mutation=Mutation)
