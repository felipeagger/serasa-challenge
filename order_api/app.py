#Dependencies
from os import getenv
from dotenv import load_dotenv
from os.path import dirname, isfile, join

# setting enviroment file
_ENV_FILE = join(dirname(__file__), '.env_')
if isfile(_ENV_FILE):
    load_dotenv(dotenv_path=_ENV_FILE)

from flask import Flask, jsonify, request, make_response, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from config import config
from routes import orderRoutes


### App Config ###

#Flask - instance
def create_app(config_name):
    app = Flask(__name__, static_folder='static')
    app.config.from_object(config[config_name])
    CORS(app)
    return app
 
app = create_app(getenv('FLASK_ENV') or 'default') 


# Register Routes
app.register_blueprint(orderRoutes)


### Swagger Documentation ###
@app.route('/swagger.json')  
def send_file():  
    return send_from_directory(app.static_folder, 'swagger.json')

SWAGGER_URL = '/api-docs'
API_URL = '/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Orders-API"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###


#### App ####
if __name__ == '__main__':
    ip = '0.0.0.0'
    port = app.config['APP_PORT']
    debug = app.config['DEBUG']

    # execute flask web server
    app.run(
        host=ip, debug=debug, port=port, use_reloader=debug
    )
#### end ####