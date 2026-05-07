import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY               = os.environ.get('SECRET_KEY', 'dev-secret-agrovision-2025')
    SQLALCHEMY_DATABASE_URI  = 'sqlite:///' + os.path.join(BASE_DIR, '..', 'agrovision.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Coordonnées GPS par zone agricole
    METEO_ZONES = {
        'Zone A': {'lat': 48.45, 'lon':  1.49, 'ville': 'Chartres'},
        'Zone B': {'lat': 47.39, 'lon':  0.69, 'ville': 'Tours'},
        'Zone C': {'lat': 44.84, 'lon': -0.58, 'ville': 'Bordeaux'},
        'Zone D': {'lat': 47.32, 'lon':  5.04, 'ville': 'Dijon'},
        'Zone E': {'lat': 43.60, 'lon':  1.44, 'ville': 'Toulouse'},
    }
