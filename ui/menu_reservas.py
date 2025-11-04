import common.entrada_datos as input_datos
import common.interfaz as interfaz
import domain.clientes as clientes
import domain.departamentos as departamentos
import domain.reservas as reservas
from common.constantes import *
from common.validaciones import validar_fecha_ingreso


def mostrar_header_reservas():
    """Muestra el encabezado del modulo de reservas"""
    interfaz.mostrar_header_modulo("GESTION DE RESERVAS")


def mostrar_menu_reservas():
    """Muestra las opciones del menu de reservas"""
    opciones = [
        "Agregar Reserva",
        "Modificar Reserva",
        "Cancelar Reserva",
        "Buscar Reservas",
        "Listar Todas las Reservas Activas",
        "Consultar Disponibilidad de Departamento",
        "Volver al Menu Principal"
    ]
    interfaz.mostrar_menu_opciones(opciones, "MENU DE RESERVAS", 45)


def pedir_opcion_menu_reservas():
    """Solicita y valida la opcion del menu de reservas"""
    return input_datos.pedir_opcion_menu(7)


def seleccionar_cliente_activo():
    """Maneja la seleccion de un cliente activo."""
    clientes_activos = clientes.listar_clientes_activos()
    if not clientes_activos:
        return None

    id_cliente = interfaz.mostrar_y_seleccionar_cliente(clientes_activos)

    return clientes.buscar_cliente_por_id(id_cliente)


# --- FUNCION MODIFICADA ---
def seleccionar_departamento_disponible(fecha_ingreso, fecha_egreso):
    """Maneja la seleccion de un departamento disponible."""
    departamentos_disponibles = departamentos.listar_departamentos_disponibles(fecha_ingreso, fecha_egreso)

    if not departamentos_disponibles:
        interfaz.mostrar_mensaje_error("No hay departamentos disponibles para esas fechas")
        return None

    titulo = f"DEPARTAMENTOS DISPONIBLES ({fecha_ingreso} al {fecha_egreso})"
    id_departamento = interfaz.mostrar_y_seleccionar_departamento(departamentos_disponibles, titulo)

    return id_departamento


def agregar_reserva_ui():
    """Guia al usuario para crear una nueva reserva"""
    interfaz.mostrar_titulo_seccion("AGREGAR NUEVA RESERVA")

    fecha_ingreso = input_datos.pedir_fecha_con_validacion("Fecha de ingreso")
    fecha_egreso = input_datos.pedir_fecha_con_validacion("Fecha de egreso")

    if reservas.comparar_fechas_string(fecha_ingreso, fecha_egreso) >= 0:
        interfaz.mostrar_mensaje_error("La fecha de egreso debe ser posterior a la de ingreso")
        return

    # La logica de seleccion ahora esta mas limpia
    cliente = seleccionar_cliente_activo()
    if cliente is None:
        interfaz.mostrar_mensaje_error("No hay clientes activos para seleccionar. Operacion cancelada.")
        return

    # La logica de seleccion ahora esta mas limpia
    id_departamento = seleccionar_departamento_disponible(fecha_ingreso, fecha_egreso)
    if id_departamento is None:
        interfaz.mostrar_mensaje_info("Operacion cancelada.")
        return

    departamento = departamentos.buscar_departamento_por_id(id_departamento)

    detalles = (f"Cliente: {cliente[NOMBRE_CLIENTE]} {cliente[APELLIDO_CLIENTE]}\n"
                f"Departamento: {departamento[UBICACION_DEPARTAMENTO]} ({departamento[AMBIENTES_DEPARTAMENTO]} amb.)\n"
                f"Periodo: {fecha_ingreso} al {fecha_egreso}\n"
                f"Precio por noche: ${departamento[PRECIO_DEPARTAMENTO]:.2f}")

    if input_datos.confirmar_operacion("reserva", detalles):
        if reservas.agregar_reserva(cliente[ID_CLIENTE], id_departamento, fecha_ingreso, fecha_egreso):
            interfaz.mostrar_mensaje_exito("Reserva creada exitosamente")
        else:
            interfaz.mostrar_mensaje_error("Error al crear la reserva")
    else:
        interfaz.mostrar_mensaje_info("Operacion cancelada")


def mostrar_reservas_activas():
    """Muestra las reservas activas del sistema con formato mejorado"""
    reservas_activas = reservas.obtener_reservas_activas()

    if not reservas_activas:
        return None

    print(f"\n{COLOR_AMARILLO}--- RESERVAS ACTIVAS ---{COLOR_RESET}")

    for reserva in reservas_activas:
        cliente = clientes.buscar_cliente_por_id(reserva[INDICE_ID_CLIENTE])
        departamento = departamentos.buscar_departamento_por_id(reserva[INDICE_ID_DEPARTAMENTO])

        if cliente and departamento:
            print(f"{COLOR_VERDE}ID {reserva[INDICE_ID_RESERVA]:5d}{COLOR_RESET} - "
                  f"{cliente[NOMBRE_CLIENTE]} {cliente[APELLIDO_CLIENTE]} | "
                  f"{departamento[UBICACION_DEPARTAMENTO]} | "
                  f"{reserva[INDICE_FECHA_INGRESO]} al {reserva[INDICE_FECHA_EGRESO]}")

    return reservas_activas


def seleccionar_reserva_activa():
    """Permite seleccionar una reserva activa"""
    reservas_activas = mostrar_reservas_activas()

    if not reservas_activas:
        interfaz.mostrar_mensaje_error("No hay reservas activas en el sistema")
        return None

    return input_datos.seleccionar_elemento_de_lista(
        reservas_activas,
        INDICE_ID_RESERVA,
        "Ingrese el ID de la reserva"
    )


def actualizar_reserva_ui():
    """Permite modificar una reserva activa"""
    interfaz.mostrar_titulo_seccion("MODIFICAR RESERVA")

    id_reserva = seleccionar_reserva_activa()
    if not id_reserva:
        return

    reserva = reservas.buscar_reserva_por_id(id_reserva)
    cliente = clientes.buscar_cliente_por_id(reserva[INDICE_ID_CLIENTE])
    departamento = departamentos.buscar_departamento_por_id(reserva[INDICE_ID_DEPARTAMENTO])

    print(f"\n{COLOR_AMARILLO}--- DATOS ACTUALES ---")
    print(f"Cliente: {cliente[NOMBRE_CLIENTE]} {cliente[APELLIDO_CLIENTE]}")
    print(f"Departamento: {departamento[UBICACION_DEPARTAMENTO]}")
    print(f"Fecha ingreso: {reserva[INDICE_FECHA_INGRESO]}")
    print(f"Fecha egreso: {reserva[INDICE_FECHA_EGRESO]}{COLOR_RESET}")

    interfaz.mostrar_mensaje_info("Ingrese los nuevos valores (presione Enter para mantener el actual)")

    nueva_fecha_ingreso = input_datos.pedir_input_con_validacion(
        f"Nueva fecha de ingreso ({reserva[INDICE_FECHA_INGRESO]})",
        validar_fecha_ingreso,
        "Fecha de ingreso invalida",
        es_opcional=True
    )

    nueva_fecha_egreso = input_datos.pedir_input_con_validacion(
        f"Nueva fecha de egreso ({reserva[INDICE_FECHA_EGRESO]})",
        validar_fecha_ingreso,
        "Fecha de egreso invalida",
        es_opcional=True
    )

    if reservas.actualizar_reserva(id_reserva, fecha_ingreso_str=nueva_fecha_ingreso,
                                   fecha_egreso_str=nueva_fecha_egreso):
        interfaz.mostrar_mensaje_exito("Reserva modificada exitosamente")
    else:
        interfaz.mostrar_mensaje_error("Error al modificar la reserva")


def cancelar_reserva_ui():
    """Permite cancelar una reserva activa"""
    interfaz.mostrar_titulo_seccion("CANCELAR RESERVA")

    id_reserva = seleccionar_reserva_activa()
    if not id_reserva:
        return

    reserva = reservas.buscar_reserva_por_id(id_reserva)
    cliente = clientes.buscar_cliente_por_id(reserva[INDICE_ID_CLIENTE])
    departamento = departamentos.buscar_departamento_por_id(reserva[INDICE_ID_DEPARTAMENTO])

    detalles = (f"Cliente: {cliente[NOMBRE_CLIENTE]} {cliente[APELLIDO_CLIENTE]}\n"
                f"Departamento: {departamento[UBICACION_DEPARTAMENTO]}\n"
                f"Periodo: {reserva[INDICE_FECHA_INGRESO]} al {reserva[INDICE_FECHA_EGRESO]}")

    if input_datos.confirmar_operacion("cancelacion de reserva", detalles):
        if reservas.cancelar_reserva(id_reserva):
            interfaz.mostrar_mensaje_exito("Reserva cancelada exitosamente")
        else:
            interfaz.mostrar_mensaje_error("Error al cancelar la reserva")
    else:
        interfaz.mostrar_mensaje_info("Operacion cancelada")


def mostrar_menu_busqueda():
    """Muestra opciones para buscar reservas"""
    opciones = [
        "Buscar por Cliente",
        "Buscar por Departamento",
        "Volver"
    ]
    interfaz.mostrar_menu_opciones(opciones, "BUSCAR RESERVAS", 35)


def buscar_reservas_submenu():
    """Submenu para buscar reservas"""
    continuar_menu = True
    while continuar_menu:
        mostrar_menu_busqueda()
        opcion = input_datos.pedir_opcion_menu(3)

        if opcion == '1':
            buscar_por_cliente()
        elif opcion == '2':
            buscar_por_departamento()
        elif opcion == '3':
            continuar_menu = False


def buscar_por_cliente():
    """Busca reservas de un cliente especifico"""
    interfaz.mostrar_subtitulo("BUSCAR RESERVAS POR CLIENTE")

    cliente = seleccionar_cliente_activo()
    if not cliente:
        interfaz.mostrar_mensaje_info("No se encontraron clientes activos")
        return

    reservas_cliente = reservas.buscar_reservas_por_cliente(cliente[ID_CLIENTE])
    if not reservas_cliente:
        interfaz.mostrar_mensaje_info("No se encontraron reservas para este cliente")
        return

    print(f"\n{COLOR_VERDE}--- RESERVAS DE {cliente[NOMBRE_CLIENTE]} {cliente[APELLIDO_CLIENTE]} ---{COLOR_RESET}")

    for reserva in reservas_cliente:
        departamento = departamentos.buscar_departamento_por_id(reserva[INDICE_ID_DEPARTAMENTO])
        estado_formateado = interfaz.formatear_estado(reserva[INDICE_ESTADO])

        print(f"ID {reserva[INDICE_ID_RESERVA]:5d} | "
              f"{departamento[UBICACION_DEPARTAMENTO]:20s} | "
              f"{reserva[INDICE_FECHA_INGRESO]} al {reserva[INDICE_FECHA_EGRESO]} | "
              f"{estado_formateado}")


def buscar_por_departamento():
    """Busca reservas de un departamento especifico"""
    interfaz.mostrar_subtitulo("BUSCAR RESERVAS POR DEPARTAMENTO")

    departamentos_activos = departamentos.listar_departamentos_activos()
    if not departamentos_activos:
        interfaz.mostrar_mensaje_error("No hay departamentos activos")
        return

    id_departamento = interfaz.mostrar_y_seleccionar_departamento(
        departamentos_activos,
        "DEPARTAMENTOS DISPONIBLES"
    )

    if not id_departamento:
        return

    reservas_departamento = reservas.buscar_reservas_por_departamento(id_departamento)

    if not reservas_departamento:
        interfaz.mostrar_mensaje_info("No se encontraron reservas para este departamento")
        return

    departamento = departamentos.buscar_departamento_por_id(id_departamento)
    print(f"\n{COLOR_VERDE}--- RESERVAS DEL DEPARTAMENTO {departamento[UBICACION_DEPARTAMENTO]} ---{COLOR_RESET}")

    for reserva in reservas_departamento:
        cliente = clientes.buscar_cliente_por_id(reserva[INDICE_ID_CLIENTE])
        estado_formateado = interfaz.formatear_estado(reserva[INDICE_ESTADO])

        apellido_truncado = cliente[APELLIDO_CLIENTE]
        if len(apellido_truncado) > 15:
            apellido_truncado = apellido_truncado[:15]

        print(f"ID {reserva[INDICE_ID_RESERVA]:5d} | "
              f"{cliente[NOMBRE_CLIENTE]} {apellido_truncado:15s} | "
              f"{reserva[INDICE_FECHA_INGRESO]} al {reserva[INDICE_FECHA_EGRESO]} | "
              f"{estado_formateado}")


def listar_reservas_activas_ui():
    """Lista todas las reservas activas con formato detallado"""
    reservas_activas = reservas.obtener_reservas_activas()

    if not reservas_activas:
        interfaz.mostrar_mensaje_info("No hay reservas activas en el sistema")
        return

    datos_tabla = []
    for reserva in reservas_activas:
        cliente = clientes.buscar_cliente_por_id(reserva[INDICE_ID_CLIENTE])
        departamento = departamentos.buscar_departamento_por_id(reserva[INDICE_ID_DEPARTAMENTO])

        if cliente and departamento:
            nombre_completo = f"{cliente[NOMBRE_CLIENTE]} {cliente[APELLIDO_CLIENTE]}"
            periodo = f"{reserva[INDICE_FECHA_INGRESO]} al {reserva[INDICE_FECHA_EGRESO]}"

            nombre_truncado = nombre_completo
            if len(nombre_completo) > 19:
                nombre_truncado = nombre_completo[:19]

            ubicacion_truncada = departamento[UBICACION_DEPARTAMENTO]
            if len(departamento[UBICACION_DEPARTAMENTO]) > 24:
                ubicacion_truncada = departamento[UBICACION_DEPARTAMENTO][:24]

            fila = [
                reserva[INDICE_ID_RESERVA],
                nombre_truncado,
                ubicacion_truncada,
                periodo,
                reserva[INDICE_ESTADO]
            ]
            datos_tabla.append(fila)

    columnas = ["ID", "CLIENTE", "DEPARTAMENTO", "PERIODO", "ESTADO"]
    anchos = [6, 20, 25, 23, 10]

    interfaz.mostrar_tabla("LISTADO COMPLETO DE RESERVAS ACTIVAS", datos_tabla, columnas, anchos)


def consultar_disponibilidad_ui():
    """Permite al usuario consultar si un depto esta libre en un rango de fechas."""
    interfaz.mostrar_titulo_seccion("CONSULTAR DISPONIBILIDAD")

    deptos_activos = departamentos.listar_departamentos_activos()

    if not deptos_activos:
        interfaz.mostrar_mensaje_error("No hay departamentos activos para consultar.")
        return

    id_depto = interfaz.mostrar_y_seleccionar_departamento(
        deptos_activos,
        "DEPARTAMENTOS ACTIVOS"
    )

    if not id_depto:
        interfaz.mostrar_mensaje_info("Seleccion cancelada.")
        return

    fecha_ingreso = input_datos.pedir_fecha_con_validacion("Fecha de inicio de la consulta")
    fecha_egreso = input_datos.pedir_fecha_con_validacion("Fecha de fin de la consulta")

    if reservas.comparar_fechas_string(fecha_ingreso, fecha_egreso) >= 0:
        interfaz.mostrar_mensaje_error("La fecha de fin debe ser posterior a la de inicio.")
        return

    if departamentos.verificar_disponibilidad_departamento(id_depto, fecha_ingreso, fecha_egreso):
        interfaz.mostrar_mensaje_exito(
            f"¡Disponible! El departamento esta libre del {fecha_ingreso} al {fecha_egreso}.")
    else:
        interfaz.mostrar_mensaje_error(f"¡No disponible! El departamento ya tiene reservas en ese periodo.")


def menu_reservas():
    """Menu principal de gestion de reservas"""
    mostrar_header_reservas()
    continuar_menu = True

    while continuar_menu:
        mostrar_menu_reservas()
        opcion = pedir_opcion_menu_reservas()

        if opcion == '1':
            agregar_reserva_ui()
        elif opcion == '2':
            actualizar_reserva_ui()
        elif opcion == '3':
            cancelar_reserva_ui()
        elif opcion == '4':
            buscar_reservas_submenu()
        elif opcion == '5':
            listar_reservas_activas_ui()
        elif opcion == '6':
            consultar_disponibilidad_ui()
        elif opcion == '7':
            interfaz.mostrar_mensaje_info("Volviendo al menu principal...")
            continuar_menu = False

        if continuar_menu:
            input_datos.pausar()