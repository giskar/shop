__author__ = 'troviln'
from flask_peewee.auth import Auth
from app import app, db
from model import User

auth = Auth(app, db, user_model=User)