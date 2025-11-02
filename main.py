import common.interfaz as interfaz
import common.entrada_datos as input_datos
from ui.menu_reservas import menu_reservas
from ui.menu_depto import *
from ui.menu_clientes import menu_clientes
from ui.menu_estadisticas import gestionar_estadisticas
import common.poblador as poblador
from common.constantes import USUARIOS
from domain.clientes import guardar_clientes_a_archivo, cargar_clientes_desde_archivo

def autenticar_usuario():
    """
    Solicita usuario y contrasenia, y los valida contra la tupla de USUARIOS.
    Ofrece un maximo de 3 intentos.
    Retorna el nombre de usuario si la autenticacion es exitosa, o None si falla.
    """
    intentos = 3
    autenticado = False
    usuario_logueado = None

    interfaz.mostrar_subtitulo("INICIO DE SESION")

    while intentos > 0 and not autenticado:
        usuario = input(f"{interfaz.COLOR_CYAN}Ingrese su usuario: {interfaz.COLOR_RESET}")
        contrasenia = input(f"{interfaz.COLOR_CYAN}Ingrese su contrasenia: {interfaz.COLOR_RESET}")

        # Iterar sobre la tupla de usuarios para validar las credenciales
        i = 0
        while i < len(USUARIOS) and not autenticado:
            usuario_valido, contrasenia_valida = USUARIOS[i]
            if usuario == usuario_valido and contrasenia == contrasenia_valida:
                autenticado = True
                usuario_logueado = usuario
            i = i + 1

        if not autenticado:
            intentos = intentos - 1
            if intentos > 0:
                interfaz.mostrar_mensaje_error(f"Credenciales incorrectas. Quedan {intentos} intentos.")
            else:
                interfaz.mostrar_mensaje_error("Ha superado el numero de intentos. El programa se cerrara.")

    return usuario_logueado


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
        "Ver Estadisticas",
        "Salir"
    ]
    interfaz.mostrar_menu_opciones(opciones, "MENU PRINCIPAL", 50)


def confirmar_salida():
    """Solicita confirmacion antes de salir del sistema"""
    return input_datos.confirmar_accion("Esta seguro que desea salir del sistema")


def main():
    """Funcion principal del sistema"""
    mostrar_bienvenida()

    usuario_logueado = autenticar_usuario()

    if usuario_logueado is None:
        # Si la autenticacion falla, termina el programa
        interfaz.mostrar_despedida()
        return  # Sale de la funcion main

    interfaz.mostrar_mensaje_exito(f"Inicio de sesion exitoso. ¡Bienvenido, {usuario_logueado}!")

    # Cargar datos iniciales desde archivos (para clientes)
    print("Cargando datos de clientes...")
    cargar_clientes_desde_archivo()


    

    poblador.poblar_datos_iniciales()

    sistema_activo = True

    while sistema_activo:
        mostrar_menu_principal()
        opcion = input_datos.pedir_opcion_menu(5)

        if opcion == '1':
            menu_clientes()
        elif opcion == '2':
            menu_departamentos()
        elif opcion == '3':
            menu_reservas()
        elif opcion == '4':
            gestionar_estadisticas()
        elif opcion == '5':
            if confirmar_salida():
                sistema_activo = False

        if sistema_activo:
            interfaz.separador_operaciones()

    #Guardo los datos de clientes cuando salgo
    print("Guardando datos de clientes...")
    guardar_clientes_a_archivo("salir del sistema")        

    interfaz.mostrar_despedida()


if __name__ == "__main__":
    main()
    