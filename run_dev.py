import logging
from main_app import create_app

mode = 'development'
app = create_app(mode=mode)

logformat = '%(asctime)s - (%(levelname)s): %(message)s'

logging.basicConfig(level=logging.DEBUG, format=logformat)
print("===== scheduled jobs nor started in development mode =======")

app.run(**app.config.get_namespace('RUN_'))