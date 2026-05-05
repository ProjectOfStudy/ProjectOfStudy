from app.models import db

class Alerte(db.Model):
    __tablename__ = 'alertes'

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date        = db.Column(db.Date, nullable=False)
    type        = db.Column(db.String(100), nullable=False)
    parcelle_id = db.Column(db.Integer, db.ForeignKey('parcelles.id'), nullable=False)
    niveau      = db.Column(db.Integer)

    def __repr__(self):
        return f'<Alerte {self.type} - niveau {self.niveau}>'
