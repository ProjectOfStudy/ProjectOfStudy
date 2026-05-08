from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import de tous les modèles pour que SQLAlchemy les connaisse
from app.models.parcelle import Parcelle
from app.models.culture import Culture
from app.models.observation import Observation
from app.models.meteo import Meteo
from app.models.alerte import Alerte