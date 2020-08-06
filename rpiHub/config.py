class Config:
    """ Set Flask configuration variables """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ADMIN_SWATCH = 'cerulean'
    SECRET_KEY='GDtfDCFYjD'
