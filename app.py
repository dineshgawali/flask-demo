import os
import uuid
from flask import Flask
from flask import request
from flask import session
from flask_httpauth import HTTPTokenAuth
from werkzeug.security import generate_password_hash, check_password_hash
from pathlib import Path


app = Flask(__name__)
app.secret_key = 'abcdefgashhijklwimnopni'
auth = HTTPTokenAuth(scheme='Bearer')

tokens = {}
current_directories = {}

@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]

def add_token(username):
    token = str(uuid.uuid4())
    tokens[token] = username
    return token


@app.route('/')
def ping():
    # curl http://127.0.0.1:8080/
    return 'working!'


@app.route('/restapi/login/', methods=['POST'])
def login():
    # curl -X POST -F 'username=dinesh1' http://127.0.0.1:8080/restapi/login/
    username = request.form['username']
    session['username']= username
    token = add_token(username)
    return {
        "token":token
        }
    

@app.route('/restapi/cwd/', methods=['GET'])
@auth.login_required
def cwd():
    # curl -H 'Authorization: Bearer ' localhost:8080/restapi/cwd/
    token = request.headers.get('Authorization', "").replace('Bearer ', "")
    current_directory = current_directories.get(token, os.getcwd())
    return {
        "cwd":current_directory
        }


@app.route('/restapi/ls/', methods=['GET'])
@auth.login_required
def ls():
    # curl -H 'Authorization: Bearer ' localhost:8080/restapi/ls/
    token = request.headers.get('Authorization', "").replace('Bearer ', "")
    current_directory = current_directories.get(token, os.getcwd())
    # listdir = os.scandir(current_directory)
    # response = [{"name": obj.name, "type": "FILE" if obj.is_file() else "DIRECTORY"} for obj in listdir]
    response = []
    with os.scandir(current_directory) as listdir:
        for entry in listdir:
            file_type = 'FILE' if entry.is_file() else 'DIRECTORY'
            response.append({
                'name': entry.name,
                'type': file_type
            })

    return {
        "ls":response
        }


@app.route('/restapi/cd/', methods=['GET'])
@auth.login_required
def change_directory():
    # curl -H 'Authorization: Bearer <>' http://127.0.0.1:8080/restapi/cd/?directory=\/home\/dinesh/\dinesh\/
    changed_directory = request.args['directory']
    is_directory_exists = Path(changed_directory).is_dir()
    if not is_directory_exists:
        return {
            "message": "Changed directory is not exists"
            }
    token = request.headers.get('Authorization', "").replace('Bearer ', "")
    current_directories[token] = changed_directory
    return {
        "message": "Directory Changed"
        }


@app.route('/restapi/logout/', methods=['GET'])
@auth.login_required
def logout():
    # curl -H 'Authorization: Bearer <>' http://127.0.0.1:8080/restapi/logout/
    token = request.headers.get('Authorization', "").replace('Bearer ', "")
    tokens.pop(token)
    if token in current_directories:
        current_directories.pop(token)
    return {
        "message": "User Logout"
        }