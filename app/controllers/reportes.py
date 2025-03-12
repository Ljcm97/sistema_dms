from flask import Blueprint, render_template, request, jsonify, current_app, send_file, make_response
from flask_login import login_required, current_user
from app import db
from app.models.documento import Documento, Transportadora, TipoDocumento, EstadoDocumento
from app.models.area import Area
from app.models.historial import HistorialMovimiento
from sqlalchemy import func, desc, and_, or_
from datetime import datetime, timedelta
import io
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import seaborn as sns
import numpy as np
import tempfile

# Crear blueprint
reportes_bp = Blueprint('reportes', __name__, url_prefix='/reportes')

@reportes_bp.route('/')
@login_required
def index():
    """
    Página principal de reportes
    """
    # Obtener datos para los filtros
    areas = Area.query.filter_by(activo=True).order_by(Area.nombre).all()
    tipos_documento = TipoDocumento.query.filter_by(activo=True).order_by(TipoDocumento.nombre).all()
    estados = EstadoDocumento.query.order_by(EstadoDocumento.nombre).all()
    
    return render_template('reportes/index.html',
                          title='Reportes',
                          areas=areas,
                          tipos_documento=tipos_documento,
                          estados=estados)

@reportes_bp.route('/documentos-por-area')
@login_required
def documentos_por_area():
    """
    Reporte de documentos por área
    """
    # Período de tiempo
    fecha_desde = request.args.get('fecha_desde', 
                                  (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
    fecha_hasta = request.args.get('fecha_hasta', 
                                  datetime.now().strftime('%Y-%m-%d'))
    
    # Convertir a datetime
    fecha_desde = datetime.strptime(fecha_desde, '%Y-%m-%d')
    fecha_hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d') + timedelta(days=1)  # Incluir el día completo
    
    # Consulta para documentos por área
    query = db.session.query(
        Area.nombre.label('area'),
        func.count(Documento.id).label('cantidad')
    ).join(
        Documento, Area.id == Documento.area_actual_id
    ).filter(
        Documento.fecha_recepcion >= fecha_desde,
        Documento.fecha_recepcion < fecha_hasta
    ).group_by(
        Area.nombre
    ).order_by(
        desc('cantidad')
    )
    
    # Ejecutar la consulta
    resultados = query.all()
    
    # Convertir a diccionario para la plantilla
    datos = [{'area': r.area, 'cantidad': r.cantidad} for r in resultados]
    
    return render_template('reportes/documentos_por_area.html',
                          title='Documentos por Área',
                          datos=datos,
                          fecha_desde=fecha_desde.strftime('%Y-%m-%d'),
                          fecha_hasta=(fecha_hasta - timedelta(days=1)).strftime('%Y-%m-%d'))

@reportes_bp.route('/documentos-por-estado')
@login_required
def documentos_por_estado():
    """
    Reporte de documentos por estado
    """
    # Período de tiempo
    fecha_desde = request.args.get('fecha_desde', 
                                  (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
    fecha_hasta = request.args.get('fecha_hasta', 
                                  datetime.now().strftime('%Y-%m-%d'))
    
    # Convertir a datetime
    fecha_desde = datetime.strptime(fecha_desde, '%Y-%m-%d')
    fecha_hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d') + timedelta(days=1)
    
    # Filtrar por área
    area_id = request.args.get('area_id', 0, type=int)
    
    # Consulta base
    query = db.session.query(
        EstadoDocumento.nombre.label('estado'),
        EstadoDocumento.color.label('color'),
        func.count(Documento.id).label('cantidad')
    ).join(
        Documento, EstadoDocumento.id == Documento.estado_id
    ).filter(
        Documento.fecha_recepcion >= fecha_desde,
        Documento.fecha_recepcion < fecha_hasta
    )
    
    # Aplicar filtro por área si corresponde
    if area_id > 0:
        query = query.filter(Documento.area_actual_id == area_id)
    
    # Agrupar y ordenar
    query = query.group_by(
        EstadoDocumento.nombre, EstadoDocumento.color
    ).order_by(
        desc('cantidad')
    )
    
    # Ejecutar la consulta
    resultados = query.all()
    
    # Convertir a diccionario para la plantilla
    datos = [{'estado': r.estado, 'color': r.color, 'cantidad': r.cantidad} for r in resultados]
    
    # Obtener lista de áreas para el filtro
    areas = [{'id': 0, 'nombre': 'Todas'}] + [
        {'id': a.id, 'nombre': a.nombre} for a in Area.query.filter_by(activo=True).order_by(Area.nombre).all()
    ]
    
    return render_template('reportes/documentos_por_estado.html',
                          title='Documentos por Estado',
                          datos=datos,
                          fecha_desde=fecha_desde.strftime('%Y-%m-%d'),
                          fecha_hasta=(fecha_hasta - timedelta(days=1)).strftime('%Y-%m-%d'),
                          areas=areas,
                          area_id=area_id)

@reportes_bp.route('/tiempo-procesamiento')
@login_required
def tiempo_procesamiento():
    """
    Reporte de tiempo de procesamiento por área
    """
    # Período de tiempo
    fecha_desde = request.args.get('fecha_desde', 
                                  (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
    fecha_hasta = request.args.get('fecha_hasta', 
                                  datetime.now().strftime('%Y-%m-%d'))
    
    # Convertir a datetime
    fecha_desde = datetime.strptime(fecha_desde, '%Y-%m-%d')
    fecha_hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d') + timedelta(days=1)  # Incluir el día completo
    
    # Consulta personalizada para calcular el tiempo promedio de procesamiento por área
    from sqlalchemy import text
    query = text("""
    WITH movimientos_consecutivos AS (
        SELECT 
            h1.documento_id,
            h1.area_origen_id,
            a_origen.nombre AS area_origen,
            h1.fecha_movimiento AS fecha_inicio,
            MIN(h2.fecha_movimiento) AS fecha_fin
        FROM 
            historial_movimientos h1
        JOIN
            areas a_origen ON h1.area_origen_id = a_origen.id
        LEFT JOIN 
            historial_movimientos h2 ON h1.documento_id = h2.documento_id 
            AND h1.fecha_movimiento < h2.fecha_movimiento
        WHERE 
            h1.fecha_movimiento >= :fecha_desde
            AND h1.fecha_movimiento < :fecha_hasta
        GROUP BY 
            h1.id, h1.documento_id, h1.area_origen_id, a_origen.nombre, h1.fecha_movimiento
    )
    SELECT 
        area_origen,
        AVG(TIMESTAMPDIFF(HOUR, fecha_inicio, IFNULL(fecha_fin, NOW()))) AS horas_promedio,
        COUNT(documento_id) AS cantidad_documentos
    FROM 
        movimientos_consecutivos
    GROUP BY 
        area_origen
    ORDER BY 
        horas_promedio DESC
    """)
    
    # Ejecutar la consulta
    resultados = db.session.execute(query, {
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta
    }).fetchall()
    
    # Convertir a diccionario para la plantilla
    datos = [{
        'area': r.area_origen, 
        'horas_promedio': round(r.horas_promedio, 2) if r.horas_promedio else 0,
        'cantidad': r.cantidad_documentos
    } for r in resultados]
    
    return render_template('reportes/tiempo_procesamiento.html',
                          title='Tiempo de Procesamiento por Área',
                          datos=datos,
                          fecha_desde=fecha_desde.strftime('%Y-%m-%d'),
                          fecha_hasta=(fecha_hasta - timedelta(days=1)).strftime('%Y-%m-%d'))

@reportes_bp.route('/generar-grafico/<tipo>')
@login_required
def generar_grafico(tipo):
    """
    Generar gráfico para reportes
    """
    try:
        # Configurar estilo
        plt.style.use('ggplot')
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Fecha por defecto: último mes
        fecha_desde = request.args.get('fecha_desde', 
                                      (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
        fecha_hasta = request.args.get('fecha_hasta', 
                                      datetime.now().strftime('%Y-%m-%d'))
        
        # Convertir a datetime
        fecha_desde = datetime.strptime(fecha_desde, '%Y-%m-%d')
        fecha_hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d') + timedelta(days=1)
        
        # Área para filtrar
        area_id = request.args.get('area_id', 0, type=int)
        
        # Diferentes tipos de gráficos
        if tipo == 'documentos-por-area':
            # Documentos por área
            query = db.session.query(
                Area.nombre.label('area'),
                func.count(Documento.id).label('cantidad')
            ).join(
                Documento, Area.id == Documento.area_actual_id
            ).filter(
                Documento.fecha_recepcion >= fecha_desde,
                Documento.fecha_recepcion < fecha_hasta
            ).group_by(
                Area.nombre
            ).order_by(
                desc('cantidad')
            )
            
            resultados = query.all()
            
            # Crear dataframe para el gráfico
            df = pd.DataFrame([(r.area, r.cantidad) for r in resultados], 
                             columns=['Area', 'Cantidad'])
            
            # Ordenar por cantidad descendente
            df = df.sort_values('Cantidad', ascending=False)
            
            # Crear gráfico de barras
            sns.barplot(x='Cantidad', y='Area', data=df, ax=ax)
            
            # Ajustar etiquetas
            ax.set_title('Documentos por Área')
            ax.set_xlabel('Cantidad de Documentos')
            ax.set_ylabel('Área')
            
        elif tipo == 'documentos-por-estado':
            # Documentos por estado
            query = db.session.query(
                EstadoDocumento.nombre.label('estado'),
                EstadoDocumento.color.label('color'),
                func.count(Documento.id).label('cantidad')
            ).join(
                Documento, EstadoDocumento.id == Documento.estado_id
            ).filter(
                Documento.fecha_recepcion >= fecha_desde,
                Documento.fecha_recepcion < fecha_hasta
            )
            
            # Filtrar por área si es necesario
            if area_id > 0:
                query = query.filter(Documento.area_actual_id == area_id)
            
            query = query.group_by(
                EstadoDocumento.nombre, EstadoDocumento.color
            ).order_by(
                desc('cantidad')
            )
            
            resultados = query.all()
            
            # Crear dataframe
            df = pd.DataFrame([(r.estado, r.cantidad, r.color) for r in resultados], 
                             columns=['Estado', 'Cantidad', 'Color'])
            
            # Crear gráfico circular
            wedges, texts, autotexts = ax.pie(
                df['Cantidad'], 
                labels=df['Estado'],
                autopct='%1.1f%%',
                startangle=90,
                colors=df['Color'].tolist()
            )
            
            # Ajustar etiquetas
            ax.set_title('Distribución de Documentos por Estado')
            ax.axis('equal')  # Equal aspect ratio para que el pie sea circular
            
            # Mejorar legibilidad
            plt.setp(autotexts, size=9, weight="bold")
            plt.setp(texts, size=9)
            
        elif tipo == 'tiempo-procesamiento':
            # Consulta personalizada para tiempo promedio
            query = """
            WITH movimientos_consecutivos AS (
                SELECT 
                    h1.documento_id,
                    h1.area_origen_id,
                    a_origen.nombre AS area_origen,
                    h1.fecha_movimiento AS fecha_inicio,
                    MIN(h2.fecha_movimiento) AS fecha_fin
                FROM 
                    historial_movimientos h1
                JOIN
                    areas a_origen ON h1.area_origen_id = a_origen.id
                LEFT JOIN 
                    historial_movimientos h2 ON h1.documento_id = h2.documento_id 
                    AND h1.fecha_movimiento < h2.fecha_movimiento
                WHERE 
                    h1.fecha_movimiento >= :fecha_desde
                    AND h1.fecha_movimiento < :fecha_hasta
                GROUP BY 
                    h1.id, h1.documento_id, h1.area_origen_id, a_origen.nombre, h1.fecha_movimiento
            )
            SELECT 
                area_origen,
                AVG(TIMESTAMPDIFF(HOUR, fecha_inicio, IFNULL(fecha_fin, NOW()))) AS horas_promedio,
                COUNT(documento_id) AS cantidad_documentos
            FROM 
                movimientos_consecutivos
            GROUP BY 
                area_origen
            ORDER BY 
                horas_promedio DESC
            """
            
            resultados = db.session.execute(query, {
                'fecha_desde': fecha_desde,
                'fecha_hasta': fecha_hasta
            }).fetchall()
            
            # Crear dataframe
            df = pd.DataFrame([(r.area_origen, r.horas_promedio or 0) for r in resultados], 
                             columns=['Area', 'Horas'])
            
            # Ordenar por horas promedio
            df = df.sort_values('Horas', ascending=False)
            
            # Crear gráfico de barras
            sns.barplot(x='Horas', y='Area', data=df, ax=ax)
            
            # Ajustar etiquetas
            ax.set_title('Tiempo Promedio de Procesamiento por Área')
            ax.set_xlabel('Horas Promedio')
            ax.set_ylabel('Área')
            
        else:
            # Tipo de gráfico no reconocido
            return jsonify({'error': 'Tipo de gráfico no válido'}), 400
        
        # Ajustar layout
        plt.tight_layout()
        
        # Guardar gráfico en memoria
        buf = io.BytesIO()
        canvas = FigureCanvas(fig)
        canvas.print_png(buf)
        plt.close(fig)
        
        # Enviar imagen como respuesta
        response = make_response(buf.getvalue())
        response.headers['Content-Type'] = 'image/png'
        return response
    
    except Exception as e:
        current_app.logger.error(f'Error al generar gráfico: {str(e)}')
        return jsonify({'error': str(e)}), 500

@reportes_bp.route('/exportar/<tipo>')
@login_required
def exportar(tipo):
    """
    Exportar datos de reportes a Excel
    """
    try:
        # Fecha por defecto: último mes
        fecha_desde = request.args.get('fecha_desde', 
                                      (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
        fecha_hasta = request.args.get('fecha_hasta', 
                                      datetime.now().strftime('%Y-%m-%d'))
        
        # Convertir a datetime
        fecha_desde = datetime.strptime(fecha_desde, '%Y-%m-%d')
        fecha_hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d') + timedelta(days=1)
        
        # Área para filtrar
        area_id = request.args.get('area_id', 0, type=int)
        
        # Crear un escritor de Excel
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        
        # Diferentes tipos de reportes
        if tipo == 'documentos-por-area':
            # Consulta para documentos por área
            query = db.session.query(
                Area.nombre.label('area'),
                func.count(Documento.id).label('cantidad')
            ).join(
                Documento, Area.id == Documento.area_actual_id
            ).filter(
                Documento.fecha_recepcion >= fecha_desde,
                Documento.fecha_recepcion < fecha_hasta
            ).group_by(
                Area.nombre
            ).order_by(
                desc('cantidad')
            )
            
            resultados = query.all()
            df = pd.DataFrame([(r.area, r.cantidad) for r in resultados], 
                             columns=['Área', 'Cantidad de Documentos'])
            
            # Escribir a Excel
            df.to_excel(writer, sheet_name='Documentos por Área', index=False)
            filename = f'documentos_por_area_{fecha_desde.strftime("%Y%m%d")}_{fecha_hasta.strftime("%Y%m%d")}.xlsx'
            
        elif tipo == 'documentos-por-estado':
            # Consulta para documentos por estado
            query = db.session.query(
                EstadoDocumento.nombre.label('estado'),
                func.count(Documento.id).label('cantidad')
            ).join(
                Documento, EstadoDocumento.id == Documento.estado_id
            ).filter(
                Documento.fecha_recepcion >= fecha_desde,
                Documento.fecha_recepcion < fecha_hasta
            )
            
            # Filtrar por área si es necesario
            if area_id > 0:
                query = query.filter(Documento.area_actual_id == area_id)
                area_name = Area.query.get(area_id).nombre
            else:
                area_name = "Todas"
            
            query = query.group_by(
                EstadoDocumento.nombre
            ).order_by(
                desc('cantidad')
            )
            
            resultados = query.all()
            df = pd.DataFrame([(r.estado, r.cantidad) for r in resultados], 
                             columns=['Estado', 'Cantidad de Documentos'])
            
            # Escribir a Excel
            df.to_excel(writer, sheet_name='Documentos por Estado', index=False)
            filename = f'documentos_por_estado_{area_name}_{fecha_desde.strftime("%Y%m%d")}_{fecha_hasta.strftime("%Y%m%d")}.xlsx'
            
        elif tipo == 'tiempo-procesamiento':
            # Consulta para tiempo de procesamiento
            query = """
            WITH movimientos_consecutivos AS (
                SELECT 
                    h1.documento_id,
                    h1.area_origen_id,
                    a_origen.nombre AS area_origen,
                    h1.fecha_movimiento AS fecha_inicio,
                    MIN(h2.fecha_movimiento) AS fecha_fin
                FROM 
                    historial_movimientos h1
                JOIN
                    areas a_origen ON h1.area_origen_id = a_origen.id
                LEFT JOIN 
                    historial_movimientos h2 ON h1.documento_id = h2.documento_id 
                    AND h1.fecha_movimiento < h2.fecha_movimiento
                WHERE 
                    h1.fecha_movimiento >= :fecha_desde
                    AND h1.fecha_movimiento < :fecha_hasta
                GROUP BY 
                    h1.id, h1.documento_id, h1.area_origen_id, a_origen.nombre, h1.fecha_movimiento
            )
            SELECT 
                area_origen,
                AVG(TIMESTAMPDIFF(HOUR, fecha_inicio, IFNULL(fecha_fin, NOW()))) AS horas_promedio,
                COUNT(documento_id) AS cantidad_documentos
            FROM 
                movimientos_consecutivos
            GROUP BY 
                area_origen
            ORDER BY 
                horas_promedio DESC
            """
            
            resultados = db.session.execute(query, {
                'fecha_desde': fecha_desde,
                'fecha_hasta': fecha_hasta
            }).fetchall()
            
            df = pd.DataFrame([
                (r.area_origen, round(r.horas_promedio, 2) if r.horas_promedio else 0, r.cantidad_documentos) 
                for r in resultados
            ], columns=['Área', 'Horas Promedio', 'Cantidad de Documentos'])
            
            # Escribir a Excel
            df.to_excel(writer, sheet_name='Tiempo de Procesamiento', index=False)
            filename = f'tiempo_procesamiento_{fecha_desde.strftime("%Y%m%d")}_{fecha_hasta.strftime("%Y%m%d")}.xlsx'
            
        elif tipo == 'listado-documentos':
            # Consulta para listado detallado de documentos
            query = db.session.query(
                Documento.radicado,
                Documento.fecha_recepcion,
                Transportadora.nombre.label('transportadora'),
                Documento.numero_guia,
                Documento.remitente,
                TipoDocumento.nombre.label('tipo_documento'),
                Area.nombre.label('area'),
                EstadoDocumento.nombre.label('estado'),
                Documento.es_entrada,
                Documento.fecha_finalizacion
            ).outerjoin(
                Transportadora, Documento.transportadora_id == Transportadora.id
            ).join(
                TipoDocumento, Documento.tipo_documento_id == TipoDocumento.id
            ).join(
                Area, Documento.area_actual_id == Area.id
            ).join(
                EstadoDocumento, Documento.estado_id == EstadoDocumento.id
            ).filter(
                Documento.fecha_recepcion >= fecha_desde,
                Documento.fecha_recepcion < fecha_hasta
            )
            
            # Filtrar por área si es necesario
            if area_id > 0:
                query = query.filter(Documento.area_actual_id == area_id)
                area_name = Area.query.get(area_id).nombre
            else:
                area_name = "Todas"
            
            # Ordenar por fecha
            query = query.order_by(Documento.fecha_recepcion.desc())
            
            resultados = query.all()
            
            # Crear dataframe
            df = pd.DataFrame([
                (
                    r.radicado,
                    r.fecha_recepcion.strftime('%Y-%m-%d %H:%M'),
                    r.transportadora or 'N/A',
                    r.numero_guia or 'N/A',
                    r.remitente,
                    r.tipo_documento,
                    r.area,
                    r.estado,
                    'Entrada' if r.es_entrada else 'Salida',
                    r.fecha_finalizacion.strftime('%Y-%m-%d %H:%M') if r.fecha_finalizacion else 'Pendiente'
                ) for r in resultados
            ], columns=[
                'Radicado', 'Fecha', 'Transportadora', 'Guía', 'Remitente/Destinatario',
                'Tipo Documento', 'Área Actual', 'Estado', 'Tipo', 'Fecha Finalización'
            ])
            
            # Escribir a Excel
            df.to_excel(writer, sheet_name='Listado de Documentos', index=False)
            filename = f'listado_documentos_{area_name}_{fecha_desde.strftime("%Y%m%d")}_{fecha_hasta.strftime("%Y%m%d")}.xlsx'
            
        else:
            # Tipo de reporte no reconocido
            return jsonify({'error': 'Tipo de reporte no válido'}), 400
        
        # Guardar y cerrar el escritor de Excel
        writer.save()
        output.seek(0)
        
        # Enviar archivo como respuesta
        return send_file(
            output,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    
    except Exception as e:
        current_app.logger.error(f'Error al exportar datos: {str(e)}')
        return jsonify({'error': str(e)}), 500