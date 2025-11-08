import re

# ======================= FUNCIONES DE MANEJO DE FECHAS =======================
# Todas las funciones relacionadas con validacion, comparacion y calculo de fechas

# Constante para el formato de fecha
FORMATO_FECHA = "dd/mm/aaaa"
PATRON_FECHA = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/(19|20)\d{2}$"


def parsear_fecha(fecha_str):
    """
    Parsea una fecha en formato dd/mm/aaaa y retorna sus componentes.
    
    Parametros:
        fecha_str (str): Fecha en formato "dd/mm/aaaa"
    
    Retorna:
        tupla: (dia, mes, anio) como int, o None si el formato es invalido
    """
    if not isinstance(fecha_str, str) or '/' not in fecha_str:
        return None
    
    try:
        partes = fecha_str.split('/')
        if len(partes) != 3:
            return None
        dia = int(partes[0])
        mes = int(partes[1])
        anio = int(partes[2])
        return (dia, mes, anio)
    except (ValueError, IndexError):
        return None


def formatear_fecha(dia, mes, anio):
    """
    Formatea componentes de fecha a string dd/mm/aaaa.
    
    Parametros:
        dia (int): Dia del mes
        mes (int): Mes (1-12)
        anio (int): Año
    
    Retorna:
        str: Fecha formateada como "dd/mm/aaaa"
    """
    return f"{dia:02d}/{mes:02d}/{anio:04d}"


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


def validar_fecha(fecha_str):
    """
    Valida que un string tenga formato dd/mm/aaaa y represente una fecha valida.
    Verifica dias validos segun el mes, considerando años bisiestos.
    
    Parametros:
        fecha_str (str): Fecha en formato "dd/mm/aaaa"
    
    Retorna:
        bool: True si la fecha es valida
    """
    if not isinstance(fecha_str, str):
        return False

    # Validar formato con regex
    if not re.match(PATRON_FECHA, fecha_str):
        return False

    # Parsear componentes
    fecha_parseada = parsear_fecha(fecha_str)
    if not fecha_parseada:
        return False
    
    dia, mes, anio = fecha_parseada

    # Validar que el dia no exceda los dias del mes
    return dia <= dias_en_mes(mes, anio)


def fecha_a_dias(fecha_str):
    """
    Convierte una fecha dd/mm/aaaa a un numero total de dias desde el anio 0.
    
    Parametros:
        fecha_str (str): Fecha en formato "dd/mm/aaaa"
    
    Retorna:
        int: Numero total de dias desde el año 0
    """
    fecha_parseada = parsear_fecha(fecha_str)
    if not fecha_parseada:
        return 0
    
    dia, mes, anio = fecha_parseada

    # Calcula años normales + años bisiestos adicionales
    anios_completos = anio - 1
    dias_anios = anios_completos * 365
    
    # Sumar dias extra por años bisiestos (cada 4 años, menos los centenarios que no son múltiplos de 400)
    bisiestos = anios_completos // 4 - anios_completos // 100 + anios_completos // 400
    dias_anios += bisiestos

    # Sumar los dias de los meses completos del año actual
    dias_meses = sum(dias_en_mes(m, anio) for m in range(1, mes))

    # Sumar los dias del mes actual
    return dias_anios + dias_meses + dia


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

        fecha1 = parsear_fecha(fecha1_str)
        fecha2 = parsear_fecha(fecha2_str)
        
        if not fecha1 or not fecha2:
            return None

        dia1, mes1, anio1 = fecha1
        dia2, mes2, anio2 = fecha2
        
        # Comparar primero por año, luego mes, finalmente día
        if anio1 < anio2:
            return -1
        if anio1 > anio2:
            return 1
        
        if mes1 < mes2:
            return -1
        if mes1 > mes2:
            return 1
        
        if dia1 < dia2:
            return -1
        if dia1 > dia2:
            return 1
        
        return 0  # Son iguales
    except (ValueError, IndexError):
        return None


def diferencia_dias(fecha_inicio_str, fecha_fin_str):
    """
    Calcula la diferencia en dias entre dos fechas.
    
    Parametros:
        fecha_inicio_str (str): Fecha inicial en formato "dd/mm/aaaa"
        fecha_fin_str (str): Fecha final en formato "dd/mm/aaaa"
    
    Retorna:
        int: Cantidad de dias entre las fechas (puede ser negativo si fecha_fin < fecha_inicio)
        None si hay error en las fechas
    """
    try:
        if not validar_fecha(fecha_inicio_str) or not validar_fecha(fecha_fin_str):
            return None
        
        dias_inicio = fecha_a_dias(fecha_inicio_str)
        dias_fin = fecha_a_dias(fecha_fin_str)
        
        return dias_fin - dias_inicio
    except (ValueError, TypeError):
        return None


def sumar_dias(fecha_str, cantidad_dias):
    """
    Suma una cantidad de dias a una fecha.
    
    Parametros:
        fecha_str (str): Fecha base en formato "dd/mm/aaaa"
        cantidad_dias (int): Cantidad de dias a sumar (puede ser negativo para restar)
    
    Retorna:
        str: Nueva fecha en formato "dd/mm/aaaa", o None si hay error
    """
    try:
        if not validar_fecha(fecha_str):
            return None
        
        fecha = parsear_fecha(fecha_str)
        if not fecha:
            return None
        
        dia, mes, anio = fecha
        
        # Sumar/restar dias
        dia += cantidad_dias
        
        # Ajustar mientras el dia sea invalido
        while dia > dias_en_mes(mes, anio):
            dia -= dias_en_mes(mes, anio)
            mes += 1
            if mes > 12:
                mes = 1
                anio += 1
        
        while dia < 1:
            mes -= 1
            if mes < 1:
                mes = 12
                anio -= 1
            dia += dias_en_mes(mes, anio)
        
        return formatear_fecha(dia, mes, anio)
    except (ValueError, TypeError):
        return None


# ======================= FUNCIONES DE VALIDACION GENERAL =======================

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