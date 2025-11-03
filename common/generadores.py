import random

def generar_id_unico_lista(lista):
    """
    Genera un ID unico para lista de listas donde el ID esta en posicion 0.
    
    Parametros:
        lista (list): Lista de listas
    
    Retorna:
        int: ID unico entre 10000 y 99999
    """
    ids_existentes = {elemento[0] for elemento in lista}
    while True:
        id_generado = random.randint(10000, 99999)
        if id_generado not in ids_existentes:
            return id_generado


def generar_id_unico_diccionario(lista, clave_id):
    """
    Genera un ID unico para lista de diccionarios.
    
    Parametros:
        lista (list): Lista de diccionarios
        clave_id (str): Nombre de la clave que contiene el ID
    
    Retorna:
        int: ID unico entre 10000 y 99999
    """
    ids_existentes = {elemento[clave_id] for elemento in lista}
    while True:
        id_generado = random.randint(10000, 99999)
        if id_generado not in ids_existentes:
            return id_generado
