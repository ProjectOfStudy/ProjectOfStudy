from app.models import db

class Proprietaire(db.Model):
    __tablename__ = 'proprietaires'

    id       = db.Column(db.Integer, primary_key=True)
    nom      = db.Column(db.String(100), nullable=False)
    prenom   = db.Column(db.String(100), nullable=False)
    email    = db.Column(db.String(150), unique=True, nullable=False)

    parcelles = db.relationship('Parcelle', backref='proprietaire', lazy=True)

    def __repr__(self):
        return f'<Proprietaire {self.prenom} {self.nom}>'
