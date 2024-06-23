from flask import Flask
from firebase_admin import credentials, initialize_app
from flask_cors import CORS, cross_origin

cred = credentials.Certificate("D:/Users/DELL/Desktop/SWHackathon/API/api/key.json")
default_app = initialize_app(cred)


def create_app():
    app = Flask(__name__)
    cors = CORS(app, origins=["https://cecb-2603-7080-2004-d100-b94b-cc2b-4a59-3cf7.ngrok-free.app"])

    app.config["SECRET_KEY"] = "12345678jkdbshb"

    from .userAPI import userAPI

    app.register_blueprint(userAPI)
    return app
