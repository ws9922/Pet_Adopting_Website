import os
import sqlalchemy
from yaml import load, Loader
from flask import Flask, jsonify, render_template


def init_connect_engine():
    if os.environ.get('GAE_ENV') != 'standard':
        variables = load(open("app.yaml"), Loader=Loader)
        env_variables = variables['env_variables']
        for var in env_variables:
            os.environ[var] = env_variables[var]
    pool = sqlalchemy.create_engine(
            sqlalchemy.engine.url.URL(
                drivername="mysql+pymysql",
                username=os.environ.get('MYSQL_USER'), #username
                password=os.environ.get('MYSQL_PASSWORD'), #user password
                database=os.environ.get('MYSQL_DB'), #database name
                host=os.environ.get('MYSQL_HOST') #ip
            )
        )
    return pool

db = init_connect_engine()


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

from app import routes
