from common.generadores import generar_id_unico_diccionario
from common.constantes import *

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
    i = 0
    while i < len(departamentos):
        if departamentos[i][ID_DEPARTAMENTO] == id_departamento:
            return departamentos[i]
        i = i + 1
    return None


def listar_departamentos_activos():
    """Lista todos los departamentos activos"""
    return [depto for depto in departamentos if depto[ACTIVO_DEPARTAMENTO]]