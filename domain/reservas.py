import utils
from datetime import date

from utils import validar_campos, validar_fecha

# Matriz de reservas, que relaciona departamentos con clientes.
# ID Reserva (int)[0] - ID Cliente (int)[1] - ID Dpto (int)[2] - Fecha Ingreso (date)[3] - Fecha Egreso (date)[4] - Estado (str)[5]

# Indices.
ID_RESERVA = 0
ID_CLIENTE = 1
ID_DEPTO = 2
FECHA_INGRESO = 3
FECHA_EGRESO = 4
ESTADO = 5

ESTADO_ELIMINADO = "ELIMINADO"
ESTADO_ACTIVO = "ACTIVO"
ESTADO_CANCELADO = "CANCELADO"

reservas = []


def _reserva_es_visible(reserva):
    """
    Determina si una reserva debe ser visible (no eliminada logicamente).
    """
    return reserva[ESTADO] != ESTADO_ELIMINADO


def _reserva_es_activa(reserva):
    """
    Determina si una reserva esta en estado activo.
    """
    return reserva[ESTADO] == ESTADO_ACTIVO


def _reserva_es_cancelada(reserva):
    """
    Determina si una reserva esta en estado cancelado.
    """
    return reserva[ESTADO] == ESTADO_CANCELADO


def _convertir_fecha_si_es_string(fecha):
    """
    Convierte una fecha string a objeto date si es necesario.
    Si ya es un objeto date, lo devuelve tal como está.
    """
    if isinstance(fecha, str):
        if not validar_fecha(fecha):
            return None
        try:
            dia, mes, año = fecha.split('/')
            return date(int(año), int(mes), int(dia))
        except (ValueError, TypeError):
            return None
    elif isinstance(fecha, date):
        return fecha
    else:
        return None


def cargar_reserva(id_cliente, id_departamento, fecha_ingreso, fecha_egreso):
    """
    Carga una reserva y verifica que los campos ingresados son validos.
    Las fechas pueden ser strings en formato dd/mm/aaaa o objetos date.
    """
    # Convertir fechas string a objetos date si es necesario
    fecha_ingreso_obj = _convertir_fecha_si_es_string(fecha_ingreso)
    fecha_egreso_obj = _convertir_fecha_si_es_string(fecha_egreso)

    # Validar que las fechas se convirtieron correctamente
    if fecha_ingreso_obj is None or fecha_egreso_obj is None:
        return None

    # Validar que la fecha de ingreso no sea posterior a la de egreso
    if fecha_ingreso_obj >= fecha_egreso_obj:
        return None

    # Validar otros campos
    if validar_campos(id_cliente, id_departamento, fecha_ingreso_obj, fecha_egreso_obj) is False:
        return None

    id_reserva = utils.generar_id_unico(reservas)
    reservas.append([id_reserva, id_cliente, id_departamento, fecha_ingreso_obj, fecha_egreso_obj, ESTADO_ACTIVO])
    return id_reserva


def cargar_reserva_con_fechas_string(id_cliente, id_departamento, fecha_ingreso_str, fecha_egreso_str):
    """
    Versión específica que acepta solo strings de fecha y los valida explícitamente.
    """
    # Validar formato de fechas
    if not validar_fecha(fecha_ingreso_str) or not validar_fecha(fecha_egreso_str):
        return None

    return cargar_reserva(id_cliente, id_departamento, fecha_ingreso_str, fecha_egreso_str)


def buscar_reservas(id_cliente=None, id_departamento=None, incluir_canceladas=False, incluir_eliminadas=False):
    """
    Busca reservas filtrando opcionalmente por cliente y/o departamento.
    Si ambos son None, devuelve todas las reservas visibles.

    Args:
        id_cliente: ID del cliente a filtrar (opcional)
        id_departamento: ID del departamento a filtrar (opcional)
        incluir_canceladas: Si incluir reservas canceladas en el resultado
        incluir_eliminadas: Si incluir reservas eliminadas en el resultado
    """
    resultados = []
    for reserva in reservas:
        # Filtrar por eliminacion logica
        if not incluir_eliminadas and not _reserva_es_visible(reserva):
            continue

        # Filtrar por estado cancelado
        if not incluir_canceladas and _reserva_es_cancelada(reserva):
            continue

        # Filtrar por criterios de busqueda
        if (id_cliente is None or reserva[ID_CLIENTE] == id_cliente) and \
                (id_departamento is None or reserva[ID_DEPTO] == id_departamento):
            resultados.append(reserva)
    return resultados


def buscar_reserva_por_id(id_reserva, solo_activas=True, incluir_eliminadas=False):
    """
    Busca una reserva por su id.

    Args:
        id_reserva: ID de la reserva a buscar
        solo_activas: Si solo buscar reservas activas
        incluir_eliminadas: Si incluir reservas eliminadas en la busqueda
    """
    for reserva in reservas:
        if reserva[ID_RESERVA] == id_reserva:
            # Filtrar por eliminacion logica
            if not incluir_eliminadas and not _reserva_es_visible(reserva):
                continue

            # Filtrar por estado activo
            if solo_activas and not _reserva_es_activa(reserva):
                continue

            return reserva
    return None


def buscar_reserva_activa_por_id(id_reserva):
    """
    Busca una reserva por su id que este en estado ACTIVO.
    """
    return buscar_reserva_por_id(id_reserva, solo_activas=True, incluir_eliminadas=False)


def eliminar_reserva_por_id(id_reserva):
    """
    Elimina logicamente una reserva por su id.
    Solo puede eliminar reservas activas o canceladas.
    """
    reserva = buscar_reserva_por_id(id_reserva, solo_activas=False, incluir_eliminadas=False)
    if reserva is None:
        return False  # No existe la reserva o ya esta eliminada

    reserva[ESTADO] = ESTADO_ELIMINADO
    return True


def cancelar_reserva_por_id(id_reserva):
    """
    Cancela una reserva por su id.
    Solo puede cancelar reservas activas.
    """
    reserva = buscar_reserva_activa_por_id(id_reserva)
    if reserva is None:
        return False  # No existe la reserva o no esta activa

    reserva[ESTADO] = ESTADO_CANCELADO
    return True


def reactivar_reserva_por_id(id_reserva):
    """
    Reactiva una reserva cancelada.
    Solo puede reactivar reservas canceladas.
    """
    reserva = buscar_reserva_por_id(id_reserva, solo_activas=False, incluir_eliminadas=False)
    if reserva is None or not _reserva_es_cancelada(reserva):
        return False  # No existe la reserva o no esta cancelada

    reserva[ESTADO] = ESTADO_ACTIVO
    return True


def buscar_reservas_por_rango(fecha_inicio, fecha_fin, incluir_canceladas=False, incluir_eliminadas=False):
    """
    Devuelve todas las reservas que se solapen con el rango [fecha_inicio, fecha_fin].
    Las fechas pueden ser strings en formato dd/mm/aaaa o objetos Date.

    Args:
        fecha_inicio: Fecha de inicio del rango (string o date)
        fecha_fin: Fecha de fin del rango (string o date)
        incluir_canceladas: Si incluir reservas canceladas
        incluir_eliminadas: Si incluir reservas eliminadas
    """
    # Convertir fechas si son strings
    fecha_inicio_obj = _convertir_fecha_si_es_string(fecha_inicio)
    fecha_fin_obj = _convertir_fecha_si_es_string(fecha_fin)

    if fecha_inicio_obj is None or fecha_fin_obj is None:
        return []  # Fechas no validas

    if fecha_inicio_obj > fecha_fin_obj:
        return []  # Rango no valido

    resultados = []
    for reserva in reservas:
        # Filtrar por eliminacion logica
        if not incluir_eliminadas and not _reserva_es_visible(reserva):
            continue

        # Filtrar por estado cancelado
        if not incluir_canceladas and _reserva_es_cancelada(reserva):
            continue

        ingreso = reserva[FECHA_INGRESO]
        egreso = reserva[FECHA_EGRESO]
        if ingreso <= fecha_fin_obj and egreso >= fecha_inicio_obj:
            resultados.append(reserva)
    return resultados


def buscar_reservas_por_rango_string(fecha_inicio_str, fecha_fin_str, incluir_canceladas=False,
                                     incluir_eliminadas=False):
    """
    Versión especifica que acepta solo strings de fecha y los valida.
    """
    # Validar formato de fechas
    if not validar_fecha(fecha_inicio_str) or not validar_fecha(fecha_fin_str):
        return []

    return buscar_reservas_por_rango(fecha_inicio_str, fecha_fin_str, incluir_canceladas, incluir_eliminadas)


def actualizar_reserva(id_reserva, id_cliente=None, id_departamento=None, fecha_ingreso=None, fecha_egreso=None):
    """
    Actualiza los campos de una reserva existente.
    Solo actualiza los campos que se pasen como argumentos (opcionales).
    Solo puede actualizar reservas activas.
    Las fechas pueden ser strings en formato dd/mm/aaaa o objetos date.

    Returns:
        True si se actualizo correctamente
        False si la reserva no existe, no esta activa, o si algun campo es invalido.
    """
    reserva = buscar_reserva_activa_por_id(id_reserva)
    if reserva is None:
        return False  # No existe la reserva o no esta activa

    # Convertir fechas si son strings
    fecha_ingreso_obj = None
    fecha_egreso_obj = None

    if fecha_ingreso is not None:
        fecha_ingreso_obj = _convertir_fecha_si_es_string(fecha_ingreso)
        if fecha_ingreso_obj is None:
            return False  # Fecha de ingreso invalida

    if fecha_egreso is not None:
        fecha_egreso_obj = _convertir_fecha_si_es_string(fecha_egreso)
        if fecha_egreso_obj is None:
            return False  # Fecha de egreso invalida

    fecha_ingreso_final = fecha_ingreso_obj if fecha_ingreso_obj is not None else reserva[FECHA_INGRESO]
    fecha_egreso_final = fecha_egreso_obj if fecha_egreso_obj is not None else reserva[FECHA_EGRESO]

    if fecha_ingreso_final >= fecha_egreso_final:
        return False  # La fecha de ingreso debe ser anterior a la de egreso

    # Validar otros campos no Nonne si se pasan
    campos_a_validar = [c for c in (id_cliente, id_departamento, fecha_ingreso_final, fecha_egreso_final) if
                        c is not None]
    if campos_a_validar and validar_campos(*campos_a_validar) is False:
        return False

    # Actualizar los campos que se pasen
    if id_cliente is not None:
        reserva[ID_CLIENTE] = id_cliente
    if id_departamento is not None:
        reserva[ID_DEPTO] = id_departamento
    if fecha_ingreso_obj is not None:
        reserva[FECHA_INGRESO] = fecha_ingreso_obj
    if fecha_egreso_obj is not None:
        reserva[FECHA_EGRESO] = fecha_egreso_obj

    return True


def actualizar_reserva_con_fechas_string(id_reserva, id_cliente=None, id_departamento=None, fecha_ingreso_str=None,
                                         fecha_egreso_str=None):
    """
    Versión especifica que acepta solo strings de fecha y los valida.
    """
    # Validar formato de fechas si no son None.
    if fecha_ingreso_str is not None and not validar_fecha(fecha_ingreso_str):
        return False

    if fecha_egreso_str is not None and not validar_fecha(fecha_egreso_str):
        return False

    return actualizar_reserva(id_reserva, id_cliente, id_departamento, fecha_ingreso_str, fecha_egreso_str)


def obtener_reservas_activas():
    """
    Devuelve todas las reservas en estado activo.
    """
    return [reserva for reserva in reservas if _reserva_es_activa(reserva)]


def obtener_reservas_canceladas():
    """
    Devuelve todas las reservas en estado cancelado.
    """
    return [reserva for reserva in reservas if _reserva_es_cancelada(reserva)]


def obtener_estadisticas_reservas():
    """
    Devuelve un diccionario con estadisticas de las reservas.
    """
    activas = sum(1 for r in reservas if _reserva_es_activa(r))
    canceladas = sum(1 for r in reservas if _reserva_es_cancelada(r))
    eliminadas = sum(1 for r in reservas if not _reserva_es_visible(r))

    return {
        'total': len(reservas),
        'activas': activas,
        'canceladas': canceladas,
        'eliminadas': eliminadas,
        'visibles': activas + canceladas
    }
