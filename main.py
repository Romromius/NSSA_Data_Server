from flask import Flask, request, jsonify
from data_bank import NSSADataBank
import subprocess

app = Flask(__name__)


def check_for_updates():
    try:
        _ = subprocess.run(["git", "fetch"], check=True)
        status = subprocess.run(["git", "status", "-uno"], capture_output=True, text=True)
    except subprocess.CalledProcessError:
        return False

    if "Your branch is behind" in status.stdout:
        return True
    return False


def pull_updates():
    try:
        subprocess.run(["git", "pull"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False


@app.route('/')
def index():
    response = {}
    db = NSSADataBank()
    key = request.args.get('key')
    password = request.args.get('password')
    language = request.args.get('language')
    if language:
        response['response'] = db.get_data(key, password, language)
    else:
        response['response'] = db.get_data(key, password)
    return jsonify(response)


@app.route('/update')
def update():
    responce = {}
    responce['has_updates'] = check_for_updates()
    if responce['has_updates']:
        update_status = pull_updates()
    if update_status:
        responce['status'] = 'OK'
    return jsonify(responce)


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True)