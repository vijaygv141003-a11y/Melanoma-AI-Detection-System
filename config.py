import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

def resolve_database_uri():
    default_uri = 'sqlite:///instance/melanoma_detection.db'
    database_url = os.environ.get('DATABASE_URL', default_uri)
    if database_url.startswith('sqlite:///'):
        sqlite_path = database_url[len('sqlite:///'):]
        if not os.path.isabs(sqlite_path):
            sqlite_path = os.path.abspath(os.path.join(basedir, sqlite_path))
            sqlite_path = sqlite_path.replace('\\', '/')
            database_url = f"sqlite:///{sqlite_path}"
    return database_url

class Config:
    """Base configuration"""
    FLASK_APP = os.environ.get('FLASK_APP', 'app.py')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-this')
    
    # Database
    SQLALCHEMY_DATABASE_URI = resolve_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
    
    # Email
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@melanoma-detection.com')
    MAIL_USE_TLS = True
    
    # Model
    MODEL_PATH = os.environ.get('MODEL_PATH', 'model/melanoma_model.h5')
    LABELS_PATH = os.environ.get('LABELS_PATH', 'model/labels.txt')
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Security
    BCRYPT_LOG_ROUNDS = int(os.environ.get('BCRYPT_LOG_ROUNDS', 12))
    
    # Pagination
    ITEMS_PER_PAGE = 10
    
    # AWS S3 (Optional)
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_melanoma.db'
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
