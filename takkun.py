import sqlite3

from flask import Flask, g
from werkzeug.middleware.proxy_fix import ProxyFix

import environment

app = Flask(__name__)

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1) # In production we pass requests through ngix as a reverse proxy. And a lot of things break... This fixes them!

def get_db():
    if "db" not in g:
      g.db = sqlite3.connect(environment.DATABASE_PATH)

    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

app.teardown_appcontext(close_db)

@app.route("/training-sessions", methods=["GET"])
def get_training_sessions():
    # TODO: query all training sessions logic
    pass

@app.route("/training-sessions/<int:id>", methods=["GET"])
def get_training_session_by_id(id : int):
    # TODO: query training session logic
    pass

@app.route("/training-sessions", methods=["POST"])
def get_training_session_by_id(id : int):
    # TODO: create session logic
    pass

@app.route("/training-sessions", methods=["DELETE"])
def get_training_session_by_id(id : int):
    # TODO: delete session logic
    pass