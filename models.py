from sqlalchemy import (create_engine,
                        MetaData,
                        Column, String, Integer, Boolean, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, scoped_session, sessionmaker

engine = create_engine('postgresql://todoapi:todoapi@db:5432/postgres')
meta_data = MetaData(bind=engine)
db_session = scoped_session(
    sessionmaker(autocommit=False,
                 autoflush=False,
                 bind=engine)
)
Base = declarative_base(metadata=meta_data, bind=engine)
Base.query = db_session.query_property()


class PrimaryKeyIdMixin:
    id = Column(Integer, primary_key=True, autoincrement=True)


class User(Base, PrimaryKeyIdMixin):
    __tablename__ = 'users'

    username = Column(String(255))
    email = Column(String(length=255))
    todos = relationship('Todo', back_populates='user', lazy='subquery')


class Todo(Base, PrimaryKeyIdMixin):
    __tablename__ = 'todos'

    title = Column(String(length=255))

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # exists in the db
    user = relationship('User', back_populates='todos')  # does not exist in db

    items = relationship('TodoItem', back_populates='todo', lazy='subquery')
    meta_info = Column(JSONB)


class TodoItem(Base, PrimaryKeyIdMixin):
    __tablename__ = 'todo_items'

    description = Column(String)
    is_done = Column(Boolean)
    priority = Column(Integer)

    todo_id = Column(Integer, ForeignKey('todos.id'))
    todo = relationship('Todo', back_populates='items', lazy='subquery')


if __name__ == '__main__':
    meta_data.create_all()
