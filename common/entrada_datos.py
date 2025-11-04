from common.constantes import *
from common.validaciones import *


# ======================= INPUT BASICO CON VALIDACION =======================

def pedir_input_con_validacion(prompt, funcion_validacion=None, mensaje_error="Dato invalido", es_opcional=False):
    """
    Pide un input al usuario con validacion

    prompt: El texto a mostrar al usuario
    funcion_validacion: Funcion que valida el input
    mensaje_error: Mensaje a mostrar si la validacion falla
    es_opcional: Si True, permite valores vacios
    """
    from common.interfaz import mostrar_mensaje_error
    
    while True:
        valor = input(f"{COLOR_CYAN}{FLECHA} {prompt}: {COLOR_RESET}").strip()

        if es_opcional and not valor:
            return None

        if not valor and not es_opcional:
            mostrar_mensaje_error("Este campo es obligatorio")
        elif funcion_validacion:
            if funcion_validacion(valor):
                return valor
            else:
                mostrar_mensaje_error(mensaje_error)
        else:
            return valor


# ======================= OPCIONES DE MENU =======================

def pedir_opcion_menu(cantidad_opciones, mensaje=""):
    """Solicita y valida una opcion de menu"""
    from common.interfaz import mostrar_mensaje_error
    
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

def pedir_texto_alfabetico(prompt):
    """Pide un texto que solo contenga letras y espacios"""
    return pedir_input_con_validacion(
        prompt,
        validar_alfabetico,
        "Solo se permiten letras y espacios"
    )

# ======================= SELECCION DE ELEMENTOS =======================

def seleccionar_elemento_de_lista(elementos, campo_id, mensaje):
    """Permite seleccionar un elemento de una lista por ID usando pedir_input_con_validacion."""
    if not elementos:
        return None

    ids_validos = {elemento[campo_id] for elemento in elementos}

    id_seleccionado_str = pedir_input_con_validacion(
        prompt=mensaje,
        funcion_validacion=lambda valor: valor.isdigit() and int(valor) in ids_validos,
        mensaje_error="ID no valido. Seleccione un ID de la lista"
    )
    return int(id_seleccionado_str)
# ======================= CONFIRMACIONES =======================

def confirmar_accion(mensaje="Esta seguro"):
    """Pide confirmacion al usuario"""
    from common.interfaz import mostrar_mensaje_error
    
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


# ======================= PAUSA =======================

def pausar(mensaje="Presione Enter para continuar..."):
    """Pausa la ejecucion hasta que el usuario presione Enter"""
    input(f"\n{COLOR_CYAN}{mensaje}{COLOR_RESET}")