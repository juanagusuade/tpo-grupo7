from common.generadores import generar_id_unico_diccionario
from common.constantes import *

# Crear clases de cliente Atributos: id, nombre, apellido, dni, telefono.
clientes = [
    {
        ID_CLIENTE: 1,
        NOMBRE_CLIENTE: "Carlos",
        APELLIDO_CLIENTE: "Martinez",
        DNI_CLIENTE: 39056237,
        TELEFONO_CLIENTE: 1156378923,
        ACTIVO_CLIENTE: True
    },
]


# Funcion que Permite registrar un nuevo cliente verificando que el DNI no se repita
def agregar_cliente(nombre, apellido, dni, telefono):
    i = 0
    repetido = False
    while i < len(clientes) and (not repetido):  # Recorro la lista clientes y verifico dni repetidos
        if clientes[i][DNI_CLIENTE] == dni:
            repetido = True
        i = i + 1

    id_nuevo = generar_id_unico_diccionario(clientes, ID_CLIENTE)
    if repetido == False:
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
        return False


# Funcion que elimina un cliente fisico de la lista de clientes
def eliminar_cliente(id_cliente):
    i = 0
    while i < len(clientes):
        if clientes[i][ID_CLIENTE] == id_cliente:
            clientes.pop(i)
            return True
        i = i + 1
    return False


# Funcion que da de baja logica un cliente de la lista de clientes
def baja_logica_cliente(id_cliente):
    i = 0
    while i < len(clientes):
        if clientes[i][ID_CLIENTE] == id_cliente:
            clientes[i][ACTIVO_CLIENTE] = False
            return True
        i = i + 1
    return False


# Funcion que da de alta logica un cliente de la lista de clientes que estaba de baja
def alta_logica_cliente(id_cliente):
    i = 0
    while i < len(clientes):
        if clientes[i][ID_CLIENTE] == id_cliente:
            if clientes[i][ACTIVO_CLIENTE] == False:
                clientes[i][ACTIVO_CLIENTE] = True
                return True
            else:
                return False  # Ya estaba activo
        i = i + 1
    return False


# Funcion que permita actualizar un cliente de la lista de cliente
def actualizar_cliente(id_cliente, nombre, apellido, dni, telefono):
    i = 0
    while i < len(clientes):
        if clientes[i][ID_CLIENTE] == id_cliente:
            clientes[i][NOMBRE_CLIENTE] = nombre
            clientes[i][APELLIDO_CLIENTE] = apellido
            clientes[i][DNI_CLIENTE] = dni
            clientes[i][TELEFONO_CLIENTE] = telefono
            return True
        i = i + 1
    return False


# Funcion que permita buscar cliente por DNI
def buscar_cliente_por_dni(dni):
    i = 0
    while i < len(clientes):
        if clientes[i][DNI_CLIENTE] == dni:
            return clientes[i]
        i = i + 1
    return None


# Funcion que permita buscar cliente por ID y que exista en la lista
def buscar_cliente_por_id(id_cliente):
    i = 0
    while i < len(clientes):
        if clientes[i][ID_CLIENTE] == id_cliente:
            return clientes[i]
        i = i + 1
    return None


# Funcion que permita verificar si un cliente esta activo
def cliente_activo(id_cliente):
    cliente = buscar_cliente_por_id(id_cliente)
    if cliente and ACTIVO_CLIENTE in cliente and cliente[ACTIVO_CLIENTE] == True:
        return True
    return False


# Funcion que permita listar todos los clientes en una copia
def lista_clientes_copia():
    return clientes[:]


# Funcion que permita listar todos los clientes activos
def listar_clientes_activos(filtro_id=None):  # Parametro renombrado para claridad
    clientes_activos = []
    for cliente in clientes:
        if cliente[ACTIVO_CLIENTE] == True:
            clientes_activos.append(cliente)
    return clientes_activos