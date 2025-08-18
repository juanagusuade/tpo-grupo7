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