from flask_wtf.csrf import CSRFProtect
import os


class Configuration():
    DEBUG = True

    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

    CSRF_ENABLED = True
    SECRET_KEY = 'Noonan'
    OPENID_PROVIDERS = [
        {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]

    ###Flask-security
    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'

    SECURITY_REGISTERABLE = True
    #SECURITY_REGISTER_URL = '/create_account'
    SECURITY_SEND_LOGIN_TEMPLATE = '/login'
    SECURITY_SEND_CONFIRMATION_TEMPLATE = '/login'

