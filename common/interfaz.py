from common.constantes import *
import common.entrada_datos as input_datos


# ======================= HEADERS Y TITULOS =======================

def mostrar_header_principal(titulo):
    """Muestra el header principal con estilo destacado"""
    longitud = 72
    print(f"\n{COLOR_AZUL}{'#' * longitud}")
    print(f"#{COLOR_RESET}{' ' * (longitud - 2)}{COLOR_AZUL}#")
    print(f"#{COLOR_RESET}{titulo:^{longitud - 2}}{COLOR_AZUL}#")
    print(f"#{COLOR_RESET}{' ' * (longitud - 2)}{COLOR_AZUL}#")
    print(f"{'#' * longitud}{COLOR_RESET}\n")


def mostrar_header_modulo(titulo):
    """Muestra el header de modulo con estilo destacado"""
    longitud = 62
    print(f"\n{COLOR_MAGENTA}+{'-' * (longitud - 2)}+")
    print(f"|{COLOR_RESET}{titulo:^{longitud - 2}}{COLOR_MAGENTA}|")
    print(f"+{'-' * (longitud - 2)}+{COLOR_RESET}\n")


def mostrar_titulo_seccion(titulo):
    """Muestra titulo de seccion"""
    longitud = 52
    print(f"\n{COLOR_CYAN}[{' ' * (longitud - 2)}]")
    print(f"[{COLOR_RESET}{titulo:^{longitud - 2}}{COLOR_CYAN}]")
    print(f"[{'-' * (longitud - 2)}]{COLOR_RESET}\n")


def mostrar_subtitulo(subtitulo):
    """Muestra subtitulo con estilo simple"""
    print(f"\n{COLOR_CYAN}>> {subtitulo}{COLOR_RESET}")
    print(f"{COLOR_CYAN}{LINEA_FINA * (len(subtitulo) + 3)}{COLOR_RESET}\n")

# ======================= MENUS =======================

def mostrar_menu_opciones(opciones, titulo, ancho):
    """Muestra un menu con opciones numeradas"""
    # Marco superior
    print(f"\n{COLOR_CYAN}+{'-' * (ancho - 2)}+")
    print(f"|{COLOR_RESET}{titulo:^{ancho - 2}}{COLOR_CYAN}|")
    print(f"+{'-' * (ancho - 2)}+{COLOR_RESET}")
    
    # Opciones
    for i, opcion in enumerate(opciones):
        numero = f"[{i + 1}]"
        print(f"  {COLOR_VERDE}{numero:4}{COLOR_RESET} {opcion}")
    
    # Marco inferior
    print(f"{COLOR_CYAN}+{'-' * (ancho - 2)}+{COLOR_RESET}\n")


# ======================= MENSAJES =======================

def mostrar_mensaje_exito(mensaje):
    """Muestra un mensaje de exito"""
    print(f"\n{COLOR_VERDE}[{MARCA_OK}] EXITO: {mensaje}{COLOR_RESET}\n")


def mostrar_mensaje_error(mensaje):
    """Muestra un mensaje de error"""
    print(f"\n{COLOR_ROJO}[{MARCA_ERROR}] ERROR: {mensaje}{COLOR_RESET}\n")


def mostrar_mensaje_info(mensaje):
    """Muestra un mensaje informativo"""
    print(f"\n{COLOR_AMARILLO}[i] INFO: {mensaje}{COLOR_RESET}\n")


# ======================= LISTAS DE DATOS =======================

def mostrar_lista_clientes(clientes_lista):
    """Muestra lista de clientes con columna de estado"""
    print(f"\n{COLOR_AMARILLO}+{'=' * 78}+")
    print(f"| {'LISTA DE CLIENTES':^76} |")
    print(f"+{'=' * 78}+{COLOR_RESET}")
    print(f"{COLOR_CYAN}  {'ID':<8} {'NOMBRE COMPLETO':<30} {'DNI':<15} {'ESTADO':<12}{COLOR_RESET}")
    print(f"{COLOR_CYAN}  {'-' * 8} {'-' * 30} {'-' * 15} {'-' * 12}{COLOR_RESET}")
    
    for cliente in clientes_lista:
        nombre_completo = f"{cliente[NOMBRE_CLIENTE]} {cliente[APELLIDO_CLIENTE]}"
        if len(nombre_completo) > 30:
            nombre_completo = nombre_completo[:27] + "..."
        
        # Determinar estado y color
        if cliente.get(ACTIVO_CLIENTE, False):
            estado = "ACTIVO"
            color_estado = COLOR_VERDE
        else:
            estado = "INACTIVO"
            color_estado = COLOR_ROJO
        
        print(f"  {COLOR_VERDE}{cliente[ID_CLIENTE]:<8d}{COLOR_RESET} "
              f"{nombre_completo:<30} {cliente[DNI_CLIENTE]:<15} "
              f"{color_estado}{estado:<12}{COLOR_RESET}")
    
    print(f"{COLOR_AMARILLO}+{'=' * 78}+{COLOR_RESET}\n")
    return True


def mostrar_lista_departamentos_detallada(departamentos, titulo="LISTA DE DEPARTAMENTOS"):
    """Muestra departamentos en formato de tabla detallada
    
    Acepta una lista de departamentos o un solo departamento (dict).
    """
    # Normalizar entrada a lista
    if isinstance(departamentos, dict):
        lista = [departamentos]
    else:
        lista = departamentos
    
    if not lista:
        mostrar_mensaje_info("No hay departamentos cargados.")
        return

    # Imprimir encabezado
    ancho = 94
    print(f"\n{COLOR_AMARILLO}+{'=' * (ancho - 2)}+")
    print(f"| {titulo:^{ancho - 4}} |")
    print(f"+{'=' * (ancho - 2)}+{COLOR_RESET}")
    print(f"{COLOR_MAGENTA}  {'ID':<7} {'UBICACION':<26} {'AMB':<5} {'CAP':<5} {'PRECIO':>10} {'ESTADO':<14} {'ACTIVO':<8}{COLOR_RESET}")
    print(f"{COLOR_CYAN}  {'-' * 7} {'-' * 26} {'-' * 5} {'-' * 5} {'-' * 10} {'-' * 14} {'-' * 8}{COLOR_RESET}")

    # Imprimir cada departamento
    for dep in lista:
        id_dep = dep.get(ID_DEPARTAMENTO, 0)
        ubicacion = dep.get(UBICACION_DEPARTAMENTO, "N/A")
        ambientes = dep.get(AMBIENTES_DEPARTAMENTO, "N/A")
        capacidad = dep.get(CAPACIDAD_DEPARTAMENTO, "N/A")
        estado = dep.get(ESTADO_DEPARTAMENTO, "N/A")
        activo = dep.get(ACTIVO_DEPARTAMENTO, False)
        
        try:
            precio = float(dep.get(PRECIO_DEPARTAMENTO, 0.0))
        except (ValueError, TypeError):
            precio = 0.0
        
        # Formatear estado activo
        if activo:
            etiqueta_activo = f"{COLOR_VERDE}ACTIVO{COLOR_RESET}"
        else:
            etiqueta_activo = f"{COLOR_ROJO}INACTIVO{COLOR_RESET}"
        
        print(f"  {COLOR_VERDE}{id_dep:<7d}{COLOR_RESET} "
              f"{ubicacion:<26s} "
              f"{str(ambientes):>3s}   "
              f"{str(capacidad):>3s}   "
              f"${precio:>9.2f} "
              f"{estado:<14s} "
              f"{etiqueta_activo}")

    # Imprimir pie
    print(f"{COLOR_AMARILLO}+{'=' * (ancho - 2)}+{COLOR_RESET}")
    print(f"{COLOR_CYAN}Total: {len(lista)} departamento(s){COLOR_RESET}\n")

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
    ancho_total = ancho_total + len(anchos) + 1

    # Marco superior con titulo
    print(f"\n{COLOR_AZUL}+{'=' * (ancho_total - 2)}+")
    print(f"| {titulo:^{ancho_total - 4}} |")
    print(f"+{'=' * (ancho_total - 2)}+{COLOR_RESET}")

    # Header de columnas con padding
    header = " "
    for i, col in enumerate(columnas):
        ancho = anchos[i]
        header = header + f"{col:<{ancho}}"
        if i < len(columnas) - 1:
            header = header + " "
    print(f"{COLOR_MAGENTA}{header}{COLOR_RESET}")
    
    # Linea separadora
    separador = " "
    for i, ancho in enumerate(anchos):
        separador = separador + ("-" * ancho)
        if i < len(anchos) - 1:
            separador = separador + " "
    print(f"{COLOR_CYAN}{separador}{COLOR_RESET}")

    # Datos con padding
    for fila in datos:
        linea = " "
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

    # Marco inferior con conteo
    print(f"{COLOR_AZUL}+{'-' * (ancho_total - 2)}+{COLOR_RESET}")
    print(f"{COLOR_CYAN}Total de registros: {COLOR_VERDE}{len(datos)}{COLOR_RESET}\n")


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


# ======================= SEPARADOR =======================

def separador_operaciones():
    """Separador especifico entre operaciones con estilo mejorado"""
    print(f"\n{COLOR_CYAN}{'=' * 72}{COLOR_RESET}")
    print(f"{COLOR_CYAN}{'=' * 72}{COLOR_RESET}\n")

# ======================= DESPEDIDA =======================

def mostrar_despedida():
    """Muestra el mensaje de despedida cuando el usuario sale"""
    print(f"\n{COLOR_VERDE}╔══════════════════════════════════════════════════════════════════╗{COLOR_RESET}")
    print(f"{COLOR_VERDE}║                                                                  ║{COLOR_RESET}")
    print(f"{COLOR_VERDE}║ Gracias por usar el Sistema de Gestion de Alquileres Temporarios ║{COLOR_RESET}")
    print(f"{COLOR_VERDE}║                                                                  ║{COLOR_RESET}")
    print(f"{COLOR_VERDE}╚══════════════════════════════════════════════════════════════════╝{COLOR_RESET}\n")


# ======================= SELECCION DE UI =======================

def mostrar_y_seleccionar_cliente(clientes_lista):
    """
    Muestra la lista de clientes y pide al usuario que elija uno.
    Retorna el ID del cliente seleccionado.
    """
    if not clientes_lista:
        return None

    mostrar_lista_clientes(clientes_lista)
    print(f"\n{COLOR_CYAN}{'─' * 72}{COLOR_RESET}")

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

    mostrar_lista_departamentos_detallada(departamentos_lista, titulo)
    print(f"\n{COLOR_CYAN}{'─' * 72}{COLOR_RESET}")

    return input_datos.seleccionar_elemento_de_lista(
        departamentos_lista,
        ID_DEPARTAMENTO,
        "Ingrese el ID del departamento"
    )