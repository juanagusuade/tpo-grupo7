import domain.reservas as reservas
import domain.departamentos as departamentos
import domain.clientes as clientes
from common.constantes import *
from common.interfaz import *
from common.entrada_datos import *
from domain.departamentos import listar_departamentos_activos

OPCIONES_MENU = ["1. Agregar reserva.", "2. Listar reservas.", "3. Eliminar reserva.", "4. Volver al menu principal."]
def menuReservas():
    menuActivo = True

    while menuActivo:
        mostrar_separador()
        mostrar_opciones_menu(OPCIONES_MENU, "Menu de Reservas")

        opcion = pedir_input_con_validacion(
            "Seleccione una opción (1-4): ",
            lambda x: x in ["1", "2", "3", "4"],
            "Opción inválida. Por favor, seleccione una opción válida."
        )

        mostrar_separador()

        if opcion == "1":
            # Seleccionar cliente valido
            clientes_activos = clientes.listar_clientes_activos(None)
            if clientes_activos == []:
                mostrar_mensaje_error("No hay clientes activos registrados.")

            mostrar_opciones_menu(
                [f"ID: {cliente[ID_CLIENTE]} - {cliente[NOMBRE_CLIENTE]} {cliente[APELLIDO_CLIENTE]}" for cliente in clientes_activos],
                "Clientes Activos"
            )

            id_cliente = pedir_input_con_validacion(
                "Seleccione un cliente por su ID",
                lambda valor: valor.isdigit() and int(valor) in [cliente[ID_CLIENTE] for cliente in clientes_activos],
                "Debe ingresar un ID válido de la lista."
            )
            id_cliente = int(id_cliente)

            # Select dates
            fecha_ingreso = pedir_fecha("Fecha de Ingreso (dd/mm/yyyy): ")
            fecha_egreso = pedir_fecha("Fecha de Egreso (dd/mm/yyyy): ")

            # Select department
            departamentos_disponibles = listar_departamentos_disponibles(fecha_ingreso, fecha_egreso)
            if not departamentos_disponibles:
                mostrar_mensaje_error("No hay departamentos disponibles para las fechas seleccionadas.")
                continue

            mostrar_opciones_menu([depto[0] for depto in departamentos_disponibles], "Departamentos Disponibles")

            id_departamento = pedir_input_con_validacion(
                "Seleccione un departamento por su ID",
                lambda valor: valor.isdigit() and int(valor) in [depto[1] for depto in departamentos_disponibles],
                "Debe ingresar un ID válido de la lista."
            )
            id_departamento = int(id_departamento)

            print(f"Cliente seleccionado: {id_cliente}, Departamento seleccionado: {id_departamento}")

        elif opcion == "2":
            if len(reservas.reservas) == 0:
                print("No hay reservas registradas.")
            else:
                print("\nLista de Reservas:")
                for reserva in reservas.reservas:
                    print(f"ID Reserva: {reserva[0]}, ID Cliente: {reserva[1]}, ID Departamento: {reserva[2]}, "
                          f"Fecha Ingreso: {reserva[3]}, Fecha Egreso: {reserva[4]}, Estado: {reserva[5]}")

        elif opcion == "3":
            menuActivo = False
            print("Volviendo al Menu Principal...")

        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

def listar_departamentos_disponibles(fecha_ingreso, fecha_egreso):
    departamentos_disponibles = []
    departamentos_activos = listar_departamentos_activos()

    for depto in departamentos_activos:
        if depto[INDICE_ESTADO] == ESTADO_DISPONIBLE and reservas.verificar_disponibilidad_departamento(depto[ID_DEPARTAMENTO], fecha_ingreso, fecha_egreso):
            depto_str = f"ID departamento: {depto[ID_DEPARTAMENTO]} - Ubicación: {depto[UBICACION_DEPARTAMENTO]}, Ambientes: {depto[AMBIENTES_DEPARTAMENTO]}, Capacidad: {depto[CAPACIDAD_DEPARTAMENTO]}, Precio/noche: {depto[PRECIO_DEPARTAMENTO]}"
            departamentos_disponibles.append((depto_str, depto[ID_DEPARTAMENTO]))
    return departamentos_disponibles

def seleccionar_departamento(fecha_ingreso, fecha_egreso):
    departamentos_disponibles = listar_departamentos_disponibles(fecha_ingreso, fecha_egreso)

    if not departamentos_disponibles:
        mostrar_mensaje_error("No hay departamentos disponibles para las fechas seleccionadas.")
        return None

    # Mostrar las opciones disponibles
    mostrar_opciones_menu([depto[0] for depto in departamentos_disponibles], "Departamentos Disponibles")

    # Validar el input del usuario
    id_departamento = pedir_input_con_validacion(
        "Seleccione un departamento por su ID",
        lambda valor: valor.isdigit() and int(valor) in [depto[1] for depto in departamentos_disponibles],
        "Debe ingresar un ID válido de la lista."
    )

    return int(id_departamento)