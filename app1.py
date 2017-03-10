__author__ = 'troviln'
from flask import Flask, render_template
from flask_peewee.auth import Auth
from flask_peewee.db import Database
import os
# configure our database
DATABASE = {
    'name': 'example.db',
    'engine': 'peewee.SqliteDatabase',
}
DEBUG = True
SECRET_KEY = 'ssshhhh'

app = Flask(__name__)
app.config.from_object(__name__)
db = Database(app)

APP_ROOT = os.path.dirname(os.path.realpath(__file__))

MEDIA_ROOT = os.path.join(APP_ROOT, 'static/media')

MEDIA_URL = '/static/media/'

app.config['MEDIA_ROOT'] = MEDIA_ROOT
app.config['MEDIA_URL'] = MEDIA_URL

####################Model#########################################
from peewee import *
import datetime
import os
from flask import Markup
from werkzeug.utils import secure_filename


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
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=35)
    amount = IntegerField()
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
        return '%s: %s' % (self.name, self.amount)


class Users(db.Model):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=35)

    @property
    def serialize(self):
        data = {
            'id': self.id,
            'name': str(self.name).strip(),

        }

        return data

    def __str__(self):
        return '%s: %s' % (self.id, self.name)


class Reviews(db.Model):
    goods = ForeignKeyField(Goods, related_name='good')
    review = CharField(max_length=200)
    pub_date = DateTimeField(default=datetime.datetime.now)
    author = ForeignKeyField(Users, related_name='user')

    def __str__(self):
        return '%s: %s' % (self.pub_date, self.review)


from flask import Flask, jsonify, request, abort

app.errorhandler(404)


def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


@app.route('/api/users', methods=['POST'])
def users_endpoint(page=1):
    if request.method == 'POST':  # post request

        row = Users.create(**request.json)
        query = Users.select().where(
            Users.id == row.id,
            Users.name == row.name
        )
        data = [i.serialize for i in query]
        res = jsonify({
            'users': data,
            'meta': {'page_url': request.url}
        })
        res.status_code = 201
        return res


#
# @app.route('/api/reviews', methods=['POST'])
# def reviews_endpoint(page=1):
#
#
#     if request.method == 'POST':  # post request
#
#         row = Reviews.create(**request.json)
#
#         try:
#             foreignkey = Goods.get(
#                 Goods.id == row.goods
#                 )
#         except:
#
#             foreignkey = None
#
#         if foreignkey:
#             print(foreignkey)
#             query = Reviews.select().where(
#                 Reviews.goods == row.goods,
#                 Reviews.review == row.review,
#                 Reviews.pub_date == row.pub_date,
#                 Reviews.author == row.author
#                 )
#             data = [i.serialize for i in query]
#             res = jsonify({
#                 'reviews': data,
#                 'meta': {'page_url': request.url}
#                 })
#             res.status_code = 201
#             return res
#
#         else:
#             # if no results are found.
#             output = {
#                 "error": "No results found. Check url again",
#                 "url": request.url,
#             }
#             res = jsonify(output)
#             res.status_code = 404
#
#
#
##########################################################################
from flask_peewee.utils import get_object_or_404, object_list


@app.route('/')
def goods_list():
    goods = Goods.select()
    return object_list('goods_list.html', goods, 'goods_list')


@app.route('/goods/<id>/')
def goods_detail(id):
    # good = get_object_or_404(Goods, Goods.id == id)
    good = Goods.select().where(Goods.id == id).get()

    return render_template('good_detail.html', good=good)


#################AdminPanel########################
from flask_peewee.admin import Admin, ModelAdmin

auth = Auth(app, db)

from wtforms.fields import FileField, HiddenField, IntegerField, StringField
from wtforms.form import Form


class GoodsAdmin(ModelAdmin):
    columns = ('id', 'name', 'amount', 'size', 'image', 'thumb')

    def get_form(self, adding=False):
        class PhotoForm(Form):
            id = IntegerField()
            name = StringField()
            amount = IntegerField()
            size = StringField()
            image = HiddenField()
            image_file = FileField('Image file')

        return PhotoForm

    def save_model(self, instance, form, adding=False):
        instance = super(GoodsAdmin, self).save_model(instance, form, adding)
        if 'image_file' in request.files:
            file = request.files['image_file']
            instance.save_image(file)
        return instance


class UsersAdmin(ModelAdmin):
    columns = ('id', 'name')


class ReviewsAdmin(ModelAdmin):
    columns = ('goods', 'review', 'pub_date', 'author')


class PhotoAdmin(ModelAdmin):
    columns = ['image', 'thumb']

    def get_form(self, adding=False):
        class PhotoForm(Form):
            image = HiddenField()
            image_file = FileField('Image file')

        return PhotoForm

    def save_model(self, instance, form, adding=False):
        instance = super(PhotoAdmin, self).save_model(instance, form, adding)
        if 'image_file' in request.files:
            file = request.files['image_file']
            instance.save_image(file)
        return instance


admin = Admin(app, auth)
admin.register(Photo, PhotoAdmin)
admin.register(Goods, GoodsAdmin)
admin.register(Users, UsersAdmin)
admin.register(Reviews, ReviewsAdmin)

admin.setup()
######################API#############################
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
api.register(Users)
api.register(Reviews, MessageResource)
api.setup()
########################################################
if __name__ == '__main__':
    auth.User.create_table(fail_silently=True)
    Goods.create_table(fail_silently=True)
    Users.create_table(fail_silently=True)
    Reviews.create_table(fail_silently=True)
    Photo.create_table(fail_silently=True)
    app.run()
