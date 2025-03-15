from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField, 
                    SelectField, TextAreaField, DateTimeField, HiddenField)
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, ValidationError
from app.models.usuario import Usuario
from app.models.documento import Transportadora, TipoDocumento, EstadoDocumento
from app.models.area import Area
from app.models.cargo import Cargo
from app.models.persona import Persona
from app import db

class LoginForm(FlaskForm):
    """
    Formulario de inicio de sesión
    """
    username = StringField('Usuario', validators=[DataRequired(), Length(1, 50)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordar sesión')
    submit = SubmitField('Iniciar Sesión')

class CambiarPasswordForm(FlaskForm):
    """
    Formulario para cambiar contraseña
    """
    password_actual = PasswordField('Contraseña Actual', validators=[DataRequired()])
    password = PasswordField('Nueva Contraseña', validators=[
        DataRequired(), 
        Length(min=8, message='La contraseña debe tener al menos 8 caracteres')
    ])
    password2 = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(), 
        EqualTo('password', message='Las contraseñas deben coincidir')
    ])
    submit = SubmitField('Cambiar Contraseña')

class UsuarioForm(FlaskForm):
    """
    Formulario para crear/editar usuarios
    """
    username = StringField('Nombre de Usuario', validators=[
        DataRequired(), 
        Length(1, 50)
    ])
    persona_id = SelectField('Persona', coerce=int, validators=[DataRequired()])
    rol_id = SelectField('Rol', coerce=int, validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[
        Length(min=8, message='La contraseña debe tener al menos 8 caracteres'),
        Optional()
    ])
    password2 = PasswordField('Confirmar Contraseña', validators=[
        EqualTo('password', message='Las contraseñas deben coincidir'),
        Optional()
    ])
    activo = BooleanField('Activo')
    submit = SubmitField('Guardar')

    def __init__(self, *args, usuario_actual=None, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        self.usuario_actual = usuario_actual
        self.persona_id.choices = [(p.id, f"{p.nombre} {p.apellido}") 
                                  for p in Persona.query.filter_by(activo=True).all()]
        from app.models.usuario import Rol
        self.rol_id.choices = [(r.id, r.nombre) 
                              for r in Rol.query.all()]

    def validate_username(self, field):
        if self.usuario_actual is None or field.data != self.usuario_actual.username:
            if Usuario.query.filter_by(username=field.data).first():
                raise ValidationError('Este nombre de usuario ya está en uso.')

class PersonaForm(FlaskForm):
    """
    Formulario para crear/editar personas
    """
    nombre = StringField('Nombre', validators=[DataRequired(), Length(1, 100)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(1, 100)])
    email = StringField('Email', validators=[Email(), Length(1, 100), Optional()])
    telefono = StringField('Teléfono', validators=[Length(1, 20), Optional()])
    area_id = SelectField('Área', coerce=int, validators=[DataRequired()])
    cargo_id = SelectField('Cargo', coerce=int, validators=[Optional()])
    activo = BooleanField('Activo', default=True)
    submit = SubmitField('Guardar')
    
    def __init__(self, *args, **kwargs):
        super(PersonaForm, self).__init__(*args, **kwargs)
        self.area_id.choices = [(a.id, a.nombre) 
                               for a in Area.query.filter_by(activo=True).order_by(Area.nombre).all()]
        self.cargo_id.choices = [(0, '-- Seleccione --')] + [(c.id, c.nombre) 
                                for c in Cargo.query.filter_by(activo=True).order_by(Cargo.nombre).all()]


class DocumentoEntradaForm(FlaskForm):
    """
    Formulario para registrar documentos entrantes
    """
    fecha_recepcion = DateTimeField('Fecha y Hora de Recepción', format='%Y-%m-%d %H:%M', 
                                   validators=[DataRequired()])
    transportadora_id = SelectField('Transportadora', coerce=int, validators=[Optional()])
    numero_guia = StringField('Número de Guía', validators=[Length(1, 50), Optional()])
    remitente = StringField('Remitente', validators=[DataRequired(), Length(1, 255)])
    tipo_documento_id = SelectField('Tipo de Documento', coerce=int, validators=[DataRequired()])
    contenido = TextAreaField('Contenido')
    observaciones = TextAreaField('Observaciones')
    area_destino_id = SelectField('Área Destino', coerce=int, validators=[DataRequired()])
    persona_destino_id = SelectField('Persona Destino', coerce=int)  # Sin validadores
    submit = SubmitField('Registrar Documento')
    
    def __init__(self, *args, **kwargs):
        super(DocumentoEntradaForm, self).__init__(*args, **kwargs)
        self.transportadora_id.choices = [(0, '-- Seleccione --')] + [
            (t.id, t.nombre) for t in Transportadora.query.filter_by(activo=True).order_by(Transportadora.nombre).all()
        ]
        self.tipo_documento_id.choices = [
            (t.id, t.nombre) for t in TipoDocumento.query.filter_by(activo=True).order_by(TipoDocumento.nombre).all()
        ]
        self.area_destino_id.choices = [
            (a.id, a.nombre) for a in Area.query.filter_by(activo=True).order_by(Area.nombre).all()
        ]
        self.persona_destino_id.choices = [(0, '-- Seleccione --')]
        
    def validate_persona_destino_id(self, field):
        # Si el valor es 0 o no está en las opciones, simplemente no lo validamos
        return True

class DocumentoSalidaForm(FlaskForm):
    """
    Formulario para registrar documentos salientes
    """
    fecha_envio = DateTimeField('Fecha y Hora de Envío', format='%Y-%m-%d %H:%M', 
                               validators=[DataRequired()])
    transportadora_id = SelectField('Transportadora', coerce=int, validators=[DataRequired()])
    numero_guia = StringField('Número de Guía', validators=[Length(1, 50), Optional()])
    area_origen_id = SelectField('Área Origen', coerce=int, validators=[DataRequired()])
    persona_origen_id = SelectField('Persona Origen', coerce=int)  # Sin validadores
    destinatario = StringField('Destinatario', validators=[DataRequired(), Length(1, 255)])
    tipo_documento_id = SelectField('Tipo de Documento', coerce=int, validators=[DataRequired()])
    contenido = TextAreaField('Contenido')
    observaciones = TextAreaField('Observaciones')
    submit = SubmitField('Registrar Envío')
    
    def __init__(self, *args, **kwargs):
        super(DocumentoSalidaForm, self).__init__(*args, **kwargs)
        self.transportadora_id.choices = [
            (t.id, t.nombre) for t in Transportadora.query.filter_by(activo=True).order_by(Transportadora.nombre).all()
        ]
        self.tipo_documento_id.choices = [
            (t.id, t.nombre) for t in TipoDocumento.query.filter_by(activo=True).order_by(TipoDocumento.nombre).all()
        ]
        self.area_origen_id.choices = [
            (a.id, a.nombre) for a in Area.query.filter_by(activo=True).order_by(Area.nombre).all()
        ]
        self.persona_origen_id.choices = [(0, '-- Seleccione --')]
        
    def validate_persona_origen_id(self, field):
        # Si el valor es 0 o no está en las opciones, simplemente no lo validamos
        return True

class TransferenciaDocumentoForm(FlaskForm):
    """
    Formulario para transferir documentos entre áreas
    """
    documento_id = HiddenField('ID Documento', validators=[DataRequired()])
    area_destino_id = SelectField('Área Destino', coerce=int, validators=[DataRequired()])
    persona_destino_id = SelectField('Persona Destino', coerce=int, validators=[Optional()])
    estado_id = SelectField('Estado', coerce=int, validators=[DataRequired()])
    observaciones = TextAreaField('Observaciones')
    submit = SubmitField('Transferir Documento')
    
    def __init__(self, *args, **kwargs):
        super(TransferenciaDocumentoForm, self).__init__(*args, **kwargs)
        self.area_destino_id.choices = [
            (a.id, a.nombre) for a in Area.query.filter_by(activo=True).order_by(Area.nombre).all()
        ]
        self.persona_destino_id.choices = [(0, '-- Seleccione --')]
        self.estado_id.choices = [
            (e.id, e.nombre) for e in EstadoDocumento.query.order_by(EstadoDocumento.nombre).all()
        ]

class BusquedaForm(FlaskForm):
    """
    Formulario para búsqueda avanzada
    """
    radicado = StringField('Radicado')
    fecha_desde = DateTimeField('Fecha Desde', format='%Y-%m-%d', validators=[Optional()])
    fecha_hasta = DateTimeField('Fecha Hasta', format='%Y-%m-%d', validators=[Optional()])
    transportadora_id = SelectField('Transportadora', coerce=int, validators=[Optional()])
    numero_guia = StringField('Número de Guía')
    remitente = StringField('Remitente/Destinatario')
    tipo_documento_id = SelectField('Tipo de Documento', coerce=int, validators=[Optional()])
    area_id = SelectField('Área Actual', coerce=int, validators=[Optional()])
    estado_id = SelectField('Estado', coerce=int, validators=[Optional()])
    es_entrada = SelectField('Tipo', choices=[
        ('', 'Todos'), 
        ('1', 'Entrada'), 
        ('0', 'Salida')
    ], validators=[Optional()])
    submit = SubmitField('Buscar')
    
    def __init__(self, *args, **kwargs):
        super(BusquedaForm, self).__init__(*args, **kwargs)
        self.transportadora_id.choices = [(0, 'Todas')] + [
            (t.id, t.nombre) for t in Transportadora.query.filter_by(activo=True).order_by(Transportadora.nombre).all()
        ]
        self.tipo_documento_id.choices = [(0, 'Todos')] + [
            (t.id, t.nombre) for t in TipoDocumento.query.filter_by(activo=True).order_by(TipoDocumento.nombre).all()
        ]
        self.area_id.choices = [(0, 'Todas')] + [
            (a.id, a.nombre) for a in Area.query.filter_by(activo=True).order_by(Area.nombre).all()
        ]
        self.estado_id.choices = [(0, 'Todos')] + [
            (e.id, e.nombre) for e in EstadoDocumento.query.order_by(EstadoDocumento.nombre).all()
        ]

class TransportadoraForm(FlaskForm):
    """
    Formulario para crear/editar transportadoras
    """
    nombre = StringField('Nombre', validators=[DataRequired(), Length(1, 100)])
    descripcion = TextAreaField('Descripción')
    activo = BooleanField('Activo', default=True)
    submit = SubmitField('Guardar')

class TipoDocumentoForm(FlaskForm):
    """
    Formulario para crear/editar tipos de documento
    """
    nombre = StringField('Nombre', validators=[DataRequired(), Length(1, 100)])
    descripcion = TextAreaField('Descripción')
    activo = BooleanField('Activo', default=True)
    submit = SubmitField('Guardar')

class RemitenteForm(FlaskForm):
    """
    Formulario para crear/editar remitentes
    """
    nombre = StringField('Nombre', validators=[DataRequired(), Length(1, 100)])
    tipo = SelectField('Tipo', choices=[
        ('PROVEEDOR', 'Proveedor'),
        ('CLIENTE', 'Cliente'),
        ('INTERNO', 'Interno'),
        ('OTRO', 'Otro')
    ], validators=[DataRequired()])
    email = StringField('Email', validators=[Email(), Length(1, 100), Optional()])
    telefono = StringField('Teléfono', validators=[Length(1, 20), Optional()])
    direccion = StringField('Dirección', validators=[Length(1, 255), Optional()])
    activo = BooleanField('Activo', default=True)
    submit = SubmitField('Guardar')

class AreaForm(FlaskForm):
    """
    Formulario para crear/editar áreas
    """
    nombre = StringField('Nombre', validators=[DataRequired(), Length(1, 100)])
    descripcion = TextAreaField('Descripción')
    activo = BooleanField('Activo', default=True)
    submit = SubmitField('Guardar')

class CargoForm(FlaskForm):
    """
    Formulario para crear/editar cargos
    """
    nombre = StringField('Nombre', validators=[DataRequired(), Length(1, 100)])
    descripcion = TextAreaField('Descripción')
    activo = BooleanField('Activo', default=True)
    submit = SubmitField('Guardar')

class ZonaEconomicaForm(FlaskForm):
    """
    Formulario para crear/editar zonas económicas
    """
    nombre = StringField('Nombre', validators=[DataRequired(), Length(1, 100)])
    descripcion = TextAreaField('Descripción')
    activo = BooleanField('Activo', default=True)
    submit = SubmitField('Guardar')