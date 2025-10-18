from common.constantes import *
from common.generadores import generar_id_unico_lista
from common.validaciones import validar_fecha, campos_son_validos, fecha_a_dias
from common.manejo_errores import manejar_error_inesperado
from functools import reduce

ENTIDAD_RESERVAS = "Reservas"

# Estructura: [id_reserva, id_cliente, id_departamento, fecha_ingreso_str, fecha_egreso_str, estado]
reservas = []


def comparar_fechas_string(fecha1_str, fecha2_str):
    """Compara dos fechas en formato dd/mm/yyyy. Retorna: -1, 0, o 1."""
    try:
        if not validar_fecha(fecha1_str) or not validar_fecha(fecha2_str):
            # Usamos ValueError porque el problema está en el valor/formato de la fecha.
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
    """Agrega una nueva reserva, validando la disponibilidad y los datos."""
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
    """Busca una reserva por su ID de forma eficiente."""
    try:
        return next((r for r in reservas if r[INDICE_ID_RESERVA] == id_reserva), None)
    except TypeError:
        manejar_error_inesperado(ENTIDAD_RESERVAS, "buscar reserva por ID", "El ID proporcionado no es válido.")
        return None


def buscar_reservas_por_cliente(id_cliente):
    """Busca todas las reservas de un cliente usando comprensión de listas."""
    try:
        return [r for r in reservas if r[INDICE_ID_CLIENTE] == id_cliente and r[INDICE_ESTADO] != ESTADO_ELIMINADO]
    except TypeError:
        manejar_error_inesperado(ENTIDAD_RESERVAS, "buscar reservas por cliente", "El ID de cliente no es válido.")
        return []


def buscar_reservas_por_departamento(id_departamento):
    """Busca todas las reservas de un departamento usando comprensión de listas."""
    try:
        return [r for r in reservas if
                r[INDICE_ID_DEPARTAMENTO] == id_departamento and r[INDICE_ESTADO] != ESTADO_ELIMINADO]
    except TypeError:
        manejar_error_inesperado(ENTIDAD_RESERVAS, "buscar reservas por departamento", "El ID de depto. no es válido.")
        return []


def modificar_estado_reserva(id_reserva, estado_nuevo, estado_requerido=None):
    """
    Función genérica y reutilizable para cambiar el estado de una reserva.
    Retorna True si tuvo éxito, False en caso contrario.
    """
    try:
        reserva = buscar_reserva_por_id(id_reserva)
        if not reserva:
            return False  # La reserva no existe

        # Si se requiere un estado previo (ej: para cancelar, debe estar 'ACTIVO')
        if estado_requerido and reserva[INDICE_ESTADO] != estado_requerido:
            return False

        reserva[INDICE_ESTADO] = estado_nuevo
        return True
    except (IndexError, TypeError):
        mensaje = f"No se pudo cambiar el estado a '{estado_nuevo}' por un error interno."
        manejar_error_inesperado(ENTIDAD_RESERVAS, "modificar estado de reserva", mensaje)
        return False


def cancelar_reserva(id_reserva):
    """Cancela una reserva activa."""
    return modificar_estado_reserva(id_reserva, ESTADO_CANCELADO, estado_requerido=ESTADO_ACTIVO)


def eliminar_reserva(id_reserva):
    """Baja lógica de una reserva."""
    return modificar_estado_reserva(id_reserva, ESTADO_ELIMINADO)


def reactivar_reserva(id_reserva):
    """Reactiva una reserva cancelada."""
    return modificar_estado_reserva(id_reserva, ESTADO_ACTIVO, estado_requerido=ESTADO_CANCELADO)


def actualizar_reserva(id_reserva, id_cliente=None, id_departamento=None, fecha_ingreso_str=None,
                       fecha_egreso_str=None):
    """Actualiza los datos de una reserva existente."""
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
    """Obtiene todas las reservas activas."""
    try:
        return [r for r in reservas if r[INDICE_ESTADO] == ESTADO_ACTIVO]
    except (IndexError, TypeError):
        manejar_error_inesperado(ENTIDAD_RESERVAS, "obtener reservas activas")
        return []


def obtener_todas_las_reservas():
    """Obtiene una copia de todas las reservas (incluidas las eliminadas)."""
    try:
        return reservas[:]
    except Exception:  # Aquí una excepción genérica puede estar bien como último recurso
        manejar_error_inesperado(ENTIDAD_RESERVAS, "obtener todas las reservas")
        return []


# --- Funciones para Estadísticas ---

def calcular_dias_ocupados_depto(id_departamento, periodo_dias):
    """Calcula el total de días que un depto estuvo ocupado en un periodo."""
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
    """Calcula la duración promedio en días de todas las reservas activas."""
    try:
        reservas_activas = obtener_reservas_activas()
        if not reservas_activas:
            return 0.0

        total_dias = reduce(
            lambda acumulador, reserva: acumulador + (
                        fecha_a_dias(reserva[INDICE_FECHA_EGRESO]) - fecha_a_dias(reserva[INDICE_FECHA_INGRESO])),
            reservas_activas,
            0  #valor inicial del acumulador
        )

        return float(total_dias) / len(reservas_activas)
    except (TypeError, ValueError, ZeroDivisionError):
        manejar_error_inesperado(ENTIDAD_RESERVAS, "calcular duración promedio")
        return 0.0