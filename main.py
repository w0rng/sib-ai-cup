from flask import Flask, request
import db


app = Flask(__name__)


@app.route('/reg/<name>', methods=['POST'])
def reg(name):
    return db.register(name.lower())


@app.route('/bots', methods=['GET'])
def get_bots():
    return db.get_bots()


if __name__ == "__main__":
    app.run()
