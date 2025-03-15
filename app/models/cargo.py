from datetime import datetime
from app import db

class Cargo(db.Model):
    """
    Modelo para los cargos de la empresa
    """
    __tablename__ = 'cargos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    personas = db.relationship('Persona', backref='cargo', lazy='dynamic')
    
    def __repr__(self):
        return f'<Cargo {self.nombre}>'
    
    @classmethod
    def get_active_cargos(cls):
        """
        Obtener todos los cargos activos
        """
        return cls.query.filter_by(activo=True).order_by(cls.nombre).all()