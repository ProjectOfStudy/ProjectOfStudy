from datetime import date, datetime

from app.models import db
from app.models.meteo import Meteo
from app.models.observation import Observation
from app.models.parcelle import Parcelle


def generate_daily_observations():
    """
    Génère une observation par heure pour chaque parcelle
    en utilisant la météo de sa zone.
    Retourne le nombre d'observations créées.
    """
    today        = date.today()
    heure_actuelle = datetime.now().hour
    parcelles    = Parcelle.query.all()
    created      = 0

    for p in parcelles:
        # Évite le doublon pour la même parcelle, le même jour et la même heure
        if Observation.query.filter_by(parcelle_id=p.id, date=today, heure=heure_actuelle).first():
            continue

        meteo = Meteo.query.filter_by(date=today, zone=p.localisation).first()
        if not meteo:
            continue

        etat, commentaire = _apply_rules(meteo)

        obs = Observation(
            date=today,
            heure=heure_actuelle,
            etat=etat,
            parcelle_id=p.id,
            commentaire=commentaire,
        )
        db.session.add(obs)
        created += 1

    db.session.commit()

    # Génère les alertes à partir de la dernière observation par parcelle
    from app.services.alerte_service import generate_alerts_from_observations
    generate_alerts_from_observations()

    return created


def _apply_rules(meteo):
    """
    Règles métier pour déterminer l'état d'une culture.

    Priorité décroissante :
      1. Humidité > 90 %                       → Maladie détectée
      2. Humidité > 80 % ET T ≥ 5 °C          → Risque maladie
      3. Pluie < 2 mm ET température > 25 °C  → Stress hydrique
      4. Sinon                                 → OK
    """
    t = meteo.temperature or 0
    h = meteo.humidite    or 0
    p = meteo.pluie_mm    or 0

    if h > 90:
        return 'Maladie détectée', f'Humidité critique {h}% — intervention recommandée'

    if h > 80 and t >= 5:
        return 'Risque maladie', f'Humidité {h}% et température {t}°C — conditions favorables aux maladies'

    if p < 2 and t > 25:
        return 'Stress hydrique', f'Température {t}°C et précipitations insuffisantes ({p} mm)'

    return 'OK', f'Conditions normales — {t}°C, humidité {h}%, pluie {p} mm'
