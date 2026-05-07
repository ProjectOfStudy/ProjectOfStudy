from flask import Blueprint, redirect, url_for, flash
from flask_login import login_required
from app.models.zone import Zone
from app.services.meteo_service import fetch_and_save_today
from app.services.analyse_service import generate_daily_observations

meteo_bp = Blueprint('meteo', __name__, url_prefix='/meteo')


@meteo_bp.route('/actualiser', methods=['POST'])
@login_required
def actualiser():
    """Déclenche manuellement la récupération météo pour toutes les zones."""
    zones = Zone.query.all()

    for z in zones:
        _, msg = fetch_and_save_today(z.latitude, z.longitude, z.nom)
        flash(msg)

    nb = generate_daily_observations()
    if nb > 0:
        flash(f'{nb} observations générées automatiquement.')
    else:
        flash("Observations déjà enregistrées pour aujourd'hui.")

    return redirect(url_for('dashboard.dashboard'))
