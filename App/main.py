import os
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

from App.database import init_db, db
from App.config import load_config

from App.controllers import (
    setup_jwt,
    add_auth_context
)

from App.views import views


def add_views(app):
    for view in views:
        app.register_blueprint(view)


def create_app(overrides={}):
    # Load environment variables from .env
    load_dotenv()

    app = Flask(__name__, static_url_path='/static')

    # Load config from environment or override dict
    load_config(app, overrides)
    
    # Optional fallback config
    app.config.from_pyfile('default_config.py', silent=True)

    CORS(app)
    add_auth_context(app)
    
    # Database setup
    init_db(app)
    with app.app_context():
        db.create_all()

    # File upload setup
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)

    # Register views
    add_views(app)
    
    # JWT setup
    jwt = setup_jwt(app)

    @jwt.invalid_token_loader
    @jwt.unauthorized_loader
    def custom_unauthorized_response(error):
        return render_template('401.html', error=error), 401
    
    # Push context if needed
    app.app_context().push()

    return app
