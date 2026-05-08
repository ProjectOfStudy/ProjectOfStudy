from app.models import db

class Observation(db.Model):
    __tablename__ = 'observations'

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date        = db.Column(db.Date, nullable=False)
    heure       = db.Column(db.Integer, nullable=True)   # 0-23, None pour les données historiques
    etat        = db.Column(db.String(100))
    parcelle_id = db.Column(db.Integer, db.ForeignKey('parcelles.id'), nullable=False)
    commentaire = db.Column(db.String(200))

    def __repr__(self):
        return f'<Observation {self.etat} - {self.date} {self.heure}h>'
