from common.generadores import generar_id_unico_diccionario
from common.constantes import *
from common.manejo_errores import manejar_error_inesperado

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
    except (KeyError, TypeError):
        manejar_error_inesperado("Departamentos", "agregar departamento", "Error al crear el departamento")
        return False


def eliminar_departamento(id_departamento):
    """Elimina fisicamente un departamento de la lista"""
    try:
        i = 0
        while i < len(departamentos):
            if departamentos[i][ID_DEPARTAMENTO] == id_departamento:
                departamentos.pop(i)
                return True
            i = i + 1
        return False
    except (KeyError, IndexError):
        manejar_error_inesperado("Departamentos", "eliminar departamento", "Error al eliminar de la lista")
        return False


def actualizar_departamento(id_departamento, ubicacion, ambientes, capacidad, estado, precio_noche):
    """Actualiza los datos de un departamento existente"""
    try:
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
    except (KeyError, IndexError, TypeError):
        manejar_error_inesperado("Departamentos", "actualizar departamento", "Error al modificar los datos")
        return False


def reemplazar_departamento(id_departamento, ubicacion, ambientes, capacidad, estado, precio_noche):
    """Reemplaza completamente un departamento"""
    try:
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
    except (KeyError, TypeError):
        manejar_error_inesperado("Departamentos", "reemplazar departamento", "Error al reemplazar los datos")
        return False


def baja_logica_departamento(id_departamento):
    """Realiza baja logica de un departamento"""
    try:
        i = 0
        while i < len(departamentos):
            if departamentos[i][ID_DEPARTAMENTO] == id_departamento:
                departamentos[i][ACTIVO_DEPARTAMENTO] = False
                return True
            i = i + 1
        return False
    except (KeyError, IndexError):
        manejar_error_inesperado("Departamentos", "baja logica departamento", "Error al dar de baja")
        return False


def alta_logica_departamento(id_departamento):
    """Da de alta logica un departamento"""
    try:
        i = 0
        while i < len(departamentos):
            if departamentos[i][ID_DEPARTAMENTO] == id_departamento:
                departamentos[i][ACTIVO_DEPARTAMENTO] = True
                return True
            i = i + 1
        return False
    except (KeyError, IndexError):
        manejar_error_inesperado("Departamentos", "alta logica departamento", "Error al dar de alta")
        return False


def buscar_departamento_por_id(id_departamento):
    """Busca un departamento por su ID"""
    try:
        i = 0
        while i < len(departamentos):
            if departamentos[i][ID_DEPARTAMENTO] == id_departamento:
                return departamentos[i]
            i = i + 1
        return None
    except (KeyError, IndexError):
        manejar_error_inesperado("Departamentos", "buscar departamento por ID", "Error al buscar en los datos")
        return None


def listar_departamentos_activos():
    """Lista todos los departamentos activos"""
    try:
        departamentos_activos = []
        i = 0
        while i < len(departamentos):
            if departamentos[i][ACTIVO_DEPARTAMENTO]:
                departamentos_activos.append(departamentos[i])
            i = i + 1
        return departamentos_activos
    except (KeyError, IndexError):
        manejar_error_inesperado("Departamentos", "listar departamentos activos", "Error al acceder a los datos")
        return []
