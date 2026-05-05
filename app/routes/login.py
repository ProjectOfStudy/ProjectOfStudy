from flask import Blueprint, render_template

login_bp = Blueprint('login', __name__)

@login_bp.route('/login')
def dashboard():
    return render_template('login.html')