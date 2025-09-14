import random
import domain.clientes as clientes
import domain.departamentos as departamentos
import domain.reservas as reservas
import common.interfaz as interfaz

# --- Listas de datos de ejemplo para generar aleatoriedad ---
NOMBRES = ["Ana", "Juan", "Maria", "Carlos", "Sofia", "Luis", "Elena", "Miguel"]
APELLIDOS = ["Garcia", "Rodriguez", "Martinez", "Lopez", "Perez", "Gomez", "Sanchez"]
UBICACIONES = [
    "Capital Federal, Palermo", "Cordoba, Centro", "Rosario, Pichincha",
    "Mendoza, Ciudad", "Bariloche, Circuito Chico", "Salta, Casco Historico"
]


def poblar_datos_iniciales(num_clientes=5, num_deptos=5, num_reservas=7):
    """
    Verifica si las listas de dominio estan vacias y, de ser asi,
    las puebla con datos aleatorios de ejemplo.
    """
    # Se ejecuta solo si el sistema no tiene ningun cliente
    if not clientes.listar_clientes_activos():
        interfaz.mostrar_mensaje_info("Sistema vacio. Cargando datos de ejemplo...")

        # --- 1. Crear Clientes ---
        i = 0
        while i < num_clientes:
            nombre = random.choice(NOMBRES)
            apellido = random.choice(APELLIDOS)
            dni = str(random.randint(20000000, 45000000))
            telefono = "11" + str(random.randint(20000000, 69999999))
            clientes.agregar_cliente(nombre, apellido, dni, telefono)
            i = i + 1

        # --- 2. Crear Departamentos ---
        j = 0
        while j < num_deptos:
            ubicacion = random.choice(UBICACIONES)
            ambientes = random.randint(1, 4)
            capacidad = ambientes * 2
            precio = round(random.uniform(50.0, 250.0), 2)
            departamentos.agregar_departamento(ubicacion, ambientes, capacidad, "Disponible", precio)
            j = j + 1

        # --- 3. Crear Reservas ---
        clientes_existentes = clientes.listar_clientes_activos()
        deptos_existentes = departamentos.listar_departamentos_activos()
        ids_clientes = [c["id"] for c in clientes_existentes]
        ids_deptos = [d["id"] for d in deptos_existentes]

        k = 0
        intentos = 0  # Para evitar bucles infinitos si no hay disponibilidad
        while k < num_reservas and intentos < 50:
            id_cliente_sel = random.choice(ids_clientes)
            id_depto_sel = random.choice(ids_deptos)

            anio = 2025
            mes = random.randint(9, 12)
            dia_ingreso = random.randint(1, 20)
            duracion = random.randint(3, 8)
            dia_egreso = dia_ingreso + duracion

            fecha_ingreso_str = f"{dia_ingreso:02d}/{mes:02d}/{anio}"
            fecha_egreso_str = f"{dia_egreso:02d}/{mes:02d}/{anio}"

            if reservas.agregar_reserva(id_cliente_sel, id_depto_sel, fecha_ingreso_str, fecha_egreso_str):
                k = k + 1

            intentos = intentos + 1

        interfaz.mostrar_mensaje_exito(
            f"Se cargaron {num_clientes} clientes, {num_deptos} departamentos y {k} reservas.")