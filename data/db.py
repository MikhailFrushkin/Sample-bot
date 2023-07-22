from peewee import *

from data.config import path

db = SqliteDatabase(f'{path}\mydatabase.db')


class Contact(Model):
    name = CharField()
    string = CharField()
    type_contact = CharField()

    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db


class Catalog(Model):
    name = CharField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db


class Sales(Model):
    name = CharField()
    image = CharField()
    url = CharField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db
