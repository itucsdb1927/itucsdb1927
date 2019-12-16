import os

from flask import Flask, session, render_template
from flask_bcrypt import Bcrypt

from routes.auth import auth_blueprint
from routes.root import root_blueprint

from models.user import User
from util import user_logged_in

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.urandom(32), WTF_CSRF_SECRET_KEY=os.urandom(32), BCRYPT=Bcrypt(app)
)
app.register_blueprint(root_blueprint, url_prefix='/')
app.register_blueprint(auth_blueprint, url_prefix="/auth")


if __name__ == "__main__":
    app.config['SECRET_KEY'] = os.urandom(32)
    app.run()
