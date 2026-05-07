import time
import requests
from datetime import date

from app.models import db
from app.models.meteo import Meteo

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
RETRY_DELAYS   = [2, 5, 10]  # secondes entre chaque tentative


def fetch_and_save_today(latitude, longitude, zone='Zone A'):
    """
    Récupère la météo du jour pour une zone via Open-Meteo.
    Retry automatique (3 tentatives) en cas de 429 Too Many Requests.
    Met à jour l'enregistrement existant s'il y en a déjà un (upsert).
    Retourne (meteo, message).
    """
    today  = date.today()
    params = {
        'latitude':  latitude,
        'longitude': longitude,
        'current':   'temperature_2m,relative_humidity_2m,precipitation',
        'timezone':  'Europe/Paris',
    }

    resp = None
    for tentative, delai in enumerate(RETRY_DELAYS + [None], start=1):
        try:
            resp = requests.get(OPEN_METEO_URL, params=params, timeout=10)
            if resp.status_code == 429 and delai is not None:
                time.sleep(delai)
                continue
            resp.raise_for_status()
            break
        except requests.RequestException as e:
            if delai is not None:
                time.sleep(delai)
            else:
                return None, f"Erreur météo {zone} après {tentative} tentatives : {e}"

    if resp is None or not resp.ok:
        return None, f"Erreur météo {zone} : impossible de contacter l'API."

    current = resp.json().get('current', {})
    meteo   = Meteo.query.filter_by(date=today, zone=zone).first()

    if meteo:
        meteo.temperature = current.get('temperature_2m')
        meteo.humidite    = current.get('relative_humidity_2m')
        meteo.pluie_mm    = current.get('precipitation', 0.0)
        msg = f"Météo {zone} mise à jour — {meteo.temperature}°C, {meteo.humidite}% humidité."
    else:
        meteo = Meteo(
            date=today,
            zone=zone,
            temperature=current.get('temperature_2m'),
            humidite=current.get('relative_humidity_2m'),
            pluie_mm=current.get('precipitation', 0.0),
        )
        db.session.add(meteo)
        msg = f"Météo {zone} enregistrée — {meteo.temperature}°C, {meteo.humidite}% humidité."

    db.session.commit()
    return meteo, msg
