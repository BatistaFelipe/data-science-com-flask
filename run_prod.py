# https://docs.gunicorn.org/en/stable/custom.html - data: 01/05/2020

import logging
from main_app import create_app
import multiprocessing
from gunicorn.app.base import BaseApplication

def number_of_workers():
	return (multiprocessing.cpu_count() * 2) + 1

class StandaloneApplication(BaseApplication):
	def __init__(self, app, options=None):
		self.options = options or {}
		self.application = app
		super(StandaloneApplication, self).__init__()
	
	def load_config(self):
		config = dict([(key, value) for key, value in self.options.items()
		if key in self.cfg.settings and value is not None])
		for key, value in config.items():
			self.cfg.set(key.lower(), value)


	def load(self):
		return self.application

		
if __name__ == '__main__':
	app = create_app()
	logformat = '%(asctime)s [%(process)s] [%(levelname)s]: %(message)s'
	logging.basicConfig(level=logging.INFO, format=logformat)
	
	print("===== scheduled jobs nor started in development mode =======")

	options = {
        'bind': '%s:%s' % ('127.0.0.1', '8000'),
		'workers': number_of_workers(),
		"threads": 4,
		"worker-class": "eventlet",
	}

	StandaloneApplication(app, options).run()