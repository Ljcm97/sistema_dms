from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models.documento import TipoDocumento, Documento, EstadoDocumento, Transportadora
from app.forms import TipoDocumentoForm, DocumentoEntradaForm, DocumentoSalidaForm, TransferenciaDocumentoForm, BusquedaForm
from sqlalchemy import func, desc
from datetime import datetime, timedelta
import os
from werkzeug.utils import secure_filename
from app.models.historial import HistorialMovimiento
from app.models.area import Area
from app.models.persona import Persona
from app.models.usuario import Usuario
from app.utils.decoradores import permiso_requerido, solo_superadmin

# Crear blueprint
tipos_bp = Blueprint('tipos', __name__, url_prefix='/tipos')
documentos_bp = Blueprint('documentos', __name__)

@tipos_bp.route('/')
@login_required
@solo_superadmin
def index():
    """
    Lista de tipos de documento
    """
    # Ya no es necesario verificar permisos aquí porque el decorador @solo_superadmin lo hace
    
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
    form = BusquedaForm()
    
    # Consulta base
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
    
    # Más filtros...
    
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
    
    # Verificar si el usuario puede crear documentos
    puede_crear_documentos = current_user.puede_registrar_documentos()
    
    return render_template('documentos/lista.html',
                          title='Lista de Documentos',
                          documentos=pagination.items,
                          pagination=pagination,
                          form=form,
                          puede_crear_documentos=puede_crear_documentos)

@documentos_bp.route('/<int:id>')
@login_required
def detalle_documento(id):
    """
    Detalle de un documento
    """
    # Obtener el documento
    documento = Documento.query.get_or_404(id)
    
    # Verificar permisos
    if not current_user.is_superadmin() and not current_user.puede_ver_documentos_area():
        if documento.area_actual_id != current_user.persona.area_id or documento.persona_actual_id != current_user.persona_id:
            flash('No tienes permisos para ver este documento', 'danger')
            return redirect(url_for('documentos.dashboard'))
    
    # Obtener el historial de movimientos
    historial = HistorialMovimiento.query.filter_by(documento_id=id).order_by(HistorialMovimiento.fecha_movimiento.desc()).all()
    
    # Formulario de transferencia
    form_transferencia = TransferenciaDocumentoForm()
    form_transferencia.documento_id.data = id
    
    # Verificar si el usuario puede transferir el documento
    puede_transferir = current_user.is_superadmin() or (
        documento.area_actual_id == current_user.persona.area_id and 
        (documento.persona_actual_id == current_user.persona_id or current_user.puede_ver_documentos_area())
    )
    
    # Verificar si el usuario es el destinatario y si el documento está pendiente de aceptación
    es_destinatario = current_user.persona_id == documento.persona_actual_id
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
@permiso_requerido('puede_registrar_documentos')
def registrar_entrada():
    """
    Registrar un nuevo documento entrante
    """
    # Ya no es necesario verificar permisos aquí porque el decorador lo hace
    
    form = DocumentoEntradaForm()
    
    # Obtener todas las áreas activas para el formulario
    areas = Area.query.filter_by(activo=True).order_by(Area.nombre).all()
    
    # Establecer fecha y hora actual si el formulario es nuevo
    if request.method == 'GET':
        form.fecha_recepcion.data = datetime.now()
    
    if form.validate_on_submit():
        try:
            # Generar radicado único
            radicado = Documento.generar_radicado()
            
            # Validar si la persona_destino_id está vacía o no
            persona_destino_id = None
            if form.persona_destino_id.data and form.persona_destino_id.data != '':
                persona_destino_id = int(form.persona_destino_id.data)
                
            # Crear el documento
            documento = Documento(
                radicado=radicado,
                fecha_recepcion=form.fecha_recepcion.data,
                transportadora_id=form.transportadora_id.data if form.transportadora_id.data > 0 else None,
                numero_guia=form.numero_guia.data,
                remitente=form.remitente.data,
                tipo_documento_id=form.tipo_documento_id.data,
                contenido=form.contenido.data,
                observaciones=form.observaciones.data,
                area_actual_id=form.area_destino_id.data,
                persona_actual_id=persona_destino_id,
                estado_id=EstadoDocumento.query.filter_by(nombre='Recibido').first().id,
                es_entrada=True,
                usuario_creacion_id=current_user.id
            )
            
            db.session.add(documento)
            db.session.flush()  # Para obtener el ID sin hacer commit aún
            
            # Registrar en el historial
            historial = HistorialMovimiento(
                documento_id=documento.id,
                fecha_movimiento=documento.fecha_recepcion,
                area_origen_id=current_user.persona.area_id,
                persona_origen_id=current_user.persona_id,
                area_destino_id=documento.area_actual_id,
                persona_destino_id=persona_destino_id,
                estado_id=documento.estado_id,
                observaciones=documento.observaciones,
                usuario_id=current_user.id
            )
            
            db.session.add(historial)
            db.session.commit()
            
            # Crear notificación si hay persona destino
            if documento.persona_actual_id:
                from app.models.notificacion import Notificacion
                usuario_destino = Usuario.query.filter_by(persona_id=documento.persona_actual_id).first()
                if usuario_destino:
                    Notificacion.crear_notificacion_documento(
                        usuario_id=usuario_destino.id,
                        documento_id=documento.id,
                        accion="recibido"
                    )
            
            flash(f'Documento entrante registrado correctamente con radicado {radicado}', 'success')
            # Redirigir a la misma página para limpiar el formulario
            return redirect(url_for('documentos.registrar_entrada'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error al registrar documento entrante: {str(e)}')
            flash(f'Error al registrar el documento: {str(e)}', 'danger')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error en el campo {field}: {error}', 'danger')
    
    # Obtener documentos entrantes recientes
    documentos = Documento.query.filter_by(
        es_entrada=True,
        usuario_creacion_id=current_user.id
    ).order_by(Documento.creado_en.desc()).limit(10).all()
    
    return render_template('documentos/registrar_entrada.html',
                          title='Registrar Documento Entrante',
                          form=form,
                          areas=areas,
                          documentos=documentos)

@documentos_bp.route('/registrar-entrada-completo', methods=['GET', 'POST'])
@login_required
@permiso_requerido('puede_registrar_documentos')
def registrar_entrada_completo():
    """
    Vista completa para registrar un documento entrante
    """
    return registrar_entrada()

@documentos_bp.route('/registrar-salida', methods=['GET', 'POST'])
@login_required
@permiso_requerido('puede_registrar_documentos')
def registrar_salida():
    """
    Registrar un nuevo documento saliente
    """
    # Ya no es necesario verificar permisos aquí porque el decorador lo hace
    
    form = DocumentoSalidaForm()
    
    # Obtener todas las áreas activas para el formulario
    areas = Area.query.filter_by(activo=True).order_by(Area.nombre).all()
    
    if form.validate_on_submit():
        try:
            # Generar radicado único
            radicado = Documento.generar_radicado()
            
            # Crear el documento
            documento = Documento(
                radicado=radicado,
                fecha_recepcion=form.fecha_envio.data,
                transportadora_id=form.transportadora_id.data,
                numero_guia=form.numero_guia.data,
                remitente=form.destinatario.data,  # En salidas, el remitente es el destinatario
                tipo_documento_id=form.tipo_documento_id.data,
                contenido=form.contenido.data,
                observaciones=form.observaciones.data,
                area_actual_id=form.area_origen_id.data,
                persona_actual_id=form.persona_origen_id.data if form.persona_origen_id.data > 0 else None,
                estado_id=EstadoDocumento.query.filter_by(nombre='Finalizado').first().id,
                es_entrada=False,
                fecha_finalizacion=datetime.now(),
                usuario_creacion_id=current_user.id
            )
            
            db.session.add(documento)
            db.session.flush() # Para obtener el ID sin hacer commit aún
            
            # Registrar en el historial
            historial = HistorialMovimiento(
                documento_id=documento.id,
                fecha_movimiento=documento.fecha_recepcion,
                area_origen_id=documento.area_actual_id,
                persona_origen_id=documento.persona_actual_id,
                area_destino_id=documento.area_actual_id,
                persona_destino_id=documento.persona_actual_id,
                estado_id=documento.estado_id,
                observaciones=documento.observaciones,
                usuario_id=current_user.id
            )
            
            db.session.add(historial)
            db.session.commit()
            
            flash(f'Documento saliente registrado correctamente con radicado {radicado}', 'success')
            return redirect(url_for('documentos.registrar_salida'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error al registrar documento saliente: {str(e)}')
            flash(f'Error al registrar el documento: {str(e)}', 'danger')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error en el campo {field}: {error}', 'danger')
    
    # Obtener documentos salientes recientes
    documentos = Documento.query.filter_by(
        es_entrada=False,
        usuario_creacion_id=current_user.id
    ).order_by(Documento.creado_en.desc()).limit(10).all()
    
    return render_template('documentos/registrar_salida.html',
                          title='Registrar Documento Saliente',
                          form=form,
                          areas=areas,
                          documentos=documentos)

@documentos_bp.route('/registrar-salida-completo', methods=['GET', 'POST'])
@login_required
@permiso_requerido('puede_registrar_documentos')
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
    form = TransferenciaDocumentoForm()
    
    # Obtener todas las áreas activas para posibles mensajes de error
    areas = Area.query.filter_by(activo=True).order_by(Area.nombre).all()
    
    if form.validate_on_submit():
        documento_id = form.documento_id.data
        documento = Documento.query.get_or_404(documento_id)
        
        # Verificar permisos
        if not current_user.is_superadmin() and documento.area_actual_id != current_user.persona.area_id:
            flash('No tienes permisos para transferir este documento', 'danger')
            return redirect(url_for('documentos.detalle_documento', id=documento_id))
        
        try:
            # Guardar datos actuales para el historial
            area_origen_id = documento.area_actual_id
            persona_origen_id = documento.persona_actual_id
            
            # Actualizar documento - manejo de persona_destino_id como string vacío
            documento.area_actual_id = form.area_destino_id.data
            
            # Manejar el caso de persona_destino_id como string vacío
            if form.persona_destino_id.data and form.persona_destino_id.data != '':
                documento.persona_actual_id = int(form.persona_destino_id.data)
            else:
                documento.persona_actual_id = None
                
            documento.estado_id = form.estado_id.data
            documento.usuario_actualizacion_id = current_user.id
            documento.actualizado_en = datetime.now()
            
            # Si el estado es "Finalizado", guardar fecha de finalización
            if EstadoDocumento.query.get(form.estado_id.data).nombre == 'Finalizado':
                documento.fecha_finalizacion = datetime.now()
            
            db.session.commit()
            
            # Registrar en el historial
            historial = HistorialMovimiento(
                documento_id=documento_id,
                fecha_movimiento=datetime.now(),
                area_origen_id=area_origen_id,
                persona_origen_id=persona_origen_id,
                area_destino_id=documento.area_actual_id,
                persona_destino_id=documento.persona_actual_id,
                estado_id=documento.estado_id,
                observaciones=form.observaciones.data,
                usuario_id=current_user.id
            )
            
            db.session.add(historial)
            db.session.commit()
            
            # Crear notificación si hay persona destino
            if documento.persona_actual_id:
                from app.models.notificacion import Notificacion
                usuario_destino = Usuario.query.filter_by(persona_id=documento.persona_actual_id).first()
                if usuario_destino:
                    Notificacion.crear_notificacion_documento(
                        usuario_id=usuario_destino.id,
                        documento_id=documento.id,
                        accion="recibido" if EstadoDocumento.query.get(form.estado_id.data).nombre == 'Recibido' else "transferido"
                    )
            
            flash('Documento transferido correctamente', 'success')
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error al transferir documento: {str(e)}')
            flash(f'Error al transferir el documento: {str(e)}', 'danger')
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
    documento = Documento.query.get_or_404(id)
    
    # Verificar permisos
    if documento.persona_actual_id != current_user.persona_id:
        flash('No tienes permisos para aceptar este documento', 'danger')
        return redirect(url_for('documentos.detalle_documento', id=id))
    
    try:
        # Cambiar estado a "En proceso"
        estado_en_proceso = EstadoDocumento.query.filter_by(nombre='En proceso').first()
        
        if not estado_en_proceso:
            flash('No se encontró el estado "En proceso"', 'danger')
            return redirect(url_for('documentos.detalle_documento', id=id))
        
        # Guardar datos actuales para el historial
        area_origen_id = documento.area_actual_id
        persona_origen_id = documento.persona_actual_id
        
        # Actualizar estado
        documento.estado_id = estado_en_proceso.id
        documento.usuario_actualizacion_id = current_user.id
        documento.actualizado_en = datetime.now()
        
        db.session.commit()
        
        # Registrar en el historial
        historial = HistorialMovimiento(
            documento_id=id,
            fecha_movimiento=datetime.now(),
            area_origen_id=area_origen_id,
            persona_origen_id=persona_origen_id,
            area_destino_id=documento.area_actual_id,  # No cambia
            persona_destino_id=documento.persona_actual_id,  # No cambia
            estado_id=documento.estado_id,
            observaciones='Documento aceptado por el destinatario',
            usuario_id=current_user.id
        )
        
        db.session.add(historial)
        db.session.commit()
        
        flash('Documento aceptado correctamente', 'success')
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error al aceptar documento: {str(e)}')
        flash(f'Error al aceptar el documento: {str(e)}', 'danger')
    
    return redirect(url_for('documentos.detalle_documento', id=id))

@documentos_bp.route('/rechazar/<int:id>', methods=['POST'])
@login_required
def rechazar_documento(id):
    """
    Rechazar un documento asignado
    """
    documento = Documento.query.get_or_404(id)
    motivo = request.form.get('motivo', '')
    
    # Verificar permisos
    if documento.persona_actual_id != current_user.persona_id:
        flash('No tienes permisos para rechazar este documento', 'danger')
        return redirect(url_for('documentos.detalle_documento', id=id))
    
    if not motivo:
        flash('Debe proporcionar un motivo para rechazar el documento', 'danger')
        return redirect(url_for('documentos.detalle_documento', id=id))
    
    try:
        # Guardar datos actuales para el historial
        area_origen_id = documento.area_actual_id
        persona_origen_id = documento.persona_actual_id
        
        # Volver el documento al área de recepción o al remitente
        area_recepcion = Area.query.filter_by(nombre='RECEPCIÓN').first()
        
        if not area_recepcion:
            flash('No se encontró el área de recepción', 'danger')
            return redirect(url_for('documentos.detalle_documento', id=id))
        
        # Actualizar documento
        documento.area_actual_id = area_recepcion.id
        documento.persona_actual_id = None  # Quitar asignación personal
        documento.usuario_actualizacion_id = current_user.id
        documento.actualizado_en = datetime.now()
        
        db.session.commit()
        
        # Registrar en el historial
        historial = HistorialMovimiento(
            documento_id=id,
            fecha_movimiento=datetime.now(),
            area_origen_id=area_origen_id,
            persona_origen_id=persona_origen_id,
            area_destino_id=documento.area_actual_id,
            persona_destino_id=documento.persona_actual_id,
            estado_id=documento.estado_id,
            observaciones=f'Documento rechazado. Motivo: {motivo}',
            usuario_id=current_user.id
        )
        
        db.session.add(historial)
        db.session.commit()
        
        # Notificar al área de recepción
        from app.models.notificacion import Notificacion
        
        usuarios_recepcion = Usuario.query.join(Persona).filter(
            Persona.area_id == area_recepcion.id,
            Usuario.activo == True
        ).all()
        
        for usuario in usuarios_recepcion:
            Notificacion.crear_notificacion_documento(
                usuario_id=usuario.id,
                documento_id=documento.id,
                accion="rechazado"
            )
        
        flash('Documento rechazado correctamente', 'success')
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error al rechazar documento: {str(e)}')
        flash(f'Error al rechazar el documento: {str(e)}', 'danger')
    
    return redirect(url_for('documentos.lista_documentos'))