from flask import Flask
from flask_graphql import GraphQLView

from models import db_session
from schema import schema

app = Flask(__name__)

app.add_url_rule('/graphiql',  # the endpoint

                 # setting the view function
                 view_func=GraphQLView.as_view(
                     'graphql',

                     # we set the schema that we generate
                     schema=schema,

                     # We say that we *do* want a graphiql interface
                     graphiql=True
                 )
                 )


@app.teardown_appcontext
def remove_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run(debug=True)
