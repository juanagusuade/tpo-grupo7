import common.interfaz as interfaz
import domain.clientes as clientes
from common.constantes import *
import common.entrada_datos as entrada_datos

OPCIONES_MENU_CLIENTES = [
    "Agregar cliente",
    "Listar clientes",
    "Dar de baja cliente",
    "Modificar cliente",
    "Volver al menu principal"]


def accion_agregar_cliente():
    """Agregar un cliente"""
    interfaz.mostrar_subtitulo("AGREGAR NUEVO CLIENTE")
    nombre = entrada_datos.pedir_texto_alfabetico("Nombre")
    apellido = entrada_datos.pedir_texto_alfabetico("Apellido")
    dni = entrada_datos.pedir_dni()
    telefono = entrada_datos.pedir_telefono()

    if clientes.agregar_cliente(nombre, apellido, dni, telefono):
        interfaz.mostrar_mensaje_exito("Cliente agregado correctamente.")
    else:
        interfaz.mostrar_mensaje_error("Error: Ya existe un cliente con ese DNI.")


def accion_listar_clientes():
    """Listar clientes activos"""
    interfaz.mostrar_subtitulo("LISTA DE CLIENTES ACTIVOS")
    clientes_activos = clientes.listar_clientes_activos()
    if not clientes_activos:
        interfaz.mostrar_mensaje_error("No hay clientes activos.")
        return
    interfaz.mostrar_lista_clientes_activos(clientes_activos)


def accion_baja_cliente():
    """Dar de baja un cliente"""
    interfaz.mostrar_subtitulo("DAR DE BAJA UN CLIENTE")

    activos = clientes.listar_clientes_activos()
    if not activos:
        interfaz.mostrar_mensaje_error("No hay clientes activos para dar de baja.")
        return

    interfaz.mostrar_lista_clientes_activos(activos)
    id_cliente = entrada_datos.seleccionar_elemento_de_lista(activos, ID_CLIENTE,
                                                             "Seleccione el ID del cliente a eliminar")

    if clientes.baja_logica_cliente(id_cliente):
        interfaz.mostrar_mensaje_exito("Cliente dado de baja correctamente.")
    else:
        interfaz.mostrar_mensaje_error("Cliente no encontrado o ya inactivo.")


def pedir_datos_actualizacion_cliente(cliente_actual):
    """
    Pide los nuevos datos para modificar un cliente, permitiendo mantener los actuales.
    Retorna una tupla con todos los datos.
    """
    print(f"Deje vacío para mantener el valor actual.")

    # Valores actuales
    nombre_actual = cliente_actual[NOMBRE_CLIENTE]
    apellido_actual = cliente_actual[APELLIDO_CLIENTE]
    dni_actual = cliente_actual[DNI_CLIENTE]
    telefono_actual = cliente_actual[TELEFONO_CLIENTE]

    # Pedir Nombre
    nuevo_nombre = entrada_datos.pedir_input_con_validacion(
        f"Nombre [{nombre_actual}]",
        entrada_datos.validar_alfabetico,
        "Solo se permiten letras y espacios",
        es_opcional=True
    )
    if nuevo_nombre is None:
        nuevo_nombre = nombre_actual

    # Pedir Apellido
    nuevo_apellido = entrada_datos.pedir_input_con_validacion(
        f"Apellido [{apellido_actual}]",
        entrada_datos.validar_alfabetico,
        "Solo se permiten letras y espacios",
        es_opcional=True
    )
    if nuevo_apellido is None:
        nuevo_apellido = apellido_actual

    # Pedir DNI
    nuevo_dni = entrada_datos.pedir_input_con_validacion(
        f"DNI [{dni_actual}]",
        entrada_datos.validar_dni,
        "El DNI debe contener solo numeros y tener entre 7 y 8 digitos",
        es_opcional=True
    )
    if nuevo_dni is None:
        nuevo_dni = dni_actual

    # Pedir Telefono
    nuevo_telefono = entrada_datos.pedir_input_con_validacion(
        f"Teléfono [{telefono_actual}]",
        entrada_datos.validar_telefono,
        "El telefono debe tener al menos 7 caracteres validos",
        es_opcional=True
    )
    if nuevo_telefono is None:
        nuevo_telefono = telefono_actual

    return (nuevo_nombre, nuevo_apellido, nuevo_dni, nuevo_telefono)


def accion_modificar_cliente():
    """Maneja el flujo de modificar un cliente"""
    interfaz.mostrar_subtitulo("MODIFICAR CLIENTE")

    activos = clientes.listar_clientes_activos()
    if not activos:
        interfaz.mostrar_mensaje_error("No hay clientes activos para modificar.")
        return

    interfaz.mostrar_lista_clientes_activos(activos)
    id_modificado = entrada_datos.seleccionar_elemento_de_lista(activos, ID_CLIENTE,
                                                                "Seleccione el ID del cliente a modificar")

    cliente_actual = clientes.buscar_cliente_por_id(id_modificado)
    if not cliente_actual:
        interfaz.mostrar_mensaje_error("Error: Cliente no encontrado.")
        return

    (nombre, apellido, dni, telefono) = pedir_datos_actualizacion_cliente(cliente_actual)

    if clientes.dni_repetido(dni, id_modificado, clientes.lista_clientes_copia()):
        interfaz.mostrar_mensaje_error("Error: Ya existe otro cliente con ese DNI.")
        return

    if clientes.actualizar_cliente(id_modificado, nombre, apellido, dni, telefono):
        interfaz.mostrar_mensaje_exito("Cliente modificado correctamente.")
    else:
        interfaz.mostrar_mensaje_error("Error: Cliente no encontrado o ya inactivo.")


def menu_clientes():
    """Menu principal de gestion de clientes"""
    interfaz.mostrar_header_modulo("GESTIÓN DE CLIENTES")
    menuActivo = True

    while menuActivo:
        interfaz.mostrar_menu_opciones(OPCIONES_MENU_CLIENTES, "MENÚ DE CLIENTES", 45)
        opcion = entrada_datos.pedir_opcion_menu(len(OPCIONES_MENU_CLIENTES))

        if opcion == "1":
            accion_agregar_cliente()
        elif opcion == "2":
            accion_listar_clientes()
        elif opcion == "3":
            accion_baja_cliente()
        elif opcion == "4":
            accion_modificar_cliente()
        elif opcion == "5":
            interfaz.mostrar_mensaje_info("Volviendo al menu principal...")
            menuActivo = False

        if menuActivo:
            entrada_datos.pausar()