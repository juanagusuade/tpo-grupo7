import re


# --- Funciones de Validacion General ---

def campos_son_validos(*campos):
    """
    Verifica que los campos no sean None ni vacios.
    Devuelve True si todos los campos son validos.
    Devuelve False si al menos uno es None o vacio.
    """
    i = 0
    while i < len(campos):
        campo = campos[i]
        if campo is None:
            return False

        # Verificar si es string vacio
        if type(campo) == str and len(campo.strip()) == 0:
            return False

        # Verificar si es lista vacia
        if type(campo) == list and len(campo) == 0:
            return False

        i = i + 1

    return True


def validar_numero_decimal(valor_str):
    """Valida que un string represente un numero decimal positivo"""
    if type(valor_str) != str:
        return False

    # Regex para matchear decimales positivos
    return bool(re.fullmatch(r"(0|[1-9]\d*)(\.\d+)?", valor_str))


def validar_entero_rango(valor, minimo=1, maximo=None):
    """Valida que un valor sea un entero dentro de un rango"""
    if not valor.isdigit():
        return False
    num = int(valor)
    if num < minimo:
        return False
    if maximo and num > maximo:
        return False
    return True


def validar_opcion_numerica(opcion, cantidad_opciones):
    """Valida que una opcion sea numerica y este en rango"""
    patron = f'^[1-{cantidad_opciones}]$'
    return re.match(patron, opcion.strip()) is not None


def validar_dni(dni):
    """Valida formato de DNI"""
    # DNI debe ser numerico y tener entre 7 y 8 digitos
    return dni.isdigit() and 7 <= len(dni) <= 8


def validar_telefono(tel):
    """Valida formato de telefono"""
    # Telefono puede contener numeros, espacios, guiones y parentesis
    caracteres_validos = "0123456789 -()+."
    if len(tel) < 7:
        return False

    # Verificar caracter por caracter
    i = 0
    while i < len(tel):
        if tel[i] not in caracteres_validos:
            return False
        i = i + 1
    return True


# --- Funciones de Validacion y Calculo de Fechas ---

def validar_fecha(fecha_str):
    """
    Valida que un string tenga formato dd/mm/aaaa y represente una fecha valida.
    """
    if type(fecha_str) != str:
        return False

    patron = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/(19|20)\d{2}$"
    if not re.match(patron, fecha_str):
        return False

    partes = fecha_str.split('/')
    dia = int(partes[0])
    mes = int(partes[1])
    anio = int(partes[2])

    dias_por_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    es_bisiesto_flag = (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)
    if es_bisiesto_flag:
        dias_por_mes[1] = 29

    return dia <= dias_por_mes[mes - 1]


def validar_fecha_ingreso(fecha):
    """Valida formato de fecha usando regex (para reservas)"""
    patron_fecha = r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/(19|20)\d{2}$'
    return re.match(patron_fecha, fecha) is not None and validar_fecha(fecha)


def es_bisiesto(anio):
    """Verifica si un anio es bisiesto."""
    return (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)


def dias_en_mes(mes, anio):
    """Devuelve la cantidad de dias de un mes/anio."""
    if mes == 2:
        return 29 if es_bisiesto(anio) else 28
    elif mes in [4, 6, 9, 11]:
        return 30
    else:
        return 31


def fecha_a_dias(fecha_str):
    """Convierte una fecha dd/mm/yyyy a un numero total de dias desde el anio 0."""
    partes = fecha_str.split('/')
    dia = int(partes[0])
    mes = int(partes[1])
    anio = int(partes[2])

    total_dias = 0
    y = 1
    while y < anio:
        total_dias = total_dias + (366 if es_bisiesto(y) else 365)
        y = y + 1

    m = 1
    while m < mes:
        total_dias = total_dias + dias_en_mes(m, anio)
        m = m + 1

    total_dias = total_dias + dia
    return total_dias