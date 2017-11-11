# encoding=utf-8

import graphene

from mutations import CreateUser, DeleteUser, CreateTodo, AddTodoItem, DeleteTodo, DeleteTodoItem, CompleteTodoItem
from objects import UserObject


class Query(graphene.ObjectType):

    user = graphene.Field(UserObject,
                          id=graphene.Int(),
                          username=graphene.String())

    def resolve_user(self, args, context, info):
        query = UserObject.get_query(context)
        query = query.filter_by(**args)
        return query.first()


class Mutations(graphene.ObjectType):

    create_user = CreateUser.Field(description='Creates a new user. Given a username and email.')
    delete_user = DeleteUser.Field(description='Deletes a user. Given the id.')
    create_todo = CreateTodo.Field(description='Creates a todo given description and user id')
    delete_todo = DeleteTodo.Field(description='Deletes a todo given the id and user.')
    add_todo_item = AddTodoItem.Field(description='Adds an item to an existing todo list')
    delete_todo_item = DeleteTodoItem.Field()
    complete_todo_item = CompleteTodoItem.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
