from common.constantes import *
from common.generadores import generar_id_unico_lista
from common.validaciones import validar_fecha, campos_son_validos, fecha_a_dias
from common.manejo_errores import manejar_error_inesperado
from functools import reduce

ENTIDAD_RESERVAS = "Reservas"

reservas = []


def comparar_fechas_string(fecha1_str, fecha2_str):
    """
    Compara dos fechas en formato dd/mm/yyyy.
    
    Parametros:
        fecha1_str (str): Primera fecha en formato "dd/mm/aaaa"
        fecha2_str (str): Segunda fecha en formato "dd/mm/aaaa"
    
    Retorna: int:
        - -1 si fecha1 < fecha2
        - 0 si son iguales
        - 1 si fecha1 > fecha2
        - None si hay error en las fechas
    """
    try:
        if not validar_fecha(fecha1_str) or not validar_fecha(fecha2_str):
            raise ValueError("Fecha invalida o mal formateada")

        partes1 = fecha1_str.split('/')
        partes2 = fecha2_str.split('/')

        fecha1_num = int(partes1[2]) * 10000 + int(partes1[1]) * 100 + int(partes1[0])
        fecha2_num = int(partes2[2]) * 10000 + int(partes2[1]) * 100 + int(partes2[0])

        if fecha1_num < fecha2_num:
            return -1
        return 1 if fecha1_num > fecha2_num else 0
    except (ValueError, IndexError):
        mensaje = "Asegurese de que las fechas tengan el formato 'dd/mm/aaaa' y sean validas."
        manejar_error_inesperado(ENTIDAD_RESERVAS, "comparar_fechas_string", mensaje)
        return None


def agregar_reserva(id_cliente, id_departamento, fecha_ingreso_str, fecha_egreso_str):
    """
    Agrega una nueva reserva validando los datos.
    
    Parametros:
        id_cliente (int): ID del cliente que reserva
        id_departamento (int): ID del departamento a reservar
        fecha_ingreso_str (str): Fecha de ingreso en formato "dd/mm/aaaa"
        fecha_egreso_str (str): Fecha de egreso en formato "dd/mm/aaaa"
    
    Retorna:
        bool: True si se creo la reserva, False si hay error
    """
    try:
        comparacion = comparar_fechas_string(fecha_ingreso_str, fecha_egreso_str)
        if comparacion is None or not campos_son_validos(id_cliente, id_departamento) or comparacion >= 0:
            raise ValueError("Reserva con campos invalidos o fechas incorrectas.")

        id_reserva = generar_id_unico_lista(reservas)
        nueva_reserva = [id_reserva, id_cliente, id_departamento, fecha_ingreso_str, fecha_egreso_str, ESTADO_ACTIVO]
        reservas.append(nueva_reserva)
        return True
    except (ValueError, TypeError):
        mensaje = "Verifique IDs de cliente/departamento, los campos a guardar y que las fechas sean correctas."
        manejar_error_inesperado(ENTIDAD_RESERVAS, "agregar_reserva", mensaje)
        return False


def buscar_reserva_por_id(id_reserva):
    """
    Busca una reserva por su ID de forma eficiente.
    
    Parametros:
        id_reserva (int): ID de la reserva a buscar
    
    Retorna:
        list or None: Lista con los datos de la reserva si existe, None si no se encuentra
    """
    try:
        return next((r for r in reservas if r[INDICE_ID_RESERVA] == id_reserva), None)
    except TypeError:
        manejar_error_inesperado(ENTIDAD_RESERVAS, "buscar reserva por ID", "El ID proporcionado no es válido.")
        return None


def buscar_reservas_por_cliente(id_cliente):
    """
    Busca todas las reservas de un cliente usando comprension de listas.
    
    Parametros:
        id_cliente (int): ID del cliente
    
    Retorna:
        list: Lista de reservas del cliente (excluye eliminadas)
    """
    try:
        return [r for r in reservas if r[INDICE_ID_CLIENTE] == id_cliente and r[INDICE_ESTADO] != ESTADO_ELIMINADO]
    except TypeError:
        manejar_error_inesperado(ENTIDAD_RESERVAS, "buscar reservas por cliente", "El ID de cliente no es válido.")
        return []


def buscar_reservas_por_departamento(id_departamento):
    """
    Busca todas las reservas de un departamento usando comprension de listas.
    
    Parametros:
        id_departamento (int): ID del departamento
    
    Retorna:
        list: Lista de reservas del departamento (excluye eliminadas)
    """
    try:
        return [r for r in reservas if
                r[INDICE_ID_DEPARTAMENTO] == id_departamento and r[INDICE_ESTADO] != ESTADO_ELIMINADO]
    except TypeError:
        manejar_error_inesperado(ENTIDAD_RESERVAS, "buscar reservas por departamento", "El ID de depto. no es válido.")
        return []


def modificar_estado_reserva(id_reserva, estado_nuevo, estado_requerido=None):
    """
    Funcion generica y reutilizable para cambiar el estado de una reserva.
    
    Parametros:
        id_reserva (int): ID de la reserva a modificar
        estado_nuevo (str): Nuevo estado (ACTIVO, CANCELADO, ELIMINADO)
        estado_requerido (str): Estado previo requerido (opcional)
    
    Retorna:
        bool: True si tuvo exito, False si la reserva no existe o no cumple requisitos
    """
    try:
        reserva = buscar_reserva_por_id(id_reserva)
        if not reserva:
            return False

        if estado_requerido and reserva[INDICE_ESTADO] != estado_requerido:
            return False

        reserva[INDICE_ESTADO] = estado_nuevo
        return True
    except (IndexError, TypeError):
        mensaje = f"No se pudo cambiar el estado a '{estado_nuevo}' por un error interno."
        manejar_error_inesperado(ENTIDAD_RESERVAS, "modificar estado de reserva", mensaje)
        return False


def cancelar_reserva(id_reserva):
    """
    Cancela una reserva activa.
    
    Parametros:
        id_reserva (int): ID de la reserva a cancelar
    
    Retorna:
        bool: True si se cancelo correctamente, False si no esta activa o no existe
    """
    return modificar_estado_reserva(id_reserva, ESTADO_CANCELADO, estado_requerido=ESTADO_ACTIVO)


def eliminar_reserva(id_reserva):
    """
    Baja logica de una reserva.
    
    Parametros:
        id_reserva (int): ID de la reserva a eliminar
    
    Retorna:
        bool: True si se elimino correctamente, False si no existe
    """
    return modificar_estado_reserva(id_reserva, ESTADO_ELIMINADO)


def reactivar_reserva(id_reserva):
    """
    Reactiva una reserva cancelada.
    
    Parametros:
        id_reserva (int): ID de la reserva a reactivar
    
    Retorna:
        bool: True si se reactivo correctamente, False si no estaba cancelada o no existe
    """
    return modificar_estado_reserva(id_reserva, ESTADO_ACTIVO, estado_requerido=ESTADO_CANCELADO)


def actualizar_reserva(id_reserva, id_cliente=None, id_departamento=None, fecha_ingreso_str=None,
                       fecha_egreso_str=None):
    """
    Actualiza los datos de una reserva existente.
    Valida que las nuevas fechas no tengan conflictos con otras reservas.
    
    Parametros:
        id_reserva (int): ID de la reserva a actualizar
        id_cliente (int): Nuevo ID de cliente (opcional)
        id_departamento (int): Nuevo ID de departamento (opcional)
        fecha_ingreso_str (str): Nueva fecha de ingreso (opcional)
        fecha_egreso_str (str): Nueva fecha de egreso (opcional)
    
    Retorna:
        bool: True si se actualizo correctamente, False si hay error o conflicto
    """
    try:
        reserva = buscar_reserva_por_id(id_reserva)
        if not reserva or reserva[INDICE_ESTADO] != ESTADO_ACTIVO:
            return False

        fecha_ingreso_actualizada = reserva[INDICE_FECHA_INGRESO]
        fecha_egreso_actualizada = reserva[INDICE_FECHA_EGRESO]

        if fecha_ingreso_str is not None:
            if not validar_fecha(fecha_ingreso_str): return False
            fecha_ingreso_actualizada = fecha_ingreso_str

        if fecha_egreso_str is not None:
            if not validar_fecha(fecha_egreso_str): return False
            fecha_egreso_actualizada = fecha_egreso_str

        comparacion = comparar_fechas_string(fecha_ingreso_actualizada, fecha_egreso_actualizada)
        if comparacion is None or comparacion >= 0:
            return False

        if id_cliente is not None: reserva[INDICE_ID_CLIENTE] = id_cliente
        if id_departamento is not None: reserva[INDICE_ID_DEPARTAMENTO] = id_departamento
        reserva[INDICE_FECHA_INGRESO] = fecha_ingreso_actualizada
        reserva[INDICE_FECHA_EGRESO] = fecha_egreso_actualizada

        return True
    except (IndexError, TypeError, ValueError):
        mensaje = "Revise el ID de la reserva y que los nuevos datos sean válidos."
        manejar_error_inesperado(ENTIDAD_RESERVAS, "actualizar reserva", mensaje)
        return False


def obtener_reservas_activas():
    """
    Obtiene todas las reservas activas.
    
    Retorna:
        list: Lista de reservas con estado ACTIVO
    """
    try:
        return [r for r in reservas if r[INDICE_ESTADO] == ESTADO_ACTIVO]
    except (IndexError, TypeError):
        manejar_error_inesperado(ENTIDAD_RESERVAS, "obtener reservas activas")
        return []


def obtener_todas_las_reservas():
    """
    Obtiene una copia de todas las reservas (incluidas las eliminadas).
    
    Retorna:
        list: Copia de todas las reservas
    """
    try:
        return reservas[:]
    except Exception:
        manejar_error_inesperado(ENTIDAD_RESERVAS, "obtener todas las reservas")
        return []


# --- Funciones para Estadisticas ---

def calcular_porcentaje_ocupacion_depto(id_departamento, periodo_dias=365):
    """
    Calcula el porcentaje de ocupacion de un departamento en un periodo.
    
    Parametros:
        id_departamento (int): ID del departamento
        periodo_dias (int): Cantidad de dias del periodo (por defecto 365)
    
    Retorna:
        float: Porcentaje de ocupacion (0.0 a 100.0)
    """
    try:
        total_dias_ocupados = sum(
            fecha_a_dias(r[INDICE_FECHA_EGRESO]) - fecha_a_dias(r[INDICE_FECHA_INGRESO])
            for r in reservas
            if r[INDICE_ID_DEPARTAMENTO] == id_departamento and r[INDICE_ESTADO] == ESTADO_ACTIVO
        )
        
        if periodo_dias <= 0:
            return 0.0
        
        porcentaje = (float(total_dias_ocupados) / periodo_dias) * 100
        return porcentaje if porcentaje <= 100.0 else 100.0
    except (TypeError, ValueError, ZeroDivisionError):
        manejar_error_inesperado(ENTIDAD_RESERVAS, "calcular porcentaje ocupacion")
        return 0.0


def calcular_dias_ocupados_depto(id_departamento, periodo_dias):
    """
    Calcula el total de dias que un depto estuvo ocupado en un periodo.
    NOTA: Esta funcion se mantiene por compatibilidad, usar calcular_porcentaje_ocupacion_depto.
    
    Parametros:
        id_departamento (int): ID del departamento
        periodo_dias (int): Periodo en dias (no utilizado, se mantiene por compatibilidad)
    
    Retorna:
        int: Total de dias ocupados
    """
    try:
        return sum(
            fecha_a_dias(r[INDICE_FECHA_EGRESO]) - fecha_a_dias(r[INDICE_FECHA_INGRESO])
            for r in reservas
            if r[INDICE_ID_DEPARTAMENTO] == id_departamento and r[INDICE_ESTADO] == ESTADO_ACTIVO
        )
    except (TypeError, ValueError):
        manejar_error_inesperado(ENTIDAD_RESERVAS, "calcular días ocupados")
        return 0



def calcular_duracion_promedio_reservas():
    """
    Calcula la duracion promedio en dias de todas las reservas activas.
    
    Retorna:
        float: Duracion promedio en dias (0.0 si no hay reservas)
    """
    try:
        reservas_activas = obtener_reservas_activas()
        if not reservas_activas:
            return 0.0

        total_dias = reduce(
            lambda acumulador, reserva: acumulador + (
                        fecha_a_dias(reserva[INDICE_FECHA_EGRESO]) - fecha_a_dias(reserva[INDICE_FECHA_INGRESO])),
            reservas_activas,
            0
        )

        return float(total_dias) / len(reservas_activas)
    except (TypeError, ValueError):
        manejar_error_inesperado(ENTIDAD_RESERVAS, "calcular duración promedio")
        return 0.0