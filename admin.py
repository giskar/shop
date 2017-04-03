import pprint

__author__ = 'troviln'
from flask_peewee.admin import Admin, ModelAdmin, AdminPanel
from app import app, db
from auth import auth
from model import Goods, User, Reviews, Photo, Order
from wtforms.fields import FileField, HiddenField, IntegerField, StringField, FloatField
from wtforms.form import Form
from flask import request


class GoodsAdmin(ModelAdmin):
    columns = ('id', 'name', 'amount', 'price', 'size', 'image', 'thumb')

    def get_form(self, adding=False):
        class PhotoForm(Form):

            name = StringField()
            amount = IntegerField()
            size = StringField()
            price = FloatField()
            image = HiddenField()
            image_file = FileField('Image file')

        return PhotoForm

    def save_model(self, instance, form, adding=False):
        instance = super(GoodsAdmin, self).save_model(instance, form, adding)
        if 'image_file' in request.files:
            file = request.files['image_file']
            instance.save_image(file)
        return instance


class UserAdmin(ModelAdmin):
    columns = ('username', 'admin')

    def save_model(self, instance, form, adding=False):
        orig_password = instance.password

        user = super(UserAdmin, self).save_model(instance, form, adding)

        if orig_password != form.password.data:
            user.set_password(form.password.data)
            user.save()

        return user


class CustomAdmin(Admin):
    def check_user_permission(self, user):
        return user.admin


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


class NotePanel(AdminPanel):
    template_name = 'admin/note.html'

    def get_context(self):

        return {
            'list': Order.select(),
        }


admin = Admin(app, auth, branding='Example Site')

auth.register_admin(admin)
admin = CustomAdmin(app, auth)
admin.register(Photo, PhotoAdmin)
admin.register(Goods, GoodsAdmin)
admin.register(User, UserAdmin)
admin.register(Reviews, ReviewsAdmin)
admin.register(Order)
admin.register_panel('Orders', NotePanel)


