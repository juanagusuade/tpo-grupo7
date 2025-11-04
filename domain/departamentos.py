from common.generadores import generar_id_unico_diccionario
from common.constantes import *
from common.manejo_errores import manejar_error_inesperado
from domain.reservas import comparar_fechas_string, ENTIDAD_RESERVAS, obtener_todas_las_reservas

ENTIDAD_DEPARTAMENTOS = "Departamentos"

departamentos = []


def agregar_departamento(ubicacion, ambientes, capacidad, estado, precio_noche):
    """
    Agrega un nuevo departamento a la lista.
    
    Parametros:
        ubicacion (str): Ubicacion del departamento
        ambientes (int): Cantidad de ambientes
        capacidad (int): Capacidad de personas
        estado (str): Estado (Disponible/Ocupado/Mantenimiento)
        precio_noche (float): Precio por noche
    
    Retorna:
        bool: True si se agrego correctamente, False si hay error
    """
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
        guardar_departamentos_a_archivo("agregar departamento")
        return True
    except Exception as e:
        manejar_error_inesperado(ENTIDAD_DEPARTAMENTOS, "agregar departamento", str(e))
        return False


def eliminar_departamento(id_departamento):
    """
    Elimina fisicamente un departamento de la lista.
    
    Parametros:
        id_departamento (int): ID del departamento a eliminar
    
    Retorna:
        bool: True si se elimino correctamente, False si no se encontro
    """
    try:
        depto_a_eliminar = None
        for depto in departamentos:
            if depto[ID_DEPARTAMENTO] == id_departamento:
                depto_a_eliminar = depto

        if depto_a_eliminar:
            departamentos.remove(depto_a_eliminar)
            guardar_departamentos_a_archivo("eliminar departamento")
            return True
        return False
    except (KeyError, ValueError):
        manejar_error_inesperado(ENTIDAD_DEPARTAMENTOS, "eliminar departamento",
                                 "Error al intentar remover el depto. de la lista.")
        return False


def actualizar_departamento(id_departamento, ubicacion, ambientes, capacidad, estado, precio_noche):
    """
    Actualiza los datos de un departamento existente.
    
    Parametros:
        id_departamento (int): ID del departamento a actualizar
        ubicacion (str): Nueva ubicacion
        ambientes (int): Nueva cantidad de ambientes
        capacidad (int): Nueva capacidad
        estado (str): Nuevo estado
        precio_noche (float): Nuevo precio por noche
    
    Retorna:
        bool: True si se actualizo correctamente, False si no se encontro
    """
    try:
        for depto in departamentos:
            if depto[ID_DEPARTAMENTO] == id_departamento:
                depto[UBICACION_DEPARTAMENTO] = ubicacion
                depto[AMBIENTES_DEPARTAMENTO] = ambientes
                depto[CAPACIDAD_DEPARTAMENTO] = capacidad
                depto[ESTADO_DEPARTAMENTO] = estado
                depto[PRECIO_DEPARTAMENTO] = precio_noche
                guardar_departamentos_a_archivo("actualizar departamento")
                return True
        return False
    except KeyError:
        manejar_error_inesperado(ENTIDAD_DEPARTAMENTOS, "actualizar departamento", "Datos de departamento corruptos.")
        return False


def reemplazar_departamento(id_departamento, ubicacion, ambientes, capacidad, estado, precio_noche):
    """
    Reemplaza completamente un departamento.
    
    Parametros:
        id_departamento (int): ID del departamento a reemplazar
        ubicacion (str): Nueva ubicacion
        ambientes (int): Nueva cantidad de ambientes
        capacidad (int): Nueva capacidad
        estado (str): Nuevo estado
        precio_noche (float): Nuevo precio por noche
    
    Retorna:
        bool: True si se reemplazo correctamente, False si no se encontro
    """
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
                guardar_departamentos_a_archivo("reemplazar departamento")
                return True
        return False
    except KeyError:
        manejar_error_inesperado(ENTIDAD_DEPARTAMENTOS, "reemplazar departamento", "Datos de departamento corruptos.")
        return False


def cambiar_estado_departamento(id_departamento, nuevo_estado):
    """
    Funcion generica para cambiar el estado de un departamento.
    
    Parametros:
        id_departamento (int): ID del departamento
        nuevo_estado (bool): True para activar, False para desactivar
    
    Retorna:
        bool: True si se cambio el estado correctamente, False si no se encontro
    """
    try:
        for depto in departamentos:
            if depto[ID_DEPARTAMENTO] == id_departamento:
                depto[ACTIVO_DEPARTAMENTO] = nuevo_estado
                guardar_departamentos_a_archivo("cambiar estado departamento")
                return True
        return False
    except KeyError:
        manejar_error_inesperado(ENTIDAD_DEPARTAMENTOS, "cambiar estado", "Datos de departamento corruptos.")
        return False


def baja_logica_departamento(id_departamento):
    """
    Realiza baja logica de un departamento.
    
    Parametros:
        id_departamento (int): ID del departamento a dar de baja
    
    Retorna:
        bool: True si se dio de baja correctamente, False si no se encontro
    """
    return cambiar_estado_departamento(id_departamento, False)


def alta_logica_departamento(id_departamento):
    """
    Da de alta logica un departamento.
    
    Parametros:
        id_departamento (int): ID del departamento a dar de alta
    
    Retorna:
        bool: True si se dio de alta correctamente, False si no se encontro
    """
    return cambiar_estado_departamento(id_departamento, True)


def buscar_departamento_por_id(id_departamento, indice=0):
    """
    Busca  un departamento por su ID.
    
    Parametros:
        id_departamento (int): ID del departamento a buscar
        indice (int): Indice actual en la recursion
    
    Retorna:
        dict or None: Diccionario del departamento si se encuentra, None si no existe
    """
    try:
        if indice >= len(departamentos):
            return None
        
        if departamentos[indice][ID_DEPARTAMENTO] == id_departamento:
            return departamentos[indice]
        
        return buscar_departamento_por_id(id_departamento, indice + 1)
    except KeyError:
        manejar_error_inesperado(ENTIDAD_DEPARTAMENTOS, "buscar por ID", "Datos de departamento corruptos.")
        return None


def listar_departamentos_activos():
    """
    Lista todos los departamentos activos.
    
    Retorna:
        list: Lista de diccionarios con departamentos activos
    """
    try:
        return list(filter(lambda depto: depto[ACTIVO_DEPARTAMENTO], departamentos))
    except KeyError:
        manejar_error_inesperado(ENTIDAD_DEPARTAMENTOS, "listar activos", "Datos de departamento corruptos.")
        return []


def listar_departamentos_disponibles(fecha_ingreso, fecha_egreso):
    """
    Lista los departamentos disponibles para un rango de fechas.
    
    Parametros:
        fecha_ingreso (str): Fecha de ingreso en formato "dd/mm/aaaa"
        fecha_egreso (str): Fecha de egreso en formato "dd/mm/aaaa"
    
    Retorna:
        list: Lista de departamentos disponibles
    """
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
    Verifica si un departamento esta disponible en un rango de fechas.
    Permite que el ultimo dia de una reserva coincida con el primer dia de otra.
    
    Parametros:
        id_departamento (int): ID del departamento
        fecha_ingreso_str (str): Fecha de ingreso deseada
        fecha_egreso_str (str): Fecha de egreso deseada
    
    Retorna:
        bool: True si esta disponible, False si hay solapamiento o error
    """
    try:
        reservas = obtener_todas_las_reservas()
        for r in reservas:
            if r[INDICE_ID_DEPARTAMENTO] == id_departamento and r[INDICE_ESTADO] == ESTADO_ACTIVO:
                comp_inicio_nueva_fin_reserva = comparar_fechas_string(fecha_ingreso_str, r[INDICE_FECHA_EGRESO])
                comp_inicio_reserva_fin_nueva = comparar_fechas_string(r[INDICE_FECHA_INGRESO], fecha_egreso_str)

                if comp_inicio_nueva_fin_reserva is None or comp_inicio_reserva_fin_nueva is None:
                    return False

                if comp_inicio_nueva_fin_reserva < 0 and comp_inicio_reserva_fin_nueva < 0:
                    return False

        return True
    except (TypeError, IndexError):
        manejar_error_inesperado(ENTIDAD_RESERVAS, "verificar disponibilidad")
        return False


# =============================================================================
# FUNCIONES DE PERSISTENCIA - INTEGRACION CON JSON
# =============================================================================

def cargar_departamentos_desde_archivo():
    """
    Carga los departamentos desde archivo JSON al iniciar el sistema.
    Esta función debe llamarse al inicio del programa.
    
    Retorna:
        bool: True si se cargaron correctamente, False si hubo error
    """
    try:
        from repository.persistence_json import inicializar_datos_departamentos
        global departamentos
        departamentos_cargados = inicializar_datos_departamentos()
        
        # Reemplazar la lista global con los datos cargados
        departamentos.clear()
        departamentos.extend(departamentos_cargados)
        
        return True
    except ImportError:
        manejar_error_inesperado(ENTIDAD_DEPARTAMENTOS, "cargar desde archivo", "Módulo de persistencia no disponible")
        return False
    except Exception as e:
        manejar_error_inesperado(ENTIDAD_DEPARTAMENTOS, "cargar desde archivo", str(e))
        return False


def guardar_departamentos_a_archivo(operacion="operación"):
    """
    Guarda los departamentos actuales en archivo JSON.
    Se puede llamar después de operaciones críticas.
    
    Parametros:
        operacion (str): Descripción de la operación que desencadenó el guardado
    
    Retorna:
        bool: True si se guardó correctamente, False si hubo error
    """
    try:
        from repository.persistence_json import guardar_cambios_departamentos
        return guardar_cambios_departamentos(departamentos, operacion)
    except ImportError:
        manejar_error_inesperado(ENTIDAD_DEPARTAMENTOS, "guardar a archivo", "Módulo de persistencia no disponible")
        return False
    except Exception as e:
        manejar_error_inesperado(ENTIDAD_DEPARTAMENTOS, "guardar a archivo", str(e))
        return False