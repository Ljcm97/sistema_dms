from flask import Flask, render_template
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask_moment import Moment
from datetime import datetime  # Importa datetime para obtener la fecha actual

# Inicialización de extensiones
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
mail = Mail()
moment = Moment()

def create_app(config_name=None):
    """
    Función de fábrica para crear la aplicación Flask
    """
    app = Flask(__name__)
    
    # Configuración
    config_class = os.environ.get('FLASK_CONFIG', 'development')
    app.config.from_object(f'app.config.{config_class.capitalize()}Config')
    
    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    
    # Configuración de login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicie sesión para acceder a esta página.'
    login_manager.login_message_category = 'warning'
    
    # Registrar blueprints
    from app.controllers.auth import auth_bp
    from app.controllers.admin import admin_bp
    from app.controllers.documentos import documentos_bp
    from app.controllers.reportes import reportes_bp
    from app.controllers.api import api_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(documentos_bp)
    app.register_blueprint(reportes_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Handlers para errores
    register_error_handlers(app)
    
    # Contexto shell para pruebas
    @app.shell_context_processor
    def make_shell_context():
        from app.models.usuario import Usuario
        from app.models.documento import Documento
        from app.models.area import Area
        from app.models.persona import Persona
        return {
            'db': db,
            'Usuario': Usuario,
            'Documento': Documento,
            'Area': Area,
            'Persona': Persona
        }
    
    # Contexto global para las plantillas (para pasar `now` a todas las plantillas)
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}
    
    return app

def register_error_handlers(app):
    """
    Registrar handlers para errores comunes
    """
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403
