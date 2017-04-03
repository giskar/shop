__author__ = 'troviln'
from flask_peewee.auth import BaseUser
from peewee import *
import datetime
import os
from flask import Markup
from werkzeug.utils import secure_filename
from app import db, app
from playhouse.fields import ManyToManyField

class Photo(db.Model):
    image = CharField()

    def __str__(self):
        return self.image

    def save_image(self, file_obj):
        self.image = secure_filename(file_obj.filename)
        full_path = os.path.join(app.config['MEDIA_ROOT'], self.image)
        file_obj.save(full_path)
        self.save()

    def url(self):
        return os.path.join(app.config['MEDIA_URL'], self.image)

    def thumb(self):
        return Markup('<img src="%s" style="height: 80px;" />' % self.url())


class Goods(db.Model):
    name = CharField(max_length=35)
    amount = IntegerField()
    price = FloatField()
    size = CharField(max_length=20)

    image = CharField()

    # def __str__(self):
    #     return self.image

    def save_image(self, file_obj):
        self.image = secure_filename(file_obj.filename)
        full_path = os.path.join(app.config['MEDIA_ROOT'], self.image)
        file_obj.save(full_path)
        self.save()

    def url(self):
        return os.path.join(app.config['MEDIA_URL'], self.image)

    def thumb(self):
        return Markup('<img src="%s" style="height: 80px;" />' % self.url())

    def __str__(self):
        return '%s: %s' % (self.id, self.name)


class User(db.Model, BaseUser):

    username = CharField(max_length=35)
    password = CharField(max_length=55)
    email = CharField()
    active = BooleanField(default=True)
    admin = BooleanField(default=False)


    def __str__(self):
        return '%s' % ( self.username)


class Reviews(db.Model):
    goods = ForeignKeyField(Goods, related_name='good')
    review = CharField(null=False, max_length=200)
    pub_date = DateTimeField(default=datetime.datetime.now)
    author = ForeignKeyField(User, related_name='user')

    def __str__(self):
        return '%s: %s' % (self.pub_date, self.review)



class Order(db.Model):

    goods = ManyToManyField(Goods, related_name='orders')
    #goods = CharField()
    name = CharField(max_length=55)
    phone = IntegerField()
    pay_method = CharField(max_length=55)
    del_method = CharField(max_length=55)
    pub_date = DateTimeField(default=datetime.datetime.now)


    def __str__(self):
        return '%s' % ( self.name)