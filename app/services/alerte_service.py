"""
Service de gestion des alertes.
Enregistre les alertes détectées en base de données.
"""

from datetime import date
from app.models import db
from app.models.alerte import Alerte
from app.services.analyse_service import analyser_toutes_parcelles


def enregistrer_alertes(date_reference=None):
    """
    Lance l'analyse et enregistre les nouvelles alertes en BDD.
    Évite les doublons (même parcelle + même type + même date).
    Retourne le nombre d'alertes nouvellement créées.
    """
    if date_reference is None:
        date_reference = date.today()

    alertes_detectees = analyser_toutes_parcelles(date_reference)
    nb_creees = 0

    for a in alertes_detectees:
        # Vérifier si l'alerte existe déjà pour cette parcelle ce jour-là
        existe = Alerte.query.filter_by(
            parcelle_id=a['parcelle'].id,
            type=a['type'],
            date=date_reference
        ).first()

        if not existe:
            nouvelle_alerte = Alerte(
                date=date_reference,
                type=a['type'],
                parcelle_id=a['parcelle'].id,
                niveau=a['niveau']
            )
            db.session.add(nouvelle_alerte)
            nb_creees += 1

    db.session.commit()
    return nb_creees


def get_alertes_actives(jours=7):
    """
    Récupère les alertes des X derniers jours pour le dashboard.
    """
    from datetime import timedelta
    date_limite = date.today() - timedelta(days=jours)

    return Alerte.query.filter(
        Alerte.date >= date_limite
    ).order_by(Alerte.date.desc(), Alerte.niveau.desc()).all()