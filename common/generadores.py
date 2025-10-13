import random

def generar_id_unico_lista(lista):
    """
    Genera un ID unico para lista de listas donde el ID esta en posicion 0.
    Para usar con reservas. Para saber si existe o no, usa un set
    """
    ids_existentes = {elemento[0] for elemento in lista}
    while True:
        id_generado = random.randint(10000, 99999)
        if id_generado not in ids_existentes:
            return id_generado


def generar_id_unico_diccionario(lista, clave_id):
    """
    Genera un ID unico para lista de diccionarios.
    Para usar con clientes y departamentos
    lista: Lista de diccionarios
    clave_id: Nombre de la key que contiene el ID
    """
    ids_existentes = {elemento[clave_id] for elemento in lista}
    while True:
        id_generado = random.randint(10000, 99999)
        if id_generado not in ids_existentes:
            return id_generado
