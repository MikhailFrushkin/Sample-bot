from datetime import datetime

from peewee import *

from data.config import path

db = SqliteDatabase(f'{path}\mydatabase.db')


class User(Model):
    user_id = IntegerField()
    first_name = CharField(null=True)
    last_name = CharField(null=True)
    nickname = CharField(null=True)
    lesson = IntegerField(default=1)
    check_1 = BooleanField(default=False)
    check_2 = BooleanField(default=False)

    created_at = DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.user_id} - {self.nickname}'

    class Meta:
        database = db


def get_or_create_user(user_id, first_name, last_name=None, nickname=None):
    user, created = User.get_or_create(
        user_id=user_id,
        defaults={
            'first_name': first_name,
            'last_name': last_name,
            'nickname': nickname
        }
    )

    if created:
        print(f"Новый пользователь добавлен: {user_id}")
    else:
        print(f"Пользователь уже существует: {user_id}")

    return user
