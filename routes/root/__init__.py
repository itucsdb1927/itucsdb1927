from flask import Blueprint

root_blueprint = Blueprint('root', __name__)

from . import home, search
