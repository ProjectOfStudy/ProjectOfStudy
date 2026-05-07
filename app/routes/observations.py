"""
Routes pour la gestion des observations terrain.
Permet la saisie et la consultation de l'historique des observations.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import date
from app.models import db
from app.models.observation import Observation
from app.models.parcelle import Parcelle

observations_bp = Blueprint('observations', __name__, url_prefix='/observations')


# Liste des états possibles (pour le dropdown du formulaire)
ETATS_POSSIBLES = [
    'Bon état',
    'Croissance normale',
    'Stress hydrique',
    'Maladie détectée',
    'Présence de ravageurs',
    'Carence nutritionnelle',
    'Mauvaises herbes',
    'Récolte imminente',
]


@observations_bp.route('/')
def liste():
    """Affiche l'historique de toutes les observations, les plus récentes en premier."""
    observations = Observation.query.order_by(Observation.date.desc()).all()
    return render_template('observations/list.html', observations=observations)


@observations_bp.route('/ajouter', methods=['GET', 'POST'])
def ajouter():
    """Formulaire de saisie d'une nouvelle observation."""
    parcelles = Parcelle.query.all()

    if request.method == 'POST':
        try:
            date_str = request.form.get('date')
            parcelle_id = request.form.get('parcelle_id')
            etat = request.form.get('etat')
            commentaire = request.form.get('commentaire', '')

            # Validation basique
            if not date_str or not parcelle_id or not etat:
                flash("Tous les champs obligatoires doivent être remplis.", 'error')
                return render_template(
                    'observations/form.html',
                    parcelles=parcelles,
                    etats=ETATS_POSSIBLES
                )

            # Création de l'observation
            from datetime import datetime
            nouvelle_obs = Observation(
                date=datetime.strptime(date_str, '%Y-%m-%d').date(),
                parcelle_id=int(parcelle_id),
                etat=etat,
                commentaire=commentaire
            )
            db.session.add(nouvelle_obs)
            db.session.commit()

            flash("Observation enregistrée avec succès !", 'success')
            return redirect(url_for('observations.liste'))

        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de l'enregistrement : {str(e)}", 'error')

    return render_template(
        'observations/form.html',
        parcelles=parcelles,
        etats=ETATS_POSSIBLES,
        date_aujourdhui=date.today().isoformat()
    )


@observations_bp.route('/supprimer/<int:obs_id>', methods=['POST', 'GET'])
def supprimer(obs_id):
    """Supprime une observation."""
    observation = Observation.query.get_or_404(obs_id)
    db.session.delete(observation)
    db.session.commit()
    flash("Observation supprimée.", 'success')
    return redirect(url_for('observations.liste'))