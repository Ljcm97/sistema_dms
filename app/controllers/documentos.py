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
    
    # Filtrar según el rol y área del usuario
    if not current_user.is_superadmin():
        area_id = current_user.persona.area_id
        
        # Si es rol de Recepción, puede ver todos los documentos del área
        if current_user.rol.nombre == 'Recepción':
            query = query.filter_by(area_actual_id=area_id)
        else:
            # Los demás roles solo ven documentos asignados directamente a ellos
            query = query.filter(
                (Documento.area_actual_id == area_id) & 
                ((Documento.persona_actual_id == current_user.persona.id) | 
                 (Documento.persona_actual_id == None))
            )
    
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
    
    # Crear formularios para modales con valores predeterminados
    entrada_form = DocumentoEntradaForm()
    entrada_form.area_destino_id.default = current_user.persona.area_id
    entrada_form.process()  # Procesar el formulario con los valores predeterminados
    
    salida_form = DocumentoSalidaForm()
    salida_form.area_origen_id.default = current_user.persona.area_id
    salida_form.process()  # Procesar el formulario con los valores predeterminados
    
    return render_template('documentos/lista.html',
                          title='Documentos',
                          documentos=pagination.items,
                          pagination=pagination,
                          form=form,
                          entrada_form=entrada_form,
                          salida_form=salida_form)

@documentos_bp.route('/documentos/entrada', methods=['POST'])
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
                ruta_adjunto=None,
                es_entrada=True,
                usuario_creacion_id=current_user.id
            )
            
            db.session.add(documento)
            db.session.commit()
            
            # Crear historial de movimiento inicial
            movimiento = HistorialMovimiento(
                documento_id=documento.id,
                fecha_movimiento=datetime.utcnow(),
                area_origen_id=current_user.persona.area_id,
                persona_origen_id=current_user.persona.id,
                area_destino_id=form.area_destino_id.data,
                persona_destino_id=form.persona_destino_id.data if form.persona_destino_id.data != 0 else None,
                estado_id=Documento.get_estado_recibido().id,
                observaciones=form.observaciones.data,
                usuario_id=current_user.id
            )
            
            db.session.add(movimiento)
            db.session.commit()
            
            current_app.logger.info(f'Usuario {current_user.username} registró un nuevo documento entrante: {radicado}')
            flash(f'Documento {radicado} registrado correctamente', 'success')
            return redirect(url_for('documentos.lista_documentos'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error al registrar documento: {str(e)}')
            flash(f'Error al registrar el documento: {str(e)}', 'danger')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error en el campo {getattr(form, field).label.text}: {error}', 'danger')
    
    return redirect(url_for('documentos.lista_documentos'))

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
    
    # Si no es rol de Recepción, verificar si está asignado al usuario
    if not current_user.is_superadmin() and current_user.rol.nombre != 'Recepción':
        if documento.persona_actual_id and documento.persona_actual_id != current_user.persona.id:
            flash('No tienes permisos para ver este documento', 'danger')
            return redirect(url_for('documentos.lista_documentos'))
    
    # Obtener historial de movimientos
    historial = HistorialMovimiento.get_timeline(documento.id)
    
    # Formulario de transferencia
    form_transferencia = TransferenciaDocumentoForm()
    form_transferencia.documento_id.data = documento.id
    
    # Verificar si se puede transferir (solo si está en el área del usuario)
    puede_transferir = (documento.area_actual_id == current_user.persona.area_id)
    
    # Si no es rol de Recepción, solo puede transferir si está asignado a él
    if not current_user.is_superadmin() and current_user.rol.nombre != 'Recepción':
        puede_transferir = puede_transferir and (documento.persona_actual_id == current_user.persona.id or documento.persona_actual_id is None)
    
    # Verificar si se puede aceptar o rechazar (solo destinatarios)
    es_destinatario = False
    pendiente_aceptacion = False
    
    # Obtener el último movimiento
    ultimo_movimiento = HistorialMovimiento.query.filter_by(documento_id=documento.id).order_by(HistorialMovimiento.fecha_movimiento.desc()).first()
    
    if ultimo_movimiento and ultimo_movimiento.area_destino_id == current_user.persona.area_id:
        es_destinatario = True
        # Verificar si está pendiente de aceptación (no ha sido marcado como recibido)
        pendiente_aceptacion = (documento.estado_id == EstadoDocumento.query.filter_by(nombre='Transferido').first().id)
    
    return render_template('documentos/detalle.html',
                          title=f'Documento {documento.radicado}',
                          documento=documento,
                          historial=historial,
                          form_transferencia=form_transferencia,
                          puede_transferir=puede_transferir,
                          es_destinatario=es_destinatario,
                          pendiente_aceptacion=pendiente_aceptacion)

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
        
        # Si no es rol de Recepción, verificar si está asignado al usuario
        if not current_user.is_superadmin() and current_user.rol.nombre != 'Recepción':
            if documento.persona_actual_id and documento.persona_actual_id != current_user.persona.id:
                flash('No tienes permisos para transferir este documento', 'danger')
                return redirect(url_for('documentos.detalle_documento', id=documento_id))
        
        try:
            # Actualizar el documento
            documento.area_actual_id = form.area_destino_id.data
            documento.persona_actual_id = form.persona_destino_id.data if form.persona_destino_id.data != 0 else None
            documento.estado_id = form.estado_id.data
            documento.usuario_actualizacion_id = current_user.id
            
            if form.estado_id.data == Documento.get_estado_finalizado().id:
                documento.fecha_finalizacion = datetime.utcnow()
            
            # Registrar movimiento en el historial
            movimiento = HistorialMovimiento(
                documento_id=documento.id,
                fecha_movimiento=datetime.utcnow(),
                area_origen_id=current_user.persona.area_id,
                persona_origen_id=current_user.persona.id,
                area_destino_id=form.area_destino_id.data,
                persona_destino_id=form.persona_destino_id.data if form.persona_destino_id.data != 0 else None,
                estado_id=form.estado_id.data,
                observaciones=form.observaciones.data,
                usuario_id=current_user.id
            )
            
            db.session.add(movimiento)
            db.session.commit()
            
            # Crear notificaciones para las personas del área destino
            from app.models.notificacion import Notificacion
            from app.models.usuario import Usuario
            from app.models.persona import Persona
            
            # Si se especificó una persona destino, enviar notificación solo a esa persona
            if form.persona_destino_id.data and form.persona_destino_id.data != 0:
                usuarios_destino = Usuario.query.filter_by(persona_id=form.persona_destino_id.data).all()
                for usuario in usuarios_destino:
                    Notificacion.crear_notificacion_documento(usuario.id, documento.id, "recibido")
            else:
                # Si no, enviar a todos los usuarios del área destino
                personas_area = Persona.query.filter_by(area_id=form.area_destino_id.data).all()
                for persona in personas_area:
                    usuario = Usuario.query.filter_by(persona_id=persona.id).first()
                    if usuario:
                        Notificacion.crear_notificacion_documento(usuario.id, documento.id, "recibido")
            
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

@documentos_bp.route('/documentos/aceptar/<int:id>', methods=['POST'])
@login_required
def aceptar_documento(id):
    """
    Aceptar un documento transferido
    """
    documento = Documento.query.get_or_404(id)
    
    # Verificar que el documento esté en el área del usuario actual
    if documento.area_actual_id != current_user.persona.area_id:
        flash('No tienes permisos para aceptar este documento', 'danger')
        return redirect(url_for('documentos.lista_documentos'))
    
    # Si no es rol de Recepción y el documento está asignado a una persona específica
    if not current_user.is_superadmin() and current_user.rol.nombre != 'Recepción':
        if documento.persona_actual_id and documento.persona_actual_id != current_user.persona.id:
            flash('No tienes permisos para aceptar este documento', 'danger')
            return redirect(url_for('documentos.lista_documentos'))
    
    try:
        # Cambiar estado a "Recibido"
        estado_recibido = EstadoDocumento.query.filter_by(nombre='Recibido').first()
        documento.estado_id = estado_recibido.id
        documento.usuario_actualizacion_id = current_user.id
        
        # Registrar en historial
        movimiento = HistorialMovimiento(
            documento_id=documento.id,
            fecha_movimiento=datetime.utcnow(),
            area_origen_id=documento.area_actual_id,
            persona_origen_id=current_user.persona.id,
            area_destino_id=documento.area_actual_id,
            persona_destino_id=current_user.persona.id,
            estado_id=estado_recibido.id,
            observaciones='Documento aceptado',
            usuario_id=current_user.id
        )
        
        db.session.add(movimiento)
        db.session.commit()
        
        flash(f'Documento {documento.radicado} aceptado correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error al aceptar documento: {str(e)}')
        flash(f'Error al aceptar el documento: {str(e)}', 'danger')
    
    return redirect(url_for('documentos.detalle_documento', id=id))

@documentos_bp.route('/documentos/rechazar/<int:id>', methods=['POST'])
@login_required
def rechazar_documento(id):
    """
    Rechazar un documento transferido
    """
    documento = Documento.query.get_or_404(id)
    motivo = request.form.get('motivo', 'Documento rechazado')
    
    # Verificar que el documento esté en el área del usuario actual
    if documento.area_actual_id != current_user.persona.area_id:
        flash('No tienes permisos para rechazar este documento', 'danger')
        return redirect(url_for('documentos.lista_documentos'))
    
    # Si no es rol de Recepción y el documento está asignado a una persona específica
    if not current_user.is_superadmin() and current_user.rol.nombre != 'Recepción':
        if documento.persona_actual_id and documento.persona_actual_id != current_user.persona.id:
            flash('No tienes permisos para rechazar este documento', 'danger')
            return redirect(url_for('documentos.lista_documentos'))
    
    # Obtener el último movimiento para saber de dónde vino
    ultimo_movimiento = HistorialMovimiento.query.filter_by(documento_id=documento.id).order_by(HistorialMovimiento.fecha_movimiento.desc()).first()
    
    if not ultimo_movimiento or ultimo_movimiento.area_origen_id == documento.area_actual_id:
        flash('No se puede rechazar el documento porque no hay área de origen', 'danger')
        return redirect(url_for('documentos.detalle_documento', id=id))
    
    try:
        # Devolver el documento al área de origen
        documento.area_actual_id = ultimo_movimiento.area_origen_id
        documento.persona_actual_id = ultimo_movimiento.persona_origen_id
        documento.estado_id = EstadoDocumento.query.filter_by(nombre='Rechazado').first().id
        documento.usuario_actualizacion_id = current_user.id
        
        # Registrar en historial
        movimiento = HistorialMovimiento(
            documento_id=documento.id,
            fecha_movimiento=datetime.utcnow(),
            area_origen_id=current_user.persona.area_id,
            persona_origen_id=current_user.persona.id,
            area_destino_id=ultimo_movimiento.area_origen_id,
            persona_destino_id=ultimo_movimiento.persona_origen_id,
            estado_id=EstadoDocumento.query.filter_by(nombre='Rechazado').first().id,
            observaciones=f'Documento rechazado: {motivo}',
            usuario_id=current_user.id
        )
        
        db.session.add(movimiento)
        db.session.commit()
        
        flash(f'Documento {documento.radicado} rechazado y devuelto al remitente', 'success')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error al rechazar documento: {str(e)}')
        flash(f'Error al rechazar el documento: {str(e)}', 'danger')
    
    return redirect(url_for('documentos.lista_documentos'))

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

@documentos_bp.route('/documentos/salida', methods=['POST'])
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
                ruta_adjunto=None,
                es_entrada=False,
                usuario_creacion_id=current_user.id
            )
            
            db.session.add(documento)
            db.session.commit()
            
            # Crear historial de movimiento inicial
            movimiento = HistorialMovimiento(
                documento_id=documento.id,
                fecha_movimiento=datetime.utcnow(),
                area_origen_id=form.area_origen_id.data,
                persona_origen_id=form.persona_origen_id.data if form.persona_origen_id.data != 0 else None,
                area_destino_id=form.area_origen_id.data,  # En salida, el destino inicial es el mismo origen
                persona_destino_id=form.persona_origen_id.data if form.persona_origen_id.data != 0 else None,
                estado_id=Documento.get_estado_recibido().id,
                observaciones=form.observaciones.data,
                usuario_id=current_user.id
            )
            
            db.session.add(movimiento)
            db.session.commit()
            
            current_app.logger.info(f'Usuario {current_user.username} registró un nuevo documento saliente: {radicado}')
            flash(f'Documento {radicado} registrado correctamente', 'success')
            return redirect(url_for('documentos.lista_documentos'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error al registrar documento: {str(e)}')
            flash(f'Error al registrar el documento: {str(e)}', 'danger')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error en el campo {getattr(form, field).label.text}: {error}', 'danger')
    
    return redirect(url_for('documentos.lista_documentos'))