from app.models import db

class Culture(db.Model):
    __tablename__ = 'cultures'

    id          = db.Column(db.Integer, primary_key=True)
    type        = db.Column(db.String(100), nullable=False)
    date_semis  = db.Column(db.Date)
    parcelle_id = db.Column(db.Integer, db.ForeignKey('parcelles.id'), nullable=False)

    def __repr__(self):
        return f'<Culture {self.type}>'
