import graphene
import json
from datetime import datetime


class User(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    last_login = graphene.DateTime(name="last_login", required=False)


class Query(graphene.ObjectType):
    is_staff = graphene.Boolean(name="is_staff")
    users = graphene.List(User, first=graphene.Int())

    def resolve_is_staff(self, info):
        return True

    def resolve_users(self, info, first):
        return [
            User(username="Ana", last_login=datetime.now()),
            User(username="Aga", last_login=datetime.now()),
            User(username="Ane", last_login=datetime.now()),
        ][:first]


class CreateUser(graphene.Mutation):
    class Arguments:
        # arguments that are required in order to create a new user
        username = graphene.String()

    user = graphene.Field(User)

    def mutate(self, info, username):
        if info.context.get("is_vip"):
            username = username.upper()
        user = User(username=username)
        return CreateUser(user=user)


class Mutations(graphene.ObjectType):
    create_user = CreateUser.Field(name="create_user")


# schema = graphene.Schema(query=Query, auto_camelcase=False)

# result = schema.execute(
#     '''
#     {
#         users(first: 2) {
#             username
#             last_login
#         }
#     }
#     '''
# )

schema = graphene.Schema(query=Query, mutation=Mutations)

result = schema.execute(
    """
    mutation createUser($username: String) {
        create_user(username: $username) {
            user {
                username
            }
        }
    }
    """,
    variable_values={"username": "boo"},
    context={"is_vip": True},
)

items = dict(result.data.items())

print(json.dumps(items, indent=4))
