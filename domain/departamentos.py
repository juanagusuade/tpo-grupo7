from common.generadores import generar_id_unico_diccionario
from common.constantes import *
from common.manejo_errores import manejar_error_inesperado
from domain.reservas import reservas, comparar_fechas_string, ENTIDAD_RESERVAS

ENTIDAD_DEPARTAMENTOS = "Departamentos"

departamentos = []


def agregar_departamento(ubicacion, ambientes, capacidad, estado, precio_noche):
    """Agrega un nuevo departamento a la lista"""
    try:
        id_departamento = generar_id_unico_diccionario(departamentos, ID_DEPARTAMENTO)
        nuevo_departamento = {
            ID_DEPARTAMENTO: id_departamento,
            UBICACION_DEPARTAMENTO: ubicacion,
            AMBIENTES_DEPARTAMENTO: ambientes,
            CAPACIDAD_DEPARTAMENTO: capacidad,
            ESTADO_DEPARTAMENTO: estado,
            PRECIO_DEPARTAMENTO: precio_noche,
            ACTIVO_DEPARTAMENTO: True
        }
        departamentos.append(nuevo_departamento)
        return True
    except Exception as e:
        manejar_error_inesperado(ENTIDAD_DEPARTAMENTOS, "agregar departamento", str(e))
        return False


def eliminar_departamento(id_departamento):
    """Elimina fisicamente un departamento de la lista"""
    try:
        depto_a_eliminar = None
        for depto in departamentos:
            if depto[ID_DEPARTAMENTO] == id_departamento:
                depto_a_eliminar = depto

        if depto_a_eliminar:
            departamentos.remove(depto_a_eliminar)
            return True
        return False  # No se encontro
    except (KeyError, ValueError):
        manejar_error_inesperado(ENTIDAD_DEPARTAMENTOS, "eliminar departamento",
                                 "Error al intentar remover el depto. de la lista.")
        return False


def actualizar_departamento(id_departamento, ubicacion, ambientes, capacidad, estado, precio_noche):
    """Actualiza los datos de un departamento existente"""
    try:
        for depto in departamentos:
            if depto[ID_DEPARTAMENTO] == id_departamento:
                depto[UBICACION_DEPARTAMENTO] = ubicacion
                depto[AMBIENTES_DEPARTAMENTO] = ambientes
                depto[CAPACIDAD_DEPARTAMENTO] = capacidad
                depto[ESTADO_DEPARTAMENTO] = estado
                depto[PRECIO_DEPARTAMENTO] = precio_noche
                return True
        return False  # No se encontro
    except KeyError:
        manejar_error_inesperado(ENTIDAD_DEPARTAMENTOS, "actualizar departamento", "Datos de departamento corruptos.")
        return False


def reemplazar_departamento(id_departamento, ubicacion, ambientes, capacidad, estado, precio_noche):
    """Reemplaza completamente un departamento"""
    try:
        for i, depto in enumerate(departamentos):
            if depto[ID_DEPARTAMENTO] == id_departamento:
                departamentos[i] = {
                    ID_DEPARTAMENTO: id_departamento,
                    UBICACION_DEPARTAMENTO: ubicacion,
                    AMBIENTES_DEPARTAMENTO: ambientes,
                    CAPACIDAD_DEPARTAMENTO: capacidad,
                    ESTADO_DEPARTAMENTO: estado,
                    PRECIO_DEPARTAMENTO: precio_noche,
                    ACTIVO_DEPARTAMENTO: True
                }
                return True
        return False  # No se encontro
    except KeyError:
        manejar_error_inesperado(ENTIDAD_DEPARTAMENTOS, "reemplazar departamento", "Datos de departamento corruptos.")
        return False


def baja_logica_departamento(id_departamento):
    """Realiza baja logica de un departamento"""
    try:
        for depto in departamentos:
            if depto[ID_DEPARTAMENTO] == id_departamento:
                depto[ACTIVO_DEPARTAMENTO] = False
                return True
        return False  # No se encontro
    except KeyError:
        manejar_error_inesperado(ENTIDAD_DEPARTAMENTOS, "baja logica", "Datos de departamento corruptos.")
        return False


def alta_logica_departamento(id_departamento):
    """Da de alta logica un departamento"""
    try:
        for depto in departamentos:
            if depto[ID_DEPARTAMENTO] == id_departamento:
                depto[ACTIVO_DEPARTAMENTO] = True
                return True
        return False  # No se encontro
    except KeyError:
        manejar_error_inesperado(ENTIDAD_DEPARTAMENTOS, "alta logica", "Datos de departamento corruptos.")
        return False


def buscar_departamento_por_id(id_departamento):
    """Busca un departamento por su ID"""
    try:
        for departamento in departamentos:
            if departamento[ID_DEPARTAMENTO] == id_departamento:
                return departamento
        return None
    except KeyError:
        manejar_error_inesperado(ENTIDAD_DEPARTAMENTOS, "buscar por ID", "Datos de departamento corruptos.")
        return None


def listar_departamentos_activos():
    """Lista todos los departamentos activos"""
    try:
        return list(filter(lambda depto: depto[ACTIVO_DEPARTAMENTO], departamentos))
    except KeyError:
        manejar_error_inesperado(ENTIDAD_DEPARTAMENTOS, "listar activos", "Datos de departamento corruptos.")
        return []


def listar_departamentos_disponibles(fecha_ingreso, fecha_egreso):
    try:
        departamentos_activos = listar_departamentos_activos()

        return [
            depto for depto in departamentos_activos
            if depto[ESTADO_DEPARTAMENTO] == ESTADO_DISPONIBLE and
               verificar_disponibilidad_departamento(depto[ID_DEPARTAMENTO], fecha_ingreso, fecha_egreso)
        ]
    except KeyError:
        manejar_error_inesperado(ENTIDAD_DEPARTAMENTOS, "listar disponibles", "Datos de departamento corruptos.")
        return []


def verificar_disponibilidad_departamento(id_departamento, fecha_ingreso_str, fecha_egreso_str):
    """
    Verifica si un departamento está disponible.
    Retorna True si está disponible, False si hay solapamiento o error.
    """
    # Esta funcion ya usaba 'try-except' y 'for', esta bien.
    try:
        for r in reservas:
            if r[INDICE_ID_DEPARTAMENTO] == id_departamento and r[INDICE_ESTADO] == ESTADO_ACTIVO:
                fin_reserva_vs_inicio_nueva = comparar_fechas_string(r[INDICE_FECHA_EGRESO], fecha_ingreso_str)
                fin_nueva_vs_inicio_reserva = comparar_fechas_string(fecha_egreso_str, r[INDICE_FECHA_INGRESO])

                if fin_reserva_vs_inicio_nueva is None or fin_nueva_vs_inicio_reserva is None:
                    return False

                if not (fin_reserva_vs_inicio_nueva <= 0 or fin_nueva_vs_inicio_reserva <= 0):
                    return False

        return True
    except (TypeError, IndexError):
        manejar_error_inesperado(ENTIDAD_RESERVAS, "verificar disponibilidad")
        return False