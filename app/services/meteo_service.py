import requests
from datetime import date

from app.models import db
from app.models.meteo import Meteo

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


def fetch_and_save_today(latitude, longitude, zone='Zone A'):
    """
    Récupère la météo du jour pour une zone via Open-Meteo.
    Met à jour l'enregistrement existant s'il y en a déjà un (upsert).
    Retourne (meteo, message).
    """
    today = date.today()

    params = {
        'latitude':  latitude,
        'longitude': longitude,
        'current':   'temperature_2m,relative_humidity_2m,precipitation',
        'timezone':  'Europe/Paris',
    }

    try:
        resp = requests.get(OPEN_METEO_URL, params=params, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        return None, f"Erreur météo {zone} : {e}"

    current = resp.json().get('current', {})

    meteo = Meteo.query.filter_by(date=today, zone=zone).first()

    if meteo:
        # Mise à jour de l'enregistrement existant
        meteo.temperature = current.get('temperature_2m')
        meteo.humidite    = current.get('relative_humidity_2m')
        meteo.pluie_mm    = current.get('precipitation', 0.0)
        msg = f"Météo {zone} mise à jour — {meteo.temperature}°C, {meteo.humidite}% humidité."
    else:
        # Création d'un nouvel enregistrement
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
