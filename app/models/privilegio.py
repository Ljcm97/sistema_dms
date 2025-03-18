from datetime import datetime
from app import db

class Privilegio(db.Model):
    """
    Modelo para privilegios especiales de usuarios
    """
    __tablename__ = 'privilegios'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False, unique=True)
    
    # Permisos de documentos
    puede_registrar_documentos = db.Column(db.Boolean, default=False)
    puede_ver_documentos_area = db.Column(db.Boolean, default=False)
    
    # Permisos de administración
    puede_administrar_usuarios = db.Column(db.Boolean, default=False)
    puede_administrar_personas = db.Column(db.Boolean, default=False)
    puede_administrar_areas = db.Column(db.Boolean, default=False)
    
    creado_por = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relaciones específicas con claves foráneas
    creador = db.relationship('Usuario', foreign_keys=[creado_por])
    usuario = db.relationship('Usuario', 
                              foreign_keys=[usuario_id], 
                              back_populates='privilegios', 
                              uselist=False,
                              # Especificar explícitamente las claves foráneas
                              primaryjoin='Privilegio.usuario_id == Usuario.id')
    
    def __repr__(self):
        return f'<Privilegio para usuario_id={self.usuario_id}>'