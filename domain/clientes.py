import utils
#Crear clases de cliente Atributos: id, nombre, apellido, dni, telefono.
clientes = [
    {
        "id": 1,
        "Nombre": "Carlos",
        "Apellido": "Martinez",
        "DNI": 39056237,
        "Telefono":1156378923,
        "Activo":True
    },
]



#Funcion que Permite registrar un nuevo cliente verificando que el DNI no se repita

def agregar_cliente(nombre, apellido, dni, telefono):

        i = 0
        repetido = False
        while i < len(clientes): #Recorro la lista clientes y verifico dni repetidos
         if clientes[i]["DNI"] == dni:
            repetido = True
         i = i + 1
        id=utils.generar_id_unico(clientes)
        if repetido == False:
         nuevo_cliente = {
          "id": id,
          "Nombre":nombre,
          "Apellido": apellido,
          "DNI": dni,
          "Telefono":telefono,
          "Activo": True 
    }
         clientes.append(nuevo_cliente)
         print("Cliente agregado con éxito.")
        else:
         print("Error: el DNI ya está registrado.")
        return clientes




#Funcion que elimina un cliente fisico de la lista de clientes
def eliminar_cliente(id):
    i = 0
    while i < len(clientes):
        if clientes[i]["id"] == id:
            clientes.remove(clientes[i])
            print("Cliente con id", id, "eliminado")
            return id
        i = i + 1
    
    
    return False

#Funcion que da de baja logica  un cliente de la lista de clientes
def baja_logica_cliente(id):
    i = 0
    while i < len(clientes):
        if clientes[i]["id"] == id:
            clientes[i]["Estado"] = False
            print("Cliente con id", id, " dado de baja (lógica)")
            return clientes
        i = i + 1
    
    
    return False

#Funcion que da de alta logica  un cliente de la lista de clientes que estaba de baja

def alta_logica_cliente(id):
    i = 0
    while i < len(clientes):
        if clientes[i]["id"] == id:
            if clientes[i]["Estado"] == False:
               clientes[i]["Estado"] = True
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
        if  clien["id"] == id:
            clien["nombre"] = nombre
            clien["apellido"] = apellido
            clien["dni"] = dni
            clien["telefono"] = telefono
           
            return clientes
        else:
        
         return False
    

 #Funcion que permita buscar cliente por DNI
   
def buscar_cliente_por_dni(dni):
    
    i = 0
    while i < len(clientes):
        if clientes[i]["DNI"] == dni:
            return clientes[i]
        i = i + 1
    return None

#Funcion que permita buscar cliente por ID y que exista en la lista
def buscar_cliente_por_id(id_cliente):
    
    i = 0
    while i < len(clientes):
        if clientes[i]["ID"] == id_cliente:
            return clientes[i]
        i = i + 1
    return None

#Funcion que permita verificar si un cliente esta activo

def cliente_activo(id_cliente):
    cliente = buscar_cliente_por_id(id_cliente)
    if cliente and "Activo" in cliente and cliente["Activo"] == True:
        return True
    return False

#Funcion que permita listar todos los clientes en una copia


def lista_clientes_copia():
    return clientes[:]

#Funcion que permita listar todos los clientes activos 
def listar_clientes_activos(id_cliente):
    clientes_activos=[]
    for cliente in clientes:
        if cliente["Activo"] == True:
            clientes_activos.append(cliente)
    return clientes_activos
        
