# Este archivo hace que la carpeta 'controllers' sea un paquete de Python

from app.controllers.auth import auth_bp
from app.controllers.admin import admin_bp
from app.controllers.documentos import documentos_bp
from app.controllers.reportes import reportes_bp
from app.controllers.api import api_bp