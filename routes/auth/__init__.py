from flask import Blueprint

auth_blueprint = Blueprint('auth', __name__)

from . import login, logout, signup, change_password
