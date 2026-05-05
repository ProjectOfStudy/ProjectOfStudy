"""
Routes pour la gestion des parcelles.
TODO: à compléter (CRUD parcelles).
"""

from flask import Blueprint, render_template
from app.models.parcelle import Parcelle

parcelles_bp = Blueprint('parcelles', __name__, url_prefix='/parcelles')


@parcelles_bp.route('/')
def liste():
    """Affiche la liste des parcelles."""
    parcelles = Parcelle.query.all()
    return render_template('parcelles/list.html', parcelles=parcelles)