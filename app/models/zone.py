from app.models import db

class Zone(db.Model):
    __tablename__ = 'zones'

    id        = db.Column(db.Integer, primary_key=True)
    nom       = db.Column(db.String(10), unique=True, nullable=False)
    ville     = db.Column(db.String(100), nullable=False)
    latitude  = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Zone {self.nom} — {self.ville}>'
