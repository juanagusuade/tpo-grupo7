#crear clases de departamento Atributos: id, ubicacion, ambientes, capacidad, estado, precio_noche.


departamento = [
    {
        "id": 1,
        "ubicacion": "Centro",
        "ambientes": 3,
        "capacidad": 4,
        "estado": "Disponible",
        "precio_noche": 100.0
    },]



#funcion que permita agregar un departamento a la lista de departamentos
def agregar_departamento(departamento, id, ubicacion, ambientes, capacidad, estado, precio_noche):
    nuevo_departamento = {
        "id": id,
        "ubicacion": ubicacion,
        "ambientes": ambientes,
        "capacidad": capacidad,
        "estado": estado,
        "precio_noche": precio_noche
    }
    departamento.append(nuevo_departamento)
    return departamento 


#funcion que permita eliminar un departamento de la lista de departamentos
def eliminar_departamento(departamento, id):
    for deptos in departamento:
        if deptos["id"] == id:
            departamento.remove(deptos)
            print(f"Departamento con id {id} eliminado")
            return departamento
    else:
        print(f"Departamento con id {id} no encontrado")   
        return "Departamento no encontrado"

#funcion que permita actualizar un departamento de la lista de departamentos
def actualizar_departamento(departamento, id, ubicacion, ambientes, capacidad, estado, precio_noche):
    for deptos in departamento:
        if deptos["id"] == id:
            deptos["ubicacion"] = ubicacion
            deptos["ambientes"] = ambientes
            deptos["capacidad"] = capacidad
            deptos["estado"] = estado
            deptos["precio_noche"] = precio_noche
            print(f"Departamento con id {id} actualizado")
            return departamento
    else:
        print(f"Departamento con id {id} no encontrado")
        return "Departamento no encontrado"
    

#funcion que permita remplazar un departamento de la lista de departamentos
def reemplazar_departamento(departamento, id, ubicacion, ambientes, capacidad, estado, precio_noche):
    for i, deptos in enumerate(departamento):
        if deptos["id"] == id:
            departamento[i] = {
                "id": id,
                "ubicacion": ubicacion,
                "ambientes": ambientes,
                "capacidad": capacidad,
                "estado": estado,
                "precio_noche": precio_noche
            }
            print(f"Departamento con id {id} reemplazado")
            return departamento
    else:
        print(f"Departamento con id {id} no encontrado")
        return "Departamento no encontrado"

# función que permite realizar una baja lógica de un departamento
def baja_logica_departamento(departamento, id):
    for deptos in departamento:
        if deptos["id"] == id:
            deptos["estado"] = "Inactivo"
            print(f"Baja lógica realizada para el departamento con id {id}")
            return departamento
    else:
        print(f"Departamento con id {id} no encontrado")
        return "Departamento no encontrado"

# función que permite listar solo los departamentos activos
def listar_departamentos(departamento):
    for deptos in departamento:
        if deptos["estado"] != "Inactivo":
            print(f"ID: {deptos['id']}, Ubicación: {deptos['ubicacion']}, Ambientes: {deptos['ambientes']}, Capacidad: {deptos['capacidad']}, Estado: {deptos['estado']}, Precio por noche: {deptos['precio_noche']}")
    return departamento

