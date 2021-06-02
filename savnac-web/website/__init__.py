from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, current_user
from os import environ

db = SQLAlchemy()

def create_app():
	app = Flask(__name__)
	app.config['SECRET_KEY'] = environ['SECRET_KEY']
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2' + environ['DATABASE_URL'][8:]
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)

	from .pages import pages
	from .auth import auth
	
	app.register_blueprint(pages,url_prefix='/')
	app.register_blueprint(auth,url_prefix='/')

	from .models import User

	db.create_all(app=app)

	login_manager = LoginManager()
	login_manager.login_view = 'auth.login'
	login_manager.init_app(app)

	@login_manager.user_loader
	def load_user(id):
		return User.query.get(int(id))
	
	@app.errorhandler(404)
	def notfound(e):
		return render_template('not_found.html', user=current_user)

	return app
