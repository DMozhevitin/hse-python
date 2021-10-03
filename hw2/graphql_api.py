from graphene import ObjectType, String, Schema, Int, List, Float, Field, Schema
from starlette.graphql import GraphQLApp
from service import account_service, user_service
from model.user import User
from model.account import Account

class AccountQuery(ObjectType):
    id = Int()
    owner = Field('graphql_api.UserQuery')
    currency_type = String()
    balance = Float()

    def resolve_owner(parent, info):
        owner_id = account_service.get_account_by_id(parent.id).owner_id
        return user_to_query(user_service.get_user_by_id(owner_id))

class UserQuery(ObjectType):
    id = Int()
    name = String()
    email = String()
    accounts = List(AccountQuery)

    def resolve_accounts(parent, info):
        return list(map(account_to_query, account_service.get_accounts_by_owner_id(parent.id)))

class Query(ObjectType):
    user = Field(UserQuery, id=Int(required=True))
    account_by_id = Field(AccountQuery, id=Int(required=True))
    accounts_by_owner_id = Field(List(AccountQuery), owner_id=Int(required=True))

    def resolve_user(parent, info, id):
        return user_to_query(user_service.get_user_by_id(id))

    def resolve_account_by_id(parent, info, id):
        return account_to_query(account_service.get_account_by_id(id))

    def resolve_accounts_by_owner_id(parent, info, owner_id):
        return list(map(account_to_query, account_service.get_accounts_by_owner_id(owner_id)))

app = GraphQLApp(schema=Schema(query=Query))

#############################################
# Converters
#############################################

def user_to_query(user: User) -> UserQuery:
    return UserQuery(id=user.id, name=user.name, email=user.email, accounts=None)

def account_to_query(account: Account) -> AccountQuery:
    return AccountQuery(id=account.id, owner=None, currency_type=str(account.currency_type), balance=account.balance)
