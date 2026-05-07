"""
Service de gestion des alertes.
Enregistre les alertes détectées en base de données.
"""
from datetime import date, timedelta

from app.models import db
from app.models.alerte import Alerte
from app.models.observation import Observation
from app.models.parcelle import Parcelle

ETAT_VERS_ALERTE = {
    'Maladie détectée': ('Maladie détectée', 3),
    'Risque maladie':   ('Risque maladie',   2),
    'Stress hydrique':  ('Stress hydrique',  1),
}


def enregistrer_alertes(date_reference=None):
    """
    Lance l'analyse (règles météo) et enregistre les nouvelles alertes en BDD.
    Évite les doublons (même parcelle + même type + même date).
    Retourne le nombre d'alertes nouvellement créées.
    """
    from app.services.analyse_service import analyser_toutes_parcelles

    if date_reference is None:
        date_reference = date.today()

    alertes_detectees = analyser_toutes_parcelles(date_reference)
    nb_creees = 0

    for a in alertes_detectees:
        existe = Alerte.query.filter_by(
            parcelle_id=a['parcelle'].id,
            type=a['type'],
            date=date_reference
        ).first()
        if not existe:
            db.session.add(Alerte(
                date=date_reference,
                type=a['type'],
                parcelle_id=a['parcelle'].id,
                niveau=a['niveau']
            ))
            nb_creees += 1

    db.session.commit()
    return nb_creees


def get_alertes_actives(jours=7):
    """
    Récupère les alertes des X derniers jours pour le dashboard.
    """
    date_limite = date.today() - timedelta(days=jours)
    return Alerte.query.filter(
        Alerte.date >= date_limite
    ).order_by(Alerte.date.desc(), Alerte.niveau.desc()).all()


def generate_alerts_from_observations():
    """
    Pour chaque parcelle, récupère uniquement la dernière observation du jour
    et génère une alerte si l'état le justifie.
    Évite les doublons (une alerte par parcelle/jour/type/niveau).
    Retourne le nombre d'alertes créées.
    """
    today   = date.today()
    created = 0

    for p in Parcelle.query.all():
        derniere_obs = (Observation.query
                        .filter_by(parcelle_id=p.id, date=today)
                        .order_by(Observation.id.desc())
                        .first())

        if not derniere_obs or derniere_obs.etat not in ETAT_VERS_ALERTE:
            continue

        type_alerte, niveau = ETAT_VERS_ALERTE[derniere_obs.etat]

        if Alerte.query.filter_by(
            parcelle_id=p.id,
            date=today,
            type=type_alerte,
            niveau=niveau,
        ).first():
            continue

        db.session.add(Alerte(
            date=today,
            type=type_alerte,
            parcelle_id=p.id,
            niveau=niveau,
        ))
        created += 1

    db.session.commit()
    return created
