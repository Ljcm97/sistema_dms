# En un nuevo archivo app/models/zona_economica.py

from datetime import datetime
from app import db

class ZonaEconomica(db.Model):
    """
    Modelo para las zonas económicas
    """
    __tablename__ = 'zonas_economicas'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ZonaEconomica {self.nombre}>'
    
    @classmethod
    def get_active_zonas(cls):
        """
        Obtener todas las zonas económicas activas
        """
        return cls.query.filter_by(activo=True).order_by(cls.nombre).all()