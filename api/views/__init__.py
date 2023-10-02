"""API Views"""
from flask import Blueprint


api_views = Blueprint("api_views", __name__)

from .video_upload import *
from .video_stream import *
