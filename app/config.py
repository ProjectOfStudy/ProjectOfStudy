import os

class Config:
    # 1. On récupère l'URL de Render
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # 2. Correction du nom pour SQLAlchemy
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    
    # 3. SÉCURITÉ : Si SQLALCHEMY_DATABASE_URI est vide (sur ton PC), on met SQLite
    if not SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///agrovision.db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-agrovision-2025')
    # Coordonnées GPS par zone agricole
    METEO_ZONES = {
        'Zone A': {'lat': 48.45, 'lon':  1.49, 'ville': 'Chartres'},
        'Zone B': {'lat': 47.39, 'lon':  0.69, 'ville': 'Tours'},
        'Zone C': {'lat': 44.84, 'lon': -0.58, 'ville': 'Bordeaux'},
        'Zone D': {'lat': 47.32, 'lon':  5.04, 'ville': 'Dijon'},
        'Zone E': {'lat': 43.60, 'lon':  1.44, 'ville': 'Toulouse'},
    }
