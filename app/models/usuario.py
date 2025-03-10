from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class Rol(db.Model):
    """
    Modelo para los roles de usuario
    """
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.Text)
    es_superadmin = db.Column(db.Boolean, default=False)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    usuarios = db.relationship('Usuario', backref='rol', lazy='dynamic')
    
    def __repr__(self):
        return f'<Rol {self.nombre}>'

class Usuario(UserMixin, db.Model):
    """
    Modelo para los usuarios del sistema
    """
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    persona_id = db.Column(db.Integer, db.ForeignKey('personas.id'), nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    ultimo_acceso = db.Column(db.DateTime)
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    documentos_creados = db.relationship('Documento', 
                                        foreign_keys='Documento.usuario_creacion_id', 
                                        backref='creador', 
                                        lazy='dynamic')
    documentos_actualizados = db.relationship('Documento', 
                                             foreign_keys='Documento.usuario_actualizacion_id', 
                                             backref='actualizador', 
                                             lazy='dynamic')
    movimientos = db.relationship('HistorialMovimiento', 
                                 backref='usuario', 
                                 lazy='dynamic')
    
    @property
    def password(self):
        """
        Prevenir acceso a la contraseña
        """
        raise AttributeError('La contraseña no es un atributo legible')
    
    @password.setter
    def password(self, password):
        """
        Establecer hash de contraseña
        """
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        """
        Verificar contraseña
        """
        return check_password_hash(self.password_hash, password)
    
    def update_ultimo_acceso(self):
        """
        Actualizar la fecha del último acceso
        """
        self.ultimo_acceso = datetime.utcnow()
        db.session.commit()
    
    def is_superadmin(self):
        """
        Verificar si el usuario es superadministrador
        """
        return self.rol.es_superadmin
    
    def __repr__(self):
        return f'<Usuario {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    """
    Callback para cargar un usuario desde la sesión
    """
    return Usuario.query.get(int(user_id))