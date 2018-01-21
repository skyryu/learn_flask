'''
package entrance
'''

import os

from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from logging import DEBUG

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = '010018'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(BASE_DIR, 'dark_soul.db')

#I can't see any case in this app that we need to track obj modifcations of sqlalchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.logger.setLevel(DEBUG)

#sqlite db
db = SQLAlchemy(app)

#configure authentication
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)

import dark_soul.models
import dark_soul.views
