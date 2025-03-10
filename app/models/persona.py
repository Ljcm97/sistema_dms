from datetime import datetime
from app import db

class Persona(db.Model):
    """
    Modelo para las personas/empleados de la empresa
    """
    __tablename__ = 'personas'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    telefono = db.Column(db.String(20))
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    usuario = db.relationship('Usuario', backref='persona', uselist=False)
    documentos_actuales = db.relationship('Documento', 
                                        foreign_keys='Documento.persona_actual_id', 
                                        backref='persona_actual', 
                                        lazy='dynamic')
    
    @property
    def nombre_completo(self):
        """
        Obtener el nombre completo de la persona
        """
        return f"{self.nombre} {self.apellido}"
    
    def __repr__(self):
        return f'<Persona {self.nombre} {self.apellido}>'
    
    @classmethod
    def get_by_area(cls, area_id):
        """
        Obtener todas las personas de un área específica
        """
        return cls.query.filter_by(area_id=area_id, activo=True).order_by(cls.nombre, cls.apellido).all()