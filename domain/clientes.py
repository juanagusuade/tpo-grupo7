from common.generadores import generar_id_unico_diccionario
from common.constantes import *
from common.manejo_errores import manejar_error_inesperado
from repository.persistence_json import leer_clientes, guardar_clientes

ENTIDAD_CLIENTES = "Clientes"

clientes = []


def buscar_dni(lista_clientes, dni):
    """
    Busca un DNI en la lista de clientes usando programacion funcional.
    
    Parametros:
        lista_clientes (list): Lista de diccionarios de clientes
        dni (str): DNI a buscar
    
    Retorna:
        bool: True si el DNI ya existe, False si no existe
    """
    try:
        return any(cliente[DNI_CLIENTE] == dni for cliente in lista_clientes)
    except (KeyError, IndexError):
        manejar_error_inesperado(ENTIDAD_CLIENTES, "buscar DNI", "Error en estructura de datos.")
        return True


def agregar_cliente(nombre, apellido, dni, telefono):
    """
    Permite registrar un nuevo cliente verificando que el DNI no se repita.
    
    Parametros:
        nombre (str): Nombre del cliente
        apellido (str): Apellido del cliente
        dni (str): DNI del cliente (debe ser unico)
        telefono (str): Telefono del cliente
    
    Retorna:
        bool: True si se agrego correctamente, False si el DNI ya existe o hay error
    """
    try:
        if buscar_dni(clientes, dni):
            return False
        
        id_nuevo = generar_id_unico_diccionario(clientes, ID_CLIENTE)
        nuevo_cliente = {
            ID_CLIENTE: id_nuevo,
            NOMBRE_CLIENTE: nombre,
            APELLIDO_CLIENTE: apellido,
            DNI_CLIENTE: dni,
            TELEFONO_CLIENTE: telefono,
            ACTIVO_CLIENTE: True
        }
        clientes.append(nuevo_cliente)
        guardar_clientes_a_archivo("agregar cliente")
        return True
    except KeyError:
        manejar_error_inesperado(ENTIDAD_CLIENTES, "agregar cliente", "Datos de cliente corruptos.")
        return False
    except Exception as e:
        manejar_error_inesperado(ENTIDAD_CLIENTES, "agregar cliente", str(e))
        return False


def eliminar_cliente(id_cliente):
    """
    Elimina un cliente fisico de la lista de clientes.
    
    Parametros:
        id_cliente (int): ID del cliente a eliminar
    
    Retorna:
        bool: True si se elimino correctamente, False si no se encontro
    """
    try:
        cliente_a_eliminar = None
        for cliente in clientes:
            if cliente[ID_CLIENTE] == id_cliente:
                cliente_a_eliminar = cliente

        if cliente_a_eliminar:
            clientes.remove(cliente_a_eliminar)
            guardar_clientes_a_archivo("eliminar cliente")
            return True
        return False
    except (KeyError, ValueError):
        manejar_error_inesperado(ENTIDAD_CLIENTES, "eliminar cliente",
                                 "Error al intentar remover el cliente de la lista.")
        return False


def cambiar_estado_cliente(id_cliente, nuevo_estado):
    """
    Funcion generica para cambiar el estado activo/inactivo de un cliente.
    
    Parametros:
        id_cliente (int): ID del cliente
        nuevo_estado (bool): True para activar, False para desactivar
    
    Retorna:
        bool: True si se cambio el estado correctamente, False si no se encontro
    """
    try:
        for cliente in clientes:
            if cliente[ID_CLIENTE] == id_cliente:
                cliente[ACTIVO_CLIENTE] = nuevo_estado
                return True
        return False
    except KeyError:
        manejar_error_inesperado(ENTIDAD_CLIENTES, "cambiar estado", "Datos de cliente corruptos.")
        return False


def baja_logica_cliente(id_cliente):
    """
    Da de baja logica un cliente de la lista de clientes.
    
    Parametros:
        id_cliente (int): ID del cliente a dar de baja
    
    Retorna:
        bool: True si se dio de baja correctamente, False si no se encontro
    """
    resultado= cambiar_estado_cliente(id_cliente, False)
    if resultado:
        guardar_clientes_a_archivo("baja logica cliente")
    return resultado    


def alta_logica_cliente(id_cliente):
    """
    Da de alta logica un cliente que estaba de baja.
    
    Parametros:
        id_cliente (int): ID del cliente a dar de alta
    
    Retorna:
        bool: True si se dio de alta correctamente, False si no se encontro o ya estaba activo
    """
    try:
        for cliente in clientes:
            if cliente[ID_CLIENTE] == id_cliente:
                if cliente[ACTIVO_CLIENTE] == False:
                    cliente[ACTIVO_CLIENTE] = True
                    guardar_clientes_a_archivo("alta logica de cliente")
                    return True
                else:
                    return False
        return False
    except KeyError:
        manejar_error_inesperado(ENTIDAD_CLIENTES, "alta logica", "Datos de cliente corruptos.")
        return False


def buscar_dni_diferente_id(lista_clientes, dni, id_excluir):
    """
    Busca un DNI en la lista excluyendo un ID especifico.
    
    Parametros:
        lista_clientes (list): Lista de diccionarios de clientes
        dni (str): DNI a buscar
        id_excluir (int): ID del cliente a excluir de la busqueda
    
    Retorna:
        bool: True si el DNI existe en otro cliente, False si no existe
    """
    try:
        return any(
            cliente[DNI_CLIENTE] == dni and cliente[ID_CLIENTE] != id_excluir
            for cliente in lista_clientes
        )
    except (KeyError, IndexError):
        manejar_error_inesperado(ENTIDAD_CLIENTES, "buscar DNI diferente ID", "Error en estructura de datos.")
        return True


def actualizar_cliente(id_cliente, nombre, apellido, dni, telefono):
    """
    Permite actualizar un cliente de la lista de clientes.
    Valida que el nuevo DNI no este repetido en otro cliente.
    
    Parametros:
        id_cliente (int): ID del cliente a actualizar
        nombre (str): Nuevo nombre
        apellido (str): Nuevo apellido
        dni (str): Nuevo DNI (debe ser unico)
        telefono (str): Nuevo telefono
    
    Retorna:
        bool: True si se actualizo correctamente, False si no se encontro o DNI repetido
    """
    try:
        if buscar_dni_diferente_id(clientes, dni, id_cliente):
            return False
        actualizado= False
        for cliente in clientes:
            if cliente[ID_CLIENTE] == id_cliente:
                cliente[NOMBRE_CLIENTE] = nombre
                cliente[APELLIDO_CLIENTE] = apellido
                cliente[DNI_CLIENTE] = dni
                cliente[TELEFONO_CLIENTE] = telefono
                actualizado= True
                break
        if actualizado:
            guardar_clientes_a_archivo("actualizar cliente")
            return True 
        return False
    except KeyError:
        manejar_error_inesperado(ENTIDAD_CLIENTES, "actualizar cliente", "Datos de cliente corruptos.")
        return False


def buscar_cliente_por_dni(dni):
    """
    Busca un cliente por su DNI.
    
    Parametros:
        dni (str): DNI del cliente a buscar
    
    Retorna:
        dict or None: Diccionario del cliente si se encuentra, None si no existe
    """
    try:
        for cliente in clientes:
            if cliente[DNI_CLIENTE] == dni:
                return cliente
        return None
    except KeyError:
        manejar_error_inesperado(ENTIDAD_CLIENTES, "buscar por DNI", "Datos de cliente corruptos.")
        return None


def buscar_cliente_por_id(id_cliente):
    """
    Busca un cliente por su ID.
    
    Parametros:
        id_cliente (int): ID del cliente a buscar
    
    Retorna:
        dict or None: Diccionario del cliente si se encuentra, None si no existe
    """
    try:
        for cliente in clientes:
            if cliente[ID_CLIENTE] == id_cliente:
                return cliente
        return None
    except KeyError:
        manejar_error_inesperado(ENTIDAD_CLIENTES, "buscar por ID", "Datos de cliente corruptos.")
        return None


def cliente_activo(id_cliente):
    """
    Verifica si un cliente esta activo.
    
    Parametros:
        id_cliente (int): ID del cliente a verificar
    
    Retorna:
        bool: True si el cliente existe y esta activo, False en caso contrario
    """
    try:
        cliente = buscar_cliente_por_id(id_cliente)
        if cliente and ACTIVO_CLIENTE in cliente and cliente[ACTIVO_CLIENTE] == True:
            return True
        return False
    except KeyError:
        manejar_error_inesperado(ENTIDAD_CLIENTES, "verificar activo", "Datos de cliente corruptos.")
        return False


def lista_clientes_copia():
    """
    Retorna una copia de la lista de todos los clientes.
    
    Retorna:
        list: Copia de la lista de clientes
    """
    return clientes[:]


def listar_clientes_activos():
    """
    Lista todos los clientes activos usando programacion funcional.
    
    Retorna:
        list: Lista de diccionarios con clientes activos
    """
    try:
        return list(filter(lambda cliente: cliente[ACTIVO_CLIENTE], clientes))
    except KeyError:
        manejar_error_inesperado(ENTIDAD_CLIENTES, "listar activos", "Datos de cliente corruptos.")
        return []


def dni_repetido(dni, id_cliente, lista_clientes):
    """
    Verifica si un DNI ya existe en la lista para un cliente distinto.
    
    Parametros:
        dni (str): DNI a verificar
        id_cliente (int): ID del cliente a excluir de la busqueda
        lista_clientes (list): Lista de clientes donde buscar
    
    Retorna:
        bool: True si el DNI esta repetido, False si no
    """
    try:
        for cliente in lista_clientes:
            if cliente[DNI_CLIENTE] == dni and cliente[ID_CLIENTE] != id_cliente:
                return True
        return False
    except KeyError:
        manejar_error_inesperado(ENTIDAD_CLIENTES, "verificar DNI repetido", "Datos de cliente corruptos.")
        return True
    

    # Funciones de persistencia agregadas para guardar cambios en el archivo JSON

def cargar_clientes_desde_archivo():
    """
        Carga la lista de clientes desde el archivo JSON al iniciar el sistema.
        Actualiza la lista global 'clientes'.
    
        Retorna:
        bool: True si se cargaron correctamente, False si hubo error
    """
    try:
        global clientes
        clientes_cargados = leer_clientes()

        clientes.clear()
        clientes.extend(clientes_cargados)
        print(f"Se cargaron {len(clientes_cargados)} clientes desde archivo JSON")
        return True
    except Exception as e:                    
        manejar_error_inesperado(ENTIDAD_CLIENTES, "cargar clientes desde archivo", str(e))
        return False   
    except ImportError:
        manejar_error_inesperado(ENTIDAD_CLIENTES, "cargar clientes desde archivo", "Error al importar funciones de persistencia.")
        return False     
        
def guardar_clientes_a_archivo(operacion="se realiza operacion"):
    """
    Guarda la lista de clientes actual en el archivo JSON.
    
    Parametros:
        operacion (str): Descripcion de la operacion que genero el guardado (para logs)
    
    Retorna:
        bool: True si se guardaron correctamente, False si hubo error
    """
    try:
        if guardar_clientes(clientes):
            print(f"Cambios guardados en archivo JSON tras {operacion}")
            return True
        else:
            print("Error al guardar clientes en archivo JSON")
            return False
    except Exception as e:
        manejar_error_inesperado(ENTIDAD_CLIENTES, "guardar archivo", str(e))
        return False
    except ImportError:
        manejar_error_inesperado(ENTIDAD_CLIENTES, "guardar archivo", "Error al importar funciones de persistencia.")
        return False