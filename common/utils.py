import random
from common.constantes import *


def generar_id_unico_lista(lista):
    """
    Genera un ID unico para lista de listas donde el ID esta en posicion 0.
    Para usar con reservas
    """
    while True:
        id_generado = random.randint(10000, 99999)
        existe_id = False
        i = 0
        while i < len(lista):
            if lista[i][0] == id_generado:
                existe_id = True
                i = len(lista)
            else:
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
        while i < len(lista):
            if lista[i][clave_id] == id_generado:
                existe_id = True
                i = len(lista)
            else:
                i = i + 1
        if not existe_id:
            return id_generado


def validar_campos(*campos):
    """
    Verifica que los campos no sean None ni vacios.
    Devuelve True si todos los campos son validos.
    Devuelve False si al menos uno es None o vacio.
    """
    for campo in campos:
        if campo is None:
            return False
        if isinstance(campo, str) and len(campo.strip()) == 0:
            return False
        if isinstance(campo, list) and len(campo) == 0:
            return False
    return True


def validar_fecha(fecha_str):
    """
    Valida que un string tenga formato dd/mm/aaaa y represente una fecha valida.
    """
    if not isinstance(fecha_str, str):
        return False

    if not fecha_str.strip():
        return False

    if len(fecha_str) != 10:
        return False

    if fecha_str[2] != '/' or fecha_str[5] != '/':
        return False

    partes = fecha_str.split('/')
    if len(partes) != 3:
        return False

    dia_str, mes_str, anio_str = partes

    if not (dia_str.isdigit() and mes_str.isdigit() and anio_str.isdigit()):
        return False

    dia = int(dia_str)
    mes = int(mes_str)
    anio = int(anio_str)

    if mes < 1 or mes > 12:
        return False

    if dia < 1 or dia > 31:
        return False

    if anio < 1900 or anio > 2100:
        return False

    dias_por_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    es_bisiesto = (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)
    if es_bisiesto:
        dias_por_mes[1] = 29

    if dia > dias_por_mes[mes - 1]:
        return False

    return True


def validar_numero_entero(valor_str):
    """Valida que un string represente un numero entero positivo"""
    if not isinstance(valor_str, str):
        return False

    if not valor_str.strip():
        return False

    if not valor_str.isdigit():
        return False

    return int(valor_str) > 0


def validar_numero_decimal(valor_str):
    """Valida que un string represente un numero decimal positivo"""
    if not isinstance(valor_str, str):
        return False

    if not valor_str.strip():
        return False

    if valor_str.count('.') > 1:
        return False

    partes = valor_str.split('.')
    if len(partes) == 1:
        return partes[0].isdigit() and int(partes[0]) > 0
    elif len(partes) == 2:
        return partes[0].isdigit() and partes[1].isdigit() and int(partes[0]) >= 0

    return False

def pausar():
    """Pausa la ejecucion hasta que el usuario presione Enter"""
    input(f"\n{COLOR_CYAN}Presione Enter para continuar...{COLOR_RESET}")


def mostrar_titulo(titulo):
    """Muestra un titulo con formato"""
    longitud = len(titulo)
    borde = LINEA_GRUESA * (longitud + 4)
    print(f"\n{COLOR_AZUL}{borde}")
    print(f"  {titulo}")
    print(f"{borde}{COLOR_RESET}")


def mostrar_subtitulo(subtitulo):
    """Muestra un subtitulo con formato"""
    longitud = len(subtitulo)
    borde = LINEA_FINA * (longitud + 4)
    print(f"\n{COLOR_MAGENTA}{borde}")
    print(f"  {subtitulo}")
    print(f"{borde}{COLOR_RESET}")


def mostrar_mensaje_exito(mensaje):
    """Muestra un mensaje de exito"""
    print(f"\n{COLOR_VERDE}{MARCA_OK} {mensaje}{COLOR_RESET}")


def mostrar_mensaje_error(mensaje):
    """Muestra un mensaje de error"""
    print(f"\n{COLOR_ROJO}{MARCA_ERROR} {mensaje}{COLOR_RESET}")


def mostrar_mensaje_info(mensaje):
    """Muestra un mensaje informativo"""
    print(f"\n{COLOR_AMARILLO}ℹ {mensaje}{COLOR_RESET}")


def pedir_input_con_validacion(prompt, funcion_validacion=None, mensaje_error="Dato invalido", es_opcional=False):
    """
    Pide un input al usuario con validacion en tiempo real

    prompt: El texto a mostrar al usuario
    funcion_validacion: Funcion que valida el input
    mensaje_error: Mensaje a mostrar si la validacion falla
    es_opcional: Si True, permite valores vacios
    """
    while True:
        valor = input(f"{COLOR_CYAN}{FLECHA} {prompt}: {COLOR_RESET}").strip()

        # Si es opcional y esta vacio, retorna None
        if es_opcional and not valor:
            return None

        # Si no es opcional y esta vacio, pide de nuevo
        if not valor and not es_opcional:
            mostrar_mensaje_error("Este campo es obligatorio")
            continue

        # Si hay funcion de validacion, usarla
        if funcion_validacion:
            if funcion_validacion(valor):
                return valor
            else:
                mostrar_mensaje_error(mensaje_error)
        else:
            return valor


def pedir_dni():
    """Pide un DNI con validacion"""

    def validar_dni(dni):
        # DNI debe ser numerico y tener entre 7 y 8 digitos
        return dni.isdigit() and 7 <= len(dni) <= 8

    return pedir_input_con_validacion(
        "DNI (7-8 digitos)",
        validar_dni,
        "El DNI debe contener solo numeros y tener entre 7 y 8 digitos"
    )


def pedir_telefono():
    """Pide un telefono con validacion basica"""

    def validar_telefono(tel):
        # Telefono puede contener numeros, espacios, guiones y parentesis
        caracteres_validos = "0123456789 -()+."
        return len(tel) >= 7 and all(c in caracteres_validos for c in tel)

    return pedir_input_con_validacion(
        "Telefono",
        validar_telefono,
        "El telefono debe tener al menos 7 caracteres y solo contener numeros, espacios, guiones y parentesis"
    )


def pedir_numero_entero(prompt, minimo=1, maximo=None):
    """Pide un numero entero con validacion de rango"""

    def validar_entero(valor):
        if not valor.isdigit():
            return False
        num = int(valor)
        if num < minimo:
            return False
        if maximo and num > maximo:
            return False
        return True

    mensaje_error = f"Debe ser un numero entero mayor o igual a {minimo}"
    if maximo:
        mensaje_error += f" y menor o igual a {maximo}"

    valor_str = pedir_input_con_validacion(prompt, validar_entero, mensaje_error)
    return int(valor_str)


def pedir_numero_decimal(prompt, minimo=0.01):
    """Pide un numero decimal con validacion"""

    mensaje_error = f"Debe ser un numero decimal mayor o igual a {minimo}"
    valor_str = pedir_input_con_validacion(
        prompt,
        lambda valor: validar_numero_decimal(valor) and float(valor) >= minimo,
        mensaje_error
    )
    return float(valor_str)

def pedir_fecha(prompt="Fecha (dd/mm/yyyy)"):
    """Pide una fecha con validacion"""
    return pedir_input_con_validacion(
        prompt,
        validar_fecha,
        "La fecha debe tener formato dd/mm/yyyy y ser valida"
    )


def pedir_estado_departamento():
    """Pide el estado de un departamento con opciones predefinidas"""
    print(f"\n{COLOR_AMARILLO}Estados disponibles:")
    print(f"1. {ESTADO_DISPONIBLE}")
    print(f"2. {ESTADO_OCUPADO}")
    print(f"3. {ESTADO_MANTENIMIENTO}{COLOR_RESET}")

    def validar_opcion_estado(valor):
        return valor in ["1", "2", "3"]

    opcion = pedir_input_con_validacion(
        "Seleccione estado (1-3)",
        validar_opcion_estado,
        "Debe seleccionar 1, 2 o 3"
    )

    estados = {
        "1": ESTADO_DISPONIBLE,
        "2": ESTADO_OCUPADO,
        "3": ESTADO_MANTENIMIENTO
    }

    return estados[opcion]


def confirmar_accion(mensaje="Esta seguro"):
    """Pide confirmacion al usuario"""
    respuesta = input(f"{COLOR_AMARILLO}{mensaje}? (s/n): {COLOR_RESET}").lower().strip()
    return respuesta == 's' or respuesta == 'si'


def mostrar_separador():
    """Muestra un separador visual"""
    print(f"\n{COLOR_CYAN}{LINEA_FINA * 60}{COLOR_RESET}")


def mostrar_opciones_menu(opciones, titulo="Menu"):
    """Muestra opciones de menu de forma elegante"""
    mostrar_subtitulo(titulo)
    for i, opcion in enumerate(opciones, 1):
        print(f"{COLOR_CYAN}{i:2d}. {COLOR_RESET}{opcion}")
    mostrar_separador()










