from flask import Flask
import locale

def create_app(mode="production"):

	app = Flask("data-science")
	locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

	from blueprints.base import base as base_blueprint
	from blueprints.aula1 import aula1 as aula1_blueprint

	app.register_blueprint(base_blueprint)
	app.register_blueprint(aula1_blueprint, url_prefix="/aula1")

	if mode == "production":
		app.config.from_object('config.production')
	else:
		app.config.from_object('config.development')

	return app