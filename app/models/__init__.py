# Este archivo hace que la carpeta 'models' sea un paquete de Python
# También facilita la importación de modelos

from app.models.usuario import Usuario, Rol
from app.models.area import Area
from app.models.persona import Persona
from app.models.documento import Documento, Transportadora, TipoDocumento, EstadoDocumento
from app.models.historial import HistorialMovimiento