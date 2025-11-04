import random
import domain.clientes as clientes
import domain.departamentos as departamentos
import domain.reservas as reservas
import common.interfaz as interfaz
from common.constantes import ID_CLIENTE, ID_DEPARTAMENTO

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
    
    Parametros:
        num_clientes (int): Cantidad de clientes a generar
        num_deptos (int): Cantidad de departamentos a generar
        num_reservas (int): Cantidad de reservas a intentar generar
    """
    if not clientes.listar_clientes_activos():
        interfaz.mostrar_mensaje_info("Sistema vacio. Cargando datos de ejemplo...")

        for _ in range(num_clientes):
            nombre = random.choice(NOMBRES)
            apellido = random.choice(APELLIDOS)
            dni = str(random.randint(20000000, 45000000))
            telefono = "11" + str(random.randint(20000000, 69999999))
            clientes.agregar_cliente(nombre, apellido, dni, telefono)

        for _ in range(num_deptos):
            ubicacion = random.choice(UBICACIONES)
            ambientes = random.randint(1, 4)
            capacidad = ambientes * 2
            precio = round(random.uniform(50.0, 250.0), 2)
            departamentos.agregar_departamento(ubicacion, ambientes, capacidad, "Disponible", precio)

        clientes_existentes = clientes.listar_clientes_activos()
        deptos_existentes = departamentos.listar_departamentos_activos()

        ids_clientes = list(map(lambda c: c[ID_CLIENTE], clientes_existentes))
        ids_deptos = list(map(lambda d: d[ID_DEPARTAMENTO], deptos_existentes))

        k = 0
        intentos = 0

        for _ in range(num_reservas):
            if intentos < 50:
                reserva_creada = False
                while not reserva_creada and intentos < 50:
                    id_cliente_sel = random.choice(ids_clientes)
                    id_depto_sel = random.choice(ids_deptos)

                    anio = 2025
                    mes = random.randint(10, 12)
                    
                    # Determinar días máximos del mes
                    if mes == 2:
                        # Verificar año bisiesto
                        es_bisiesto = (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)
                        dias_maximos = 29 if es_bisiesto else 28
                    elif mes in [4, 6, 9, 11]:
                        dias_maximos = 30
                    else:
                        dias_maximos = 31
                    
                    # Limitar el dia de ingreso para que no se pase del mes
                    dia_ingreso = random.randint(1, min(20, dias_maximos - 8))
                    duracion = random.randint(3, 8)
                    dia_egreso = dia_ingreso + duracion
                    
                    # Asegurar que el dia de egreso no exceda el mes
                    if dia_egreso <= dias_maximos:
                        fecha_ingreso_str = f"{dia_ingreso:02d}/{mes:02d}/{anio}"
                        fecha_egreso_str = f"{dia_egreso:02d}/{mes:02d}/{anio}"

                        if reservas.agregar_reserva(id_cliente_sel, id_depto_sel, fecha_ingreso_str, fecha_egreso_str):
                            k = k + 1
                            reserva_creada = True

                    intentos = intentos + 1

        interfaz.mostrar_mensaje_exito(
            f"Se cargaron {num_clientes} clientes, {num_deptos} departamentos y {k} reservas.")