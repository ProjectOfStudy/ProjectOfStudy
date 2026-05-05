from app.models import db

class Observation(db.Model):
    __tablename__ = 'observations'

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date        = db.Column(db.Date, nullable=False)
    etat        = db.Column(db.String(100))
    parcelle_id = db.Column(db.Integer, db.ForeignKey('parcelles.id'), nullable=False)
    commentaire = db.Column(db.String(200))

    def __repr__(self):
        return f'<Observation {self.etat} - {self.date}>'
