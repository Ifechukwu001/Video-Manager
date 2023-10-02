"""Main App"""
import os
from flask import Flask, jsonify
from flask_swagger import swagger
from api.views import api_views
import models


app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 * 2
app.config["TEMPORARY_FOLDER"] = "./temp"
app.config["PERMANENT_FOLDER"] = "./Videos"

app.register_blueprint(api_views, )


@app.route("/api/docs")
def docs():
    base_path = os.path.join(app.root_path, "docs")
    return jsonify(swagger(app, from_file_keyword="swagger_file", base_path=base_path))


@app.teardown_appcontext
def close_db(exception):
    models.storage.close()
