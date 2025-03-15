from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models.documento import TipoDocumento, Documento, EstadoDocumento
from app.forms import TipoDocumentoForm, DocumentoEntradaForm, DocumentoSalidaForm, TransferenciaDocumentoForm, BusquedaForm
from sqlalchemy import func
from datetime import datetime, timedelta

# Crear blueprint
tipos_bp = Blueprint('tipos', __name__, url_prefix='/tipos')
documentos_bp = Blueprint('documentos', __name__)

@tipos_bp.route('/')
@login_required
def index():
    """
    Lista de tipos de documento
    """
    # Verificar que el usuario sea superadministrador
    if not current_user.is_superadmin():
        flash('No tienes permisos para acceder a esta sección', 'danger')
        return redirect(url_for('documentos.dashboard'))
    
    page = request.args.get('page', 1, type=int)
    
    # Filtro de búsqueda
    search = request.args.get('search', '')
    
    # Query base
    query = TipoDocumento.query
    
    # Aplicar filtro de búsqueda
    if search:
        query = query.filter(TipoDocumento.nombre.like(f'%{search}%'))
    
    # Ordenar por nombre
    query = query.order_by(TipoDocumento.nombre)
    
    # Paginación
    pagination = query.paginate(
        page=page, 
        per_page=current_app.config['ITEMS_PER_PAGE'],
        error_out=False
    )
    
    # Estadísticas
    total_tipos = TipoDocumento.query.count()
    activos = TipoDocumento.query.filter_by(activo=True).count()
    
    # Uso de tipos de documento
    from app.models.documento import Documento
    tipos_uso = db.session.query(
        TipoDocumento.id,
        TipoDocumento.nombre,
        func.count(Documento.id).label('num_documentos')
    ).outerjoin(
        Documento, Documento.tipo_documento_id == TipoDocumento.id
    ).group_by(
        TipoDocumento.id, TipoDocumento.nombre
    ).order_by(
        func.count(Documento.id).desc()
    ).limit(5).all()
    
    return render_template('tipos/index.html',
                          title='Gestión de Tipos de Documento',
                          tipos=pagination.items,
                          pagination=pagination,
                          search=search,
                          total_tipos=total_tipos,
                          activos=activos,
                          tipos_uso=tipos_uso)

@tipos_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    """
    Crear un nuevo tipo de documento
    """
    # Verificar que el usuario sea superadministrador
    if not current_user.is_superadmin():
        flash('No tienes permisos para acceder a esta sección', 'danger')
        return redirect(url_for('documentos.dashboard'))
    
    form = TipoDocumentoForm()
    
    if form.validate_on_submit():
        # Verificar si ya existe un tipo con el mismo nombre
        if TipoDocumento.query.filter(func.lower(TipoDocumento.nombre) == func.lower(form.nombre.data)).first():
            flash('Ya existe un tipo de documento con este nombre', 'danger')
            return render_template('tipos/crear.html', form=form, title='Crear Tipo de Documento')
        
        # Crear tipo de documento
        tipo = TipoDocumento(
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            activo=form.activo.data
        )
        
        db.session.add(tipo)
        db.session.commit()
        
        flash(f'Tipo de documento {tipo.nombre} creado correctamente', 'success')
        return redirect(url_for('tipos.index'))
    
    return render_template('tipos/crear.html', form=form, title='Crear Tipo de Documento')

@tipos_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    """
    Editar un tipo de documento existente
    """
    # Verificar que el usuario sea superadministrador
    if not current_user.is_superadmin():
        flash('No tienes permisos para acceder a esta sección', 'danger')
        return redirect(url_for('documentos.dashboard'))
    
    tipo = TipoDocumento.query.get_or_404(id)
    form = TipoDocumentoForm()
    
    if request.method == 'GET':
        form.nombre.data = tipo.nombre
        form.descripcion.data = tipo.descripcion
        form.activo.data = tipo.activo
    
    if form.validate_on_submit():
        # Verificar si ya existe otro tipo con el mismo nombre
        duplicate = TipoDocumento.query.filter(
            func.lower(TipoDocumento.nombre) == func.lower(form.nombre.data),
            TipoDocumento.id != tipo.id
        ).first()
        
        if duplicate:
            flash('Ya existe otro tipo de documento con este nombre', 'danger')
            return render_template('tipos/editar.html', form=form, tipo=tipo, title='Editar Tipo de Documento')
        
        # Actualizar tipo de documento
        tipo.nombre = form.nombre.data
        tipo.descripcion = form.descripcion.data
        tipo.activo = form.activo.data
        
        db.session.commit()
        
        flash(f'Tipo de documento {tipo.nombre} actualizado correctamente', 'success')
        return redirect(url_for('tipos.index'))
    
    return render_template('tipos/editar.html', form=form, tipo=tipo, title='Editar Tipo de Documento')

@tipos_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    """
    Eliminar un tipo de documento
    """
    # Verificar que el usuario sea superadministrador
    if not current_user.is_superadmin():
        flash('No tienes permisos para acceder a esta sección', 'danger')
        return redirect(url_for('documentos.dashboard'))
    
    try:
        tipo = TipoDocumento.query.get_or_404(id)
        
        # Verificar si el tipo está en uso
        if tipo.documentos.count() > 0:
            flash(f'No se puede eliminar el tipo de documento {tipo.nombre} porque está en uso', 'danger')
            return redirect(url_for('tipos.index'))
        
        # Guardar nombre para mensaje
        nombre = tipo.nombre
        
        db.session.delete(tipo)
        db.session.commit()
        
        flash(f'Tipo de documento {nombre} eliminado correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar: {str(e)}', 'danger')
    
    return redirect(url_for('tipos.index'))

@documentos_bp.route('/')
@login_required
def dashboard():
    """
    Dashboard principal
    """
    # Obtener documentos pendientes para el área del usuario
    from app.models.documento import Documento, EstadoDocumento
    
    # Estado finalizado
    estado_finalizado = EstadoDocumento.query.filter_by(nombre='Finalizado').first()
    
    if current_user.is_superadmin():
        # Si es superadmin, mostrar datos globales
        documentos_pendientes = Documento.query.filter(
            Documento.estado_id != estado_finalizado.id if estado_finalizado else False
        ).count()
        
        documentos_finalizados = Documento.query.filter_by(
            estado_id=estado_finalizado.id if estado_finalizado else 0
        ).count()
        
        documentos_recientes = Documento.query.order_by(
            Documento.fecha_recepcion.desc()
        ).limit(10).all()
    else:
        # Si no es superadmin, mostrar solo datos del área del usuario
        documentos_pendientes = Documento.query.filter(
            Documento.area_actual_id == current_user.persona.area_id,
            Documento.estado_id != estado_finalizado.id if estado_finalizado else False
        ).count()
        
        documentos_finalizados = Documento.query.filter_by(
            area_actual_id=current_user.persona.area_id,
            estado_id=estado_finalizado.id if estado_finalizado else 0
        ).count()
        
        documentos_recientes = Documento.query.filter_by(
            area_actual_id=current_user.persona.area_id
        ).order_by(
            Documento.fecha_recepcion.desc()
        ).limit(10).all()
    
    # Obtener movimientos recientes
    from app.models.historial import HistorialMovimiento
    
    if current_user.is_superadmin():
        movimientos_recientes = HistorialMovimiento.query.order_by(
            HistorialMovimiento.fecha_movimiento.desc()
        ).limit(10).all()
    else:
        # Si no es superadmin, mostrar solo movimientos del área del usuario
        movimientos_recientes = HistorialMovimiento.query.filter(
            (HistorialMovimiento.area_origen_id == current_user.persona.area_id) |
            (HistorialMovimiento.area_destino_id == current_user.persona.area_id)
        ).order_by(
            HistorialMovimiento.fecha_movimiento.desc()
        ).limit(10).all()
    
    return render_template('documentos/dashboard.html',
                          title='Dashboard',
                          documentos_pendientes=documentos_pendientes,
                          documentos_finalizados=documentos_finalizados,
                          documentos_recientes=documentos_recientes,
                          movimientos_recientes=movimientos_recientes)

@documentos_bp.route('/lista')
@login_required
def lista_documentos():
    """
    Lista de documentos
    """
    # Obtener parámetros de búsqueda y filtrado
    page = request.args.get('page', 1, type=int)
    
    # Crear formulario de búsqueda
    from app.forms import BusquedaForm
    form = BusquedaForm()
    
    # Consulta base
    from app.models.documento import Documento
    query = Documento.query
    
    # Aplicar filtros de búsqueda si se proporcionaron
    if request.args.get('radicado'):
        query = query.filter(Documento.radicado.like(f"%{request.args.get('radicado')}%"))
    
    if request.args.get('fecha_desde'):
        fecha_desde = datetime.strptime(request.args.get('fecha_desde'), '%Y-%m-%d')
        query = query.filter(Documento.fecha_recepcion >= fecha_desde)
    
    if request.args.get('fecha_hasta'):
        fecha_hasta = datetime.strptime(request.args.get('fecha_hasta'), '%Y-%m-%d')
        fecha_hasta = fecha_hasta + timedelta(days=1)  # Incluir todo el día
        query = query.filter(Documento.fecha_recepcion <= fecha_hasta)
    
    if request.args.get('transportadora_id') and int(request.args.get('transportadora_id')) > 0:
        query = query.filter(Documento.transportadora_id == int(request.args.get('transportadora_id')))
    
    if request.args.get('tipo_documento_id') and int(request.args.get('tipo_documento_id')) > 0:
        query = query.filter(Documento.tipo_documento_id == int(request.args.get('tipo_documento_id')))
    
    if request.args.get('area_id') and int(request.args.get('area_id')) > 0:
        query = query.filter(Documento.area_actual_id == int(request.args.get('area_id')))
    
    if request.args.get('estado_id') and int(request.args.get('estado_id')) > 0:
        query = query.filter(Documento.estado_id == int(request.args.get('estado_id')))
    
    if request.args.get('es_entrada') in ['0', '1']:
        query = query.filter(Documento.es_entrada == (request.args.get('es_entrada') == '1'))
    
    if request.args.get('remitente'):
        query = query.filter(Documento.remitente.like(f"%{request.args.get('remitente')}%"))
    
    # Si no es superadmin, mostrar solo documentos del área del usuario
    if not current_user.is_superadmin() and not current_user.puede_ver_documentos_area():
        # Limitar a documentos donde el usuario es la persona asignada
        query = query.filter(Documento.persona_actual_id == current_user.persona_id)
    elif not current_user.is_superadmin():
        # Limitar a documentos del área del usuario
        query = query.filter(Documento.area_actual_id == current_user.persona.area_id)
    
    # Ordenar por fecha de recepción descendente
    query = query.order_by(Documento.fecha_recepcion.desc())
    
    # Paginación
    pagination = query.paginate(
        page=page, 
        per_page=current_app.config['ITEMS_PER_PAGE'],
        error_out=False
    )
    
    # Formularios para modales
    from app.forms import DocumentoEntradaForm, DocumentoSalidaForm
    entrada_form = DocumentoEntradaForm()
    salida_form = DocumentoSalidaForm()
    
    # Verificar si el usuario puede crear documentos
    puede_crear_documentos = current_user.puede_registrar_documentos()
    
    return render_template('documentos/lista.html',
                          title='Lista de Documentos',
                          documentos=pagination.items,
                          pagination=pagination,
                          form=form,
                          entrada_form=entrada_form,
                          salida_form=salida_form,
                          puede_crear_documentos=puede_crear_documentos)

@documentos_bp.route('/<int:id>')
@login_required
def detalle_documento(id):
    """
    Detalle de un documento
    """
    # Obtener el documento
    from app.models.documento import Documento
    documento = Documento.query.get_or_404(id)
    
    # Verificar permisos
    if not current_user.is_superadmin() and not current_user.puede_ver_documentos_area():
        if documento.area_actual_id != current_user.persona.area_id or documento.persona_actual_id != current_user.persona_id:
            flash('No tienes permisos para ver este documento', 'danger')
            return redirect(url_for('documentos.dashboard'))
    
    # Obtener el historial de movimientos
    from app.models.historial import HistorialMovimiento
    historial = HistorialMovimiento.query.filter_by(documento_id=id).order_by(HistorialMovimiento.fecha_movimiento.desc()).all()
    
    # Formulario de transferencia
    from app.forms import TransferenciaDocumentoForm
    form_transferencia = TransferenciaDocumentoForm()
    form_transferencia.documento_id.data = id
    
    # Verificar si el usuario puede transferir el documento
    puede_transferir = current_user.is_superadmin() or (
        documento.area_actual_id == current_user.persona.area_id and 
        (documento.persona_actual_id == current_user.persona_id or current_user.puede_ver_documentos_area())
    )
    
    # Verificar si el usuario es el destinatario y si el documento está pendiente de aceptación
    es_destinatario = current_user.persona_id == documento.persona_actual_id
    from app.models.documento import EstadoDocumento
    estado_recibido = EstadoDocumento.query.filter_by(nombre='Recibido').first()
    pendiente_aceptacion = documento.estado_id == estado_recibido.id if estado_recibido else False
    
    return render_template('documentos/detalle.html',
                          title=f'Documento {documento.radicado}',
                          documento=documento,
                          historial=historial,
                          form_transferencia=form_transferencia,
                          puede_transferir=puede_transferir,
                          es_destinatario=es_destinatario,
                          pendiente_aceptacion=pendiente_aceptacion)

@documentos_bp.route('/registrar-entrada', methods=['GET', 'POST'])
@login_required
def registrar_entrada():
    """
    Registrar un nuevo documento entrante
    """
    # Verificar que el usuario pueda registrar documentos
    if not current_user.puede_registrar_documentos():
        flash('No tienes permisos para registrar documentos', 'danger')
        return redirect(url_for('documentos.dashboard'))
    
    from app.forms import DocumentoEntradaForm
    form = DocumentoEntradaForm()
    
    if form.validate_on_submit():
        # Código para procesar el formulario
        # ...
        flash('Documento registrado correctamente', 'success')
        return redirect(url_for('documentos.lista_documentos'))
    
    return render_template('documentos/registrar_entrada.html',
                          title='Registrar Documento Entrante',
                          form=form)

@documentos_bp.route('/registrar-entrada-completo', methods=['GET', 'POST'])
@login_required
def registrar_entrada_completo():
    """
    Vista completa para registrar un documento entrante
    """
    return registrar_entrada()

@documentos_bp.route('/registrar-salida', methods=['GET', 'POST'])
@login_required
def registrar_salida():
    """
    Registrar un nuevo documento saliente
    """
    # Verificar que el usuario pueda registrar documentos
    if not current_user.puede_registrar_documentos():
        flash('No tienes permisos para registrar documentos', 'danger')
        return redirect(url_for('documentos.dashboard'))
    
    from app.forms import DocumentoSalidaForm
    form = DocumentoSalidaForm()
    
    if form.validate_on_submit():
        # Código para procesar el formulario
        # ...
        flash('Documento registrado correctamente', 'success')
        return redirect(url_for('documentos.lista_documentos'))
    
    return render_template('documentos/registrar_salida.html',
                          title='Registrar Documento Saliente',
                          form=form)

@documentos_bp.route('/registrar-salida-completo', methods=['GET', 'POST'])
@login_required
def registrar_salida_completo():
    """
    Vista completa para registrar un documento saliente
    """
    return registrar_salida()

@documentos_bp.route('/transferir', methods=['POST'])
@login_required
def transferir_documento():
    """
    Transferir un documento a otra área/persona
    """
    from app.forms import TransferenciaDocumentoForm
    form = TransferenciaDocumentoForm()
    
    if form.validate_on_submit():
        # Código para procesar el formulario
        # ...
        flash('Documento transferido correctamente', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error en el campo {field}: {error}', 'danger')
    
    return redirect(url_for('documentos.detalle_documento', id=form.documento_id.data))

@documentos_bp.route('/aceptar/<int:id>', methods=['POST'])
@login_required
def aceptar_documento(id):
    """
    Aceptar un documento asignado
    """
    # Código para aceptar el documento
    # ...
    flash('Documento aceptado correctamente', 'success')
    return redirect(url_for('documentos.detalle_documento', id=id))

@documentos_bp.route('/rechazar/<int:id>', methods=['POST'])
@login_required
def rechazar_documento(id):
    """
    Rechazar un documento asignado
    """
    motivo = request.form.get('motivo', '')
    
    if not motivo:
        flash('Debe proporcionar un motivo para rechazar el documento', 'danger')
        return redirect(url_for('documentos.detalle_documento', id=id))
    
    # Código para rechazar el documento
    # ...
    flash('Documento rechazado correctamente', 'success')
    return redirect(url_for('documentos.lista_documentos'))