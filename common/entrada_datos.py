from common.constantes import *
from common.validaciones import *
from common.interfaz import mostrar_mensaje_error


# ======================= INPUT BASICO CON VALIDACION =======================

def pedir_input_con_validacion(prompt, funcion_validacion=None, mensaje_error="Dato invalido", es_opcional=False):
    """
    Pide un input al usuario con validacion

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


# ======================= OPCIONES DE MENU =======================

def pedir_opcion_menu(cantidad_opciones, mensaje=""):
    """Solicita y valida una opcion de menu"""
    if not mensaje:
        mensaje = f"Seleccione una opcion (1-{cantidad_opciones})"

    while True:
        opcion = input(f"\n{COLOR_AMARILLO}{mensaje}: {COLOR_RESET}").strip()

        if validar_opcion_numerica(opcion, cantidad_opciones):
            return opcion
        else:
            mostrar_mensaje_error(f"Debe ingresar un numero del 1 al {cantidad_opciones}")


# ======================= DATOS ESPECIFICOS =======================

def pedir_dni():
    """Pide un DNI con validacion"""
    return pedir_input_con_validacion(
        "DNI (7-8 digitos)",
        validar_dni,
        "El DNI debe contener solo numeros y tener entre 7 y 8 digitos"
    )


def pedir_telefono():
    """Pide un telefono con validacion basica"""
    return pedir_input_con_validacion(
        "Telefono",
        validar_telefono,
        "El telefono debe tener al menos 7 caracteres y solo contener numeros, espacios, guiones y parentesis"
    )


def pedir_numero_entero(prompt, minimo=1, maximo=None):
    """Pide un numero entero con validacion de rango"""
    mensaje_error = f"Debe ser un numero entero mayor o igual a {minimo}" + (f" y menor o igual a {maximo}" if maximo else "")

    valor_str = pedir_input_con_validacion(
        prompt,
        lambda valor: validar_entero_rango(valor, minimo, maximo),
        mensaje_error
    )
    return int(valor_str)


def pedir_numero_decimal(prompt, minimo=0.01):
    """Pide un numero decimal con validacion"""
    return pedir_input_con_validacion(
        prompt,
        lambda valor: validar_numero_decimal(valor) and float(valor) >= minimo,
        f"Debe ser un numero decimal mayor o igual a {minimo}"
    )


def pedir_fecha(prompt="Fecha (dd/mm/yyyy)"):
    """Pide una fecha con validacion"""
    return pedir_input_con_validacion(
        prompt,
        validar_fecha,
        "La fecha debe tener formato dd/mm/yyyy y ser valida"
    )


def pedir_fecha_con_validacion(prompt):
    """Pide una fecha con validacion mejorada (para reservas)"""
    return pedir_input_con_validacion(
        f"{prompt} (dd/mm/yyyy)",
        validar_fecha_ingreso,
        "Fecha invalida. Use formato dd/mm/yyyy"
    )


def pedir_estado_departamento():
    """Pide el estado de un departamento con opciones predefinidas"""
    print(f"\n{COLOR_AMARILLO}Estados disponibles:")
    print(f"1. {ESTADO_DISPONIBLE}")
    print(f"2. {ESTADO_OCUPADO}")
    print(f"3. {ESTADO_MANTENIMIENTO}{COLOR_RESET}")

    opcion = pedir_input_con_validacion(
        "Seleccione estado (1-3)",
        lambda valor: valor in ["1", "2", "3"],
        "Debe seleccionar 1, 2 o 3"
    )

    return {
        "1": ESTADO_DISPONIBLE,
        "2": ESTADO_OCUPADO,
        "3": ESTADO_MANTENIMIENTO
    }[opcion]


def pedir_texto_simple(prompt, longitud_minima=1, longitud_maxima=100):
    """Pide un texto simple con validacion de longitud"""
    return pedir_input_con_validacion(
        prompt,
        lambda valor: longitud_minima <= len(valor.strip()) <= longitud_maxima,
        f"El texto debe tener entre {longitud_minima} y {longitud_maxima} caracteres"
    )


def pedir_texto_no_vacio(prompt):
    """Pide un texto que no puede estar vacio"""
    return pedir_input_con_validacion(
        prompt,
        lambda valor: len(valor.strip()) > 0,
        "Este campo no puede estar vacio"
    )


# ======================= SELECCION DE ELEMENTOS =======================

def seleccionar_elemento_de_lista(elementos, campo_id, mensaje):
    """Permite seleccionar un elemento de una lista por ID"""
    if not elementos:
        return None

    try:
        ids_validos = [elemento[campo_id] for elemento in elementos]
    except (TypeError, KeyError):
        ids_validos = [elemento[campo_id] for elemento in elementos]

    while True:
        entrada = input(f"\n{COLOR_CYAN}{mensaje}: {COLOR_RESET}").strip()

        if entrada.isdigit():
            id_seleccionado = int(entrada)

            if id_seleccionado in ids_validos:
                return id_seleccionado
            else:
                mostrar_mensaje_error("ID no valido. Seleccione un ID de la lista")
        else:
            mostrar_mensaje_error("Debe ingresar un numero entero")


# ======================= CONFIRMACIONES =======================

def confirmar_accion(mensaje="Esta seguro"):
    """Pide confirmacion al usuario"""
    while True:
        respuesta = input(f"{COLOR_AMARILLO}{mensaje}? (s/n): {COLOR_RESET}").lower().strip()
        if respuesta in ['s', 'si']:
            return True
        elif respuesta in ['n', 'no']:
            return False
        else:
            mostrar_mensaje_error("Ingrese 's' para Si o 'n' para No")


def confirmar_operacion(tipo_operacion, detalles=""):
    """Confirma una operacion especifica con detalles"""
    print(f"\n{COLOR_AMARILLO}--- CONFIRMACION DE {tipo_operacion.upper()} ---")
    if detalles:
        print(detalles)
    print(f"{COLOR_RESET}")

    return confirmar_accion(f"Confirmar {tipo_operacion.lower()}")


# ======================= VALIDACIONES CON LAMBDAS ESPECIALIZADAS =======================

def pedir_entero_positivo(prompt):
    """Pide un entero positivo"""
    return pedir_input_con_validacion(
        prompt,
        lambda valor: valor.isdigit() and int(valor) > 0,
        "Debe ingresar un numero entero positivo"
    )

def pedir_opcion_si_no(prompt):
    """Pide una confirmación simple si/no y retorna boolean"""
    respuesta = pedir_input_con_validacion(
        f"{prompt} (s/n)",
        lambda valor: valor.lower() in ['s', 'n', 'si', 'no'],
        "Responda con 's' para Si o 'n' para No"
    )
    return respuesta.lower() in ['s', 'si']

# ======================= PAUSA =======================

def pausar(mensaje="Presione Enter para continuar..."):
    """Pausa la ejecucion hasta que el usuario presione Enter"""
    input(f"\n{COLOR_CYAN}{mensaje}{COLOR_RESET}")


# ======================= VALIDACIONES AVANZADAS CON LAMBDAS =======================

def pedir_rango_numerico(prompt, minimo, maximo):
    """Pide un numero en un rango específico"""
    return int(pedir_input_con_validacion(
        f"{prompt} ({minimo}-{maximo})",
        lambda valor: valor.isdigit() and minimo <= int(valor) <= maximo,
        f"Debe ingresar un numero entre {minimo} y {maximo}"
    ))


def pedir_texto_alfabetico(prompt):
    """Pide un texto que solo contenga letras y espacios"""
    return pedir_input_con_validacion(
        prompt,
        lambda valor: all(c.isalpha() or c.isspace() for c in valor) and len(valor.strip()) > 0,
        "Solo se permiten letras y espacios"
    )


def pedir_seleccion_multiple(prompt, opciones_validas):
    """Permite seleccionar múltiples opciones de una lista"""
    opciones_str = ", ".join(opciones_validas)
    return pedir_input_con_validacion(
        f"{prompt} ({opciones_str})",
        lambda valor: valor.lower() in [op.lower() for op in opciones_validas],
        f"Seleccione una opción válida: {opciones_str}"
    )