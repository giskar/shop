__author__ = 'troviln'
class Configuration(object):
    DATABASE = {
        'name': 'example2.db',
        'engine': 'peewee.SqliteDatabase',
        'check_same_thread': False,
    }
    DEBUG = True
    SECRET_KEY = 'shhhh'



    # DATABASE = {
    #     'name': 'postgres',
    #     'engine': 'peewee.PostgresqlDatabase',
    #
    #
    # }