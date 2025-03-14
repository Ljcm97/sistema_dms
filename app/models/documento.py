from datetime import datetime
from app import db

class Transportadora(db.Model):
    """
    Modelo para las empresas transportadoras
    """
    __tablename__ = 'transportadoras'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    documentos = db.relationship('Documento', backref='transportadora', lazy='dynamic')
    
    def __repr__(self):
        return f'<Transportadora {self.nombre}>'
    
    @classmethod
    def get_active_transportadoras(cls):
        """
        Obtener todas las transportadoras activas
        """
        return cls.query.filter_by(activo=True).order_by(cls.nombre).all()

class TipoDocumento(db.Model):
    """
    Modelo para los tipos de documento
    """
    __tablename__ = 'tipos_documento'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    documentos = db.relationship('Documento', backref='tipo_documento', lazy='dynamic')
    
    def __repr__(self):
        return f'<TipoDocumento {self.nombre}>'
    
    @classmethod
    def get_active_tipos(cls):
        """
        Obtener todos los tipos de documento activos
        """
        return cls.query.filter_by(activo=True).order_by(cls.nombre).all()

class EstadoDocumento(db.Model):
    """
    Modelo para los estados de documento
    """
    __tablename__ = 'estados_documento'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.Text)
    color = db.Column(db.String(7), default='#000000')
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    documentos = db.relationship('Documento', backref='estado', lazy='dynamic')
    movimientos = db.relationship('HistorialMovimiento', backref='estado', lazy='dynamic')
    
    def __repr__(self):
        return f'<EstadoDocumento {self.nombre}>'

class Documento(db.Model):
    """
    Modelo para los documentos
    """
    __tablename__ = 'documentos'
    
    id = db.Column(db.Integer, primary_key=True)
    radicado = db.Column(db.String(20), unique=True, nullable=False)
    fecha_recepcion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    transportadora_id = db.Column(db.Integer, db.ForeignKey('transportadoras.id'))
    numero_guia = db.Column(db.String(50))
    remitente = db.Column(db.String(255), nullable=False)
    tipo_documento_id = db.Column(db.Integer, db.ForeignKey('tipos_documento.id'), nullable=False)
    contenido = db.Column(db.Text)
    observaciones = db.Column(db.Text)
    area_actual_id = db.Column(db.Integer, db.ForeignKey('areas.id'), nullable=False)
    persona_actual_id = db.Column(db.Integer, db.ForeignKey('personas.id'))
    estado_id = db.Column(db.Integer, db.ForeignKey('estados_documento.id'), nullable=False)
    ruta_adjunto = db.Column(db.String(255))
    es_entrada = db.Column(db.Boolean, default=True)
    fecha_finalizacion = db.Column(db.DateTime)
    
    # Usuarios que crearon o actualizaron el documento
    usuario_creacion_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    usuario_actualizacion_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    
    # Timestamps
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relaciones
    historial = db.relationship('HistorialMovimiento', backref='documento', lazy='dynamic',
                               cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Documento {self.radicado}>'
    
    def get_estado_badge(self):
        """
        Obtener el HTML para mostrar el estado como un badge
        """
        return f'<span class="badge" style="background-color: {self.estado.color}">{self.estado.nombre}</span>'
    
    @classmethod
    def generar_radicado(cls):
        """
        Generar un nuevo número de radicado asegurando que sea único
        """
        import datetime
        
        # Generar el prefijo con la fecha de hoy
        today = datetime.date.today()
        prefix = today.strftime("%Y%m%d")
        
        # Buscar el último número de radicado para hoy
        last_doc = cls.query.filter(
            cls.radicado.like(f"{prefix}-%")
        ).order_by(cls.radicado.desc()).first()
        
        if last_doc:
            # Obtener el número y añadir 1
            last_num = int(last_doc.radicado.split('-')[1])
            new_num = last_num + 1
        else:
            # Primer documento del día
            new_num = 1
        
        # Formatear el radicado con el nuevo número
        radicado = f"{prefix}-{new_num:04d}"
        
        # Verificar que no exista ya (por si acaso)
        while cls.query.filter_by(radicado=radicado).first():
            new_num += 1
            radicado = f"{prefix}-{new_num:04d}"
        
        return radicado
    
    def transferir(self, area_id, persona_id, estado_id, observaciones, usuario_id):
        """
        Transferir el documento a otra área/persona
        """
        # Actualizar el documento
        self.area_actual_id = area_id
        self.persona_actual_id = persona_id
        self.estado_id = estado_id
        self.usuario_actualizacion_id = usuario_id
        
        if estado_id == self.get_estado_finalizado().id:
            self.fecha_finalizacion = datetime.utcnow()
        
        db.session.commit()
        
        return True
    
    @classmethod
    def get_estado_finalizado(cls):
        """
        Obtener el estado "Finalizado"
        """
        return EstadoDocumento.query.filter_by(nombre='Finalizado').first()
    
    @classmethod
    def get_estado_recibido(cls):
        """
        Obtener el estado "Recibido"
        """
        return EstadoDocumento.query.filter_by(nombre='Recibido').first()