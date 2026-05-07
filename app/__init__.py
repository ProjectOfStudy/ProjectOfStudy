import atexit
from flask import Flask, app
from flask_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler
from app.models import db
from app.config import Config

login_manager = LoginManager()


def create_app():
    app = Flask(__name__, template_folder='template', static_folder='static')
    app.config.from_object(Config)

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view    = 'login.login_page'
    login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'

    # Importer tous les modèles pour que SQLAlchemy les enregistre
    from app.models import proprietaire, parcelle, culture, alerte, observation, meteo, zone  # noqa: F401

    # Crée les tables si elles n'existent pas (SQLite local ou PostgreSQL Render)
    with app.app_context():
        db.create_all()

    from app.models.proprietaire import Proprietaire

    @login_manager.user_loader
    def load_user(user_id):
        return Proprietaire.query.get(int(user_id))

    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    from app.routes.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)

    from app.routes.parcelles import parcelles_bp
    app.register_blueprint(parcelles_bp)

    from app.routes.alertes import alertes_bp
    app.register_blueprint(alertes_bp)

    from app.routes.meteo import meteo_bp
    app.register_blueprint(meteo_bp)

    from app.routes.login import login_bp
    app.register_blueprint(login_bp)

    from app.routes.observations import observations_bp
    app.register_blueprint(observations_bp)

    _start_scheduler(app)

    return app


def _start_scheduler(app):
    """Lance une tâche automatique toutes les heures pour toutes les zones."""
    def hourly_job():
        with app.app_context():
            from app.models.zone import Zone
            from app.services.meteo_service import fetch_and_save_today
            from app.services.analyse_service import generate_daily_observations
            for z in Zone.query.all():
                _, msg = fetch_and_save_today(z.latitude, z.longitude, z.nom)
                print(f'[Scheduler] {msg}')
            nb = generate_daily_observations()
            print(f'[Scheduler] {nb} observations générées.')

    scheduler = BackgroundScheduler(timezone='Europe/Paris')
    scheduler.add_job(func=hourly_job, trigger='interval', hours=1)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
