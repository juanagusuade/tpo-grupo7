from operator import indexOf

from common.utils import generar_id_unico_diccionario
from common.constantes import *
#Crear clases de cliente Atributos: id, nombre, apellido, dni, telefono.
clientes = [
    {
        ID_CLIENTE: 1,
        NOMBRE_CLIENTE: "Carlos",
        APELLIDO_CLIENTE: "Martinez",
        DNI_CLIENTE: 39056237,
        TELEFONO_CLIENTE:1156378923,
        ACTIVO_CLIENTE:True
    },
]



#Funcion que Permite registrar un nuevo cliente verificando que el DNI no se repita
def agregar_cliente(nombre, apellido, dni, telefono):

    i = 0
    repetido = False
    while i < len(clientes) and (not repetido): #Recorro la lista clientes y verifico dni repetidos
        if clientes[i][DNI_CLIENTE] == dni:
            repetido = True
        i = i + 1

        id=generar_id_unico_diccionario(clientes)
        if repetido == False:
         nuevo_cliente = {
          ID_CLIENTE: id,
          NOMBRE_CLIENTE:nombre,
          APELLIDO_CLIENTE: apellido,
          DNI_CLIENTE: dni,
          TELEFONO_CLIENTE:telefono,
          ACTIVO_CLIENTE: True 
    }
         clientes.append(nuevo_cliente)
         print("Cliente agregado con éxito.")
        else:
         print("Error: el DNI ya está registrado.")
        return clientes




#Funcion que elimina un cliente fisico de la lista de clientes
def eliminar_cliente(id):
    i = 0
    for i in range(len(clientes)):
        if clientes[i][ID_CLIENTE] == id:
            clientes.remove(clientes[i])
            print("Cliente con id", id, "eliminado")
            return id
        i = i + 1

    return False

#Funcion que da de baja logica  un cliente de la lista de clientes
def baja_logica_cliente(id):
    i = 0
    while i < len(clientes):
        if clientes[i][ID_CLIENTE] == id:
            clientes[i][ACTIVO_CLIENTE] = False
            print("Cliente con id", id, " dado de baja (lógica)")
            return clientes
        i = i + 1
    
    
    return False

#Funcion que da de alta logica un cliente de la lista de clientes que estaba de baja

def alta_logica_cliente(id):
    i = 0
    while i < len(clientes):
        if clientes[i][ID_CLIENTE] == id:
            if clientes[i][ACTIVO_CLIENTE] == False:
               clientes[i][ACTIVO_CLIENTE] = True
               print("Cliente con id", id, " activo")
               return clientes
            else:
             print("El cliente con id", id, "ya estaba activo")
             return clientes
        i = i + 1

    
    return False
            

#Funcion que permita actualizar un cliente  de la lista de cliente

def actualizar_cliente(id, nombre, apellido, dni, telefono):
    for clien in clientes:
        if  clien[ID_CLIENTE] == id:
            clien[NOMBRE_CLIENTE] = nombre
            clien[APELLIDO_CLIENTE] = apellido
            clien[DNI_CLIENTE] = dni
            clien[TELEFONO_CLIENTE] = telefono
           
            return clientes
        else:
        
         return False
    

 #Funcion que permita buscar cliente por DNI
   
def buscar_cliente_por_dni(dni):
    cliente_encontrado = list(filter(lambda c: c[DNI_CLIENTE] == dni, clientes))

    if len(cliente_encontrado) == 1:
        cliente_encontrado = cliente_encontrado[0]  # Devuelve el único cliente encontrado
    else:
        cliente_encontrado = False  # Devuelve False si hay más de uno o ninguno
    i = 0
    while i < len(clientes):
        if clientes[i][DNI_CLIENTE] == dni:
            return clientes[i]
        i = i + 1
    return None

#Funcion que permita buscar cliente por ID y que exista en la lista
def buscar_cliente_por_id(id_cliente):
    
    i = 0
    while i < len(clientes):
        if clientes[i][ID_CLIENTE] == id_cliente:
            return clientes[i]
        i = i + 1
    return None

#Funcion que permita verificar si un cliente esta activo

def cliente_activo(id_cliente):
    cliente = buscar_cliente_por_id(id_cliente)
    if cliente and ACTIVO_CLIENTE in cliente and cliente[ACTIVO_CLIENTE] == True:
        return True
    return False

#Funcion que permita listar todos los clientes en una copia


def lista_clientes_copia():
    return clientes[:]

#Funcion que permita listar todos los clientes activos 
def listar_clientes_activos(id_cliente):
    clientes_activos=[]
    for cliente in clientes:
        if cliente[ACTIVO_CLIENTE] == True:
            clientes_activos.append(cliente)
    return clientes_activos
        
