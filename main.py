import common.interfaz as interfaz
import common.entrada_datos as input_datos
from ui.menu_reservas import gestionar_reservas
from ui.menu_depto import *
from ui.menu_clientes import menuClientes

def mostrar_bienvenida():
    """Muestra el mensaje de bienvenida del sistema"""
    interfaz.mostrar_header_principal("SISTEMA DE GESTION DE ALQUILERES TEMPORARIOS")
    print(f"{'Grupo VII - Programacion I':^70}")


def mostrar_menu_principal():
    """Muestra las opciones del menu principal"""
    opciones = [
        "Gestionar Clientes",
        "Gestionar Departamentos",
        "Gestionar Reservas",
        "Salir"
    ]
    interfaz.mostrar_menu_opciones(opciones, "MENU PRINCIPAL", 50)


def gestionar_clientes():
    menuClientes()


def confirmar_salida():
    """Solicita confirmacion antes de salir del sistema"""
    return input_datos.confirmar_accion("Esta seguro que desea salir del sistema")


def main():
    """Funcion principal del sistema"""
    mostrar_bienvenida()

    sistema_activo = True

    while sistema_activo:
        mostrar_menu_principal()
        opcion = input_datos.pedir_opcion_menu(4)

        # Procesar la opcion seleccionada
        if opcion == '1':
            gestionar_clientes()
        elif opcion == '2':
            menu_departamentos()
        elif opcion == '3':
            gestionar_reservas()
        elif opcion == '4':
            if confirmar_salida():
                sistema_activo = False
        

        # Separador visual entre iteraciones (excepto al salir)
        if sistema_activo:
            interfaz.separador_operaciones()

    interfaz.mostrar_despedida()


if __name__ == "__main__":
    main()