"""
Service d'analyse des données agricoles.
Applique les règles métier pour détecter les situations à risque.
"""
from datetime import date, datetime, timedelta

from app.models import db
from app.models.meteo import Meteo
from app.models.observation import Observation
from app.models.parcelle import Parcelle


# ── Seuils des règles météo (modifiables en un seul endroit) ──────────────────
SEUIL_HUMIDITE_MALADIE     = 85
SEUIL_TEMP_MALADIE_MIN     = 15
SEUIL_TEMP_MALADIE_MAX     = 25
SEUIL_TEMP_SECHERESSE      = 25
JOURS_SANS_PLUIE_SECHERESSE = 7
SEUIL_TEMP_GEL             = 2


# ── Règles météo (utilisées par enregistrer_alertes) ─────────────────────────

def detecter_risque_maladie(meteo_jour):
    """Risque maladie cryptogamique : humidité élevée + température douce."""
    if meteo_jour is None:
        return False
    return (
        meteo_jour.humidite > SEUIL_HUMIDITE_MALADIE
        and SEUIL_TEMP_MALADIE_MIN <= meteo_jour.temperature <= SEUIL_TEMP_MALADIE_MAX
    )


def detecter_risque_secheresse(date_reference=None):
    """Risque sécheresse : pas de pluie depuis 7 jours ET température élevée."""
    if date_reference is None:
        date_reference = date.today()

    date_debut = date_reference - timedelta(days=JOURS_SANS_PLUIE_SECHERESSE)
    meteos = Meteo.query.filter(
        Meteo.date >= date_debut,
        Meteo.date <= date_reference
    ).all()

    if not meteos:
        return False

    pluie_totale = sum((m.pluie_mm or 0) for m in meteos)
    temp_max     = max((m.temperature or 0) for m in meteos)
    return pluie_totale < 1 and temp_max > SEUIL_TEMP_SECHERESSE


def detecter_risque_gel(date_reference=None):
    """Risque gel : température < 2°C dans les 48h."""
    if date_reference is None:
        date_reference = date.today()

    date_fin = date_reference + timedelta(days=2)
    meteos_futures = Meteo.query.filter(
        Meteo.date >= date_reference,
        Meteo.date <= date_fin
    ).all()

    if not meteos_futures:
        return False

    return any((m.temperature or 99) < SEUIL_TEMP_GEL for m in meteos_futures)


def analyser_toutes_parcelles(date_reference=None):
    """
    Analyse toutes les parcelles et retourne la liste des alertes détectées.
    Retourne : [{parcelle, type, niveau}, ...]
    """
    if date_reference is None:
        date_reference = date.today()

    meteo_jour = Meteo.query.filter_by(date=date_reference).first()
    parcelles  = Parcelle.query.all()

    risque_maladie    = detecter_risque_maladie(meteo_jour)
    risque_secheresse = detecter_risque_secheresse(date_reference)
    risque_gel        = detecter_risque_gel(date_reference)

    alertes_detectees = []
    for parcelle in parcelles:
        if risque_maladie:
            alertes_detectees.append({'parcelle': parcelle, 'type': 'Risque maladie',    'niveau': 2})
        if risque_secheresse:
            alertes_detectees.append({'parcelle': parcelle, 'type': 'Risque sécheresse', 'niveau': 3})
        if risque_gel:
            alertes_detectees.append({'parcelle': parcelle, 'type': 'Risque gel',        'niveau': 3})

    return alertes_detectees


# ── Observations horaires (utilisées par le scheduler) ───────────────────────

def generate_daily_observations():
    """
    Génère une observation par heure pour chaque parcelle
    en utilisant la météo de sa zone.
    Retourne le nombre d'observations créées.
    """
    today          = date.today()
    heure_actuelle = datetime.now().hour
    created        = 0

    for p in Parcelle.query.all():
        if Observation.query.filter_by(parcelle_id=p.id, date=today, heure=heure_actuelle).first():
            continue

        meteo = Meteo.query.filter_by(date=today, zone=p.localisation).first()
        if not meteo:
            continue

        etat, commentaire = _apply_rules(meteo)

        db.session.add(Observation(
            date=today,
            heure=heure_actuelle,
            etat=etat,
            parcelle_id=p.id,
            commentaire=commentaire,
        ))
        created += 1

    db.session.commit()

    from app.services.alerte_service import generate_alerts_from_observations
    generate_alerts_from_observations()

    return created


def _apply_rules(meteo):
    """
    Règles métier pour les observations horaires.

    Priorité décroissante :
      1. Humidité > 90 %                      → Maladie détectée
      2. Humidité > 80 % ET T ≥ 5 °C         → Risque maladie
      3. Pluie < 2 mm ET température > 25 °C → Stress hydrique
      4. Sinon                                → OK
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
