import random

"""
    Genera un ID unico para una lista dada.
    """
def generar_id_unico(lista):
    id_generado = random.randint(1000, 9999)
    existe_id_igual = True
    while existe_id_igual:
        existe_id_igual = False
        for e in lista:
            if e[0] == id:
                existe_id_igual = True
                id_generado = random.randint(1000, 9999)
                break
    return id

"""
    Verifica que los campos no sean None ni vacíos.
    Devuelve True si todos los campos son válidos.
    Devuelve False si al menos uno es None o vacío.
    """
def validar_campos(*campos):
    for campo in campos:
        if campo is None:
            return False
        # Para tipos que soportan len(), se chequea por vacio.
        if hasattr(campo, '__len__') and len(campo) == 0:
            return False
    return True
