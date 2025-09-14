from common.constantes import *
from common.generadores import generar_id_unico_lista
from common.validaciones import validar_fecha, validar_campos

# Estructura: [id_reserva, id_cliente, id_departamento, fecha_ingreso_str, fecha_egreso_str, estado]
reservas = []

def comparar_fechas_string(fecha1_str, fecha2_str):
    """
    Compara dos fechas en formato dd/mm/yyyy
    Retorna: -1 si fecha1 < fecha2, 0 si son iguales, 1 si fecha1 > fecha2
    """
    if not validar_fecha(fecha1_str) or not validar_fecha(fecha2_str):
        return None

    # Convertir a formato comparable YYYYMMDD
    partes1 = fecha1_str.split('/')
    partes2 = fecha2_str.split('/')

    fecha1_num = int(partes1[2]) * 10000 + int(partes1[1]) * 100 + int(partes1[0])
    fecha2_num = int(partes2[2]) * 10000 + int(partes2[1]) * 100 + int(partes2[0])

    if fecha1_num < fecha2_num:
        return -1
    elif fecha1_num > fecha2_num:
        return 1
    else:
        return 0


def agregar_reserva(id_cliente, id_departamento, fecha_ingreso_str, fecha_egreso_str):
    """Agrega una nueva reserva"""

    if not validar_fecha(fecha_ingreso_str) or not validar_fecha(fecha_egreso_str):
        return False

    if comparar_fechas_string(fecha_ingreso_str, fecha_egreso_str) >= 0:
        return False

    if not validar_campos(id_cliente, id_departamento):
        return False

    # Verificar disponibilidad del departamento
    if not verificar_disponibilidad_departamento(id_departamento, fecha_ingreso_str, fecha_egreso_str):
        return False

    id_reserva = generar_id_unico_lista(reservas)
    nueva_reserva = [id_reserva, id_cliente, id_departamento, fecha_ingreso_str, fecha_egreso_str, ESTADO_ACTIVO]
    reservas.append(nueva_reserva)
    return True


def verificar_disponibilidad_departamento(id_departamento, fecha_ingreso_str, fecha_egreso_str):
    """Verifica si un departamento esta disponible en el rango de fechas"""
    i = 0
    while i < len(reservas):
        reserva = reservas[i]
        if reserva[INDICE_ID_DEPARTAMENTO] == id_departamento and reserva[INDICE_ESTADO] == ESTADO_ACTIVO:
            reserva_ingreso_str = reserva[INDICE_FECHA_INGRESO]
            reserva_egreso_str = reserva[INDICE_FECHA_EGRESO]

            # Verificar solapamiento
            # TODO: Evaluar si pueden ingresar el mismo dia que un egreso (ver actualizar_reserva).
            if not (comparar_fechas_string(fecha_egreso_str, reserva_ingreso_str) <= 0 or
                    comparar_fechas_string(fecha_ingreso_str, reserva_egreso_str) >= 0):
                return False
        i = i + 1
    return True


def buscar_reserva_por_id(id_reserva):
    """Busca una reserva por su ID"""
    i = 0
    while i < len(reservas):
        if reservas[i][INDICE_ID_RESERVA] == id_reserva:
            return reservas[i]
        i = i + 1
    return None


def buscar_reservas_por_cliente(id_cliente):
    """Busca todas las reservas de un cliente"""
    reservas_cliente = []
    i = 0
    while i < len(reservas):
        reserva = reservas[i]
        if reserva[INDICE_ID_CLIENTE] == id_cliente and reserva[INDICE_ESTADO] != ESTADO_ELIMINADO:
            reservas_cliente.append(reserva)
        i = i + 1
    return reservas_cliente


def buscar_reservas_por_departamento(id_departamento):
    """Busca todas las reservas de un departamento"""
    reservas_departamento = []
    i = 0
    while i < len(reservas):
        reserva = reservas[i]
        if reserva[INDICE_ID_DEPARTAMENTO] == id_departamento and reserva[INDICE_ESTADO] != ESTADO_ELIMINADO:
            reservas_departamento.append(reserva)
        i = i + 1
    return reservas_departamento


def cancelar_reserva(id_reserva):
    """Cancela una reserva activa"""
    i = 0
    while i < len(reservas):
        reserva = reservas[i]
        if reserva[INDICE_ID_RESERVA] == id_reserva:
            if reserva[INDICE_ESTADO] == ESTADO_ACTIVO:
                reserva[INDICE_ESTADO] = ESTADO_CANCELADO
                return True
            else:
                return False  # No esta activa
        i = i + 1
    return False  # No encontrada


def eliminar_reserva(id_reserva):
    """Baja logica de una reserva"""
    i = 0
    while i < len(reservas):
        reserva = reservas[i]
        if reserva[INDICE_ID_RESERVA] == id_reserva:
            reserva[INDICE_ESTADO] = ESTADO_ELIMINADO
            return True
        i = i + 1
    return False


def reactivar_reserva(id_reserva):
    """Reactiva una reserva cancelada"""
    i = 0
    while i < len(reservas):
        reserva = reservas[i]
        if reserva[INDICE_ID_RESERVA] == id_reserva:
            if reserva[INDICE_ESTADO] == ESTADO_CANCELADO:
                reserva[INDICE_ESTADO] = ESTADO_ACTIVO
                return True
            else:
                return False  # No esta cancelada
        i = i + 1
    return False  # No encontrada


def actualizar_reserva(id_reserva, id_cliente=None, id_departamento=None, fecha_ingreso_str=None,
                       fecha_egreso_str=None):
    """Actualiza una reserva existente"""
    reserva = buscar_reserva_por_id(id_reserva)
    if not reserva or reserva[INDICE_ESTADO] != ESTADO_ACTIVO:
        return False

    # Actualizar campos si se proporcionan
    if id_cliente is not None:
        reserva[INDICE_ID_CLIENTE] = id_cliente

    if id_departamento is not None:
        reserva[INDICE_ID_DEPARTAMENTO] = id_departamento

    if fecha_ingreso_str is not None:
        if validar_fecha(fecha_ingreso_str):
            reserva[INDICE_FECHA_INGRESO] = fecha_ingreso_str
        else:
            return False

    if fecha_egreso_str is not None:
        if validar_fecha(fecha_egreso_str):
            reserva[INDICE_FECHA_EGRESO] = fecha_egreso_str
        else:
            return False

    # Verificar que fecha de ingreso sea anterior a fecha de egreso
    #TODO: Evaluar si pueden ingresar el mismo dia que un egreso.
    if comparar_fechas_string(reserva[INDICE_FECHA_INGRESO], reserva[INDICE_FECHA_EGRESO]) >= 0:
        return False

    return True


def obtener_reservas_activas():
    """Obtiene todas las reservas activas"""
    reservas_activas = []
    i = 0
    while i < len(reservas):
        reserva = reservas[i]
        if reserva[INDICE_ESTADO] == ESTADO_ACTIVO:
            reservas_activas.append(reserva)
        i = i + 1
    return reservas_activas


def obtener_reservas_canceladas():
    """Obtiene todas las reservas canceladas"""
    reservas_canceladas = []
    i = 0
    while i < len(reservas):
        reserva = reservas[i]
        if reserva[INDICE_ESTADO] == ESTADO_CANCELADO:
            reservas_canceladas.append(reserva)
        i = i + 1
    return reservas_canceladas


def obtener_estadisticas_reservas():
    """Obtiene estadisticas basicas de las reservas"""
    #TODO: Preguntar si hay que tomar mas estadisticas o con esas esetan bien.
    total = len(reservas)
    activas = 0
    canceladas = 0
    eliminadas = 0

    i = 0
    while i < len(reservas):
        estado = reservas[i][INDICE_ESTADO]
        if estado == ESTADO_ACTIVO:
            activas = activas + 1
        elif estado == ESTADO_CANCELADO:
            canceladas = canceladas + 1
        elif estado == ESTADO_ELIMINADO:
            eliminadas = eliminadas + 1
        i = i + 1

    return {
        "total": total,
        "activas": activas,
        "canceladas": canceladas,
        "eliminadas": eliminadas
    }


def reserva_existe(id_reserva):
    """Verifica si existe una reserva con el ID dado"""
    return buscar_reserva_por_id(id_reserva) is not None


def reserva_esta_activa(id_reserva):
    """Verifica si una reserva esta activa"""
    reserva = buscar_reserva_por_id(id_reserva)
    return reserva is not None and reserva[INDICE_ESTADO] == ESTADO_ACTIVO


def reserva_esta_cancelada(id_reserva):
    """Verifica si una reserva esta cancelada"""
    reserva = buscar_reserva_por_id(id_reserva)
    return reserva is not None and reserva[INDICE_ESTADO] == ESTADO_CANCELADO


def obtener_todas_las_reservas():
    """Obtiene todas las reservas (incluidas las eliminadas)"""
    return reservas[:]