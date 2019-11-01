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
    print('...init...', app.config['SQLALCHEMY_DATABASE_URI'])

db = SQLAlchemy(app)

from Web_app import routes
from Web_app.commands import create_tables, drop_tables
app.cli.add_command(create_tables)
app.cli.add_command(drop_tables)

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