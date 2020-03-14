#Dependencies
from os import getenv
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

#MySQL Conection
def config_db(app):
    try:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:toor@'+getenv('DB_HOST')+':3306/db_users'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
        ma.init_app(app)
        db.create_all(app=app)

        print('Connected to MySQL')
    except:
        print('Exiting because MySQL not Connected!')
        exit(1)
    
