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

@click.command(name="db_rollback")
@with_appcontext
def db_rollback():
    db.session.rollback()

sys.path.append(os.path.join(my_dir, r"../Scraper"))
from Scraper.main_tracker import price_tracker_job
@click.command(name="main_tracker")
@with_appcontext
def main_tracker():
    print("...start tracker from command...")
    price_tracker_job()