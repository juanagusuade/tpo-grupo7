	# Constantes para claves de diccionarios y matrices

# =============+- CLIENTES -+============= #

ID_CLIENTE = "id"
NOMBRE_CLIENTE = "nombre"
APELLIDO_CLIENTE = "apellido"
DNI_CLIENTE = "dni"
TELEFONO_CLIENTE = "telefono"
ACTIVO_CLIENTE = "activo"

# =============+- DEPARTAMENTOS -+============= #

ID_DEPARTAMENTO = "id"
UBICACION_DEPARTAMENTO = "ubicacion"
AMBIENTES_DEPARTAMENTO = "ambientes"
CAPACIDAD_DEPARTAMENTO = "capacidad"
ESTADO_DEPARTAMENTO = "estado"
PRECIO_DEPARTAMENTO = "precio_noche"
ACTIVO_DEPARTAMENTO = "activo"

# Estados de departamento
ESTADO_DISPONIBLE = "Disponible"
ESTADO_OCUPADO = "Ocupado"
ESTADO_MANTENIMIENTO = "Mantenimiento"

# =============+- RESERVAS -+============= #

INDICE_ID_RESERVA = 0
INDICE_ID_CLIENTE = 1
INDICE_ID_DEPARTAMENTO = 2
INDICE_FECHA_INGRESO = 3
INDICE_FECHA_EGRESO = 4
INDICE_ESTADO = 5

# Estados de reservas
ESTADO_ACTIVO = "ACTIVO"
ESTADO_CANCELADO = "CANCELADO"
ESTADO_ELIMINADO = "ELIMINADO"

# =============+- UI -+============= #

# Colores para CLI
COLOR_RESET = "\033[0m"
COLOR_AZUL = "\033[94m"
COLOR_VERDE = "\033[92m"
COLOR_AMARILLO = "\033[93m"
COLOR_ROJO = "\033[91m"
COLOR_MAGENTA = "\033[95m"
COLOR_CYAN = "\033[96m"

# Rayas y decoraciones
LINEA_GRUESA = "="
LINEA_FINA = "-"
FLECHA = "▶"
MARCA_OK = "✓"
MARCA_ERROR = "✗"

# =============+- AUTENTICACION -+============= #

# Tupla de tuplas para almacenar usuarios validos (usuario, contrasenia)
USUARIOS = (
    ("admin", "admin123"),
    ("user", "user123"),
    ("test", "test")
)

