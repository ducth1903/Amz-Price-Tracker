'''
These settings will be loaded in __ini__() when we define the app
'''
import os
from dotenv import load_dotenv
database_local_file = "test.db"

# Actual path to this file
my_dir = os.path.dirname(os.path.realpath(__file__))
database_path = os.path.join(my_dir, r"../Database", database_local_file)

# Load env variables
load_dotenv()
# SECRET_KEY = os.environ.get("SECRET_KEY")        

class BaseConfig:
    """
    Base application configuration
    """
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False      # turn off warning
    CACHE_TYPE = "null"

class DevelopmentConfig(BaseConfig):
    """
    Development configuration
    """
    # SQLALCHEMY_DATABASE_URI = r"sqlite:///{}".format(database_path)
    # SQLALCHEMY_DATABASE_URI = r"postgresql://postgres:postgres@localhost:5432/price_tracker"
    SQLALCHEMY_DATABASE_URI = r"postgresql://postgres:postgres@localhost/price_tracker"
    # SECRET_KEY = "postgres"

class ProductionConfig(BaseConfig):
    """
    Production configuration
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")