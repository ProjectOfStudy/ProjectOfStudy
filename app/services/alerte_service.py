from datetime import date

from app.models import db
from app.models.alerte import Alerte
from app.models.observation import Observation
from app.models.parcelle import Parcelle

ETAT_VERS_ALERTE = {
    'Maladie détectée': ('Maladie détectée', 3),
    'Risque maladie':   ('Risque maladie',   2),
    'Stress hydrique':  ('Stress hydrique',  1),
}


def generate_alerts_from_observations():
    """
    Pour chaque parcelle, récupère uniquement la dernière observation du jour
    et génère une alerte si l'état le justifie.
    Evite les doublons (une alerte par parcelle/jour/type/niveau).
    Retourne le nombre d'alertes créées.
    """
    today   = date.today()
    created = 0

    for p in Parcelle.query.all():
        # Dernière observation de la journée pour cette parcelle
        derniere_obs = (Observation.query
                        .filter_by(parcelle_id=p.id, date=today)
                        .order_by(Observation.heure.desc())
                        .first())

        if not derniere_obs or derniere_obs.etat not in ETAT_VERS_ALERTE:
            continue

        type_alerte, niveau = ETAT_VERS_ALERTE[derniere_obs.etat]

        # Évite le doublon pour la même alerte aujourd'hui
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
