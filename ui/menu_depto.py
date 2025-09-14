from common.constantes import *
from common.entrada_datos import *
from common.interfaz import *
from domain.departamentos import *



def imprimir_departamento(dep: dict):

    idd = dep.get(ID_DEPARTAMENTO, "N/A")
    ubicacion = dep.get(UBICACION_DEPARTAMENTO, "N/A")
    ambientes = dep.get(AMBIENTES_DEPARTAMENTO, "N/A")
    capacidad = dep.get(CAPACIDAD_DEPARTAMENTO, "N/A")
    estado = dep.get(ESTADO_DEPARTAMENTO, "N/A")
    precio = dep.get(PRECIO_DEPARTAMENTO, "N/A")
    activo = dep.get(ACTIVO_DEPARTAMENTO, False)

    etiqueta_activo = f"{COLOR_VERDE}✅ ACTIVO{COLOR_RESET}" if activo else f"{COLOR_ROJO}⛔ INACTIVO{COLOR_RESET}"

    print(f"\n{COLOR_AZUL}Departamento{COLOR_RESET}")
    print(f"{COLOR_CYAN}ID:{COLOR_RESET} {idd}")
    print(f"{COLOR_CYAN}Ubicacion:{COLOR_RESET} {ubicacion}")
    print(f"{COLOR_CYAN}Ambientes:{COLOR_RESET} {ambientes}")
    print(f"{COLOR_CYAN}Capacidad:{COLOR_RESET} {capacidad}")
    print(f"{COLOR_CYAN}Estado:{COLOR_RESET} {estado}")
    print(f"{COLOR_CYAN}Precio/Noche:{COLOR_RESET} {precio}")
    print(f"{COLOR_CYAN}Activo:{COLOR_RESET} {etiqueta_activo}\n")



def imprimir_lista(lista: list):
    if not lista:
        mostrar_mensaje_info("No hay departamentos cargados.")
        return
    for d in lista:
        imprimir_departamento(d)
    mostrar_separador()



def creacion_depto():
    mostrar_subtitulo("Crear departamento")
    ubicacion = pedir_input_con_validacion("Ubicacion", lambda valor: validar_campos(valor), "No puede estar vacio")
    ambientes = pedir_numero_entero("Ambientes (≥ 1)", minimo=1)
    capacidad = pedir_numero_entero("Capacidad (≥ 1)", minimo=1)
    estado = pedir_estado_departamento()
    precio = pedir_numero_decimal("Precio por noche (≥ 0.01)", minimo=0.01)

    ok = agregar_departamento(ubicacion, ambientes, capacidad, estado, precio)
    if ok:
        mostrar_mensaje_exito("Departamento creado correctamente.")
    else:
        mostrar_mensaje_error("No se pudo crear el departamento.")
    pausar()


def eliminar_depto_fisico():
    mostrar_subtitulo("Eliminar departamento (FÍSICO)")
    if not departamentos:
        mostrar_mensaje_info("No hay departamentos para eliminar.")
        pausar(); return

    imprimir_lista(departamentos)
    id_dep = pedir_numero_entero("ID a eliminar", minimo=1)

    if not confirmar_accion("¿Estas seguro de eliminar definitivamente"):
        mostrar_mensaje_info("Accion cancelada.")
        pausar(); return

    ok = eliminar_departamento(id_dep)
    if ok:
        mostrar_mensaje_exito("Departamento eliminado.")
    else:
        mostrar_mensaje_error("ID no encontrado.")
    pausar()


def actualizar_depto():
    mostrar_subtitulo("Actualizar (parcial)")
    if not departamentos:
        mostrar_mensaje_info("No hay departamentos para actualizar.")
        pausar(); return

    imprimir_lista(departamentos)
    id_dep = pedir_numero_entero("ID a actualizar", minimo=1)
    dep = buscar_departamento_por_id(id_dep)
    if not dep:
        mostrar_mensaje_error("ID no encontrado.")
        pausar(); return


    idd = dep.get(ID_DEPARTAMENTO)
    ubicacion = dep.get(UBICACION_DEPARTAMENTO)
    ambientes = dep.get(AMBIENTES_DEPARTAMENTO)
    capacidad = dep.get(CAPACIDAD_DEPARTAMENTO)
    estado = dep.get(ESTADO_DEPARTAMENTO)
    precio = dep.get(PRECIO_DEPARTAMENTO)

    print(f"Deja vacío para mantener el valor actual.")


    nueva_ubi = pedir_input_con_validacion(
        f"Ubicación actual [{ubicacion}] (enter para mantener)",
        lambda valor: validar_campos(valor),
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
    if val is None:
        nuevo_amb = ambientes
    else:
        nuevo_amb = int(val)



    val = pedir_input_con_validacion(
        f"Capacidad actual [{capacidad}] (enter para mantener)",
        lambda s: s.isdigit(),
        "Debe ser entero positivo",
        es_opcional=True
    )
    if val is None:
        nueva_cap = capacidad
    else:
        nueva_cap = int(val)


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
    if val is None:
        nuevo_pre = precio
    else:
        nuevo_pre = float(val)


    ok = actualizar_departamento(id_dep, nueva_ubi, nuevo_amb, nueva_cap, nuevo_est, nuevo_pre)
    if ok:
        mostrar_mensaje_exito("Departamento actualizado.")
    else:
        mostrar_mensaje_error("No se pudo actualizar.")
    pausar()


def reemplzar_depto():
    mostrar_subtitulo("Reemplazar COMPLETO")
    if not departamentos:
        mostrar_mensaje_info("No hay departamentos para reemplazar.")
        pausar(); return

    imprimir_lista(departamentos)
    id_dep = pedir_numero_entero("ID a reemplazar", minimo=1)

    ubicacion = pedir_input_con_validacion("Ubicación", lambda valor: validar_campos(valor), "No puede estar vacío")
    ambientes = pedir_numero_entero("Ambientes (≥ 1)", minimo=1)
    capacidad = pedir_numero_entero("Capacidad (≥ 1)", minimo=1)
    estado = pedir_estado_departamento()
    precio = pedir_numero_decimal("Precio por noche (≥ 0.01)", minimo=0.01)

    ok = reemplazar_departamento(id_dep, ubicacion, ambientes, capacidad, estado, precio)
    if ok:
        mostrar_mensaje_exito("Departamento reemplazado.")
    else:
        mostrar_mensaje_error("ID no encontrado.")
    pausar()


def depto_baja_logica():
    mostrar_subtitulo("Baja lógica")
    if not departamentos:
        mostrar_mensaje_info("No hay departamentos para dar de baja.")
        pausar(); return

    imprimir_lista(departamentos)
    id_dep = pedir_numero_entero("ID a dar de baja", minimo=1)

    ok = baja_logica_departamento(id_dep)
    if ok:
        mostrar_mensaje_exito("Departamento marcado como INACTIVO.")
    else:
        mostrar_mensaje_error("ID no encontrado.")
    pausar()


def depto_alta_logica():
    mostrar_subtitulo("Alta lógica")
    if not departamentos:
        mostrar_mensaje_info("No hay departamentos para dar de alta.")
        pausar(); return

    imprimir_lista(departamentos)
    id_dep = pedir_numero_entero("ID a dar de alta", minimo=1)

    ok = alta_logica_departamento(id_dep)
    if ok:
        mostrar_mensaje_exito("Departamento marcado como ACTIVO.")
    else:
        mostrar_mensaje_error("ID no encontrado.")
    pausar()


def buscar_depto_por_id():
    mostrar_subtitulo("Buscar por ID")
    if not departamentos:
        mostrar_mensaje_info("No hay departamentos cargados.")
        pausar(); return

    id_dep = pedir_numero_entero("ID a buscar", minimo=1)
    dep = buscar_departamento_por_id(id_dep)
    if dep:
        imprimir_departamento(dep)
    else:
        mostrar_mensaje_error("ID no encontrado.")
    pausar()

#Funion que lista deptos activos
def listar_deptos_activos():
    mostrar_subtitulo("Listar ACTIVOS")
    activos = listar_departamentos_activos()
    imprimir_lista(activos)
    pausar()

#Funcion que lista deptos
def listar_deptos():
    mostrar_subtitulo("Listar TODOS")
    imprimir_lista(departamentos)
    pausar()

#Menu departamento
def menu_departamentos():
    mostrar_titulo("Menú de Departamentos")
    opciones = [
        "Crear departamento",
        "Actualizar (parcial)",
        "Reemplazar (completo)",
        "Eliminar FÍSICO",
        "Baja logca",
        "Alta logica",
        "Buscar por ID",
        "Listar ACTIVOS",
        "Listar TODOS",
        "Salir",
    ]

    while True:
        mostrar_opciones_menu(opciones, "Opciones")
        elec = pedir_input_con_validacion(
            "Eleji una opcion (1-10)",
            lambda validacion_menu: validacion_menu.isdigit() and 1 <= int(validacion_menu) <= 10,
            "Debe ser un numero entre 1 y 10",
        )
        elec = int(elec)

        if elec == 1: creacion_depto()
        elif elec == 2: actualizar_depto()
        elif elec == 3: reemplzar_depto()
        elif elec == 4: eliminar_depto_fisico()
        elif elec == 5: depto_baja_logica()
        elif elec == 6: depto_alta_logica()
        elif elec == 7: buscar_depto_por_id()
        elif elec == 8: listar_deptos_activos()
        elif elec == 9: listar_deptos()
        elif elec == 10:
            mostrar_mensaje_info("Saliendooo")
            break



if __name__ == "__main__":
    menu_departamentos()