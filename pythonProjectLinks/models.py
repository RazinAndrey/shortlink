# UserMixin - обеспечивает реализацию выжных свойств для юзер;
from flask_login import UserMixin
# импортируем db и app из init
from __init__ import db, app


# создаем класс Users
class Users(db.Model, UserMixin):
    # создаем поля
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, login, password):
        self.login = login
        self.password = password


# создаем класс Urls
class Urls(db.Model):
    # создаем поля
    id = db.Column("id", db.Integer, primary_key=True)
    long = db.Column("long", db.String())
    short = db.Column("short", db.String(3))

    def __init__(self, long, short):
        self.long = long
        self.short = short


# создание таблиц
@app.before_first_request
def create_tables():
    db.create_all()