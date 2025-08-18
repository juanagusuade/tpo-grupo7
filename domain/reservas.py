import utils
from datetime import date

from utils import validar_campos

# Matriz de reservas, que relaciona departamentos con clientes.
#ID Reserva (int)[0] - ID Cliente (int)[1] - ID Dpto (int)[2] - Fecha Ingreso (date)[3] - Fecha Egreso (date)[4].

# Indices.
ID_RESERVA = 0
ID_CLIENTE = 1
ID_DEPTO = 2
FECHA_INGRESO = 3
FECHA_EGRESO = 4

reservas = []

"""
    Carga una reserva y verifica que los campos ingresados son validos.
    """
def cargar_reserva(id_cliente, id_departamento, fecha_ingreso, fecha_egreso):
    if validar_campos(id_cliente, id_departamento, fecha_ingreso, fecha_egreso) is False:
        return None #Reemplazar por excepcion cuando lo demos.
    id_reserva = utils.generar_id_unico(reservas)
    reservas.append([id_reserva, id_cliente, id_departamento, fecha_ingreso, fecha_egreso])

"""
    Busca reservas filtrando opcionalmente por cliente y/o departamento.
    Si ambos son None, devuelve todas las reservas.
    """
def buscar_reservas(id_cliente=None, id_departamento=None):
    resultados = []
    for reserva in reservas:
        if (id_cliente is None or reserva[ID_CLIENTE] == id_cliente) and \
           (id_departamento is None or reserva[ID_DEPTO] == id_departamento):
            resultados.append(reserva)
    return resultados

"""
    Busca una reserva por su id.
    """
def buscar_reserva_por_id(id_reserva):
    for reserva in reservas:
        if reserva[ID_RESERVA] == id_reserva:
            return reserva
    return None

"""
    Elimina una reserva por su id.
    """
def eliminar_reserva_por_id(id_reserva):
    global reservas
    reservas = [reserva for reserva in reservas if reserva[ID_RESERVA] != id_reserva]

"""
    Devuelve todas las reservas que se solapen con el rango [fecha_inicio, fecha_fin].
    """
def buscar_reservas_por_rango(fecha_inicio, fecha_fin):
    resultados = []
    for reserva in reservas:
        ingreso = reserva[FECHA_INGRESO]
        egreso = reserva[FECHA_EGRESO]
        if ingreso <= fecha_fin and egreso >= fecha_inicio:
            resultados.append(reserva)
    return resultados

"""
    Actualiza los campos de una reserva existente.
    Solo actualiza los campos que se pasen como argumentos (opcionales).
    Retorna True si se actualizo correctamente, None si la reserva no existe
    o si algún campo invalido fue pasado.
    """
def actualizar_reserva(id_reserva, id_cliente=None, id_departamento=None, fecha_ingreso=None, fecha_egreso=None):
    reserva = buscar_reserva_por_id(id_reserva) # Busca por referencia
    if reserva is None:
        return None  # No existe la reserva

    # Validar campos no nulos si se pasan
    campos_a_validar = [c for c in (id_cliente, id_departamento, fecha_ingreso, fecha_egreso) if c is not None]
    if campos_a_validar and validar_campos(*campos_a_validar) is None:
        return None  # Algún campo inválido

    # Actualizar los campos que se pasen
    if id_cliente is not None:
        reserva[ID_CLIENTE] = id_cliente
    if id_departamento is not None:
        reserva[ID_DEPTO] = id_departamento
    if fecha_ingreso is not None:
        reserva[FECHA_INGRESO] = fecha_ingreso
    if fecha_egreso is not None:
        reserva[FECHA_EGRESO] = fecha_egreso

    return True