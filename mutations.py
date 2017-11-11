# encoding=utf-8
from contextlib import contextmanager

import graphene
from sqlalchemy.exc import SQLAlchemyError

from models import User, db_session, Todo, TodoItem
from objects import UserObject


@contextmanager
def make_session_scope(Session=db_session):
    session = Session()
    session.expire_on_commit = False
    try:
        yield session
    except SQLAlchemyError:
        session.rollback()
        raise
    finally:
        session.close()


class CreateUser(graphene.Mutation):

    # Your inputs
    class Input:
        username = graphene.String()
        email = graphene.String()

    # What you are returning
    user = graphene.Field(lambda: UserObject)
    ok = graphene.Boolean()

    # You might why this is not a classmethod
    # I honestly do not know the answer
    def mutate(self, args, request, info):
        with make_session_scope() as sess:
            u = User(**args)
            sess.add(u)
            sess.commit()
            return CreateUser(user=u, ok=True)


class DeleteUser(graphene.Mutation):
    class Input:
        id = graphene.Int()

    ok = graphene.Boolean()

    def mutate(self, args, request, info):
        with make_session_scope() as sess:

            if args.get('id'):
                sess.query(User) \
                    .filter(User.id == args.get('id')) \
                    .delete(synchronize_session=False)
                sess.commit()
                return DeleteUser(ok=True)
            else:
                return DeleteUser(ok=False)


class CreateTodo(graphene.Mutation):
    class Input:
        user_id = graphene.Int()
        todo_title = graphene.String()

    user = graphene.Field(lambda: UserObject)
    id = graphene.Int()
    ok = graphene.Boolean()

    def mutate(self, args, request, info):
        with make_session_scope() as sess:
            todo = Todo(title=args.get('todo_title'), user_id=args.get('user_id'))
            sess.add(todo)
            sess.commit()
            u = sess.query(User).get(args.get('user_id'))
            return CreateTodo(user=u, ok=True, id=todo.id)


class DeleteTodo(graphene.Mutation):

    class Input:
        todo_id = graphene.Int()

    ok = graphene.Boolean()

    def mutate(self, args, request, info):
        with make_session_scope() as sess:
            sess.query(TodoItem).filter_by(todo_id=args.get('todo_id')).delete()
            sess.query(Todo).filter_by(id=args.get('todo_id')).delete()
            sess.commit()

        return DeleteUser(ok=True)


class AddTodoItem(graphene.Mutation):
    class Input:
        todo_id = graphene.Int()
        description = graphene.String()

    ok = graphene.Boolean()
    user = graphene.Field(UserObject)

    def mutate(self, args, request, info):
        with make_session_scope() as sess:
            todo_item = TodoItem(**args, is_done=False)
            sess.add(todo_item)
            sess.commit()
            todo = sess.query(Todo).get(args.get('todo_id'))
            return AddTodoItem(ok=True, user=todo.user)


class DeleteTodoItem(graphene.Mutation):
    class Input:
        todo_item_id = graphene.Int()

    ok = graphene.Boolean()

    def mutate(self, args, request, info):
        with make_session_scope() as sess:
            sess.query(TodoItem).filter_by(id=args.get('todo_item_id')).delete()
            sess.commit()
        return DeleteTodoItem(ok=True)


class CompleteTodoItem(graphene.Mutation):

    class Input:
        todo_item_id = graphene.Int()

    ok = graphene.Boolean()

    def mutate(self, args, request, info):
        with make_session_scope() as sess:
            todo_item = sess.query(TodoItem).get(args.get('todo_item_id'))
            todo_item.is_done = True
            sess.add(todo_item)
            sess.commit()
        return CompleteTodoItem(ok=True)

