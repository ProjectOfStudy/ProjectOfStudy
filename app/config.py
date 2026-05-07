import os

class Config:
    # 1. On récupère l'URL de la base de données (PostgreSQL sur Render)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # 2. Correction cruciale pour SQLAlchemy (Render utilise postgres:// au lieu de postgresql://)
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    
    # 3. Si on est en local (sur ton PC), DATABASE_URL est vide, on utilise donc SQLite
    if not SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///agrovision.db'

    # Désactive le suivi des modifications pour économiser des ressources
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Clé secrète pour gérer les sessions (connexion utilisateur)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'agro-secret-2026')

    # Configuration des zones météo (GPS)
    METEO_ZONES = {
        'Zone A': {'lat': 48.45, 'lon': 1.49, 'ville': 'Chartres'},
        'Zone B': {'lat': 47.39, 'lon': 0.69, 'ville': 'Tours'},
        'Zone C': {'lat': 44.84, 'lon': -0.58, 'ville': 'Bordeaux'},
        'Zone D': {'lat': 47.32, 'lon': 5.04, 'ville': 'Dijon'},
        'Zone E': {'lat': 43.60, 'lon': 1.44, 'ville': 'Toulouse'},
    }