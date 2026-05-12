from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from app.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "warning"


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.bmi import bmi_bp
    from app.routes.diet import diet_bp
    from app.routes.progress import progress_bp
    from app.routes.profile import profile_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(bmi_bp)
    app.register_blueprint(diet_bp)
    app.register_blueprint(progress_bp)
    app.register_blueprint(profile_bp)

    return app
