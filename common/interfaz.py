from common.constantes import *
import common.entrada_datos as input_datos


# ======================= HEADERS Y TITULOS =======================

def mostrar_titulo_decorado(titulo, caracter='=', longitud_minima=50, color=COLOR_AZUL):
    """Funcion base para mostrar titulos con decoracion"""
    longitud = len(titulo)
    if longitud < longitud_minima:
        longitud = longitud_minima

    linea = caracter * longitud
    print(f"\n{color}{linea}")
    print(f"{titulo:^{longitud}}")
    print(f"{linea}{COLOR_RESET}")


def mostrar_header_principal(titulo):
    mostrar_titulo_decorado(titulo, '=', 70, COLOR_AZUL)


def mostrar_header_modulo(titulo):
    mostrar_titulo_decorado(titulo, '*', 60, COLOR_MAGENTA)


def mostrar_titulo_seccion(titulo):
    mostrar_titulo_decorado(titulo, '=', 50, COLOR_AZUL)


def mostrar_subtitulo(subtitulo):
    mostrar_titulo_decorado(subtitulo, LINEA_FINA, 35, COLOR_CYAN)

# ======================= MENUS =======================

def mostrar_menu_opciones(opciones, titulo, ancho):
    """Muestra un menu con opciones numeradas"""
    print(f"\n{COLOR_CYAN}{LINEA_FINA * ancho}")
    print(f"{titulo:^{ancho}}")
    print(f"{LINEA_FINA * ancho}{COLOR_RESET}")

    for i, opcion in enumerate(opciones):
        print(f"{COLOR_VERDE}{i + 1}.{COLOR_RESET} {opcion}")

    print(f"{COLOR_CYAN}{LINEA_FINA * ancho}{COLOR_RESET}")


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
    """Muestra lista de clientes"""
    print(f"\n{COLOR_AMARILLO}--- CLIENTES ACTIVOS DISPONIBLES ---{COLOR_RESET}")

    for cliente in clientes_lista:
        print(f"{COLOR_VERDE}ID {cliente[ID_CLIENTE]:5d}{COLOR_RESET} - "
              f"{cliente[NOMBRE_CLIENTE]} {cliente[APELLIDO_CLIENTE]} "
              f"(DNI: {cliente[DNI_CLIENTE]})")

    return True


def mostrar_lista_departamentos(departamentos_lista, titulo):
    """Muestra lista de departamentos con formato especifico"""
    print(f"\n{COLOR_AMARILLO}--- {titulo} ---{COLOR_RESET}")

    for depto in departamentos_lista:
        print(f"{COLOR_VERDE}ID {depto[ID_DEPARTAMENTO]:5d}{COLOR_RESET} - "
              f"{depto[UBICACION_DEPARTAMENTO]} | "
              f"{depto[AMBIENTES_DEPARTAMENTO]} amb. | "
              f"Cap: {depto[CAPACIDAD_DEPARTAMENTO]} pers. | "
              f"${depto[PRECIO_DEPARTAMENTO]:.2f}/noche")

    return departamentos_lista


def mostrar_departamento_detallado(dep):
    """Muestra el detalle de un departamento."""
    idd = dep.get(ID_DEPARTAMENTO, "N/A")
    ubicacion = dep.get(UBICACION_DEPARTAMENTO, "N/A")
    ambientes = dep.get(AMBIENTES_DEPARTAMENTO, "N/A")
    capacidad = dep.get(CAPACIDAD_DEPARTAMENTO, "N/A")
    estado = dep.get(ESTADO_DEPARTAMENTO, "N/A")
    precio = dep.get(PRECIO_DEPARTAMENTO, 0.0)
    activo = dep.get(ACTIVO_DEPARTAMENTO, False)

    etiqueta_activo = f"{COLOR_VERDE}ACTIVO{COLOR_RESET}" if activo else f"{COLOR_ROJO}INACTIVO{COLOR_RESET}"

    # Truncar ubicacion si es muy larga
    if len(ubicacion) > 24:
        ubicacion = ubicacion[:24] + "…"

    # ID (6) | Ubicacion (25) | Amb (5) | Cap (5) | Precio (10) | Estado (13) | Activo (8)
    print(f"{COLOR_VERDE}ID {idd:<5d}{COLOR_RESET} | "
          f"{ubicacion:<25s} | "
          f"{str(ambientes):>3s} amb | "
          f"{str(capacidad):>3s} cap | "
          f"${precio:>8.2f} | "
          f"{estado:<13s} | "
          f"{etiqueta_activo}")


def mostrar_lista_departamentos_detallada(lista: list, titulo="LISTA DE DEPARTAMENTOS"):
    """Muestra una lista de departamentos con detalles ."""
    if not lista:
        mostrar_mensaje_info("No hay departamentos cargados.")
        return

    print(f"\n{COLOR_AMARILLO}--- {titulo} ---{COLOR_RESET}")

    # encabezado de columnas
    ancho_total = 88
    header = (
        f"{COLOR_MAGENTA}ID      | "
        f"UBICACION                 | "
        f"AMB   | "
        f"CAP   | "
        f"PRECIO      | "
        f"ESTADO        | "
        f"ACTIVO{COLOR_RESET}"
    )
    print(header)
    print(f"{COLOR_CYAN}{LINEA_FINA * ancho_total}{COLOR_RESET}")

    for depto in lista:
        mostrar_departamento_detallado(depto)

    print(f"{COLOR_CYAN}{LINEA_FINA * ancho_total}{COLOR_RESET}")

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
    for ancho in anchos:
        ancho_total = ancho_total + ancho
    ancho_total = ancho_total + len(anchos) - 1

    print(f"\n{COLOR_AZUL}{'=' * ancho_total}")
    print(f"{titulo:^{ancho_total}}")
    print(f"{'=' * ancho_total}{COLOR_RESET}")

    # Header de columnas
    header = ""
    for i, col in enumerate(columnas):
        ancho = anchos[i]
        header = header + f"{col:<{ancho}}"
        if i < len(columnas) - 1:
            header = header + " "
    print(f"\n{COLOR_MAGENTA}{header}{COLOR_RESET}")
    print(f"{COLOR_CYAN}{'-' * ancho_total}{COLOR_RESET}")

    # Datos
    for fila in datos:
        linea = ""
        for j, valor_original in enumerate(fila):
            valor = str(valor_original)
            ancho = anchos[j]
            # Truncar si es muy largo
            if len(valor) >= ancho:
                valor = valor[:ancho - 1]
            linea = linea + f"{valor:<{ancho}}"
            if j < len(fila) - 1:
                linea = linea + " "
        print(linea)

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


# ======================= SELECCION DE UI (NUEVO) =======================

def mostrar_y_seleccionar_cliente(clientes_lista):
    """
    Muestra la lista de clientes y pide al usuario que elija uno.
    Retorna el ID del cliente seleccionado.
    """
    if not clientes_lista:
        return None

    mostrar_lista_clientes_activos(clientes_lista)

    return input_datos.seleccionar_elemento_de_lista(
        clientes_lista,
        ID_CLIENTE,
        "Ingrese el ID del cliente"
    )


def mostrar_y_seleccionar_departamento(departamentos_lista, titulo):
    """
    Muestra la lista de departamentos y pide al usuario que elija uno.
    Retorna el ID del depto seleccionado.
    """
    if not departamentos_lista:
        return None

    mostrar_lista_departamentos(departamentos_lista, titulo)

    return input_datos.seleccionar_elemento_de_lista(
        departamentos_lista,
        ID_DEPARTAMENTO,
        "Ingrese el ID del departamento"
    )