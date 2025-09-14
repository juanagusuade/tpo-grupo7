import re
import common.interfaz as interfaz
import common.entrada_datos as input_datos
from common.constantes import *
import domain.reservas as reservas
import domain.clientes as clientes
import domain.departamentos as departamentos
from common.validaciones import validar_fecha


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
        "Volver al Menu Principal"
    ]
    interfaz.mostrar_menu_opciones(opciones, "MENU DE RESERVAS", 45)


def pedir_opcion_reservas():
    """Solicita y valida la opcion del menu de reservas"""
    return input_datos.pedir_opcion_menu(6)


def validar_fecha_ingreso(fecha):
    """Valida formato de fecha usando regex"""
    patron_fecha = r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/(19|20)\d{2}$'
    return re.match(patron_fecha, fecha) is not None and validar_fecha(fecha)


def pedir_fecha_con_validacion(prompt):
    """Pide una fecha con validacion mejorada"""
    return input_datos.pedir_input_con_validacion(
        f"{prompt} (dd/mm/yyyy)",
        validar_fecha_ingreso,
        "Fecha invalida. Use formato dd/mm/yyyy"
    )


def mostrar_clientes_activos():
    """Muestra la lista de clientes activos disponibles"""
    clientes_activos = clientes.listar_clientes_activos()  # Parametro removido
    return interfaz.mostrar_lista_clientes(clientes_activos)


def seleccionar_cliente():
    """Permite al usuario seleccionar un cliente activo"""
    clientes_activos = mostrar_clientes_activos()

    if not clientes_activos:
        interfaz.mostrar_mensaje_error("No hay clientes activos registrados")
        return None

    return input_datos.seleccionar_elemento_de_lista(
        clientes_activos,
        ID_CLIENTE,
        "Ingrese el ID del cliente"
    )


def mostrar_departamentos_disponibles(fecha_ingreso, fecha_egreso):
    """Muestra los departamentos disponibles para las fechas especificadas"""
    departamentos_activos = departamentos.listar_departamentos_activos()
    departamentos_disponibles = []

    i = 0
    while i < len(departamentos_activos):
        depto = departamentos_activos[i]
        if (depto[ESTADO_DEPARTAMENTO] == ESTADO_DISPONIBLE and
                reservas.verificar_disponibilidad_departamento(depto[ID_DEPARTAMENTO], fecha_ingreso, fecha_egreso)):
            departamentos_disponibles.append(depto)
        i = i + 1

    titulo = f"DEPARTAMENTOS DISPONIBLES ({fecha_ingreso} al {fecha_egreso})"
    return interfaz.mostrar_lista_departamentos(departamentos_disponibles, titulo)


def seleccionar_departamento(fecha_ingreso, fecha_egreso):
    """Permite seleccionar un departamento disponible"""
    departamentos_disponibles = mostrar_departamentos_disponibles(fecha_ingreso, fecha_egreso)

    if not departamentos_disponibles:
        interfaz.mostrar_mensaje_error("No hay departamentos disponibles para esas fechas")
        return None

    return input_datos.seleccionar_elemento_de_lista(
        departamentos_disponibles,
        ID_DEPARTAMENTO,
        "Ingrese el ID del departamento"
    )


def agregar_nueva_reserva():
    """Guia al usuario para crear una nueva reserva"""
    interfaz.mostrar_titulo_seccion("AGREGAR NUEVA RESERVA")

    # Seleccionar cliente
    id_cliente = seleccionar_cliente()
    if not id_cliente:
        return

    # Pedir fechas
    fecha_ingreso = pedir_fecha_con_validacion("Fecha de ingreso")
    fecha_egreso = pedir_fecha_con_validacion("Fecha de egreso")

    # Validar que fecha egreso sea posterior a ingreso
    if reservas.comparar_fechas_string(fecha_ingreso, fecha_egreso) >= 0:
        interfaz.mostrar_mensaje_error("La fecha de egreso debe ser posterior a la de ingreso")
        return

    # Seleccionar departamento
    id_departamento = seleccionar_departamento(fecha_ingreso, fecha_egreso)
    if not id_departamento:
        return

    # Confirmar la reserva
    cliente = clientes.buscar_cliente_por_id(id_cliente)
    departamento = departamentos.buscar_departamento_por_id(id_departamento)

    detalles = (f"Cliente: {cliente[NOMBRE_CLIENTE]} {cliente[APELLIDO_CLIENTE]}\n"
                f"Departamento: {departamento[UBICACION_DEPARTAMENTO]} ({departamento[AMBIENTES_DEPARTAMENTO]} amb.)\n"
                f"Periodo: {fecha_ingreso} al {fecha_egreso}\n"
                f"Precio por noche: ${departamento[PRECIO_DEPARTAMENTO]:.2f}")

    if input_datos.confirmar_operacion("reserva", detalles):
        if reservas.agregar_reserva(id_cliente, id_departamento, fecha_ingreso, fecha_egreso):
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

    i = 0
    while i < len(reservas_activas):
        reserva = reservas_activas[i]
        cliente = clientes.buscar_cliente_por_id(reserva[INDICE_ID_CLIENTE])
        departamento = departamentos.buscar_departamento_por_id(reserva[INDICE_ID_DEPARTAMENTO])

        if cliente and departamento:
            print(f"{COLOR_VERDE}ID {reserva[INDICE_ID_RESERVA]:5d}{COLOR_RESET} - "
                  f"{cliente[NOMBRE_CLIENTE]} {cliente[APELLIDO_CLIENTE]} | "
                  f"{departamento[UBICACION_DEPARTAMENTO]} | "
                  f"{reserva[INDICE_FECHA_INGRESO]} al {reserva[INDICE_FECHA_EGRESO]}")
        i = i + 1

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


def modificar_reserva_existente():
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

    # Modificar fechas
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


def cancelar_reserva_activa():
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

    id_cliente = seleccionar_cliente()
    if not id_cliente:
        return

    reservas_cliente = reservas.buscar_reservas_por_cliente(id_cliente)

    if not reservas_cliente:
        interfaz.mostrar_mensaje_info("No se encontraron reservas para este cliente")
        return

    cliente = clientes.buscar_cliente_por_id(id_cliente)
    print(f"\n{COLOR_VERDE}--- RESERVAS DE {cliente[NOMBRE_CLIENTE]} {cliente[APELLIDO_CLIENTE]} ---{COLOR_RESET}")

    i = 0
    while i < len(reservas_cliente):
        reserva = reservas_cliente[i]
        departamento = departamentos.buscar_departamento_por_id(reserva[INDICE_ID_DEPARTAMENTO])
        estado_formateado = interfaz.formatear_estado(reserva[INDICE_ESTADO])

        print(f"ID {reserva[INDICE_ID_RESERVA]:5d} | "
              f"{departamento[UBICACION_DEPARTAMENTO]:20s} | "
              f"{reserva[INDICE_FECHA_INGRESO]} al {reserva[INDICE_FECHA_EGRESO]} | "
              f"{estado_formateado}")
        i = i + 1


def buscar_por_departamento():
    """Busca reservas de un departamento especifico"""
    interfaz.mostrar_subtitulo("BUSCAR RESERVAS POR DEPARTAMENTO")

    departamentos_activos = departamentos.listar_departamentos_activos()
    if not departamentos_activos:
        interfaz.mostrar_mensaje_error("No hay departamentos activos")
        return

    interfaz.mostrar_lista_departamentos(departamentos_activos, "DEPARTAMENTOS DISPONIBLES")

    id_departamento = input_datos.seleccionar_elemento_de_lista(
        departamentos_activos,
        ID_DEPARTAMENTO,
        "Ingrese el ID del departamento"
    )

    if not id_departamento:
        return

    reservas_departamento = reservas.buscar_reservas_por_departamento(id_departamento)

    if not reservas_departamento:
        interfaz.mostrar_mensaje_info("No se encontraron reservas para este departamento")
        return

    departamento = departamentos.buscar_departamento_por_id(id_departamento)
    print(f"\n{COLOR_VERDE}--- RESERVAS DEL DEPARTAMENTO {departamento[UBICACION_DEPARTAMENTO]} ---{COLOR_RESET}")

    i = 0
    while i < len(reservas_departamento):
        reserva = reservas_departamento[i]
        cliente = clientes.buscar_cliente_por_id(reserva[INDICE_ID_CLIENTE])
        estado_formateado = interfaz.formatear_estado(reserva[INDICE_ESTADO])

        nombre_truncado = cliente[APELLIDO_CLIENTE]
        if len(cliente[APELLIDO_CLIENTE]) > 15:
            nombre_truncado = cliente[APELLIDO_CLIENTE][:15]

        print(f"ID {reserva[INDICE_ID_RESERVA]:5d} | "
              f"{cliente[NOMBRE_CLIENTE]} {nombre_truncado:15s} | "
              f"{reserva[INDICE_FECHA_INGRESO]} al {reserva[INDICE_FECHA_EGRESO]} | "
              f"{estado_formateado}")
        i = i + 1


def listar_todas_las_reservas_activas():
    """Lista todas las reservas activas con formato detallado"""
    reservas_activas = reservas.obtener_reservas_activas()

    if not reservas_activas:
        interfaz.mostrar_mensaje_info("No hay reservas activas en el sistema")
        return

    # Preparar datos para tabla
    datos_tabla = []
    i = 0
    while i < len(reservas_activas):
        reserva = reservas_activas[i]
        cliente = clientes.buscar_cliente_por_id(reserva[INDICE_ID_CLIENTE])
        departamento = departamentos.buscar_departamento_por_id(reserva[INDICE_ID_DEPARTAMENTO])

        if cliente and departamento:
            nombre_completo = f"{cliente[NOMBRE_CLIENTE]} {cliente[APELLIDO_CLIENTE]}"
            periodo = f"{reserva[INDICE_FECHA_INGRESO]} al {reserva[INDICE_FECHA_EGRESO]}"

            # Truncar textos largos
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
        i = i + 1

    columnas = ["ID", "CLIENTE", "DEPARTAMENTO", "PERIODO", "ESTADO"]
    anchos = [6, 20, 25, 23, 10]

    interfaz.mostrar_tabla("LISTADO COMPLETO DE RESERVAS ACTIVAS", datos_tabla, columnas, anchos)


def gestionar_reservas():
    """Menu principal de gestion de reservas"""
    mostrar_header_reservas()
    continuar_menu = True

    while continuar_menu:
        mostrar_menu_reservas()
        opcion = pedir_opcion_reservas()

        if opcion == '1':
            agregar_nueva_reserva()
        elif opcion == '2':
            modificar_reserva_existente()
        elif opcion == '3':
            cancelar_reserva_activa()
        elif opcion == '4':
            buscar_reservas_submenu()
        elif opcion == '5':
            listar_todas_las_reservas_activas()
        elif opcion == '6':
            interfaz.mostrar_mensaje_info("Volviendo al menu principal...")
            continuar_menu = False

        # Pausa entre operaciones
        input_datos.pausar()