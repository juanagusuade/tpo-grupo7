import random
import domain.clientes as clientes
import domain.departamentos as departamentos
import domain.reservas as reservas
from common.constantes import (
    ID_CLIENTE, ID_DEPARTAMENTO, 
    ESTADO_DISPONIBLE, ESTADO_OCUPADO, ESTADO_MANTENIMIENTO
)
from common.validaciones import es_bisiesto, dias_en_mes, sumar_dias

NOMBRES = ["Ana", "Juan", "Maria", "Carlos", "Sofia", "Luis", "Elena", "Miguel", "Laura", "Pedro"]
APELLIDOS = ["Garcia", "Rodriguez", "Martinez", "Lopez", "Perez", "Gomez", "Sanchez", "Fernandez"]
UBICACIONES = [
    "Capital Federal, Palermo", "Cordoba, Centro", "Rosario, Pichincha",
    "Mendoza, Ciudad", "Bariloche, Circuito Chico", "Salta, Casco Historico"
]


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
    dias_maximos = dias_en_mes(mes, anio)
    dia = random.randint(1, dias_maximos - 10)
    return (dia, mes, anio)


def poblar_clientes(cantidad):
    """
    Genera clientes aleatorios.
    
    Parametros:
        cantidad (int): Cantidad de clientes a generar
    """
    for _ in range(cantidad):
        nombre = random.choice(NOMBRES)
        apellido = random.choice(APELLIDOS)
        dni = str(random.randint(20000000, 45000000))
        telefono = "11" + str(random.randint(20000000, 69999999))
        clientes.agregar_cliente(nombre, apellido, dni, telefono)


def poblar_departamentos(cantidad):
    """
    Genera departamentos aleatorios con estados variados.
    
    Parametros:
        cantidad (int): Cantidad de departamentos a generar
    """
    estados = [ESTADO_DISPONIBLE, ESTADO_OCUPADO, ESTADO_MANTENIMIENTO]
    
    for i in range(cantidad):
        ubicacion = random.choice(UBICACIONES)
        ambientes = random.randint(1, 4)
        capacidad = ambientes * 2
        precio = round(random.randint(5000, 25000) / 100.0, 2)
        
        # Garantizar al menos uno de cada estado en los primeros 3 deptos
        if i < 3:
            estado = estados[i]
        else:
            estado = random.choice(estados)
        
        departamentos.agregar_departamento(ubicacion, ambientes, capacidad, estado, precio)


def crear_reserva_aleatoria(ids_clientes_activos, ids_deptos_disponibles, dia, mes, anio, duracion):
    """
    Intenta crear una reserva aleatoria con los parametros dados.
    Solo usa clientes activos y departamentos disponibles.
    
    Parametros:
        ids_clientes_activos: Lista de IDs de clientes activos
        ids_deptos_disponibles: Lista de IDs de departamentos disponibles
        dia: Dia del mes
        mes: Mes del año
        anio: Año
        duracion: Duracion en dias
    
    Retorna:
        bool: True si se creo la reserva, False si fallo
    """
    if not ids_clientes_activos or not ids_deptos_disponibles:
        return False
    
    id_cliente_sel = random.choice(ids_clientes_activos)
    id_depto_sel = random.choice(ids_deptos_disponibles)
    
    fecha_ingreso = f"{dia:02d}/{mes:02d}/{anio}"
    fecha_egreso = sumar_dias(fecha_ingreso, duracion)
    
    if fecha_egreso and reservas.agregar_reserva(id_cliente_sel, id_depto_sel, fecha_ingreso, fecha_egreso):
        return True
    return False


def poblar_reservas_actuales(ids_clientes_activos, ids_deptos_disponibles, cantidad):
    """
    Genera reservas para el periodo actual (noviembre 8-15).
    
    Retorna:
        int: Cantidad de reservas creadas
    """
    creadas = 0
    for _ in range(cantidad):
        dia = random.randint(8, 15)
        duracion = random.randint(3, 7)
        if crear_reserva_aleatoria(ids_clientes_activos, ids_deptos_disponibles, dia, 11, 2025, duracion):
            creadas += 1
    return creadas


def poblar_reservas_futuras_cercanas(ids_clientes_activos, ids_deptos_disponibles, cantidad):
    """
    Genera reservas para el futuro cercano (noviembre 16-28 y diciembre 1-20).
    
    Retorna:
        int: Cantidad de reservas creadas
    """
    creadas = 0
    for _ in range(cantidad):
        dia, mes, anio = generar_fecha_valida(11, 12, 2025)
        if mes == 11:
            dia = random.randint(16, 28)
        else:
            dia = random.randint(1, 20)
        duracion = random.randint(5, 10)
        if crear_reserva_aleatoria(ids_clientes_activos, ids_deptos_disponibles, dia, mes, anio, duracion):
            creadas += 1
    return creadas


def poblar_reservas_futuras_lejanas(ids_clientes_activos, ids_deptos_disponibles, cantidad):
    """
    Genera reservas para el futuro lejano (diciembre 15-25).
    
    Retorna:
        int: Cantidad de reservas creadas
    """
    creadas = 0
    for _ in range(cantidad):
        dia = random.randint(15, 25)
        duracion = random.randint(4, 8)
        if crear_reserva_aleatoria(ids_clientes_activos, ids_deptos_disponibles, dia, 12, 2025, duracion):
            creadas += 1
    return creadas


def cancelar_algunas_reservas(cantidad_a_cancelar=2):
    """
    Cancela aleatoriamente algunas reservas activas.
    
    Retorna:
        int: Cantidad de reservas canceladas
    """
    todas_reservas = reservas.obtener_reservas_activas()
    canceladas = 0
    
    if not todas_reservas:
        return 0
    
    # Asegurar que no cancelemos mas reservas de las que existen
    cantidad_real = min(cantidad_a_cancelar, len(todas_reservas))
    
    # Crear una copia de la lista para ir removiendo las reservas ya seleccionadas
    reservas_disponibles = todas_reservas.copy()
    
    for _ in range(cantidad_real):
        if not reservas_disponibles:
            break
        
        reserva_sel = random.choice(reservas_disponibles)
        reservas_disponibles.remove(reserva_sel)
        
        if reservas.cancelar_reserva(reserva_sel[0]):
            canceladas += 1
    
    return canceladas


def dar_baja_algunos_clientes(cantidad_a_dar_baja=2):
    """
    Da de baja aleatoriamente algunos clientes activos.
    
    Retorna:
        int: Cantidad de clientes dados de baja
    """
    clientes_activos = clientes.listar_clientes_activos()
    dados_de_baja = 0
    
    if not clientes_activos:
        return 0
    
    # Asegurar que no demos de baja mas clientes de los que existen
    cantidad_real = min(cantidad_a_dar_baja, len(clientes_activos))
    
    # Crear una copia para ir removiendo los clientes ya seleccionados
    clientes_disponibles = clientes_activos.copy()
    
    for _ in range(cantidad_real):
        if not clientes_disponibles:
            break
        
        cliente_sel = random.choice(clientes_disponibles)
        clientes_disponibles.remove(cliente_sel)
        
        if clientes.baja_logica_cliente(cliente_sel[ID_CLIENTE]):
            dados_de_baja += 1
    
    return dados_de_baja


def cambiar_estados_departamentos(cantidad_a_cambiar=2):
    """
    Cambia el estado de algunos departamentos a Mantenimiento o los da de baja.
    
    Retorna:
        int: Cantidad de departamentos modificados
    """
    deptos_activos = departamentos.listar_departamentos_activos()
    modificados = 0
    
    if not deptos_activos:
        return 0
    
    # Asegurar que no modifiquemos mas deptos de los que existen
    cantidad_real = min(cantidad_a_cambiar, len(deptos_activos))
    
    # Crear una copia para ir removiendo los deptos ya seleccionados
    deptos_disponibles = deptos_activos.copy()
    
    for _ in range(cantidad_real):
        if not deptos_disponibles:
            break
        
        depto_sel = random.choice(deptos_disponibles)
        deptos_disponibles.remove(depto_sel)
        
        # 50% dar de baja, 50% poner en mantenimiento
        if random.random() < 0.5:
            if departamentos.baja_logica_departamento(depto_sel[ID_DEPARTAMENTO]):
                modificados += 1
        else:
            if departamentos.actualizar_departamento(
                depto_sel[ID_DEPARTAMENTO],
                depto_sel["ubicacion"],
                depto_sel["ambientes"],
                depto_sel["capacidad"],
                ESTADO_MANTENIMIENTO,
                depto_sel["precio_noche"]
            ):
                modificados += 1
    
    return modificados


def poblar_datos_iniciales(num_clientes=16, num_deptos=12, num_reservas=24):
    """
    Verifica si las listas de dominio estan vacias y las puebla con datos de ejemplo.
    Garantiza variedad de estados en clientes, departamentos y reservas.
    
    Parametros:
        num_clientes (int): Cantidad de clientes a generar
        num_deptos (int): Cantidad de departamentos a generar
        num_reservas (int): Cantidad de reservas a intentar generar
    """
    if not clientes.listar_clientes_activos():
        print("[i] INFO: Sistema vacio. Cargando datos de ejemplo...")

        # Poblar clientes y departamentos (con estados variados)
        poblar_clientes(num_clientes)
        poblar_departamentos(num_deptos)

        # Obtener IDs de clientes activos y departamentos disponibles para crear reservas
        clientes_activos = clientes.listar_clientes_activos()
        deptos_activos = departamentos.listar_departamentos_activos()
        
        # Filtrar solo departamentos disponibles para crear reservas
        deptos_disponibles = [d for d in deptos_activos 
                             if d.get("estado") == ESTADO_DISPONIBLE]
        
        ids_clientes_activos = [c[ID_CLIENTE] for c in clientes_activos]
        ids_deptos_disponibles = [d[ID_DEPARTAMENTO] for d in deptos_disponibles]

        # Crear reservas de diferentes tipos usando solo clientes activos y deptos disponibles
        cantidad_por_tipo = num_reservas // 3
        reservas_actuales = poblar_reservas_actuales(ids_clientes_activos, ids_deptos_disponibles, cantidad_por_tipo)
        reservas_futuras_cercanas = poblar_reservas_futuras_cercanas(ids_clientes_activos, ids_deptos_disponibles, cantidad_por_tipo)
        
        resto = num_reservas - (cantidad_por_tipo * 2)
        reservas_futuras_lejanas = poblar_reservas_futuras_lejanas(ids_clientes_activos, ids_deptos_disponibles, resto)
        
        reservas_creadas = reservas_actuales + reservas_futuras_cercanas + reservas_futuras_lejanas
        reservas_futuras_total = reservas_futuras_cercanas + reservas_futuras_lejanas

        # Agregar variedad: cancelar algunas reservas
        reservas_canceladas = cancelar_algunas_reservas(2)
        
        # Agregar variedad: dar de baja algunos clientes
        clientes_inactivos = dar_baja_algunos_clientes(2)
        
        # Agregar variedad: cambiar estados de algunos departamentos
        deptos_modificados = cambiar_estados_departamentos(2)

        # Mostrar resumen
        print(
            f"\n[✓] EXITO: Datos cargados:\n" +
            f"  - {num_clientes} clientes ({clientes_inactivos} dados de baja)\n" +
            f"  - {num_deptos} departamentos ({deptos_modificados} modificados)\n" +
            f"  - {reservas_creadas} reservas ({reservas_actuales} actuales, {reservas_futuras_total} futuras)\n" +
            f"  - {reservas_canceladas} reservas canceladas\n"
        )