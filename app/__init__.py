from flask import Flask
from flask_migrate import Migrate
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from flask_migrate import Migrate
# from . import routes, models
from .config import Config
from flask_bootstrap import Bootstrap
# Globally accessible libraries
db = SQLAlchemy()
r = FlaskRedis()
login_manager = LoginManager()


def create_app():
    #Initialize the core application
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config) #".config.Config"
    # Initialize Plugins
    db.init_app(app)
    r.init_app(app)

    with app.app_context():
        # Include our Routes
        # from . import routes

        # Register Blueprints
        # app.register_blueprint(auth.auth_bp)
        # app.register_blueprint(admin.admin_bp)
        # Migration

        db.create_all()
        Bootstrap(app)

        login_manager.init_app(app)
        login_manager.login_message = "You must be logged in to access this page."
        login_manager.login_view = "auth.login"

        migrate = Migrate(app, db)

        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)
        from .home import home as home_blueprint
        app.register_blueprint(home_blueprint)

        return app
