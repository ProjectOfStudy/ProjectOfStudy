from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import text
from app.models import db
from app.models.proprietaire import Proprietaire

login_bp = Blueprint('login', __name__)


@login_bp.route('/fix-sequences')
def fix_sequences():
    """Route temporaire — à supprimer après utilisation."""
    tables = ['zones', 'proprietaires', 'parcelles', 'cultures',
              'alertes', 'observations', 'meteo']
    results = []
    with db.engine.begin() as conn:
        for t in tables:
            val = conn.execute(text(
                f"SELECT setval(pg_get_serial_sequence('{t}', 'id'), "
                f"GREATEST((SELECT COALESCE(MAX(id), 1) FROM {t}), 1))"
            )).scalar()
            results.append(f"{t} → next id = {val + 1}")
    return '<br>'.join(results)


@login_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))

    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))

        user = Proprietaire.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard.dashboard'))

        flash('Email ou mot de passe incorrect.', 'error')

    return render_template('login.html')


@login_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
