from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db
from app.models.parcelle import Parcelle
from app.models.culture import Culture
from app.models.alerte import Alerte
from app.models.observation import Observation
from app.models.proprietaire import Proprietaire

parcelles_bp = Blueprint('parcelles', __name__, url_prefix='/parcelles')


@parcelles_bp.route('/')
def list():
    parcelles = Parcelle.query.order_by(Parcelle.id).all()
    for p in parcelles:
        p.last_alerte = Alerte.query.filter_by(parcelle_id=p.id).order_by(Alerte.date.desc()).first()
    return render_template('parcelles/list.html', parcelles=parcelles)


@parcelles_bp.route('/<int:id>')
def detail(id):
    parcelle     = Parcelle.query.get_or_404(id)
    alertes      = Alerte.query.filter_by(parcelle_id=id).order_by(Alerte.date.desc()).limit(5).all()
    observations = Observation.query.filter_by(parcelle_id=id).order_by(Observation.date.desc()).limit(5).all()
    return render_template('parcelles/detail.html',
                           parcelle=parcelle,
                           alertes=alertes,
                           observations=observations)


@parcelles_bp.route('/nouvelle', methods=['GET', 'POST'])
def new():
    proprietaires = Proprietaire.query.order_by(Proprietaire.nom).all()
    if request.method == 'POST':
        p = Parcelle(
            nom=request.form['nom'],
            localisation=request.form['localisation'],
            surface_ha=float(request.form['surface_ha']),
            proprietaire_id=int(request.form['proprietaire_id']) if request.form.get('proprietaire_id') else None
        )
        db.session.add(p)
        db.session.commit()
        flash('Parcelle créée avec succès.')
        return redirect(url_for('parcelles.detail', id=p.id))
    return render_template('parcelles/form.html', parcelle=None, proprietaires=proprietaires)


@parcelles_bp.route('/<int:id>/modifier', methods=['GET', 'POST'])
def edit(id):
    parcelle      = Parcelle.query.get_or_404(id)
    proprietaires = Proprietaire.query.order_by(Proprietaire.nom).all()
    if request.method == 'POST':
        parcelle.nom             = request.form['nom']
        parcelle.localisation    = request.form['localisation']
        parcelle.surface_ha      = float(request.form['surface_ha'])
        parcelle.proprietaire_id = int(request.form['proprietaire_id']) if request.form.get('proprietaire_id') else None
        db.session.commit()
        flash('Parcelle modifiée avec succès.')
        return redirect(url_for('parcelles.detail', id=id))
    return render_template('parcelles/form.html', parcelle=parcelle, proprietaires=proprietaires)


@parcelles_bp.route('/<int:id>/supprimer', methods=['POST'])
def delete(id):
    parcelle = Parcelle.query.get_or_404(id)
    db.session.delete(parcelle)
    db.session.commit()
    flash('Parcelle supprimée.')
    return redirect(url_for('parcelles.list'))


@parcelles_bp.route('/<int:id>/culture', methods=['POST'])
def add_culture(id):
    Parcelle.query.get_or_404(id)
    c = Culture(
        type=request.form['type'],
        date_semis=datetime.strptime(request.form['date_semis'], '%Y-%m-%d').date(),
        parcelle_id=id
    )
    db.session.add(c)
    db.session.commit()
    flash('Culture ajoutée.')
    return redirect(url_for('parcelles.detail', id=id))
