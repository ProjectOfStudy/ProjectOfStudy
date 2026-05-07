"""
Script d'initialisation de la base de données.
Lance avec : python init_db.py
"""
import csv
import os
from datetime import datetime

from app import create_app
from app.models import db
from app.models.proprietaire import Proprietaire
from app.models.parcelle import Parcelle
from app.models.culture import Culture
from app.models.alerte import Alerte
from app.models.observation import Observation
from app.models.meteo import Meteo
from app.models.zone import Zone

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

def parse_date(s):
    return datetime.strptime(s, '%Y-%m-%d').date()

def load_csv(filename):
    path = os.path.join(DATA_DIR, filename)
    with open(path, encoding='utf-8') as f:
        return list(csv.DictReader(f))

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    print("Tables créées.")

    # Zones (avant la météo car utilisées comme référence)
    zones_data = {
        'Zone A': {'ville': 'Chartres',  'lat':  48.45, 'lon':  1.49},
        'Zone B': {'ville': 'Tours',     'lat':  47.39, 'lon':  0.69},
        'Zone C': {'ville': 'Bordeaux',  'lat':  44.84, 'lon': -0.58},
        'Zone D': {'ville': 'Dijon',     'lat':  47.32, 'lon':  5.04},
        'Zone E': {'ville': 'Toulouse',  'lat':  43.60, 'lon':  1.44},
    }
    for nom, coords in zones_data.items():
        db.session.add(Zone(
            nom=nom,
            ville=coords['ville'],
            latitude=coords['lat'],
            longitude=coords['lon']
        ))
    db.session.commit()
    print(f"  OK {Zone.query.count()} zones importees")

    # Proprietaires (avant les parcelles car FK)
    print("\n  Comptes de connexion :")
    for row in load_csv('proprietaires.csv'):
        p = Proprietaire(
            id=int(row['id']),
            nom=row['nom'],
            prenom=row['prenom'],
            email=row['email']
        )
        p.set_password(row['password'])
        db.session.add(p)
        print(f"    {row['email']:<40} -> {row['password']}")
    db.session.commit()
    print(f"  OK {Proprietaire.query.count()} proprietaires importes")

    # Parcelles
    for row in load_csv('parcelles.csv'):
        db.session.add(Parcelle(
            id=int(row['id']),
            nom=row['nom'],
            localisation=row['localisation'],
            surface_ha=float(row['surface_ha']),
            proprietaire_id=int(row['proprietaire_id'])
        ))
    db.session.commit()
    print(f"  OK {Parcelle.query.count()} parcelles importees")

    # Cultures
    for row in load_csv('cultures.csv'):
        db.session.add(Culture(
            id=int(row['id']),
            type=row['type'],
            date_semis=parse_date(row['date_semis']),
            parcelle_id=int(row['parcelle_id'])
        ))
    db.session.commit()
    print(f"  OK {Culture.query.count()} cultures importees")

    # Alertes
    for row in load_csv('alertes.csv'):
        db.session.add(Alerte(
            date=parse_date(row['date']),
            type=row['type'],
            parcelle_id=int(row['parcelle_id']),
            niveau=int(row['niveau'])
        ))
    db.session.commit()
    print(f"  OK {Alerte.query.count()} alertes importees")

    # Observations
    for row in load_csv('observations.csv'):
        db.session.add(Observation(
            date=parse_date(row['date']),
            etat=row['etat'],
            parcelle_id=int(row['parcelle_id']),
            commentaire=row['commentaire']
        ))
    db.session.commit()
    print(f"  OK {Observation.query.count()} observations importees")

    # Meteo (données CSV historiques assignées à Zone A par défaut)
    for row in load_csv('meteo.csv'):
        db.session.add(Meteo(
            date=parse_date(row['date']),
            zone='Zone A',
            temperature=float(row['temperature']),
            humidite=float(row['humidite']),
            pluie_mm=float(row['pluie_mm'])
        ))
    db.session.commit()
    print(f"  OK {Meteo.query.count()} entrees meteo importees (Zone A)")

    print("\nBase de donnees prete : agrovision.db")
