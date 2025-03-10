import os
from datetime import timedelta

class Config:
    """
    Configuración base para la aplicación
    """
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-secreta-dificil-de-adivinar')
    
    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # Configuración de correo
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@molinosonora.com.co')
    
    # Configuración de ReCaptcha
    RECAPTCHA_SITE_KEY = os.environ.get('RECAPTCHA_SITE_KEY')
    RECAPTCHA_SECRET_KEY = os.environ.get('RECAPTCHA_SECRET_KEY')
    RECAPTCHA_ENABLED = os.environ.get('RECAPTCHA_ENABLED', 'false').lower() in ['true', 'on', '1']
    
    # Configuración de archivos
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx', 'xls', 'xlsx'}
    
    # Configuración de sesión
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    
    # Nombre de la aplicación
    APP_NAME = "Agroindustrial Molino Sonora AP S.A.S."
    
    # Configuración de paginación
    ITEMS_PER_PAGE = 10
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    """
    Configuración para desarrollo
    """
    DEBUG = True
    
    # Deshabilitar ReCaptcha en desarrollo
    RECAPTCHA_ENABLED = False

class TestingConfig(Config):
    """
    Configuración para pruebas
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/molino_sonora_dms_test'
    WTF_CSRF_ENABLED = False
    
    # Deshabilitar ReCaptcha en pruebas
    RECAPTCHA_ENABLED = False

class ProductionConfig(Config):
    """
    Configuración para producción
    """
    # SSL/TLS para producción
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Configuración de logging para producción
        import logging
        from logging.handlers import RotatingFileHandler
        
        file_handler = RotatingFileHandler('logs/molino_sonora_dms.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Molino Sonora DMS startup')