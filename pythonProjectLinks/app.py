# делаем импорт string и random для того, чтобы делать ссылку короче
import string
import random

# render_template - для работы с html; request - инструмент для составления HTTP-запросов;
# redirect - взаимодействовать с веб-приложением; flash - для вывода сообщения на самой странице;
# url_for - принимает и возвращает URL в виде строки
from flask import render_template, request, redirect, flash, url_for

# обеспечивает управление пользовательскими сеансами для Flask
from flask_login import login_user

# с помощью check_password_hash и generate_password_hash работаем с паролем
from werkzeug.security import check_password_hash, generate_password_hash

# импортируем User, Urls, app, db, login_manager из init и models
from models import Users, Urls
from __init__ import app, db, login_manager


# нужно для работы с пользователем
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


# СТАРТ
# используем декоратор route(), чтобы сказать Flask, какой из URL должен запускать нашу фуцию
@app.route("/")
def start():
    return render_template("start.html")


# ПРИЛОЖЕНИЕ

# функция, которая сокращает url
def shorten_url():
    letters = string.ascii_lowercase + string.ascii_uppercase
    while True:
        rand_letters = random.choices(letters, k=3)
        rand_letters = "".join(rand_letters)
        short_url = Urls.query.filter_by(short=rand_letters).first()
        # если не короткая ссылка,
        if not short_url:
            return rand_letters


@app.route('/links', methods=['POST', 'GET'])
def links():
    if request.method == 'POST':
        # получить url
        url_received = request.form['link']
        # проверяю, существует ли URL - адрес в базе данных
        found_url = Urls.query.filter_by(long=url_received).first()
        if found_url:
            # вернуть короткий URL, если найден
            return redirect(url_for("display_short_url", url=found_url.short))
        else:
            # создать короткий URL - адрес, если не найден
            short_url = shorten_url()
            new_url = Urls(url_received, short_url)
            db.session.add(new_url)
            db.session.commit()
            return redirect(url_for("display_short_url", url=short_url))
    else:
        return render_template('links.html')


@app.route('/display/<url>')
# функция, которая отображает короткий URL
def display_short_url(url):
    return render_template('shorturl.html', short_url_display=url)


@app.route('/<short_url>')
# функция, которая перенаправляет
def redirection(short_url):
    long_url = Urls.query.filter_by(short=short_url).first()
    if long_url:
        return redirect(long_url.long)
    else:
        return f'<h1>URL не существует</h1>'


# ВХОД
# POST предназначен для запроса, при котором веб-сервер принимает данные, заключённые в тело сообщения, для хранения
# GET -предназначен для получения информации от сервера
@app.route("/enter", methods=['POST', 'GET'])
def enter():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = Users.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            login_user(user)

            return redirect('/links')
        else:
            flash('Логин или пароль неверный')

    else:
        flash('Пожалуйста, заполните поля логина и пароля')
    return render_template('enter.html')


# РЕГИСТРАЦИЯ
@app.route("/registration", methods=['POST', 'GET'])
def registration():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if request.method == 'POST':
        if not (login or password or password2):
            flash('Пожалуйста, заполните все поля...')
        elif password != password2:
            flash('Пароли не равны!')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = Users(login=login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('enter'))

    return render_template('/registration.html')


if __name__ == "__main__":
    # запуск локального сервера
    app.run(debug=True)