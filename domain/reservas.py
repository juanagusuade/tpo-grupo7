import utils
from datetime import date, datetime
from utils import validar_campos, validar_fecha

# Estados de la reserva
ESTADO_ELIMINADO = "ELIMINADO"
ESTADO_ACTIVO = "ACTIVO"
ESTADO_CANCELADO = "CANCELADO"

# Matriz de reservas (cada reserva es un dict)
# {
#   "id_reserva": int,
#   "id_cliente": int,
#   "id_departamento": int,
#   "fecha_ingreso": date,
#   "fecha_egreso": date,
#   "estado": str
# }
reservas = []


def _reserva_es_visible(reserva):
    return reserva["estado"] != ESTADO_ELIMINADO


def _reserva_es_activa(reserva):
    return reserva["estado"] == ESTADO_ACTIVO


def _reserva_es_cancelada(reserva):
    return reserva["estado"] == ESTADO_CANCELADO


def _convertir_fecha_si_es_string(fecha):
    """
    Convierte una fecha string a objeto date si es necesario.
    Si ya es un objeto date, lo devuelve tal como está.
    """
    if isinstance(fecha, str):
        if not validar_fecha(fecha):
            return None
        return datetime.strptime(fecha, "%d/%m/%Y").date()
    elif isinstance(fecha, date):
        return fecha
    else:
        return None


def cargar_reserva(id_cliente, id_departamento, fecha_ingreso, fecha_egreso):
    fecha_ingreso_obj = _convertir_fecha_si_es_string(fecha_ingreso)
    fecha_egreso_obj = _convertir_fecha_si_es_string(fecha_egreso)

    if fecha_ingreso_obj is None or fecha_egreso_obj is None:
        return None
    if fecha_ingreso_obj >= fecha_egreso_obj:
        return None
    if validar_campos(id_cliente, id_departamento, fecha_ingreso_obj, fecha_egreso_obj) is False:
        return None

    id_reserva = utils.generar_id_unico(reservas)
    reservas.append({
        "id_reserva": id_reserva,
        "id_cliente": id_cliente,
        "id_departamento": id_departamento,
        "fecha_ingreso": fecha_ingreso_obj,
        "fecha_egreso": fecha_egreso_obj,
        "estado": ESTADO_ACTIVO
    })
    return id_reserva


def cargar_reserva_con_fechas_string(id_cliente, id_departamento, fecha_ingreso_str, fecha_egreso_str):
    if not validar_fecha(fecha_ingreso_str) or not validar_fecha(fecha_egreso_str):
        return None
    return cargar_reserva(id_cliente, id_departamento, fecha_ingreso_str, fecha_egreso_str)


def buscar_reservas(id_cliente=None, id_departamento=None, incluir_canceladas=False, incluir_eliminadas=False):
    resultados = []
    for reserva in reservas:
        if not incluir_eliminadas and not _reserva_es_visible(reserva):
            continue
        if not incluir_canceladas and _reserva_es_cancelada(reserva):
            continue
        if (id_cliente is None or reserva["id_cliente"] == id_cliente) and \
           (id_departamento is None or reserva["id_departamento"] == id_departamento):
            resultados.append(reserva)
    return resultados


def buscar_reserva_por_id(id_reserva, solo_activas=True, incluir_eliminadas=False):
    for reserva in reservas:
        if reserva["id_reserva"] == id_reserva:
            if not incluir_eliminadas and not _reserva_es_visible(reserva):
                continue
            if solo_activas and not _reserva_es_activa(reserva):
                continue
            return reserva
    return None


def buscar_reserva_activa_por_id(id_reserva):
    return buscar_reserva_por_id(id_reserva, solo_activas=True, incluir_eliminadas=False)


def eliminar_reserva_por_id(id_reserva):
    reserva = buscar_reserva_por_id(id_reserva, solo_activas=False, incluir_eliminadas=False)
    if reserva is None:
        return False
    reserva["estado"] = ESTADO_ELIMINADO
    return True


def cancelar_reserva_por_id(id_reserva):
    reserva = buscar_reserva_activa_por_id(id_reserva)
    if reserva is None:
        return False
    reserva["estado"] = ESTADO_CANCELADO
    return True


def reactivar_reserva_por_id(id_reserva):
    reserva = buscar_reserva_por_id(id_reserva, solo_activas=False, incluir_eliminadas=False)
    if reserva is None or not _reserva_es_cancelada(reserva):
        return False
    reserva["estado"] = ESTADO_ACTIVO
    return True


def buscar_reservas_por_rango(fecha_inicio, fecha_fin, incluir_canceladas=False, incluir_eliminadas=False):
    fecha_inicio_obj = _convertir_fecha_si_es_string(fecha_inicio)
    fecha_fin_obj = _convertir_fecha_si_es_string(fecha_fin)

    if fecha_inicio_obj is None or fecha_fin_obj is None:
        return []
    if fecha_inicio_obj > fecha_fin_obj:
        return []

    resultados = []
    for reserva in reservas:
        if not incluir_eliminadas and not _reserva_es_visible(reserva):
            continue
        if not incluir_canceladas and _reserva_es_cancelada(reserva):
            continue

        ingreso = reserva["fecha_ingreso"]
        egreso = reserva["fecha_egreso"]
        if ingreso <= fecha_fin_obj and egreso >= fecha_inicio_obj:
            resultados.append(reserva)
    return resultados


def buscar_reservas_por_rango_string(fecha_inicio_str, fecha_fin_str, incluir_canceladas=False, incluir_eliminadas=False):
    if not validar_fecha(fecha_inicio_str) or not validar_fecha(fecha_fin_str):
        return []
    return buscar_reservas_por_rango(fecha_inicio_str, fecha_fin_str, incluir_canceladas, incluir_eliminadas)


def actualizar_reserva(id_reserva, id_cliente=None, id_departamento=None, fecha_ingreso=None, fecha_egreso=None):
    reserva = buscar_reserva_activa_por_id(id_reserva)
    if reserva is None:
        return False

    fecha_ingreso_obj = _convertir_fecha_si_es_string(fecha_ingreso) if fecha_ingreso is not None else None
    fecha_egreso_obj = _convertir_fecha_si_es_string(fecha_egreso) if fecha_egreso is not None else None

    if fecha_ingreso is not None and fecha_ingreso_obj is None:
        return False
    if fecha_egreso is not None and fecha_egreso_obj is None:
        return False

    fecha_ingreso_final = fecha_ingreso_obj if fecha_ingreso_obj else reserva["fecha_ingreso"]
    fecha_egreso_final = fecha_egreso_obj if fecha_egreso_obj else reserva["fecha_egreso"]

    if fecha_ingreso_final >= fecha_egreso_final:
        return False

    campos_a_validar = [c for c in (id_cliente, id_departamento, fecha_ingreso_final, fecha_egreso_final) if c is not None]
    if campos_a_validar and validar_campos(*campos_a_validar) is False:
        return False

    if id_cliente is not None:
        reserva["id_cliente"] = id_cliente
    if id_departamento is not None:
        reserva["id_departamento"] = id_departamento
    if fecha_ingreso_obj is not None:
        reserva["fecha_ingreso"] = fecha_ingreso_obj
    if fecha_egreso_obj is not None:
        reserva["fecha_egreso"] = fecha_egreso_obj

    return True


def actualizar_reserva_con_fechas_string(id_reserva, id_cliente=None, id_departamento=None, fecha_ingreso_str=None, fecha_egreso_str=None):
    if fecha_ingreso_str is not None and not validar_fecha(fecha_ingreso_str):
        return False
    if fecha_egreso_str is not None and not validar_fecha(fecha_egreso_str):
        return False
    return actualizar_reserva(id_reserva, id_cliente, id_departamento, fecha_ingreso_str, fecha_egreso_str)


def obtener_reservas_activas():
    return [reserva for reserva in reservas if _reserva_es_activa(reserva)]


def obtener_reservas_canceladas():
    return [reserva for reserva in reservas if _reserva_es_cancelada(reserva)]


def obtener_estadisticas_reservas():
    activas = sum(1 for r in reservas if _reserva_es_activa(r))
    canceladas = sum(1 for r in reservas if _reserva_es_cancelada(r))
    eliminadas = sum(1 for r in reservas if not _reserva_es_visible(r))

    return {
        "total": len(reservas),
        "activas": activas,
        "canceladas": canceladas,
        "eliminadas": eliminadas,
        "visibles": activas + canceladas
    }
