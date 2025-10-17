from common.constantes import *


# ======================= HEADERS Y TITULOS =======================

def mostrar_header_principal(titulo):
    """Muestra un header principal con formato destacado"""
    longitud = len(titulo)
    if longitud < 70:
        longitud = 70
    print(f"\n{COLOR_AZUL}{'=' * longitud}")
    print(f"{titulo:^{longitud}}")
    print(f"{'=' * longitud}{COLOR_RESET}")


def mostrar_header_modulo(titulo):
    """Muestra un header de modulo con formato especifico"""
    longitud = 60
    print(f"\n{COLOR_MAGENTA}{'*' * longitud}")
    print(f"{titulo:^{longitud}}")
    print(f"{'*' * longitud}{COLOR_RESET}")


def mostrar_titulo_seccion(titulo):
    """Muestra un titulo de seccion con formato"""
    longitud = len(titulo)
    if longitud < 50:
        longitud = 50
    print(f"\n{COLOR_AZUL}{'=' * longitud}")
    print(f"{titulo:^{longitud}}")
    print(f"{'=' * longitud}{COLOR_RESET}")


def mostrar_subtitulo(subtitulo):
    """Muestra un subtitulo con formato"""
    longitud = len(subtitulo)
    if longitud < 35:
        longitud = 35
    print(f"\n{COLOR_CYAN}{LINEA_FINA * longitud}")
    print(f"{subtitulo:^{longitud}}")
    print(f"{LINEA_FINA * longitud}{COLOR_RESET}")


def mostrar_titulo(titulo):
    """Muestra un titulo con formato (version legacy de utils)"""
    longitud = len(titulo)
    borde = LINEA_GRUESA * (longitud + 4)
    print(f"\n{COLOR_AZUL}{borde}")
    print(f"  {titulo}")
    print(f"{borde}{COLOR_RESET}")


# ======================= MENUS =======================

def mostrar_menu_opciones(opciones, titulo, ancho):
    """Muestra un menu con opciones numeradas"""
    print(f"\n{COLOR_CYAN}{LINEA_FINA * ancho}")
    print(f"{titulo:^{ancho}}")
    print(f"{LINEA_FINA * ancho}{COLOR_RESET}")

    i = 0
    while i < len(opciones):
        print(f"{COLOR_VERDE}{i + 1}.{COLOR_RESET} {opciones[i]}")
        i = i + 1

    print(f"{COLOR_CYAN}{LINEA_FINA * ancho}{COLOR_RESET}")


def mostrar_opciones_menu(opciones, titulo="Menu"):
    """Muestra opciones de menu de forma elegante (version legacy)"""
    mostrar_subtitulo(titulo)
    i = 0
    while i < len(opciones):
        print(f"{COLOR_CYAN}{i + 1:2d}. {COLOR_RESET}{opciones[i]}")
        i = i + 1
    mostrar_separador()


# ======================= MENSAJES =======================

def mostrar_mensaje_exito(mensaje):
    """Muestra un mensaje de exito"""
    print(f"\n{COLOR_VERDE}{MARCA_OK} {mensaje}{COLOR_RESET}")


def mostrar_mensaje_error(mensaje):
    """Muestra un mensaje de error"""
    print(f"\n{COLOR_ROJO}{MARCA_ERROR} {mensaje}{COLOR_RESET}")


def mostrar_mensaje_info(mensaje):
    """Muestra un mensaje informativo"""
    print(f"\n{COLOR_AMARILLO}ℹ {mensaje}{COLOR_RESET}")


# ======================= LISTAS DE DATOS =======================

def mostrar_lista_clientes_activos(clientes_lista):
    """Muestra lista de clientes con formato especifico"""
    print(f"\n{COLOR_AMARILLO}--- CLIENTES ACTIVOS DISPONIBLES ---{COLOR_RESET}")

    for cliente in clientes_lista:
        print(f"{COLOR_VERDE}ID {cliente[ID_CLIENTE]:5d}{COLOR_RESET} - "
              f"{cliente[NOMBRE_CLIENTE]} {cliente[APELLIDO_CLIENTE]} "
              f"(DNI: {cliente[DNI_CLIENTE]})")

    return True


def mostrar_lista_departamentos(departamentos_lista, titulo):
    """Muestra lista de departamentos con formato especifico"""
    print(f"\n{COLOR_AMARILLO}--- {titulo} ---{COLOR_RESET}")

    i = 0
    while i < len(departamentos_lista):
        depto = departamentos_lista[i]
        print(f"{COLOR_VERDE}ID {depto[ID_DEPARTAMENTO]:5d}{COLOR_RESET} - "
              f"{depto[UBICACION_DEPARTAMENTO]} | "
              f"{depto[AMBIENTES_DEPARTAMENTO]} amb. | "
              f"Cap: {depto[CAPACIDAD_DEPARTAMENTO]} pers. | "
              f"${depto[PRECIO_DEPARTAMENTO]:.2f}/noche")
        i = i + 1

    return departamentos_lista


# ======================= TABLAS FORMATEADAS =======================

def mostrar_tabla(titulo, datos, columnas, anchos):
    """
    Muestra datos en formato de tabla

    titulo: Titulo de la tabla
    datos: Lista de datos a mostrar
    columnas: Lista con nombres de columnas
    anchos: Lista con anchos de cada columna
    """
    # Calcular ancho total
    ancho_total = 0
    i = 0
    while i < len(anchos):
        ancho_total = ancho_total + anchos[i]
        i = i + 1
    ancho_total = ancho_total + len(anchos) - 1

    print(f"\n{COLOR_AZUL}{'=' * ancho_total}")
    print(f"{titulo:^{ancho_total}}")
    print(f"{'=' * ancho_total}{COLOR_RESET}")

    # Header de columnas
    header = ""
    i = 0
    while i < len(columnas):
        col = columnas[i]
        ancho = anchos[i]
        header = header + f"{col:<{ancho}}"
        if i < len(columnas) - 1:
            header = header + " "
        i = i + 1
    print(f"\n{COLOR_MAGENTA}{header}{COLOR_RESET}")
    print(f"{COLOR_CYAN}{'-' * ancho_total}{COLOR_RESET}")

    # Datos
    i = 0
    while i < len(datos):
        fila = datos[i]
        linea = ""
        j = 0
        while j < len(fila):
            valor = str(fila[j])
            ancho = anchos[j]
            # Truncar si es muy largo
            if len(valor) >= ancho:
                valor = valor[:ancho - 1]
            linea = linea + f"{valor:<{ancho}}"
            if j < len(fila) - 1:
                linea = linea + " "
            j = j + 1
        print(linea)
        i = i + 1

    print(f"\n{COLOR_CYAN}Total de registros: {COLOR_VERDE}{len(datos)}{COLOR_RESET}")


# ======================= ESTADOS Y COLORES =======================

def obtener_color_estado(estado):
    """Retorna el color apropiado segun el estado"""
    if estado == ESTADO_ACTIVO or estado == ESTADO_DISPONIBLE:
        return COLOR_VERDE
    elif estado == ESTADO_CANCELADO or estado == ESTADO_OCUPADO:
        return COLOR_AMARILLO
    elif estado == ESTADO_ELIMINADO or estado == ESTADO_MANTENIMIENTO:
        return COLOR_ROJO
    else:
        return COLOR_RESET


def formatear_estado(estado):
    """Formatea un estado con su color correspondiente"""
    color = obtener_color_estado(estado)
    return f"{color}{estado}{COLOR_RESET}"


# ======================= SEPARADORES =======================

def mostrar_separador(caracter=LINEA_FINA, longitud=60, color=COLOR_CYAN):
    """Muestra un separador visual"""
    print(f"\n{color}{caracter * longitud}{COLOR_RESET}")


def separador_operaciones():
    """Separador especifico entre operaciones"""
    print(f"\n{COLOR_CYAN}{'*' * 70}{COLOR_RESET}")


# ======================= MENSAJES ESPECIALES =======================

def mostrar_despedida():
    """Muestra mensaje de despedida del sistema"""
    print(f"\n{COLOR_VERDE}{'=' * 50}")
    print(f"{'GRACIAS POR USAR EL SISTEMA':^50}")
    print(f"{'Hasta la proxima!':^50}")
    print(f"{'=' * 50}{COLOR_RESET}\n")