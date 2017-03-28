__author__ = 'troviln'
from app import app, db

from auth import *
from admin import admin
from api import api
from model import *
from views import *



admin.setup()
api.setup()

if __name__ == '__main__':
    auth.User.create_table(fail_silently=True)
    Goods.create_table(fail_silently=True)
    User.create_table(fail_silently=True)
    Reviews.create_table(fail_silently=True)
    Photo.create_table(fail_silently=True)
    Order.create_table(fail_silently=True)
    Order.goods.get_through_model().create_table(fail_silently=True)
    app.run()