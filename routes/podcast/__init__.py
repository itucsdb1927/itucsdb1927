from flask import Blueprint

podcast_blueprint = Blueprint('podcast', __name__)

from . import create, view, update
