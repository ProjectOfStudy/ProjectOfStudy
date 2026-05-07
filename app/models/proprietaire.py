from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db


class Proprietaire(db.Model, UserMixin):
    __tablename__ = 'proprietaires'

    id            = db.Column(db.Integer, primary_key=True)
    nom           = db.Column(db.String(100), nullable=False)
    prenom        = db.Column(db.String(100), nullable=False)
    email         = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False, default='')

    parcelles = db.relationship('Parcelle', backref='proprietaire', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Proprietaire {self.prenom} {self.nom}>'
