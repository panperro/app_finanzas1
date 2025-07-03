import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'clave-secreta-super-segura'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'datos.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False