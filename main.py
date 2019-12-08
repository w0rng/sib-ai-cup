#!/usr/bin/env python3

from flask import Flask, render_template, request
import api
from os import path, stat
from flask.helpers import url_for


app = Flask(__name__)
#app.secret_key = os.environ.get(["FLASK_KEY"])

@app.route('/')
def index():
    return render_template('index.html')

# Форма получения токена
@app.route('/token', methods=['GET'])
def token():
    return render_template('token.html')

# Генерация токена
@app.route('/get_token', methods=['POST'])
def get_token():
    return api.get_token(request.form['name'], request.form['pass'])

# Список всех ботов
@app.route('/get_bots', methods=['GET'])
def get_bots():
    return api.get_bots()

# Список всех ботов с доп. параметрами
@app.route('/get_bots_for_draw', methods=['GET'])
def get_bots_for_draw():
    return api.get_bots(True)

# Нужно, чтобы браузер не кэшировал статичные файлы
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = path.join(app.root_path, endpoint, filename)
            values['q'] = int(stat(file_path).st_mtime)
    return url_for(endpoint, **values)


if __name__ == "__main__":
    app.run()
