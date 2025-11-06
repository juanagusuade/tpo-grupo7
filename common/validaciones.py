import re

def campos_son_validos(*campos):
    """
    Verifica que los campos no sean None ni vacios.
    
    Parametros:
        *campos: Cantidad variable de campos a validar
    
    Retorna:
        bool: True si todos los campos son validos, False si al menos uno es None o vacio
    """
    for campo in campos:
        if campo is None:
            return False
        if type(campo) == str and len(campo.strip()) == 0:
            return False
        if type(campo) == list and len(campo) == 0:
            return False
        if type(campo) == dict and len(campo) == 0:
            return False
        if type(campo) in [int, float] and campo < 0:
            return False
    return True


def validar_numero_decimal(valor_str):
    """
    Valida que un string represente un numero decimal positivo.
    
    Parametros:
        valor_str (str): String a validar
    
    Retorna:
        bool: True si es un numero decimal positivo valido
    """
    if type(valor_str) != str:
        return False

    return bool(re.match(r"^(0|[1-9]\d*)(\.\d+)?$", valor_str))


def validar_entero_rango(valor, minimo=1, maximo=None):
    """
    Valida que un valor sea un entero dentro de un rango.
    
    Parametros:
        valor (str): Valor a validar
        minimo (int): Valor minimo permitido
        maximo (int): Valor maximo permitido (None para sin limite)
    
    Retorna:
        bool: True si el valor es valido
    """
    if not valor.isdigit():
        return False
    num = int(valor)
    if num < minimo:
        return False
    if maximo and num > maximo:
        return False
    return True


def validar_alfabetico(valor_str):
    """
    Valida que un string contenga solo letras y espacios,
    y que no sea un string vacio o solo de espacios.
    
    Parametros:
        valor_str (str): String a validar
    
    Retorna:
        bool: True si es valido, False en caso contrario
    """
    if not isinstance(valor_str, str):
        return False

    if not valor_str.strip():
        return False

    for caracter in valor_str:
        if not (caracter.isalpha() or caracter.isspace()):
            return False

    return True


def validar_opcion_numerica(opcion, cantidad_opciones):
    """
    Valida que una opcion sea numerica y este en rango.
    
    Parametros:
        opcion (str): Opcion ingresada por el usuario
        cantidad_opciones (int): Cantidad total de opciones disponibles
    
    Retorna:
        bool: True si la opcion es valida
    """
    opcion_limpia = opcion.strip()
    
    # Verificar que sea un numero
    if not opcion_limpia.isdigit():
        return False
    
    # Convertir a entero y verificar el rango
    numero = int(opcion_limpia)
    return 1 <= numero <= cantidad_opciones


def validar_dni(dni):
    """
    Valida formato de DNI.
    
    Parametros:
        dni (str): DNI a validar
    
    Retorna:
        bool: True si el DNI tiene formato valido (7-8 digitos numericos)
    """
    return dni.isdigit() and 7 <= len(dni) <= 8


def validar_telefono(tel):
    """
    Valida formato de telefono.
    
    Parametros:
        tel (str): Telefono a validar
    
    Retorna:
        bool: True si el telefono tiene formato valido (minimo 7 caracteres, solo numeros y caracteres especiales permitidos)
    """
    if len(tel) < 7:
        return False
    
    caracteres_validos = "0123456789 -()+."
    for caracter in tel:
        if caracter not in caracteres_validos:
            return False
    return True


# --- Funciones de Validacion y Calculo de Fechas ---

def validar_fecha(fecha_str):
    """
    Valida que un string tenga formato dd/mm/aaaa y represente una fecha valida.
    Verifica dias validos segun el mes, considerando años bisiestos.
    
    Parametros:
        fecha_str (str): Fecha en formato "dd/mm/aaaa"
    
    Retorna:
        bool: True si la fecha es valida
    """
    if type(fecha_str) != str:
        return False

    patron_de_fecha = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/(19|20)\d{2}$"
    if not re.match(patron_de_fecha, fecha_str):
        return False

    partes = fecha_str.split('/')
    dia = int(partes[0])
    mes = int(partes[1])
    anio = int(partes[2])

    dias_por_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    es_bisiesto = (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)
    if es_bisiesto:
        dias_por_mes[1] = 29

    return dia <= dias_por_mes[mes - 1]


def validar_fecha_ingreso(fecha):
    """
    Valida formato de fecha usando regex (para reservas).
    
    Parametros:
        fecha (str): Fecha en formato "dd/mm/aaaa"
    
    Retorna:
        bool: True si la fecha tiene formato valido
    """
    patron_fecha = r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/(19|20)\d{2}$'
    return re.match(patron_fecha, fecha) is not None and validar_fecha(fecha)


def es_bisiesto(anio):
    """
    Verifica si un anio es bisiesto.
    
    Parametros:
        anio (int): Año a verificar
    
    Retorna:
        bool: True si el año es bisiesto
    """
    return (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)


def dias_en_mes(mes, anio):
    """
    Devuelve la cantidad de dias de un mes/anio.
    
    Parametros:
        mes (int): Numero de mes (1-12)
        anio (int): Año
    
    Retorna:
        int: Cantidad de dias del mes
    """
    if mes == 2:
        return 29 if es_bisiesto(anio) else 28
    elif mes in [4, 6, 9, 11]:
        return 30
    else:
        return 31


def fecha_a_dias(fecha_str):
    """
    Convierte una fecha dd/mm/yyyy a un numero total de dias desde el anio 0.
    Utiliza un algoritmo que suma los dias de todos los años anteriores,
    luego los meses completos del año actual, y finalmente los dias del mes actual.
    
    Parametros:
        fecha_str (str): Fecha en formato "dd/mm/aaaa"
    
    Retorna:
        int: Numero total de dias desde el año 0
    """
    partes = fecha_str.split('/')
    dia = int(partes[0])
    mes = int(partes[1])
    anio = int(partes[2])

    total_dias = 0
    
    # Sumar todos los dias de los años completos anteriores
    y = 1
    while y < anio:
        total_dias = total_dias + (366 if es_bisiesto(y) else 365)
        y = y + 1

    # Sumar los dias de los meses completos del año actual
    m = 1
    while m < mes:
        total_dias = total_dias + dias_en_mes(m, anio)
        m = m + 1

    # Sumar los dias del mes actual
    total_dias = total_dias + dia
    return total_dias


def comparar_fechas_string(fecha1_str, fecha2_str):
    """
    Compara dos fechas en formato dd/mm/yyyy.
    
    Parametros:
        fecha1_str (str): Primera fecha en formato "dd/mm/aaaa"
        fecha2_str (str): Segunda fecha en formato "dd/mm/aaaa"
    
    Retorna: int:
        - -1 si fecha1 < fecha2
        - 0 si son iguales
        - 1 si fecha1 > fecha2
        - None si hay error en las fechas
    """
    try:
        if not validar_fecha(fecha1_str) or not validar_fecha(fecha2_str):
            raise ValueError("Fecha invalida o mal formateada")

        partes1 = fecha1_str.split('/')
        partes2 = fecha2_str.split('/')

        fecha1_num = int(partes1[2]) * 10000 + int(partes1[1]) * 100 + int(partes1[0])
        fecha2_num = int(partes2[2]) * 10000 + int(partes2[1]) * 100 + int(partes2[0])

        if fecha1_num < fecha2_num:
            return -1
        return 1 if fecha1_num > fecha2_num else 0
    except (ValueError, IndexError):
        return None