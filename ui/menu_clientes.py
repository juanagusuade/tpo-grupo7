import common.interfaz as interfaz
import domain.clientes as clientes
from common.constantes import *
import common.entrada_datos as entrada_datos

OPCIONES_MENU_CLIENTES = [
    "Agregar cliente",
    "Listar clientes",
    "Eliminar cliente",
    "Modificar cliente",
    "Volver al menu principal"]


def accion_agregar_cliente():
    """Funcion que se llama desde el menu para agregar un cliente"""
    print("\n--- Agregar cliente ---")
    nombre = entrada_datos.pedir_texto_alfabetico("Nombre")
    apellido = entrada_datos.pedir_texto_alfabetico("Apellido")
    dni = entrada_datos.pedir_dni()
    telefono = entrada_datos.pedir_telefono()

    if clientes.agregar_cliente(nombre, apellido, dni, telefono):
        interfaz.mostrar_mensaje_exito("Cliente agregado correctamente.")
        print()
    else:
        interfaz.mostrar_mensaje_error("Error: Ya existe un cliente con ese DNI.")
        print()


def accion_listar_clientes():
    """Funcion que se llama desde el menu para listar clientes activos"""
    interfaz.mostrar_lista_clientes(clientes.listar_clientes_activos())


def accion_baja_cliente():
    """Funcion que se llama desde el menu para dar de baja un cliente"""
    print("\n--- Dar de baja un cliente ---")

    activos = clientes.listar_clientes_activos()
    if not activos:
        interfaz.mostrar_mensaje_error("No hay clientes activos para dar de baja.")
        return

    interfaz.mostrar_lista_clientes(activos)
    id_cliente = entrada_datos.seleccionar_elemento_de_lista(activos, ID_CLIENTE,
                                                             "Seleccione el ID del cliente a eliminar")

    if clientes.baja_logica_cliente(id_cliente):
        interfaz.mostrar_mensaje_exito("Cliente dado de baja correctamente.")
        print()
    else:
        interfaz.mostrar_mensaje_error("Cliente no encontrado o ya inactivo.")
        print()


def accion_modificar_cliente():
    """Funcion que se llama desde el menu para modificar un cliente"""
    activos = clientes.listar_clientes_activos()
    if not activos:
        interfaz.mostrar_mensaje_error("No hay clientes activos para modificar.")
        return

    interfaz.mostrar_lista_clientes(activos)
    id_modificado = entrada_datos.seleccionar_elemento_de_lista(activos, ID_CLIENTE,
                                                                "Seleccione el ID del cliente a modificar")

    nombre = entrada_datos.pedir_texto_alfabetico("Nombre")
    apellido = entrada_datos.pedir_texto_alfabetico("Apellido")
    dni = entrada_datos.pedir_dni()
    telefono = entrada_datos.pedir_telefono()

    if clientes.dni_repetido(dni, id_modificado, clientes.lista_clientes_copia()):
        interfaz.mostrar_mensaje_error("Error: Ya existe un cliente con ese DNI.")
        return

    if clientes.actualizar_cliente(id_modificado, nombre, apellido, dni, telefono):
        interfaz.mostrar_mensaje_exito("Cliente modificado correctamente.")
    else:
        interfaz.mostrar_mensaje_error("Error:Cliente no encontrado o ya inactivo.")


def menu_clientes():
    menuActivo = True
    while menuActivo:
        interfaz.mostrar_separador()
        interfaz.mostrar_opciones_menu(OPCIONES_MENU_CLIENTES, "Menu de Clientes")
        opcion = entrada_datos.pedir_opcion_menu(len(OPCIONES_MENU_CLIENTES))

        interfaz.mostrar_separador()

        if opcion == "1":
            accion_agregar_cliente()
        elif opcion == "2":
            accion_listar_clientes()
        elif opcion == "3":
            accion_baja_cliente()
        elif opcion == "4":
            accion_modificar_cliente()
        elif opcion == "5":
            print("Volviendo al menu principal...")
            menuActivo = False

        entrada_datos.pausar()