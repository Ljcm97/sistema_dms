from flask import Blueprint, jsonify, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models.documento import Documento, EstadoDocumento
from app.models.area import Area
from app.models.persona import Persona
from app.models.historial import HistorialMovimiento
from sqlalchemy import func
from datetime import datetime, timedelta
import json

# Crear blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/documentos/pendientes')
@login_required
def documentos_pendientes():
    """
    API para obtener documentos pendientes del área del usuario
    """
    try:
        area_id = current_user.persona.area_id
        
        # Si no es superadmin, mostrar solo documentos del área del usuario
        if not current_user.is_superadmin():
            query = Documento.query.filter_by(area_actual_id=area_id)
        else:
            # Si es superadmin y se especifica un área, filtrar por esa área
            area_id = request.args.get('area_id', 0, type=int)
            if area_id > 0:
                query = Documento.query.filter_by(area_actual_id=area_id)
            else:
                query = Documento.query
        
        # Filtrar por documentos no finalizados
        query = query.filter(
            Documento.estado_id != EstadoDocumento.query.filter_by(nombre='Finalizado').first().id
        )
        
        # Ordenar por fecha de recepción descendente
        query = query.order_by(Documento.fecha_recepcion.desc())
        
        # Limitar resultados
        documentos = query.limit(10).all()
        
        # Convertir a diccionario
        resultado = []
        for doc in documentos:
            resultado.append({
                'id': doc.id,
                'radicado': doc.radicado,
                'fecha_recepcion': doc.fecha_recepcion.strftime('%Y-%m-%d %H:%M'),
                'remitente': doc.remitente,
                'tipo_documento': doc.tipo_documento.nombre,
                'estado': doc.estado.nombre,
                'area_actual': doc.area_actual.nombre,
                'persona_actual': doc.persona_actual.nombre_completo if doc.persona_actual else None,
                'url': f'/documentos/{doc.id}'
            })
        
        return jsonify({
            'status': 'success',
            'data': resultado
        })
    
    except Exception as e:
        current_app.logger.error(f'Error en API documentos pendientes: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@api_bp.route('/estadisticas/dashboard')
@login_required
def estadisticas_dashboard():
    """
    API para obtener estadísticas para el dashboard
    """
    try:
        # Si no es superadmin, mostrar solo estadísticas del área del usuario
        if not current_user.is_superadmin():
            area_id = current_user.persona.area_id
        else:
            # Si es superadmin y se especifica un área, filtrar por esa área
            area_id = request.args.get('area_id', 0, type=int)
        
        # Resultados
        resultado = {}
        
        # Si se seleccionó un área específica
        if area_id > 0:
            # Documentos pendientes en el área
            pendientes = Documento.query.filter_by(area_actual_id=area_id).filter(
                Documento.estado_id != EstadoDocumento.query.filter_by(nombre='Finalizado').first().id
            ).count()
            
            # Documentos finalizados en el área
            finalizados = Documento.query.filter_by(
                area_actual_id=area_id,
                estado_id=EstadoDocumento.query.filter_by(nombre='Finalizado').first().id
            ).count()
            
            # Documentos por estado en el área
            estados = db.session.query(
                EstadoDocumento.nombre,
                func.count(Documento.id)
            ).join(
                Documento, EstadoDocumento.id == Documento.estado_id
            ).filter(
                Documento.area_actual_id == area_id
            ).group_by(
                EstadoDocumento.nombre
            ).all()
            
            resultado = {
                'area': Area.query.get(area_id).nombre,
                'pendientes': pendientes,
                'finalizados': finalizados,
                'por_estado': {estado: count for estado, count in estados}
            }
        else:
            # Estadísticas globales
            
            # Total de documentos
            total = Documento.query.count()
            
            # Documentos por área
            por_area = db.session.query(
                Area.nombre,
                func.count(Documento.id)
            ).join(
                Documento, Area.id == Documento.area_actual_id
            ).group_by(
                Area.nombre
            ).all()
            
            # Documentos por estado
            por_estado = db.session.query(
                EstadoDocumento.nombre,
                func.count(Documento.id)
            ).join(
                Documento, EstadoDocumento.id == Documento.estado_id
            ).group_by(
                EstadoDocumento.nombre
            ).all()
            
            # Documentos pendientes (no finalizados)
            pendientes = Documento.query.filter(
                Documento.estado_id != EstadoDocumento.query.filter_by(nombre='Finalizado').first().id
            ).count()
            
            # Documentos finalizados
            finalizados = Documento.query.filter_by(
                estado_id=EstadoDocumento.query.filter_by(nombre='Finalizado').first().id
            ).count()
            
            resultado = {
                'total': total,
                'pendientes': pendientes,
                'finalizados': finalizados,
                'por_area': {area: count for area, count in por_area},
                'por_estado': {estado: count for estado, count in por_estado}
            }
        
        return jsonify({
            'status': 'success',
            'data': resultado
        })
    
    except Exception as e:
        current_app.logger.error(f'Error en API estadísticas dashboard: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@api_bp.route('/documento/<int:id>')
@login_required
def documento_detalle(id):
    """
    API para obtener detalles de un documento
    """
    try:
        documento = Documento.query.get_or_404(id)
        
        # Verificar permisos
        if not current_user.is_superadmin() and documento.area_actual_id != current_user.persona.area_id:
            return jsonify({
                'status': 'error',
                'message': 'No tienes permisos para ver este documento'
            }), 403
        
        # Obtener historial de movimientos
        historial = HistorialMovimiento.get_timeline(documento.id)
        historial_data = []
        
        for mov in historial:
            historial_data.append({
                'fecha': mov.fecha_movimiento.strftime('%Y-%m-%d %H:%M'),
                'area_origen': mov.area_origen.nombre,
                'persona_origen': mov.persona_origen.nombre_completo if mov.persona_origen else None,
                'area_destino': mov.area_destino.nombre,
                'persona_destino': mov.persona_destino.nombre_completo if mov.persona_destino else None,
                'estado': mov.estado.nombre,
                'observaciones': mov.observaciones,
                'usuario': mov.usuario.username
            })
        
        # Datos del documento
        doc_data = {
            'id': documento.id,
            'radicado': documento.radicado,
            'fecha_recepcion': documento.fecha_recepcion.strftime('%Y-%m-%d %H:%M'),
            'transportadora': documento.transportadora.nombre if documento.transportadora else None,
            'numero_guia': documento.numero_guia,
            'remitente': documento.remitente,
            'tipo_documento': documento.tipo_documento.nombre,
            'contenido': documento.contenido,
            'observaciones': documento.observaciones,
            'area_actual': documento.area_actual.nombre,
            'persona_actual': documento.persona_actual.nombre_completo if documento.persona_actual else None,
            'estado': documento.estado.nombre,
            'estado_color': documento.estado.color,
            'ruta_adjunto': documento.ruta_adjunto,
            'es_entrada': documento.es_entrada,
            'fecha_finalizacion': documento.fecha_finalizacion.strftime('%Y-%m-%d %H:%M') if documento.fecha_finalizacion else None,
            'creado_por': documento.creador.username,
            'actualizado_por': documento.actualizador.username if documento.actualizador else None,
            'creado_en': documento.creado_en.strftime('%Y-%m-%d %H:%M'),
            'actualizado_en': documento.actualizado_en.strftime('%Y-%m-%d %H:%M') if documento.actualizado_en else None,
            'historial': historial_data
        }
        
        return jsonify({
            'status': 'success',
            'data': doc_data
        })
    
    except Exception as e:
        current_app.logger.error(f'Error en API documento detalle: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@api_bp.route('/buscar-documentos')
@login_required
def buscar_documentos():
    """
    API para búsqueda de documentos
    """
    try:
        # Parámetros de búsqueda
        termino = request.args.get('termino', '').strip()
        
        if not termino:
            return jsonify({
                'status': 'error',
                'message': 'Se requiere un término de búsqueda'
            }), 400
        
        # Si no es superadmin, buscar solo en documentos del área del usuario
        if not current_user.is_superadmin():
            query = Documento.query.filter_by(area_actual_id=current_user.persona.area_id)
        else:
            query = Documento.query
        
        # Buscar en radicado, remitente o número de guía
        query = query.filter(
            (Documento.radicado.like(f'%{termino}%')) |
            (Documento.remitente.like(f'%{termino}%')) |
            (Documento.numero_guia.like(f'%{termino}%'))
        )
        
        # Limitar resultados
        documentos = query.limit(20).all()
        
        # Convertir a diccionario
        resultado = []
        for doc in documentos:
            resultado.append({
                'id': doc.id,
                'radicado': doc.radicado,
                'fecha_recepcion': doc.fecha_recepcion.strftime('%Y-%m-%d %H:%M'),
                'remitente': doc.remitente,
                'tipo_documento': doc.tipo_documento.nombre,
                'estado': doc.estado.nombre,
                'area_actual': doc.area_actual.nombre,
                'url': f'/documentos/{doc.id}'
            })
        
        return jsonify({
            'status': 'success',
            'data': resultado
        })
    
    except Exception as e:
        current_app.logger.error(f'Error en API buscar documentos: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@api_bp.route('/notificaciones')
@login_required
def notificaciones():
    """
    API para obtener notificaciones de documentos recién llegados al área
    """
    try:
        # Obtener documentos recibidos en el área del usuario en las últimas 24 horas
        area_id = current_user.persona.area_id
        desde = datetime.now() - timedelta(hours=24)
        
        # Buscar movimientos donde el área de destino sea la del usuario actual
        movimientos = HistorialMovimiento.query.filter(
            HistorialMovimiento.area_destino_id == area_id,
            HistorialMovimiento.fecha_movimiento >= desde
        ).order_by(
            HistorialMovimiento.fecha_movimiento.desc()
        ).all()
        
        # Agrupar por documento para evitar duplicados
        documentos_ids = set()
        resultado = []
        
        for mov in movimientos:
            if mov.documento_id not in documentos_ids:
                documentos_ids.add(mov.documento_id)
                doc = Documento.query.get(mov.documento_id)
                
                resultado.append({
                    'id': doc.id,
                    'radicado': doc.radicado,
                    'fecha_recepcion': mov.fecha_movimiento.strftime('%Y-%m-%d %H:%M'),
                    'remitente': doc.remitente,
                    'tipo_documento': doc.tipo_documento.nombre,
                    'estado': doc.estado.nombre,
                    'url': f'/documentos/{doc.id}'
                })
        
        return jsonify({
            'status': 'success',
            'data': resultado
        })
    
    except Exception as e:
        current_app.logger.error(f'Error en API notificaciones: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500