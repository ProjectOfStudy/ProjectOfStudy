from flask import Blueprint, render_template, request
from app.models.parcelle import Parcelle
from app.models.alerte import Alerte
from app.models.observation import Observation
from app.models.meteo import Meteo
<<<<<<< Updated upstream
from app.models.zone import Zone
=======
from datetime import datetime, date
>>>>>>> Stashed changes

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
def dashboard():
<<<<<<< Updated upstream
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

=======

    # ── Lecture des filtres depuis l'URL ──────────────────────────────────────
    date_debut_str  = request.args.get('date_debut', '')
    date_fin_str    = request.args.get('date_fin', '')
    filtre_niveau   = request.args.get('niveau', '')       # '1', '2', '3' ou ''
    filtre_parcelle = request.args.get('parcelle_id', '')  # id ou ''

    date_debut = datetime.strptime(date_debut_str, '%Y-%m-%d').date() if date_debut_str else None
    date_fin   = datetime.strptime(date_fin_str,   '%Y-%m-%d').date() if date_fin_str   else None

    # ── Requêtes alertes filtrées ─────────────────────────────────────────────
    q_alertes = Alerte.query
    if date_debut:
        q_alertes = q_alertes.filter(Alerte.date >= date_debut)
    if date_fin:
        q_alertes = q_alertes.filter(Alerte.date <= date_fin)
    if filtre_niveau:
        q_alertes = q_alertes.filter(Alerte.niveau == int(filtre_niveau))
    if filtre_parcelle:
        q_alertes = q_alertes.filter(Alerte.parcelle_id == int(filtre_parcelle))

    # ── Requêtes observations filtrées ────────────────────────────────────────
    q_obs = Observation.query
    if date_debut:
        q_obs = q_obs.filter(Observation.date >= date_debut)
    if date_fin:
        q_obs = q_obs.filter(Observation.date <= date_fin)
    if filtre_parcelle:
        q_obs = q_obs.filter(Observation.parcelle_id == int(filtre_parcelle))

    # ── Données finales ───────────────────────────────────────────────────────
    stats = {
        'nb_parcelles':    Parcelle.query.count(),
        'nb_alertes':      q_alertes.count(),
        'nb_critiques':    q_alertes.filter(Alerte.niveau == 3).count() if not filtre_niveau else (q_alertes.count() if filtre_niveau == '3' else 0),
        'nb_observations': q_obs.count(),
    }

    derniere_meteo = Meteo.query.order_by(Meteo.date.desc()).first()
    alertes        = q_alertes.order_by(Alerte.date.desc()).limit(10).all()
    observations   = q_obs.order_by(Observation.date.desc()).limit(8).all()

    parcelles     = Parcelle.query.all()
>>>>>>> Stashed changes
    for p in parcelles:
        p.last_alerte      = Alerte.query.filter_by(parcelle_id=p.id).order_by(Alerte.date.desc()).first()
        p.last_observation = Observation.query.filter_by(parcelle_id=p.id).order_by(Observation.date.desc()).first()

    # Liste des parcelles pour le filtre déroulant
    toutes_parcelles = Parcelle.query.order_by(Parcelle.id).all()

    # Filtres actifs (pour les passer au template)
    filtres = {
        'date_debut':  date_debut_str,
        'date_fin':    date_fin_str,
        'niveau':      filtre_niveau,
        'parcelle_id': filtre_parcelle,
    }
    filtres_actifs = any(filtres.values())

    return render_template('dashboard.html',
        stats=stats,
        derniere_meteo=derniere_meteo,
        alertes=alertes,
        observations=observations,
        parcelles=parcelles,
<<<<<<< Updated upstream
        zones=zones,
        zone_selectionnee=zone_selectionnee,
    )
=======
        toutes_parcelles=toutes_parcelles,
        filtres=filtres,
        filtres_actifs=filtres_actifs,
    )
>>>>>>> Stashed changes
