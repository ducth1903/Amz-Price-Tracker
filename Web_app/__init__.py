from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import file_path
import sys

sys.path.append(file_path.web_app_dir)
from config import *

app = Flask(__name__)
if os.environ.get("DATABASE_URL"):
    """
    Production env
    """
    app.config.from_object(ProductionConfig())
else:
    """
    Development env
    """
    print("...Development stage...")
    app.config.from_object(DevelopmentConfig())
# config_file = 'config.py'
# app.config.from_pyfile(config_file)

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