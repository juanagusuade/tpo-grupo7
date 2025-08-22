import random

def generar_id_unico(lista):
    """
    Genera un ID unico para una lista dada.
    """
    while True:
        id_generado = random.randint(10000, 99999)
        #Si hay 'algun' id igual en la posicion 0 en la matriz (any() returna True si hay alguno)
        existe_id_igual = any(e[0] == id_generado for e in lista)
        if not existe_id_igual:
            return id_generado


def validar_campos(*campos):
    """
    Verifica que los campos no sean None ni vacíos.
    Devuelve True si todos los campos son válidos.
    Devuelve False si al menos uno es None o vacío.
    """
    for campo in campos:
        if campo is None:
            return False
        # Para tipos que soportan len(), se chequea por vacio.
        if hasattr(campo, '__len__') and len(campo) == 0:
            return False
    return True


def validar_fecha(fecha_str):
    """
    Valida que un string tenga formato dd/mm/aaaa y represente una fecha valida.

    Args:
        fecha_str: String con la fecha a validar

    Returns:
        True si la fecha es válida en formato y contenido, False en caso contrario
    """
    # Verificar que sea un str
    if not isinstance(fecha_str, str):
        return False

    # Verificar que no este vacio
    if not fecha_str.strip():
        return False

    # Verificar formato
    if len(fecha_str) != 10:  # dd/mm/aaaa = 10 char
        return False

    if fecha_str[2] != '/' or fecha_str[5] != '/':
        return False

    # Separar las partes
    partes = fecha_str.split('/')
    if len(partes) != 3:
        return False

    dia_str, mes_str, año_str = partes

    # Verificar que todas las partes sean numéricas
    if not (dia_str.isdigit() and mes_str.isdigit() and año_str.isdigit()):
        return False

    # Convertir a enteros
    try:
        dia = int(dia_str)
        mes = int(mes_str)
        año = int(año_str)
    except ValueError:
        return False

    # Validar rangos
    if mes < 1 or mes > 12:
        return False

    if dia < 1 or dia > 31:
        return False

    if año < 1000 or año > 9999:
        return False

    # Validar dias segun mes (por orden en lista)
    dias_por_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # Verificar si es anio bisiesto
    es_bisiesto = (año % 4 == 0 and año % 100 != 0) or (año % 400 == 0)
    if es_bisiesto:
        dias_por_mes[1] = 29  # Febrero en anio bisiesto

    if dia > dias_por_mes[mes - 1]:
        return False

    return True
