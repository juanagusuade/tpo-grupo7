import random
import domain.clientes as clientes
import domain.departamentos as departamentos
import domain.reservas as reservas
import common.interfaz as interfaz
from common.constantes import ID_CLIENTE, ID_DEPARTAMENTO

NOMBRES = ["Ana", "Juan", "Maria", "Carlos", "Sofia", "Luis", "Elena", "Miguel", "Laura", "Pedro"]
APELLIDOS = ["Garcia", "Rodriguez", "Martinez", "Lopez", "Perez", "Gomez", "Sanchez", "Fernandez"]
UBICACIONES = [
    "Capital Federal, Palermo", "Cordoba, Centro", "Rosario, Pichincha",
    "Mendoza, Ciudad", "Bariloche, Circuito Chico", "Salta, Casco Historico"
]


def calcular_dias_en_mes(mes, anio):
    """
    Calcula la cantidad de dias que tiene un mes especifico.
    
    Parametros:
        mes (int): Numero del mes (1-12)
        anio (int): Año
    
    Retorna:
        int: Cantidad de dias del mes
    """
    if mes == 2:
        es_bisiesto = (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)
        return 29 if es_bisiesto else 28
    if mes in [4, 6, 9, 11]:
        return 30
    return 31


def generar_fecha_valida(mes_inicio, mes_fin, anio):
    """
    Genera una fecha valida dentro de un rango de meses.
    
    Parametros:
        mes_inicio (int): Mes inicial
        mes_fin (int): Mes final
        anio (int): Año
    
    Retorna:
        tuple: (dia, mes, anio)
    """
    mes = random.randint(mes_inicio, mes_fin)
    dias_maximos = calcular_dias_en_mes(mes, anio)
    dia = random.randint(1, dias_maximos - 10)
    return (dia, mes, anio)


def poblar_datos_iniciales(num_clientes=8, num_deptos=6, num_reservas=12):
    """
    Verifica si las listas de dominio estan vacias y, de ser asi,
    las puebla.
    
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
            precio = round(random.randint(5000, 25000) / 100.0, 2)
            departamentos.agregar_departamento(ubicacion, ambientes, capacidad, "Disponible", precio)

        clientes_existentes = clientes.listar_clientes_activos()
        deptos_existentes = departamentos.listar_departamentos_activos()

        ids_clientes = list(map(lambda c: c[ID_CLIENTE], clientes_existentes))
        ids_deptos = list(map(lambda d: d[ID_DEPARTAMENTO], deptos_existentes))

        reservas_creadas = 0
        reservas_pasadas = 0
        reservas_actuales = 0
        reservas_futuras = 0

        for _ in range(num_reservas // 3):
            id_cliente_sel = random.choice(ids_clientes)
            id_depto_sel = random.choice(ids_deptos)
            
            dia, mes, anio = generar_fecha_valida(8, 9, 2025)
            duracion = random.randint(3, 7)
            dia_egreso = dia + duracion
            
            fecha_ingreso = f"{dia:02d}/{mes:02d}/{anio}"
            fecha_egreso = f"{dia_egreso:02d}/{mes:02d}/{anio}"
            
            if reservas.agregar_reserva(id_cliente_sel, id_depto_sel, fecha_ingreso, fecha_egreso):
                reservas_creadas += 1
                reservas_pasadas += 1

        for _ in range(num_reservas // 4):
            id_cliente_sel = random.choice(ids_clientes)
            id_depto_sel = random.choice(ids_deptos)
            
            dia, mes, anio = generar_fecha_valida(11, 11, 2025)
            dia = random.randint(1, 5)
            duracion = random.randint(5, 10)
            dia_egreso = dia + duracion
            
            fecha_ingreso = f"{dia:02d}/{mes:02d}/{anio}"
            fecha_egreso = f"{dia_egreso:02d}/{mes:02d}/{anio}"
            
            if reservas.agregar_reserva(id_cliente_sel, id_depto_sel, fecha_ingreso, fecha_egreso):
                reservas_creadas += 1
                reservas_actuales += 1

        resto = num_reservas - (num_reservas // 3) - (num_reservas // 4)
        for _ in range(resto):
            id_cliente_sel = random.choice(ids_clientes)
            id_depto_sel = random.choice(ids_deptos)
            
            mes = random.choice([11, 12])
            dia, mes, anio = generar_fecha_valida(mes, mes, 2025)
            if mes == 11:
                dia = random.randint(10, 28)
            duracion = random.randint(4, 8)
            dia_egreso = dia + duracion
            
            fecha_ingreso = f"{dia:02d}/{mes:02d}/{anio}"
            fecha_egreso = f"{dia_egreso:02d}/{mes:02d}/{anio}"
            
            if reservas.agregar_reserva(id_cliente_sel, id_depto_sel, fecha_ingreso, fecha_egreso):
                reservas_creadas += 1
                reservas_futuras += 1

        todas_reservas = reservas.obtener_reservas_activas()
        reservas_canceladas = 0
        if len(todas_reservas) >= 2:
            for _ in range(min(2, len(todas_reservas))):
                reserva_sel = random.choice(todas_reservas)
                if reservas.cancelar_reserva(reserva_sel[0]):
                    reservas_canceladas += 1

        interfaz.mostrar_mensaje_exito(
            f"Datos cargados:\n" +
            f"  - {num_clientes} clientes\n" +
            f"  - {num_deptos} departamentos\n" +
            f"  - {reservas_creadas} reservas ({reservas_pasadas} pasadas, {reservas_actuales} actuales, {reservas_futuras} futuras)\n" +
            f"  - {reservas_canceladas} reservas canceladas"
        )