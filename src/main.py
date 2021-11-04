from api.utils.responses import response_with
import api.utils.responses as resp
import os
from flask import Flask
from flask import jsonify
from api.utils.database import db
from api.routes.authors import author_routes
import logging
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.register_blueprint(author_routes, url_prefix='/api/authors')


def create_app(config):
    app.config.from_object(config)

    @app.after_request
    def add_header(response):
        return response

    @app.errorhandler(400)
    def bad_request(e):
        logging.error(e)
        return response_with(resp.BAD_REQUEST_400)

    @app.errorhandler(500)
    def server_error(e):
        logging.error(e)
        return response_with(resp.SERVER_ERROR_500)

    @app.errorhandler(404)
    def not_found(e):
        logging.error(e)
        return response_with(resp.SERVER_ERROR_404)

    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app


'''if os.environ.get('WORK_ENV') == 'PROD':
    app_config = "production"
elif os.environ.get('WORK_ENV') == 'TEST':
    app_config = 'test'
else:'''
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://<username>:<password>@<ip_Address>:<database_name> '
db = SQLAlchemy(app)

app.config.from_object(app)
if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", use_reloader=True)
