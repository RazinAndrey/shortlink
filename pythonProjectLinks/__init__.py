# подключаем класс Flask - для работы с сайтом
from flask import Flask
# для работы с БД
from flask_sqlalchemy import SQLAlchemy
# LoginManager - помогает нам работать с пользователем;
from flask_login import LoginManager

# имя нашего приложения
app = Flask(__name__)
# секретный ключ
app.secret_key = 'secret_key'
# обращаемся к словарю config и задаем ему базу данных с которой мы будем работать
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///links.db'
# убераем ошибку
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# подключи менеджер в app
login_manager = LoginManager(app)
# Flask работает с БД
db = SQLAlchemy(app)


