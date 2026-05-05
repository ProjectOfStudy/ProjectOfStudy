from app.models import db

class Meteo(db.Model):
    __tablename__ = 'meteo'

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date        = db.Column(db.Date, nullable=False, unique=True)
    temperature = db.Column(db.Float)
    humidite    = db.Column(db.Float)
    pluie_mm    = db.Column(db.Float)

    def __repr__(self):
        return f'<Meteo {self.date} - {self.temperature}°C>'
