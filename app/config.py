import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'dev-secret-key-a-changer-en-prod'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(BASE_DIR), 'agrovision.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False