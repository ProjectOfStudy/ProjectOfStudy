from flask import Flask, app
from app.models import db
from app.config import Config


def create_app():
    app = Flask(__name__, template_folder='template', static_folder='static')
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes.alertes import alertes_bp
    app.register_blueprint(alertes_bp)

    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    from app.routes.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)

    return app
