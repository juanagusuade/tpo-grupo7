from common.generadores import generar_id_unico_diccionario
from common.constantes import *
from common.manejo_errores import manejar_error_inesperado

ENTIDAD_CLIENTES = "Clientes"

# Crear clases de cliente Atributos: id, nombre, apellido, dni, telefono.
clientes = []


# Funcion que Permite registrar un nuevo cliente verificando que el DNI no se repita
def agregar_cliente(nombre, apellido, dni, telefono):
    try:
        i = 0
        repetido = False
        while i < len(clientes) and (not repetido):
            if clientes[i][DNI_CLIENTE] == dni:
                repetido = True
            i = i + 1

        if repetido == False:
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
            return True
        else:
            return False  # DNI repetido, no es un error, es logica de negocio
    except KeyError:
        manejar_error_inesperado(ENTIDAD_CLIENTES, "agregar cliente", "Datos de cliente corruptos.")
        return False
    except Exception as e:
        manejar_error_inesperado(ENTIDAD_CLIENTES, "agregar cliente", str(e))
        return False


# Funcion que elimina un cliente fisico de la lista de clientes
def eliminar_cliente(id_cliente):
    try:
        cliente_a_eliminar = None
        for cliente in clientes:
            if cliente[ID_CLIENTE] == id_cliente:
                cliente_a_eliminar = cliente

        if cliente_a_eliminar:
            clientes.remove(cliente_a_eliminar)
            return True
        return False  # No se encontro
    except (KeyError, ValueError):
        manejar_error_inesperado(ENTIDAD_CLIENTES, "eliminar cliente",
                                 "Error al intentar remover el cliente de la lista.")
        return False


# Funcion que da de baja logica un cliente de la lista de clientes
def baja_logica_cliente(id_cliente):
    try:
        for cliente in clientes:
            if cliente[ID_CLIENTE] == id_cliente:
                cliente[ACTIVO_CLIENTE] = False
                return True
        return False  # No se encontro
    except KeyError:
        manejar_error_inesperado(ENTIDAD_CLIENTES, "baja logica", "Datos de cliente corruptos.")
        return False


# Funcion que da de alta logica un cliente de la lista de clientes que estaba de baja
def alta_logica_cliente(id_cliente):
    try:
        for cliente in clientes:
            if cliente[ID_CLIENTE] == id_cliente:
                if cliente[ACTIVO_CLIENTE] == False:
                    cliente[ACTIVO_CLIENTE] = True
                    return True
                else:
                    return False  # Ya estaba activo
        return False  # No se encontro
    except KeyError:
        manejar_error_inesperado(ENTIDAD_CLIENTES, "alta logica", "Datos de cliente corruptos.")
        return False


# Funcion que permita actualizar un cliente de la lista de cliente
def actualizar_cliente(id_cliente, nombre, apellido, dni, telefono):
    try:
        for cliente in clientes:
            if cliente[ID_CLIENTE] == id_cliente:
                cliente[NOMBRE_CLIENTE] = nombre
                cliente[APELLIDO_CLIENTE] = apellido
                cliente[DNI_CLIENTE] = dni
                cliente[TELEFONO_CLIENTE] = telefono
                return True
        return False  # No se encontro
    except KeyError:
        manejar_error_inesperado(ENTIDAD_CLIENTES, "actualizar cliente", "Datos de cliente corruptos.")
        return False


# Funcion que permita buscar cliente por DNI
def buscar_cliente_por_dni(dni):
    try:
        for cliente in clientes:
            if cliente[DNI_CLIENTE] == dni:
                return cliente
        return None
    except KeyError:
        manejar_error_inesperado(ENTIDAD_CLIENTES, "buscar por DNI", "Datos de cliente corruptos.")
        return None


# Funcion que permita buscar cliente por ID y que exista en la lista
def buscar_cliente_por_id(id_cliente):
    try:
        for cliente in clientes:
            if cliente[ID_CLIENTE] == id_cliente:
                return cliente
        return None
    except KeyError:
        manejar_error_inesperado(ENTIDAD_CLIENTES, "buscar por ID", "Datos de cliente corruptos.")
        return None


# Funcion que permita verificar si un cliente esta activo
def cliente_activo(id_cliente):
    try:
        cliente = buscar_cliente_por_id(id_cliente)
        if cliente and ACTIVO_CLIENTE in cliente and cliente[ACTIVO_CLIENTE] == True:
            return True
        return False
    except KeyError:
        manejar_error_inesperado(ENTIDAD_CLIENTES, "verificar activo", "Datos de cliente corruptos.")
        return False


# Funcion que permita listar todos los clientes en una copia
def lista_clientes_copia():
    return clientes[:]


# Funcion que permita listar todos los clientes activos
def listar_clientes_activos():
    try:
        return list(filter(lambda cliente: cliente[ACTIVO_CLIENTE], clientes))
    except KeyError:
        manejar_error_inesperado(ENTIDAD_CLIENTES, "listar activos", "Datos de cliente corruptos.")
        return []


def dni_repetido(dni, id_cliente, lista_clientes):
    """Verifica si un DNI ya existe en la lista para un cliente distinto."""
    try:
        for cliente in lista_clientes:
            if cliente[DNI_CLIENTE] == dni and cliente[ID_CLIENTE] != id_cliente:
                return True
        return False
    except KeyError:
        manejar_error_inesperado(ENTIDAD_CLIENTES, "verificar DNI repetido", "Datos de cliente corruptos.")
        return True  # Se asume repetido