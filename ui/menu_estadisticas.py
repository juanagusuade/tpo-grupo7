import common.interfaz as interfaz
import common.entrada_datos as input_datos
import domain.reservas as reservas
import domain.departamentos as departamentos


def gestionar_estadisticas():
    """Menu principal de gestion de estadisticas"""
    interfaz.mostrar_header_modulo("REPORTES Y ESTADISTICAS")

    continuar_menu = True
    while continuar_menu:
        opciones = [
            "Porcentaje de Ocupacion por Departamento",
            "Duracion Promedio de Reservas",
            "Volver al Menu Principal"
        ]
        interfaz.mostrar_menu_opciones(opciones, "MENU DE ESTADISTICAS", 50)

        opcion = input_datos.pedir_opcion_menu(len(opciones))

        if opcion == '1':
            mostrar_porcentaje_ocupacion()
        elif opcion == '2':
            mostrar_duracion_promedio()
        elif opcion == '3':
            continuar_menu = False

        if continuar_menu:
            input_datos.pausar()


def mostrar_porcentaje_ocupacion():
    """Muestra el porcentaje de dias ocupados de cada depto en el ultimo anio."""
    interfaz.mostrar_titulo_seccion("PORCENTAJE DE OCUPACION (ULTIMOS 365 DIAS)")

    lista_deptos = departamentos.listar_departamentos_activos()
    if not lista_deptos:
        interfaz.mostrar_mensaje_info("No hay departamentos registrados.")
        return

    datos_tabla = []
    for depto in lista_deptos:
        id_depto = depto["id"]
        total_dias_ocupado = reservas.calcular_dias_ocupados_depto(id_depto, 365)

        porcentaje = (float(total_dias_ocupado) / 365.0) * 100.0 if 365 > 0 else 0

        fila = [
            id_depto,
            depto["ubicacion"],
            total_dias_ocupado,
            f"{porcentaje:.2f}%"
        ]
        datos_tabla.append(fila)

    columnas = ["ID Depto", "Ubicacion", "Dias Ocupado (ultimo anio)", "Ocupacion"]
    anchos = [10, 30, 28, 15]
    interfaz.mostrar_tabla("Ocupacion por Departamento", datos_tabla, columnas, anchos)


def mostrar_duracion_promedio():
    """Calcula y muestra la duracion promedio de las reservas activas."""
    interfaz.mostrar_titulo_seccion("DURACION PROMEDIO DE RESERVAS")

    promedio = reservas.calcular_duracion_promedio_reservas()

    if promedio is not None:
        interfaz.mostrar_mensaje_exito(f"La duracion promedio de las reservas activas es de {promedio:.2f} dias.")
    else:
        interfaz.mostrar_mensaje_info("No hay reservas activas para calcular el promedio.")