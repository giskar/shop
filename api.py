__author__ = 'troviln'

from app import app
from auth import auth

from model import Goods, User, Reviews, Photo

from flask_peewee.rest import RestAPI, UserAuthentication, RestResource


class ForeignResource(RestResource):
    exclude = ('amount', 'size', 'photo',)


class ForeignResource1(RestResource):
    fields = ('name')


class MessageResource(RestResource):
    include_resources = {'goods': ForeignResource, 'author': ForeignResource}


# create a RestAPI container
user_auth = UserAuthentication(auth)

# create a RestAPI container
api = RestAPI(app, default_auth=user_auth)
api.register(Goods)
api.register(User)
api.register(Reviews, MessageResource)