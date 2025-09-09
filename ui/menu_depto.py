from common.utils import *
from common.constantes import *
from domain.departamentos import *


# === CRUD básico ===
def agregar_departamento_eliminar():
    ubicacion_departamento= pedir_input_con_validacion("Ubicación: ")
    ambientes_departamento= pedir_numero_entero("Ambientes: ")
    capacidad_departamento= pedir_numero_entero("Capacidad: ")
    estado_departamento = pedir_input_con_validacion("Estado (Disponible/Ocupado): ")
    precio_departamento = pedir_numero_entero("Precio por noche: ")

    nuevo_depto = {
        "ubicacion_departamento": ubicacion_departamento,
        "ambientes_departamento": ambientes_departamento,
        "capacidad_departamento": capacidad_departamento,
        "estado_departamento": estado_departamento,
        "precio_departamento": precio_departamento,
        "activo": True,
    }

    departamentos.append(nuevo_depto)
    print(f"Departamento agregado con ID único {nuevo_depto['id_departamento']}")

def listar_departamentos():
    if not departamentos:
        print("No hay departamentos cargados.\n")
        return
    for depto in departamentos:
        print(f"ID: {depto['id_departamento']} - Ubicación: {depto['ubicacion_departamento']} - Activo: {depto.get('activo', True)}")
    print()

def desactivar_departamento():
    if not departamentos:
        print("No hay departamentos para desactivar.\n")
        return

    departamento_id = pedir_input_con_validacion("Ingrese el ID del departamento a desactivar: ")

    for depto in departamentos:
        if str(depto.get("id_departamento")) == str(departamento_id):
            if not depto.get("activo", True):
                print("El departamento ya está inactivo.\n")
                return
            confirmacion = pedir_input_con_validacion(
                f"¿Confirmás desactivar el depto (ID {depto['id_departamento']})? (s/n): "
            )
            if confirmacion.strip().lower()=="s":
                depto["activo"] = False
                print("Departamento desactivado correctamente.\n")
            else:
                print("Operación cancelada.\n")
            return
    print("No se encontró un departamento con ese ID.\n")


def activar_departamento():
    if not departamentos:
        print("No hay departamentos para activar.\n")
        return

    departamento_id = pedir_input_con_validacion("Ingrese el ID del departamento a activar: ")

    for depto in departamentos:
        if str(depto.get("id_departamento")) == str(departamento_id):
            if depto.get("activo", True):
                print("El departamento ya está activo.\n")
                return
            confirmacion = pedir_input_con_validacion(
                f"¿Confirmás activar el depto (ID {depto['id_departamento']})? (s/n): "
            )
            if confirmacion.strip().lower()=="s":
                depto["activo"] = True
                print("Departamento activado correctamente.\n")
            else:
                print("Operación cancelada.\n")
            return
    print("No se encontró un departamento con ese ID.\n")

def actualizar_departamento():
    if not departamentos:
        print("No hay departamentos para actualizar.\n")
        return

    departamento_id = pedir_input_con_validacion("Ingrese el ID del departamento a actualizar: ")

    for depto in departamentos:
        if str(depto.get("id_departamento")) == str(departamento_id):
            ubicacion = input("Nueva ubicación: ")
            ambientes = pedir_numero_entero("Nuevos ambientes: ")
            capacidad = pedir_numero_entero("Nueva capacidad: ")
            estado = input("Nuevo estado (Disponible/Ocupado): ")
            precio = pedir_numero_entero("Nuevo precio por noche: ")

            depto["ubicacion_departamento"] = ubicacion
            depto["ambientes_departamento"] = ambientes
            depto["capacidad_departamento"] = capacidad
            depto["estado_departamento"] = estado
            depto["precio_departamento"] = precio
            print("Departamento actualizado correctamente.\n")
            return

    print("No se encontró un departamento con ese ID.\n")


# === Menú ===
def menu_departamento():
    while True:
        print("""
--- MENÚ DE DEPARTAMENTOS ---
1) Agregar Departamento
2) Listar Departamentos
3) Desactivar Departamento
4) Activar Departamento
5) Actualizar Departamento
0) Salir
""")
        op = input("Opción: ")
        if op == "1":
            agregar_departamento()

        elif op == "2":
            listar_departamentos()
        elif op == "3":
            desactivar_departamento()
        elif op == "4":
            activar_departamento()
        elif op == "5":
            actualizar_departamento()
        elif op == "0":
            print("Nos vemos!")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu_departamento()