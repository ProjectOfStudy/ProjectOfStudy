from app.models import db

class Parcelle(db.Model):
    __tablename__ = 'parcelles'

    id           = db.Column(db.Integer, primary_key=True)
    nom          = db.Column(db.String(100), nullable=False)
    localisation = db.Column(db.String(100))
    surface_ha   = db.Column(db.Float)

    cultures     = db.relationship('Culture',     backref='parcelle', lazy=True)
    alertes      = db.relationship('Alerte',      backref='parcelle', lazy=True)
    observations = db.relationship('Observation', backref='parcelle', lazy=True)

    def __repr__(self):
        return f'<Parcelle {self.nom}>'
