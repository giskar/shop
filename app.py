__author__ = 'troviln'
from flask import Flask

from flask_peewee.db import Database
import os

app = Flask(__name__)

app.config.from_object('config.Configuration')
db = Database(app)

APP_ROOT = os.path.dirname(os.path.realpath(__file__))

MEDIA_ROOT = os.path.join(APP_ROOT, 'static/media')

MEDIA_URL = '/static/media/'

app.config['MEDIA_ROOT'] = MEDIA_ROOT
app.config['MEDIA_URL'] = MEDIA_URL
