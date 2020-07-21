import graphene
from graphene.types.json import JSONString
from graphene_sqlalchemy import SQLAlchemyObjectType

from models import User, Todo, TodoItem


class UserObject(SQLAlchemyObjectType):

    id = graphene.Int()

    class Meta:
        model = User


class TodoObject(SQLAlchemyObjectType):

    id = graphene.Int()
    meta_info = graphene.Field(JSONString)

    def resolve_meta_info(self, info, **args):
        return self.meta_info

    class Meta:
        model = Todo


class TodoItemObject(SQLAlchemyObjectType):
    class Meta:
        model = TodoItem
