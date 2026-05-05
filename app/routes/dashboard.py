from flask import Blueprint, render_template
from app.models.parcelle import Parcelle
from app.models.alerte import Alerte
from app.models.observation import Observation
from app.models.meteo import Meteo

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    stats = {
        'nb_parcelles':    Parcelle.query.count(),
        'nb_alertes':      Alerte.query.count(),
        'nb_critiques':    Alerte.query.filter_by(niveau=3).count(),
        'nb_observations': Observation.query.count(),
    }

    derniere_meteo = Meteo.query.order_by(Meteo.date.desc()).first()
    alertes        = Alerte.query.order_by(Alerte.date.desc()).limit(10).all()
    observations   = Observation.query.order_by(Observation.date.desc()).limit(8).all()

    parcelles = Parcelle.query.all()
    for p in parcelles:
        p.last_alerte      = Alerte.query.filter_by(parcelle_id=p.id).order_by(Alerte.date.desc()).first()
        p.last_observation = Observation.query.filter_by(parcelle_id=p.id).order_by(Observation.date.desc()).first()

    return render_template('dashboard.html',
        stats=stats,
        derniere_meteo=derniere_meteo,
        alertes=alertes,
        observations=observations,
        parcelles=parcelles,
    )
