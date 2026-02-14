from functools import wraps
import sqlite3
from datetime import datetime

from flask import Flask, g, request, jsonify, current_app
from werkzeug.middleware.proxy_fix import ProxyFix

import environment

from domain import *

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

def auth_api_key(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    con = get_db()

    api_key = request.args.get("api_key", None)

    if not api_key:
      return jsonify({"error": "api_key missing"}), 401

    account = AccountRepo.get_by_api_key(con, api_key)

    if not account:
      return jsonify({"error": "invalid api_key"}), 403

    return f(account, *args, **kwargs)

  return decorated

@app.route("/training-sessions", methods=["GET"])
@auth_api_key
def get_training_sessions(account : TAccount):
  con = get_db() 

  training_sessions = TrainingSessionRepo.ReadMultiple(con, account.id)
  
  return jsonify([ts.to_dict() for ts in training_sessions])

@app.route("/training-sessions/<int:id>", methods=["GET"])
@auth_api_key
def get_training_session_by_id(account : TAccount, id : int):
  con = get_db()
  
  training_session = TrainingSessionRepo.Read(con, id)

  if not training_session:
    return {"error": "not found"}, 404
  
  if training_session.account_id != account.id:
    return {"error": "forbidden"}, 403

  return jsonify(training_session.to_dict())

@app.route("/training-sessions", methods=["POST"])
@auth_api_key
def add_training_session(account : TAccount):
  con = get_db()

  body = request.get_json()

  print("body: ", body)
  
  training_session = TTrainingSession()

  training_session.account_id = account.id
  training_session.created_at = datetime.now()
  training_session.updated_at = datetime.now()

  training_session = TrainingSessionRepo.Create(con, training_session)

  con.commit()

  return jsonify(training_session.to_dict())

@app.route("/training-sessions/<int:id>", methods=["DELETE"])
@auth_api_key
def del_training_session_by_id(account : TAccount, id : int):
  con = get_db()

  training_session = TrainingSessionRepo.Read(con, id)

  if not training_session:
    return {"error": "not found"}, 404
  
  if training_session.account_id != account.id:
    return {"error": "forbidden"}, 403

  TrainingSessionRepo.Delete(con, training_session.id)

  con.commit()
  
  return {"response": "success"}, 200