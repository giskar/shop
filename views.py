__author__ = 'troviln'
from flask import Flask, jsonify, request, abort, render_template, flash, redirect, url_for
from app import app, db
from auth import auth
from model import Goods, User, Reviews, Photo
import datetime


app.errorhandler(404)


def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


# @app.route('/api/users', methods=['POST'])
# def users_endpoint(page=1):
#     if request.method == 'POST':  # post request
#
#         row = Users.create(**request.json)
#         query = Users.select().where(
#             Users.id == row.id,
#             Users.name == row.name
#         )
#         data = [i.serialize for i in query]
#         res = jsonify({
#             'users': data,
#             'meta': {'page_url': request.url}
#         })
#         res.status_code = 201
#         return res
#

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
    if auth.get_logged_in_user():
        name = auth.get_logged_in_user()
        user = User.select().where(User.username == name.username).get()
    else: user = ''
    good = Goods.select().where(Goods.id == id).get()
    return render_template('good_detail.html', good = good, user = user)

@app.route('/join/', methods=['GET', 'POST'])
def join():
    if request.method == 'POST' and request.form['username']:
        try:
            user = User.select().where(User.username==request.form['username']).get()
            flash('That username is already taken')
        except User.DoesNotExist:
            user = User(
                username=request.form['username'],
                email=request.form['email'],

            )
            user.set_password(request.form['password'])
            user.save()

            auth.login_user(user)
            return redirect(url_for('goods_list'))

    return render_template('join.html')



@app.route('/basket/')
def basket():

    return render_template('basket.html')