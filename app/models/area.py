from datetime import datetime
from app import db

class Area(db.Model):
    """
    Modelo para las áreas de la empresa
    """
    __tablename__ = 'areas'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    personas = db.relationship('Persona', backref='area', lazy='dynamic')
    documentos_actuales = db.relationship('Documento', 
                                        foreign_keys='Documento.area_actual_id', 
                                        backref='area_actual', 
                                        lazy='dynamic')
    
    def __repr__(self):
        return f'<Area {self.nombre}>'
    
    @classmethod
    def get_active_areas(cls):
        """
        Obtener todas las áreas activas
        """
        return cls.query.filter_by(activo=True).order_by(cls.nombre).all()