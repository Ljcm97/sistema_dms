import os
from app import create_app, db
from app.models.usuario import Usuario, Rol
from app.models.area import Area
from app.models.persona import Persona
from app.models.documento import Documento, Transportadora, TipoDocumento, EstadoDocumento
from app.models.historial import HistorialMovimiento
from app.models.cargo import Cargo
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    """
    Contexto para la shell interactiva
    """
    return {
        'db': db,
        'Usuario': Usuario,
        'Rol': Rol,
        'Area': Area,
        'Persona': Persona,
        'Documento': Documento,
        'Transportadora': Transportadora,
        'TipoDocumento': TipoDocumento,
        'EstadoDocumento': EstadoDocumento,
        'HistorialMovimiento': HistorialMovimiento,
        'Cargo': Cargo
    }

@app.cli.command("create-superadmin")
def create_superadmin():
    """
    Comando para crear un superadministrador
    """
    from getpass import getpass
    
    print("Creación del usuario superadministrador")
    
    # Verificar si ya existe un superadmin
    role = Rol.query.filter_by(es_superadmin=True).first()
    if not role:
        print("Error: No existe un rol de superadministrador en la base de datos.")
        return
    
    # Solicitar datos
    username = input("Nombre de usuario: ")
    password = getpass("Contraseña: ")
    confirm_password = getpass("Confirmar contraseña: ")
    
    if password != confirm_password:
        print("Error: Las contraseñas no coinciden.")
        return
    
    # Verificar si el usuario ya existe
    if Usuario.query.filter_by(username=username).first():
        print(f"Error: El usuario {username} ya existe.")
        return
    
    # Verificar si existe el área de Sistemas
    area = Area.query.filter_by(nombre='SISTEMAS').first()
    if not area:
        print("Error: No existe el área de SISTEMAS en la base de datos.")
        return
    
    # Crear persona para el usuario
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    email = input("Email: ")
    
    persona = Persona(
        nombre=nombre,
        apellido=apellido,
        email=email,
        area_id=area.id,
        activo=True
    )
    
    db.session.add(persona)
    db.session.commit()
    
    # Crear el usuario superadmin
    usuario = Usuario(
        username=username,
        persona_id=persona.id,
        rol_id=role.id,
        activo=True
    )
    usuario.password = password
    
    db.session.add(usuario)
    db.session.commit()
    
    print(f"Usuario superadministrador {username} creado correctamente.")

@app.cli.command("init-db")
def init_db():
    """
    Comando para inicializar la base de datos con datos básicos
    """
    # Crear roles si no existen
    if Rol.query.count() == 0:
        print("Creando roles...")
        roles = [
            {'nombre': 'Superadministrador', 'descripcion': 'Control total del sistema', 'es_superadmin': True},
            {'nombre': 'Usuario', 'descripcion': 'Acceso limitado a visualización de documentos', 'es_superadmin': False}
        ]
        
        for r in roles:
            rol = Rol(nombre=r['nombre'], descripcion=r['descripcion'], es_superadmin=r['es_superadmin'])
            db.session.add(rol)
        
        db.session.commit()
        print("Roles creados correctamente.")
    
    # Crear estados de documento si no existen
    if EstadoDocumento.query.count() == 0:
        print("Creando estados de documento...")
        estados = [
            {'nombre': 'Recibido', 'descripcion': 'Documento recibido en recepción', 'color': '#3498db'},
            {'nombre': 'En proceso', 'descripcion': 'Documento en proceso de revisión', 'color': '#f39c12'},
            {'nombre': 'Transferido', 'descripcion': 'Documento transferido a otra área', 'color': '#9b59b6'},
            {'nombre': 'Finalizado', 'descripcion': 'Proceso completado', 'color': '#2ecc71'},
            {'nombre': 'Archivado', 'descripcion': 'Documento archivado', 'color': '#7f8c8d'}
        ]
        
        for e in estados:
            estado = EstadoDocumento(nombre=e['nombre'], descripcion=e['descripcion'], color=e['color'])
            db.session.add(estado)
        
        db.session.commit()
        print("Estados de documento creados correctamente.")
    
    # Crear transportadoras si no existen
    if Transportadora.query.count() == 0:
        print("Creando transportadoras...")
        transportadoras = [
            'DEPRISA', 'SERVIENTREGA', 'ENVIA', 'COORDINADORA', 
            'SAFERBO', 'INTERRAPIDISIMO', 'AXPRESS', 'REDETRANS', 
            'TCC', '4-72', 'TRANSPRENSA', 'PORTERÍA', 
            'CERTIPOSTAL', 'ENCO EXPRES', 'X-CARGO', 'DHL EXPRESS', 
            'OPEN MARKET', 'EXPRESO BOLIVARIANO', 'MERCADOLIBRE', 'INTERSERVICE'
        ]
        
        for t in transportadoras:
            transportadora = Transportadora(nombre=t)
            db.session.add(transportadora)
        
        db.session.commit()
        print("Transportadoras creadas correctamente.")
    
    # Crear tipos de documento si no existen
    if TipoDocumento.query.count() == 0:
        print("Creando tipos de documento...")
        tipos = [
            'Facturas', 'Comprobantes', 'Contratos', 'Correspondencia', 
            'Tiquetes', 'Cotizaciones', 'Órdenes de compra', 'Remisiones',
            'Hojas de vida', 'Manuales', 'Informes'
        ]
        
        for t in tipos:
            tipo = TipoDocumento(nombre=t)
            db.session.add(tipo)
        
        db.session.commit()
        print("Tipos de documento creados correctamente.")
    
    # Crear áreas si no existen
    if Area.query.count() == 0:
        print("Creando áreas...")
        areas = [
            'GERENTE GENERAL', 'GERENTE OPERATIVO', 'GERENTE ADMINISTRATIVA Y FINANCIERA',
            'CONTRALORÍA', 'ASISTENTE ADMINISTRATIVO', 'SUPERNUMERARIO',
            'SISTEMAS', 'TESORERÍA', 'COMPRAS PADDY', 'CONTABILIDAD',
            'FLETES', 'COSTOS', 'AUDITORÍA', 'CARTERA', 'VENTAS',
            'RRHH', 'FACTURACIÓN', 'SST', 'CALIDAD', 'PRODUCCIÓN',
            'COMPRAS Y ALMACÉN', 'ARCHIVO'
        ]
        
        for a in areas:
            area = Area(nombre=a)
            db.session.add(area)
        
        db.session.commit()
        print("Áreas creadas correctamente.")
    
    # Crear cargos si no existen
    if Cargo.query.count() == 0:
        print("Creando cargos...")
        cargos = [
            'Gerente', 'Director', 'Coordinador', 'Analista',
            'Auxiliar', 'Asistente', 'Secretaria', 'Operario',
            'Técnico', 'Supervisor', 'Jefe', 'Contador',
            'Auditor', 'Desarrollador', 'Líder', 'Conductor'
        ]
        
        for c in cargos:
            cargo = Cargo(nombre=c)
            db.session.add(cargo)
        
        db.session.commit()
        print("Cargos creados correctamente.")
    
    print("Inicialización de la base de datos completada.")

if __name__ == '__main__':
    app.run(debug=True)