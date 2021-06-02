from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(128), unique=True)
	password = db.Column(db.String(128))
	api_token = db.Column(db.String(69))
	domain = db.Column(db.String(128))
