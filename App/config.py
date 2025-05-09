import os


def load_config(app, overrides):
    if os.path.exists(os.path.join('./App', 'custom_config.py')):
        app.config.from_object('App.custom_config')
    else:
        app.config.from_object('App.default_config')

    # Load environment variable-based configurations
    app.config.from_prefixed_env()

    # Core settings
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['UPLOADED_PHOTOS_DEST'] = "App/uploads"

    # JWT authentication settings
    app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
    app.config["JWT_TOKEN_LOCATION"] = ["cookies", "headers"]
    app.config["JWT_COOKIE_SECURE"] = True
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False

    # Dynamic definition of valid model attributes
    app.config["JOB_POSITION_TYPES"] = set(
        app.config.get("JOB_POSITION_TYPES", []))
    app.config["APPROVAL_STATUSES"] = set(
        app.config.get("APPROVAL_STATUSES", []))
    for key in overrides:
        app.config[key] = overrides[key]
