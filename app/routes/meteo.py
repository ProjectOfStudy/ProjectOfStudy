import time
import traceback
from flask import Blueprint, redirect, url_for, flash, current_app
from flask_login import login_required
from app.models.zone import Zone
from app.services.meteo_service import fetch_and_save_today
from app.services.analyse_service import generate_daily_observations

meteo_bp = Blueprint('meteo', __name__, url_prefix='/meteo')


@meteo_bp.route('/actualiser', methods=['POST'])
@login_required
def actualiser():
    """Déclenche manuellement la récupération météo pour toutes les zones."""
    try:
        zones = Zone.query.all()

        for i, z in enumerate(zones):
            if i > 0:
                time.sleep(1)
            _, msg = fetch_and_save_today(z.latitude, z.longitude, z.nom)
            flash(msg)

        nb = generate_daily_observations()
        if nb > 0:
            flash(f'{nb} observations générées automatiquement.')
        else:
            flash("Observations déjà enregistrées pour aujourd'hui.")

    except Exception as e:
        current_app.logger.error(f"Erreur actualiser météo : {traceback.format_exc()}")
        flash(f"Erreur lors de la mise à jour météo : {e}")

    return redirect(url_for('dashboard.dashboard'))
