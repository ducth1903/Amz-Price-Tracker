import os
from dotenv import load_dotenv

# Load env variables
load_dotenv()

SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
SECRET_KEY = os.environ.get("SECRET_KEY")
CACHE_TYPE = "null"
SQLALCHEMY_TRACK_MODIFICATIONS = False            # turn off warning