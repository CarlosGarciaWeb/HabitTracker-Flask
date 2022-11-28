from flask import Flask
from routes import pages
from pymongo import MongoClient
import os

def create_app():

    mongo_address = os.environ.get("MONGODB_ADDRESS")

    client = MongoClient(mongo_address)

    app = Flask(__name__)
    

    app.db = client.flask
    app.register_blueprint(pages)

    return app