from flask import Blueprint

episode_blueprint = Blueprint('episode', __name__)

from . import create, update, delete
