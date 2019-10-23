'''
These settings will be loaded in __ini__() when we define the app
'''
import os
from dotenv import load_dotenv

# Load env variables
load_dotenv()
# SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
# SECRET_KEY = os.environ.get("SECRET_KEY")
# CACHE_TYPE = "null"
# SQLALCHEMY_TRACK_MODIFICATIONS = False            

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
    SQLALCHEMY_DATABASE_URI = r"sqlite:///C:\Code\Flask\Price_Tracker\Database\test.db"

class ProductionConfig(BaseConfig):
    """
    Production configuration
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")