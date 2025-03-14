from datetime import datetime
from app import db

class Notificacion(db.Model):
    """
    Modelo para notificaciones de usuarios
    """
    __tablename__ = 'notificaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    documento_id = db.Column(db.Integer, db.ForeignKey('documentos.id'))
    mensaje = db.Column(db.String(255), nullable=False)
    leida = db.Column(db.Boolean, default=False)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    usuario = db.relationship('Usuario', backref='notificaciones', lazy='joined')
    documento = db.relationship('Documento', backref='notificaciones', lazy='joined')
    
    def __repr__(self):
        return f'<Notificacion {self.id} - {self.mensaje[:20]}>'
    
    @classmethod
    def crear_notificacion_documento(cls, usuario_id, documento_id, accion="recibido"):
        """
        Crear una notificación para un documento
        """
        from app.models.documento import Documento
        documento = Documento.query.get(documento_id)
        
        if not documento:
            return None
            
        if accion == "recibido":
            mensaje = f"Se te ha asignado el documento {documento.radicado}"
        elif accion == "transferido":
            mensaje = f"El documento {documento.radicado} ha sido transferido a tu área"
        elif accion == "rechazado":
            mensaje = f"El documento {documento.radicado} ha sido rechazado"
        else:
            mensaje = f"Acción sobre el documento {documento.radicado}"
        
        notificacion = cls(
            usuario_id=usuario_id,
            documento_id=documento_id,
            mensaje=mensaje
        )
        db.session.add(notificacion)
        db.session.commit()
        return notificacion
    
    @classmethod
    def get_notificaciones_no_leidas(cls, usuario_id):
        """
        Obtener notificaciones no leídas de un usuario
        """
        return cls.query.filter_by(
            usuario_id=usuario_id,
            leida=False
        ).order_by(cls.creado_en.desc()).all()
    
    @classmethod
    def marcar_como_leida(cls, notificacion_id):
        """
        Marcar una notificación como leída
        """
        notificacion = cls.query.get(notificacion_id)
        if notificacion:
            notificacion.leida = True
            db.session.commit()
        return notificacion