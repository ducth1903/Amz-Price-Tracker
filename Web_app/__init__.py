from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
config_file = 'settings.py'
app.config.from_pyfile(config_file)
db = SQLAlchemy(app)

from Web_app import routes

# Initialize database once
# The database will be created if not there
# else will NOT be overwritten
# import sys
# sys.path.append('../Database')
# from Database.db_utils import *
# db.create_all()

# def create_app(config_file='settings.py'):
#     app = Flask(__name__)
#     app.config.from_pyfile(config_file)

#     db.init_app(app)

#     return app