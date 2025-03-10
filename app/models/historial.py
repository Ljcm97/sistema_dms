from datetime import datetime
from app import db

class HistorialMovimiento(db.Model):
    """
    Modelo para el historial de movimientos de documentos
    """
    __tablename__ = 'historial_movimientos'
    
    id = db.Column(db.Integer, primary_key=True)
    documento_id = db.Column(db.Integer, db.ForeignKey('documentos.id'), nullable=False)
    fecha_movimiento = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Área y persona de origen
    area_origen_id = db.Column(db.Integer, db.ForeignKey('areas.id'), nullable=False)
    persona_origen_id = db.Column(db.Integer, db.ForeignKey('personas.id'))
    
    # Área y persona de destino
    area_destino_id = db.Column(db.Integer, db.ForeignKey('areas.id'), nullable=False)
    persona_destino_id = db.Column(db.Integer, db.ForeignKey('personas.id'))
    
    estado_id = db.Column(db.Integer, db.ForeignKey('estados_documento.id'), nullable=False)
    observaciones = db.Column(db.Text)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    area_origen = db.relationship('Area', foreign_keys=[area_origen_id])
    persona_origen = db.relationship('Persona', foreign_keys=[persona_origen_id])
    area_destino = db.relationship('Area', foreign_keys=[area_destino_id])
    persona_destino = db.relationship('Persona', foreign_keys=[persona_destino_id])
    
    def __repr__(self):
        return f'<HistorialMovimiento {self.id} - Doc: {self.documento_id}>'
    
    @classmethod
    def get_timeline(cls, documento_id):
        """
        Obtener el timeline completo de un documento
        """
        return cls.query.filter_by(documento_id=documento_id)\
                .order_by(cls.fecha_movimiento.desc())\
                .all()
    
    @classmethod
    def get_recent_movements(cls, limit=10):
        """
        Obtener los movimientos recientes
        """
        return cls.query.order_by(cls.fecha_movimiento.desc())\
                .limit(limit)\
                .all()