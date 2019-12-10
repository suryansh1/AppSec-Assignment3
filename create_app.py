from flask import Flask
import os
from databases import db
basedir = os.path.abspath(os.path.dirname(__file__))

def app_creator():
	app = Flask(__name__)

	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
	
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	
	app.config.update(dict(
	    SECRET_KEY="powerful secretkey",
	    WTF_CSRF_SECRET_KEY="a csrf secret key"
	))

	db.init_app(app)

	with app.app_context():
		db.create_all()

	return app