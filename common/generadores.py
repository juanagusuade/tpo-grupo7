import random


def generar_id_unico_lista(lista):
    """
    Genera un ID unico para lista de listas donde el ID esta en posicion 0.
    Para usar con reservas
    """
    while True:
        id_generado = random.randint(10000, 99999)
        existe_id = False
        i = 0
        while i < len(lista) and not existe_id:
            if lista[i][0] == id_generado:
                existe_id = True
            i = i + 1
        if not existe_id:
            return id_generado


def generar_id_unico_diccionario(lista, clave_id):
    """
    Genera un ID unico para lista de diccionarios.
    Para usar con clientes y departamentos
    lista: Lista de diccionarios
    clave_id: Nombre de la key que contiene el ID
    """
    while True:
        id_generado = random.randint(10000, 99999)
        existe_id = False
        i = 0
        while i < len(lista) and not existe_id:
            if lista[i][clave_id] == id_generado:
                existe_id = True
            i = i + 1
        if not existe_id:
            return id_generado