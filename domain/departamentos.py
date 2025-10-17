from common.constantes import INDICE_ID_DEPARTAMENTO, INDICE_ESTADO, ESTADO_ACTIVO, INDICE_FECHA_EGRESO, \
    INDICE_FECHA_INGRESO
from common.generadores import generar_id_unico_diccionario
from common.constantes import *
from common.manejo_errores import manejar_error_inesperado
from domain.reservas import reservas, comparar_fechas_string, ENTIDAD_RESERVAS

departamentos = []

def agregar_departamento(ubicacion, ambientes, capacidad, estado, precio_noche):
    """Agrega un nuevo departamento a la lista"""
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


def eliminar_departamento(id_departamento):
    """Elimina fisicamente un departamento de la lista"""
    i = 0
    while i < len(departamentos):
        if departamentos[i][ID_DEPARTAMENTO] == id_departamento:
            departamentos.pop(i)
            return True
        i = i + 1
    return False


def actualizar_departamento(id_departamento, ubicacion, ambientes, capacidad, estado, precio_noche):
    """Actualiza los datos de un departamento existente"""
    i = 0
    while i < len(departamentos):
        if departamentos[i][ID_DEPARTAMENTO] == id_departamento:
            departamentos[i][UBICACION_DEPARTAMENTO] = ubicacion
            departamentos[i][AMBIENTES_DEPARTAMENTO] = ambientes
            departamentos[i][CAPACIDAD_DEPARTAMENTO] = capacidad
            departamentos[i][ESTADO_DEPARTAMENTO] = estado
            departamentos[i][PRECIO_DEPARTAMENTO] = precio_noche
            return True
        i = i + 1
    return False


def reemplazar_departamento(id_departamento, ubicacion, ambientes, capacidad, estado, precio_noche):
    """Reemplaza completamente un departamento"""
    i = 0
    while i < len(departamentos):
        if departamentos[i][ID_DEPARTAMENTO] == id_departamento:
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
        i = i + 1
    return False


def baja_logica_departamento(id_departamento):
    """Realiza baja logica de un departamento"""
    i = 0
    while i < len(departamentos):
        if departamentos[i][ID_DEPARTAMENTO] == id_departamento:
            departamentos[i][ACTIVO_DEPARTAMENTO] = False
            return True
        i = i + 1
    return False


def alta_logica_departamento(id_departamento):
    """Da de alta logica un departamento"""
    i = 0
    while i < len(departamentos):
        if departamentos[i][ID_DEPARTAMENTO] == id_departamento:
            departamentos[i][ACTIVO_DEPARTAMENTO] = True
            return True
        i = i + 1
    return False


def buscar_departamento_por_id(id_departamento):
    """Busca un departamento por su ID"""
    for departamento in departamentos:
        if departamento[ID_DEPARTAMENTO] == id_departamento:
            return departamento
    return None


def listar_departamentos_activos():
    """Lista todos los departamentos activos"""
    return [depto for depto in departamentos if depto[ACTIVO_DEPARTAMENTO]]

def listar_departamentos_disponibles(fecha_ingreso, fecha_egreso):
    departamentos_activos = listar_departamentos_activos()

    return [
        depto for depto in departamentos_activos
        if depto[ESTADO_DEPARTAMENTO] == ESTADO_DISPONIBLE and
           verificar_disponibilidad_departamento(depto[ID_DEPARTAMENTO], fecha_ingreso, fecha_egreso)
    ]


def verificar_disponibilidad_departamento(id_departamento, fecha_ingreso_str, fecha_egreso_str):
    """
    Verifica si un departamento está disponible.
    Retorna True si está disponible, False si hay solapamiento o error.
    """
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
