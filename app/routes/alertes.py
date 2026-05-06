"""
Routes pour gérer les alertes.
"""

from flask import Blueprint, render_template, redirect, url_for, flash
from app.services.alerte_service import enregistrer_alertes, get_alertes_actives

alertes_bp = Blueprint('alertes', __name__, url_prefix='/alertes')


@alertes_bp.route('/')
def liste():
    """Affiche la liste des alertes actives."""
    alertes = get_alertes_actives(jours=7)
    return render_template('alertes/list.html', alertes=alertes)


@alertes_bp.route('/analyser', methods=['GET', 'POST'])
def analyser():
    """Déclenche manuellement l'analyse des risques."""
    nb = enregistrer_alertes()
    flash(f"{nb} nouvelle(s) alerte(s) détectée(s)", 'success')
    return redirect(url_for('alertes.liste'))