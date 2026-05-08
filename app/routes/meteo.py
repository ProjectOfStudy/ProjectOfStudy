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
            print(f"[Meteo] {len(zones)} zones trouvées.")
            for i, z in enumerate(zones):
                if i > 0:
                    time.sleep(1)
                _, msg = fetch_and_save_today(z.latitude, z.longitude, z.nom)
                print(f"[Meteo] {msg}")
            nb = generate_daily_observations()
            print(f"[Meteo] {nb} observations générées.")
        except Exception as e:
            import traceback
            print(f"[Meteo] Erreur : {e}")
            print(traceback.format_exc())


@meteo_bp.route('/test')
@login_required
def test():
    """Route de diagnostic — à supprimer après."""
    import requests
    from app.models.zone import Zone
    from app.models.meteo import Meteo
    from datetime import date
    lignes = []
    zones = Zone.query.all()
    lignes.append(f"Zones en BDD : {len(zones)}")
    lignes.append(f"Meteo aujourd'hui ({date.today()}) : {Meteo.query.filter_by(date=date.today()).count()} enregistrements")
    # Test un seul appel API sans retry
    if zones:
        z = zones[0]
        try:
            r = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params={'latitude': z.latitude, 'longitude': z.longitude,
                        'current': 'temperature_2m', 'timezone': 'Europe/Paris'},
                timeout=5
            )
            lignes.append(f"API Open-Meteo ({z.nom}) : HTTP {r.status_code}")
        except Exception as e:
            lignes.append(f"API Open-Meteo erreur : {e}")
    return '<br>'.join(lignes)


@meteo_bp.route('/actualiser', methods=['POST'])
@login_required
def actualiser():
    """Lance la récupération météo en arrière-plan et redirige immédiatement."""
    app = current_app._get_current_object()
    thread = threading.Thread(target=_actualiser_en_arriere_plan, args=(app,), daemon=True)
    thread.start()

    flash("Actualisation météo lancée — les données seront disponibles dans quelques secondes.")
    return redirect(url_for('dashboard.dashboard'))
