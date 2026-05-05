from flask import Flask
from app.models import db
from app.config import Config


def create_app():
    app = Flask(__name__, template_folder='template', static_folder='static')
    app.config.from_object(Config)

    db.init_app(app)

    # Importer tous les modèles pour que SQLAlchemy les enregistre
    from app.models import proprietaire, parcelle, culture, alerte, observation, meteo  # noqa: F401

    # Enregistrement des blueprints
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    from app.routes.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)

    from app.routes.parcelles import parcelles_bp
    app.register_blueprint(parcelles_bp)

    from app.routes.alertes import alertes_bp
    app.register_blueprint(alertes_bp)

    return app
