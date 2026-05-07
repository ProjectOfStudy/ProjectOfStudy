import threading
from flask import Blueprint, redirect, url_for, flash, current_app
from flask_login import login_required

meteo_bp = Blueprint('meteo', __name__, url_prefix='/meteo')


def _actualiser_en_arriere_plan(app):
    """Récupère la météo et génère les observations en arrière-plan."""
    import time
    from app.models.zone import Zone
    from app.services.meteo_service import fetch_and_save_today
    from app.services.analyse_service import generate_daily_observations

    with app.app_context():
        try:
            zones = Zone.query.all()
            for i, z in enumerate(zones):
                if i > 0:
                    time.sleep(1)
                _, msg = fetch_and_save_today(z.latitude, z.longitude, z.nom)
                app.logger.info(f"[Meteo] {msg}")
            nb = generate_daily_observations()
            app.logger.info(f"[Meteo] {nb} observations générées.")
        except Exception as e:
            app.logger.error(f"[Meteo] Erreur arrière-plan : {e}")


@meteo_bp.route('/actualiser', methods=['POST'])
@login_required
def actualiser():
    """Lance la récupération météo en arrière-plan et redirige immédiatement."""
    app = current_app._get_current_object()
    thread = threading.Thread(target=_actualiser_en_arriere_plan, args=(app,), daemon=True)
    thread.start()

    flash("Actualisation météo lancée — les données seront disponibles dans quelques secondes.")
    return redirect(url_for('dashboard.dashboard'))
