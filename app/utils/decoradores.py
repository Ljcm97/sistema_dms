from functools import wraps
from flask import abort
from flask_login import current_user

def permiso_requerido(permiso):
    """
    Decorador para requerir un permiso específico
    
    Uso:
    @permiso_requerido('puede_registrar_documentos')
    def registrar_documento():
        # Solo accesible para usuarios con permiso
        pass
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.tiene_permiso(permiso):
                # Abortar con código 403 (Forbidden)
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def solo_superadmin(f):
    """
    Decorador para requerir permisos de superadministrador
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_superadmin():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function