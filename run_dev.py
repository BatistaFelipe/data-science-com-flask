import logging
from main_app import create_app

app = create_app(mode='development')

logformat = '%(asctime)s - (%(levelname)s): %(message)s'

logging.basicConfig(level=logging.DEBUG, format=logformat)
app.run(**app.config.get_namespace('RUN_'))