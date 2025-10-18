from common.entrada_datos import *
from common.interfaz import *
from domain.departamentos import *


def creacion_depto():
    mostrar_subtitulo("Crear departamento")
    ubicacion = pedir_input_con_validacion("Ubicacion", lambda valor: campos_son_validos(valor), "No puede estar vacio")
    ambientes = pedir_numero_entero("Ambientes (≥ 1)", minimo=1)
    capacidad = pedir_numero_entero("Capacidad (≥ 1)", minimo=1)
    estado = pedir_estado_departamento()
    precio = pedir_numero_decimal("Precio por noche (≥ 0.01)", minimo=0.01)

    ok = agregar_departamento(ubicacion, ambientes, capacidad, estado, precio)
    if ok:
        mostrar_mensaje_exito("Departamento creado correctamente.")
    else:
        mostrar_mensaje_error("No se pudo crear el departamento.")


def eliminar_depto_fisico():
    mostrar_subtitulo("Eliminar departamento (FÍSICO)")
    if not departamentos:
        mostrar_mensaje_info("No hay departamentos para eliminar.")
        return

    mostrar_lista_departamentos_detallada(departamentos)
    id_dep = pedir_numero_entero("ID a eliminar", minimo=1)

    if not confirmar_accion("¿Estas seguro de eliminar definitivamente"):
        mostrar_mensaje_info("Accion cancelada.")
        return

    ok = eliminar_departamento(id_dep)
    if ok:
        mostrar_mensaje_exito("Departamento eliminado.")
    else:
        mostrar_mensaje_error("ID no encontrado.")


def pedir_datos_actualizacion(dep):
    """
    Pedir al usuario los nuevos datos para un depto.
    Retorna una tupla con todos los datos listos para enviar al dominio.
    """
    ubicacion = dep.get(UBICACION_DEPARTAMENTO)
    ambientes = dep.get(AMBIENTES_DEPARTAMENTO)
    capacidad = dep.get(CAPACIDAD_DEPARTAMENTO)
    estado = dep.get(ESTADO_DEPARTAMENTO)
    precio = dep.get(PRECIO_DEPARTAMENTO)

    print(f"Deja vacío para mantener el valor actual.")

    nueva_ubi = pedir_input_con_validacion(
        f"Ubicación actual [{ubicacion}] (enter para mantener)",
        lambda valor: campos_son_validos(valor),
        "No puede estar vacío",
        es_opcional=True
    )
    if nueva_ubi is None:
        nueva_ubi = ubicacion

    val = pedir_input_con_validacion(
        f"Ambientes actual [{ambientes}] (enter para mantener)",
        lambda s: s.isdigit(),
        "Debe ser entero positivo",
        es_opcional=True
    )
    nuevo_amb = int(val) if val is not None else ambientes

    val = pedir_input_con_validacion(
        f"Capacidad actual [{capacidad}] (enter para mantener)",
        lambda s: s.isdigit(),
        "Debe ser entero positivo",
        es_opcional=True
    )
    nueva_cap = int(val) if val is not None else capacidad

    print(f"Estado actual: {estado}. Si querés cambiarlo, elegí una opción; ENTER para mantener.")
    print(f"1. {ESTADO_DISPONIBLE}\n2. {ESTADO_OCUPADO}\n3. {ESTADO_MANTENIMIENTO}")
    val = pedir_input_con_validacion(
        "Seleccione estado (1-3) o ENTER para mantener",
        lambda s: s in ["1", "2", "3"],
        "Debe seleccionar 1, 2 o 3",
        es_opcional=True
    )
    if val is None:
        nuevo_est = estado
    else:
        nuevo_est = {"1": ESTADO_DISPONIBLE, "2": ESTADO_OCUPADO, "3": ESTADO_MANTENIMIENTO}[val]

    val = pedir_input_con_validacion(
        f"Precio/noche actual [{precio}] (enter para mantener)",
        lambda s: s.replace(".", "", 1).isdigit() and float(s) >= 0.01,
        "Debe ser decimal ≥ 0.01",
        es_opcional=True
    )
    nuevo_pre = float(val) if val is not None else precio

    # Retorna todos los datos nuevos
    return (nueva_ubi, nuevo_amb, nueva_cap, nuevo_est, nuevo_pre)


def actualizar_depto():
    """Maneja el flujo de 'actualizar depto'"""
    mostrar_subtitulo("Actualizar (parcial)")
    if not departamentos:
        mostrar_mensaje_info("No hay departamentos para actualizar.")
        return

    mostrar_lista_departamentos_detallada(departamentos)
    id_dep = pedir_numero_entero("ID a actualizar", minimo=1)
    dep = buscar_departamento_por_id(id_dep)
    if not dep:
        mostrar_mensaje_error("ID no encontrado.")
        return

    (ubi, amb, cap, est, pre) = pedir_datos_actualizacion(dep)

    ok = actualizar_departamento(id_dep, ubi, amb, cap, est, pre)
    if ok:
        mostrar_mensaje_exito("Departamento actualizado.")
    else:
        mostrar_mensaje_error("No se pudo actualizar.")


def reemplazar_depto():
    mostrar_subtitulo("Reemplazar COMPLETO")
    if not departamentos:
        mostrar_mensaje_info("No hay departamentos para reemplazar.")
        return

    mostrar_lista_departamentos_detallada(departamentos)
    id_dep = pedir_numero_entero("ID a reemplazar", minimo=1)

    ubicacion = pedir_input_con_validacion("Ubicación", lambda valor: campos_son_validos(valor), "No puede estar vacío")
    ambientes = pedir_numero_entero("Ambientes (≥ 1)", minimo=1)
    capacidad = pedir_numero_entero("Capacidad (≥ 1)", minimo=1)
    estado = pedir_estado_departamento()
    precio = pedir_numero_decimal("Precio por noche (≥ 0.01)", minimo=0.01)

    ok = reemplazar_departamento(id_dep, ubicacion, ambientes, capacidad, estado, precio)
    if ok:
        mostrar_mensaje_exito("Departamento reemplazado.")
    else:
        mostrar_mensaje_error("ID no encontrado.")


def depto_baja_logica():
    mostrar_subtitulo("Baja lógica")
    if not departamentos:
        mostrar_mensaje_info("No hay departamentos para dar de baja.")
        return

    mostrar_lista_departamentos_detallada(departamentos)
    id_dep = pedir_numero_entero("ID a dar de baja", minimo=1)

    ok = baja_logica_departamento(id_dep)
    if ok:
        mostrar_mensaje_exito("Departamento marcado como INACTIVO.")
    else:
        mostrar_mensaje_error("ID no encontrado.")


def depto_alta_logica():
    mostrar_subtitulo("Alta lógica")
    if not departamentos:
        mostrar_mensaje_info("No hay departamentos para dar de alta.")
        return

    mostrar_lista_departamentos_detallada(departamentos)
    id_dep = pedir_numero_entero("ID a dar de alta", minimo=1)

    ok = alta_logica_departamento(id_dep)
    if ok:
        mostrar_mensaje_exito("Departamento marcado como ACTIVO.")
    else:
        mostrar_mensaje_error("ID no encontrado.")


def buscar_depto_por_id():
    mostrar_subtitulo("Buscar por ID")
    if not departamentos:
        mostrar_mensaje_info("No hay departamentos cargados.")
        return

    id_dep = pedir_numero_entero("ID a buscar", minimo=1)
    dep = buscar_departamento_por_id(id_dep)
    if dep:
        mostrar_lista_departamentos_detallada([dep], "DEPARTAMENTO ENCONTRADO")
    else:
        mostrar_mensaje_error("ID no encontrado.")


# Funion que lista deptos activos
def listar_deptos_activos():
    mostrar_subtitulo("Listar ACTIVOS")
    activos = listar_departamentos_activos()
    mostrar_lista_departamentos_detallada(activos, "DEPARTAMENTOS ACTIVOS")


# Funcion que lista deptos
def listar_deptos():
    mostrar_subtitulo("Listar TODOS")
    mostrar_lista_departamentos_detallada(departamentos, "TODOS LOS DEPARTAMENTOS")


def menu_departamentos():
    mostrar_header_modulo("GESTIÓN DE DEPARTAMENTOS")
    opciones = [
        "Crear departamento",
        "Actualizar (parcial)",
        "Reemplazar (completo)",
        "Eliminar FÍSICO",
        "Baja lógica",
        "Alta lógica",
        "Buscar por ID",
        "Listar ACTIVOS",
        "Listar TODOS",
        "Volver al Menú Principal",
    ]

    continuar_menu = True

    while continuar_menu:
        mostrar_menu_opciones(opciones, "MENÚ DE DEPARTAMENTOS", 45)

        elec = pedir_opcion_menu(len(opciones))

        elec = int(elec)

        if elec == 1:
            creacion_depto()
        elif elec == 2:
            actualizar_depto()
        elif elec == 3:
            reemplazar_depto()
        elif elec == 4:
            eliminar_depto_fisico()
        elif elec == 5:
            depto_baja_logica()
        elif elec == 6:
            depto_alta_logica()
        elif elec == 7:
            buscar_depto_por_id()
        elif elec == 8:
            listar_deptos_activos()
        elif elec == 9:
            listar_deptos()
        elif elec == 10:
            mostrar_mensaje_info("Volviendo al Menú Principal...")
            continuar_menu = False

        if continuar_menu:
            pausar()


if __name__ == "__main__":
    menu_departamentos()