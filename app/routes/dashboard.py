from flask import Blueprint, render_template, request
from app.models.parcelle import Parcelle
from app.models.alerte import Alerte
from app.models.observation import Observation
from app.models.meteo import Meteo
from app.models.zone import Zone

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
def dashboard():
    zone_selectionnee = request.args.get('zone', '')

    zones = Zone.query.order_by(Zone.nom).all()

    # Filtrer les parcelles selon la zone sélectionnée
    if zone_selectionnee:
        parcelles = Parcelle.query.filter_by(localisation=zone_selectionnee).all()
    else:
        parcelles = Parcelle.query.all()

    parcelle_ids = [p.id for p in parcelles]

    stats = {
        'nb_parcelles':    len(parcelles),
        'nb_alertes':      Alerte.query.filter(Alerte.parcelle_id.in_(parcelle_ids)).count(),
        'nb_critiques':    Alerte.query.filter(Alerte.parcelle_id.in_(parcelle_ids), Alerte.niveau == 3).count(),
        'nb_observations': Observation.query.filter(Observation.parcelle_id.in_(parcelle_ids)).count(),
    }

    if zone_selectionnee:
        derniere_meteo = Meteo.query.filter_by(zone=zone_selectionnee).order_by(Meteo.date.desc()).first()
    else:
        derniere_meteo = Meteo.query.order_by(Meteo.date.desc()).first()

    alertes = (Alerte.query
               .filter(Alerte.parcelle_id.in_(parcelle_ids))
               .order_by(Alerte.date.desc()).limit(10).all())

    observations = (Observation.query
                    .filter(Observation.parcelle_id.in_(parcelle_ids))
                    .order_by(Observation.date.desc()).limit(8).all())

    for p in parcelles:
        p.last_alerte      = Alerte.query.filter_by(parcelle_id=p.id).order_by(Alerte.date.desc()).first()
        p.last_observation = Observation.query.filter_by(parcelle_id=p.id).order_by(Observation.date.desc()).first()

    return render_template('dashboard.html',
        stats=stats,
        derniere_meteo=derniere_meteo,
        alertes=alertes,
        observations=observations,
        parcelles=parcelles,
        zones=zones,
        zone_selectionnee=zone_selectionnee,
    )
