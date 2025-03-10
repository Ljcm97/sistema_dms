import os
import uuid
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models.documento import Documento, Transportadora, TipoDocumento, EstadoDocumento
from app.models.area import Area
from app.models.persona import Persona
from app.models.historial import HistorialMovimiento
from app.forms import DocumentoEntradaForm, DocumentoSalidaForm, TransferenciaDocumentoForm, BusquedaForm

# Crear blueprint
documentos_bp = Blueprint('documentos', __name__)

@documentos_bp.route('/')
@login_required
def dashboard():
    """
    Dashboard principal
    """
    # Obtener estadísticas
    documentos_pendientes = Documento.query.filter_by(
        area_actual_id=current_user.persona.area_id
    ).filter(
        Documento.estado_id != EstadoDocumento.query.filter_by(nombre='Finalizado').first().id
    ).count()
    
    documentos_finalizados = Documento.query.filter_by(
        area_actual_id=current_user.persona.area_id,
        estado_id=EstadoDocumento.query.filter_by(nombre='Finalizado').first().id
    ).count()
    
    # Documentos recientes en el área del usuario
    documentos_recientes = Documento.query.filter_by(
        area_actual_id=current_user.persona.area_id
    ).order_by(
        Documento.fecha_recepcion.desc()
    ).limit(5).all()
    
    # Movimientos recientes en el área del usuario
    movimientos_recientes = HistorialMovimiento.query.join(
        Documento, HistorialMovimiento.documento_id == Documento.id
    ).filter(
        (HistorialMovimiento.area_origen_id == current_user.persona.area_id) |
        (HistorialMovimiento.area_destino_id == current_user.persona.area_id)
    ).order_by(
        HistorialMovimiento.fecha_movimiento.desc()
    ).limit(5).all()
    
    return render_template('documentos/dashboard.html',
                          title='Dashboard',
                          documentos_pendientes=documentos_pendientes,
                          documentos_finalizados=documentos_finalizados,
                          documentos_recientes=documentos_recientes,
                          movimientos_recientes=movimientos_recientes)

@documentos_bp.route('/documentos')
@login_required
def lista_documentos():
    """
    Lista de documentos
    """
    page = request.args.get('page', 1, type=int)
    
    # Filtros básicos
    query = Documento.query
    
    # Si no es superadmin, mostrar solo documentos del área del usuario
    if not current_user.is_superadmin():
        query = query.filter_by(area_actual_id=current_user.persona.area_id)
    
    # Aplicar filtros de búsqueda si existen
    form = BusquedaForm(request.args, meta={'csrf': False})
    
    if form.validate():
        # Filtrar por radicado
        if form.radicado.data:
            query = query.filter(Documento.radicado.like(f'%{form.radicado.data}%'))
        
        # Filtrar por fechas
        if form.fecha_desde.data:
            query = query.filter(Documento.fecha_recepcion >= form.fecha_desde.data)
        
        if form.fecha_hasta.data:
            query = query.filter(Documento.fecha_recepcion <= form.fecha_hasta.data)
        
        # Filtrar por transportadora
        if form.transportadora_id.data and form.transportadora_id.data > 0:
            query = query.filter_by(transportadora_id=form.transportadora_id.data)
        
        # Filtrar por número de guía
        if form.numero_guia.data:
            query = query.filter(Documento.numero_guia.like(f'%{form.numero_guia.data}%'))
        
        # Filtrar por remitente
        if form.remitente.data:
            query = query.filter(Documento.remitente.like(f'%{form.remitente.data}%'))
        
        # Filtrar por tipo de documento
        if form.tipo_documento_id.data and form.tipo_documento_id.data > 0:
            query = query.filter_by(tipo_documento_id=form.tipo_documento_id.data)
        
        # Filtrar por área
        if form.area_id.data and form.area_id.data > 0:
            query = query.filter_by(area_actual_id=form.area_id.data)
        
        # Filtrar por estado
        if form.estado_id.data and form.estado_id.data > 0:
            query = query.filter_by(estado_id=form.estado_id.data)
        
        # Filtrar por tipo de documento (entrada/salida)
        if form.es_entrada.data:
            query = query.filter_by(es_entrada=(form.es_entrada.data == '1'))
    
    # Ordenar por fecha de recepción descendente
    query = query.order_by(Documento.fecha_recepcion.desc())
    
    # Paginación
    pagination = query.paginate(
        page=page, 
        per_page=current_app.config['ITEMS_PER_PAGE'],
        error_out=False
    )
    
    return render_template('documentos/lista.html',
                          title='Documentos',
                          documentos=pagination.items,
                          pagination=pagination,
                          form=form)

@documentos_bp.route('/documentos/entrada', methods=['GET', 'POST'])
@login_required
def registrar_entrada():
    """
    Registrar un nuevo documento entrante
    """
    form = DocumentoEntradaForm()
    
    if form.validate_on_submit():
        try:
            # Generar radicado
            radicado = Documento.generar_radicado()
            
            # Manejar archivo adjunto si existe
            ruta_adjunto = None
            if form.adjunto.data:
                filename = secure_filename(form.adjunto.data.filename)
                # Generar nombre único para el archivo
                unique_filename = f"{radicado}_{str(uuid.uuid4())[:8]}_{filename}"
                
                # Guardar el archivo
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
                form.adjunto.data.save(filepath)
                ruta_adjunto = unique_filename
            
            # Crear documento
            documento = Documento(
                radicado=radicado,
                fecha_recepcion=form.fecha_recepcion.data,
                transportadora_id=form.transportadora_id.data if form.transportadora_id.data != 0 else None,
                numero_guia=form.numero_guia.data,
                remitente=form.remitente.data,
                tipo_documento_id=form.tipo_documento_id.data,
                contenido=form.contenido.data,
                observaciones=form.observaciones.data,
                area_actual_id=form.area_destino_id.data,
                persona_actual_id=form.persona_destino_id.data if form.persona_destino_id.data != 0 else None,
                estado_id=Documento.get_estado_recibido().id,
                ruta_adjunto=ruta_adjunto,
                es_entrada=True,
                usuario_creacion_id=current_user.id
            )
            
            db.session.add(documento)
            db.session.commit()
            
            current_app.logger.info(f'Usuario {current_user.username} registró un nuevo documento entrante: {radicado}')
            flash(f'Documento {radicado} registrado correctamente', 'success')
            return redirect(url_for('documentos.detalle_documento', id=documento.id))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error al registrar documento: {str(e)}')
            flash(f'Error al registrar el documento: {str(e)}', 'danger')
    
    return render_template('documentos/registrar_entrada.html',
                          title='Registrar Documento Entrante',
                          form=form)

@documentos_bp.route('/documentos/salida', methods=['GET', 'POST'])
@login_required
def registrar_salida():
    """
    Registrar un nuevo documento saliente
    """
    form = DocumentoSalidaForm()
    
    if form.validate_on_submit():
        try:
            # Generar radicado
            radicado = Documento.generar_radicado()
            
            # Manejar archivo adjunto si existe
            ruta_adjunto = None
            if form.adjunto.data:
                filename = secure_filename(form.adjunto.data.filename)
                # Generar nombre único para el archivo
                unique_filename = f"{radicado}_{str(uuid.uuid4())[:8]}_{filename}"
                
                # Guardar el archivo
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
                form.adjunto.data.save(filepath)
                ruta_adjunto = unique_filename
            
            # Crear documento
            documento = Documento(
                radicado=radicado,
                fecha_recepcion=form.fecha_envio.data,
                transportadora_id=form.transportadora_id.data,
                numero_guia=form.numero_guia.data,
                remitente=form.destinatario.data,  # En salida, el remitente es el destinatario
                tipo_documento_id=form.tipo_documento_id.data,
                contenido=form.contenido.data,
                observaciones=form.observaciones.data,
                area_actual_id=form.area_origen_id.data,
                persona_actual_id=form.persona_origen_id.data if form.persona_origen_id.data != 0 else None,
                estado_id=Documento.get_estado_recibido().id,
                ruta_adjunto=ruta_adjunto,
                es_entrada=False,
                usuario_creacion_id=current_user.id
            )
            
            db.session.add(documento)
            db.session.commit()
            
            current_app.logger.info(f'Usuario {current_user.username} registró un nuevo documento saliente: {radicado}')
            flash(f'Documento {radicado} registrado correctamente', 'success')
            return redirect(url_for('documentos.detalle_documento', id=documento.id))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error al registrar documento: {str(e)}')
            flash(f'Error al registrar el documento: {str(e)}', 'danger')
    
    return render_template('documentos/registrar_salida.html',
                          title='Registrar Documento Saliente',
                          form=form)

@documentos_bp.route('/documentos/<int:id>')
@login_required
def detalle_documento(id):
    """
    Detalle de un documento
    """
    documento = Documento.query.get_or_404(id)
    
    # Verificar permisos
    if not current_user.is_superadmin() and documento.area_actual_id != current_user.persona.area_id:
        flash('No tienes permisos para ver este documento', 'danger')
        return redirect(url_for('documentos.lista_documentos'))
    
    # Obtener historial de movimientos
    historial = HistorialMovimiento.get_timeline(documento.id)
    
    # Formulario de transferencia
    form_transferencia = TransferenciaDocumentoForm()
    form_transferencia.documento_id.data = documento.id
    
    # Verificar si se puede transferir (solo si está en el área del usuario)
    puede_transferir = (documento.area_actual_id == current_user.persona.area_id)
    
    return render_template('documentos/detalle.html',
                          title=f'Documento {documento.radicado}',
                          documento=documento,
                          historial=historial,
                          form_transferencia=form_transferencia,
                          puede_transferir=puede_transferir)

@documentos_bp.route('/documentos/transferir', methods=['POST'])
@login_required
def transferir_documento():
    """
    Transferir un documento a otra área
    """
    form = TransferenciaDocumentoForm()
    
    if form.validate_on_submit():
        documento_id = form.documento_id.data
        documento = Documento.query.get_or_404(documento_id)
        
        # Verificar permisos (solo puede transferir si está en su área)
        if documento.area_actual_id != current_user.persona.area_id:
            flash('No tienes permisos para transferir este documento', 'danger')
            return redirect(url_for('documentos.detalle_documento', id=documento_id))
        
        try:
            # Transferir documento
            documento.transferir(
                area_id=form.area_destino_id.data,
                persona_id=form.persona_destino_id.data if form.persona_destino_id.data != 0 else None,
                estado_id=form.estado_id.data,
                observaciones=form.observaciones.data,
                usuario_id=current_user.id
            )
            
            current_app.logger.info(f'Usuario {current_user.username} transfirió el documento {documento.radicado}')
            flash(f'Documento {documento.radicado} transferido correctamente', 'success')
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error al transferir documento: {str(e)}')
            flash(f'Error al transferir el documento: {str(e)}', 'danger')
        
        return redirect(url_for('documentos.detalle_documento', id=documento_id))
    
    # Si hay errores en el formulario
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'Error en el campo {getattr(form, field).label.text}: {error}', 'danger')
    
    return redirect(url_for('documentos.detalle_documento', id=form.documento_id.data))

@documentos_bp.route('/documentos/adjunto/<filename>')
@login_required
def ver_adjunto(filename):
    """
    Ver/descargar archivo adjunto
    """
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

# ==== APIs ====

@documentos_bp.route('/api/personas-por-area/<int:area_id>')
@login_required
def personas_por_area(area_id):
    """
    API para obtener personas por área
    """
    personas = Persona.get_by_area(area_id)
    return jsonify([{'id': p.id, 'nombre': p.nombre_completo} for p in personas])