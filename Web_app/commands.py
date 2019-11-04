import click 
from flask.cli import with_appcontext

from Web_app import db
import sys
import os

# Actual path to this file
my_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(my_dir, r"../Database"))
from Database.db_utils import *

@click.command(name="create_tables")
@with_appcontext
def create_tables():
    db.create_all()

@click.command(name="drop_tables")
@with_appcontext
def drop_tables():
    db.drop_all()