
#Crear clases de cliente Atributos: id, nombre, apellido, dni, telefono.
cliente = [
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

def agregar_cliente(cliente, id, nombre, apellido, dni, telefono):

        i = 0
        repetido = False
        while i < len(cliente): #Recorro la lista clientes y verifico dni repetidos
         if cliente[i]["DNI"] == dni:
            repetido = True
         i = i + 1

        if repetido == False:
         nuevo_cliente = {
          "id": id,
          "Nombre":nombre,
          "Apellido": apellido,
          "DNI": dni,
          "Telefono":telefono,
          "Activo": True 
    }
         cliente.append(nuevo_cliente)
         print("Cliente agregado con éxito.")
        else:
         print("Error: el DNI ya está registrado.")
        return cliente




#Funcion que elimina un cliente fisico de la lista de clientes
def eliminar_cliente(cliente, id):
    i = 0
    while i < len(cliente):
        if cliente[i]["id"] == id:
            cliente.remove(cliente[i])
            print("Cliente con id", id, "eliminado")
            return cliente
        i = i + 1
    
    print("Cliente con id", id, "no encontrado")
    return "Cliente no encontrado"

#Funcion que da de baja logica  un cliente de la lista de clientes
def baja_logica_cliente(clientes, id):
    i = 0
    while i < len(clientes):
        if clientes[i]["id"] == id:
            clientes[i]["Estado"] = False
            print("Cliente con id", id, " dado de baja (lógica)")
            return clientes
        i = i + 1
    
    print("Cliente con id", id, " no encontrado")
    return "Cliente no encontrado"

#Funcion que da de alta logica  un cliente de la lista de clientes que estaba de baja

def alta_logica_cliente(clientes, id):
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

    print("Cliente con id", id, " no encontrado")
    return "Cliente no encontrado"
            

    #Funcion que permita actualizar un cliente  de la lista de cliente

def actualizar_cliente(cliente, id, nombre, apellido, dni, telefono):
    for clien in cliente:
        if  clien["id"] == id:
            clien["nombre"] = nombre
            clien["apellido"] = apellido
            clien["dni"] = dni
            clien["telefono"] = telefono
            print(f"Cliente con id {id} actualizado")
            return cliente
    else:
        print(f"Cliente con id {id} no encontrado")
        return "Cliente no encontrado"
    