from app.models import db

class Meteo(db.Model):
    __tablename__ = 'meteo'

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date        = db.Column(db.Date, nullable=False)
    zone        = db.Column(db.String(10), nullable=False, default='Zone A')
    temperature = db.Column(db.Float)
    humidite    = db.Column(db.Float)
    pluie_mm    = db.Column(db.Float)

    __table_args__ = (
        db.UniqueConstraint('date', 'zone', name='uq_meteo_date_zone'),
    )

    def __repr__(self):
        return f'<Meteo {self.date} {self.zone} - {self.temperature}°C>'
