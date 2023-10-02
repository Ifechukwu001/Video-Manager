"""Main App"""
from flask import Flask
from api.views import api_views
import models


app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024
app.config["TEMPORARY_FOLDER"] = "./temp"
app.config["PERMANENT_FOLDER"] = "./Videos"

app.register_blueprint(api_views)


@app.teardown_appcontext
def close_db(exception):
    models.storage.close()
