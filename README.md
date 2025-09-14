# Sistema de Gestión de Alquileres Temporarios

## Definición de la temática del proyecto
Este sistema permite administrar eficientemente el alquiler temporal de distintos departamentos, facilitando el control de las unidades disponibles, la gestión de clientes y la organización de reservas. Está orientado a propietarios o administradores que deseen automatizar el proceso de registro, asignación y seguimiento de estadías.

Las entidades principales serán:
- **Clientes**: contienen los datos personales de los inquilinos.
- **Departamentos**: representan cada unidad disponible para alquiler con sus características (ubicación, número de ambientes, capacidad, estado, precio por noche).
- **Reservas**: vinculan a un cliente con un departamento en un período determinado.

## Objetivos
- Desarrollar un sistema que permita registrar, modificar, consultar y eliminar información sobre clientes, departamentos y reservas.
- Automatizar el proceso de reserva para evitar solapamientos de fechas o unidades ya ocupadas.
- Facilitar la consulta rápida de disponibilidad y estadísticas relacionadas con la ocupación.
- Implementar una interfaz sencilla y comprensible.

## Funcionalidades principales
- Registro, modificación y eliminación de clientes.
- Registro, modificación del estado y eliminación de departamentos.
- Creación, modificación y cancelación de reservas.
- Validación de datos para evitar reservas superpuestas o departamentos ya ocupados.
- Búsqueda de reservas por cliente o por departamento.
- Consulta de disponibilidad de un departamento en fechas específicas.
- Generación de estadísticas básicas: porcentaje de ocupación por departamento, promedio de duración de reservas y cantidad total de reservas realizadas en un período.
- Almacenamiento y recuperación de la información registrada.

## Esbozo de matrices de datos y tipos de datos

### Tabla: Clientes (Lista de Diccionarios)
| ID Cliente (int) | Nombre (string) | Apellido (string) | DNI (string) | Teléfono (string) | Activo (bool) |
|------------------|-----------------|-------------------|--------------|-------------------|---------------|
| 1                | Juan            | Pérez             | 30111222     | 1122334455        | True          |
| 2                | María           | Gómez             | 29888777     | 1144455566        | True          |
| 3                | Lucas           | Fernández         | 28444555     | 1177788899        | True          |
| 4                | Ana             | Martínez          | 31222333     | 1133344455        | True          |
| 5                | Pedro           | López             | 29999111     | 1199988877        | True          |

### Tabla: Departamentos (Lista de Diccionarios)
| ID Dpto (int) | Ubicación (string)      | Ambientes (int) | Capacidad (int) | Estado (string) | Precio/Noche (float) | Activo (bool) |
|---------------|-------------------------|-----------------|-----------------|-----------------|----------------------|---------------|
| 1             | Buenos Aires, Centro    | 2               | 4               | Disponible      | 75.50                | True          |
| 2             | Córdoba, Nueva Córdoba  | 1               | 2               | Ocupado         | 50.00                | True          |
| 3             | Mendoza, Ciudad         | 3               | 6               | Disponible      | 120.00               | True          |
| 4             | Rosario, Centro         | 2               | 4               | Disponible      | 80.00                | True          |
| 5             | Mar del Plata, Playa    | 1               | 2               | Ocupado         | 65.00                | True          |

### Tabla: Reservas (Matriz - Lista de Listas)
| ID Reserva (int) | ID Cliente (int) | ID Dpto (int) | Fecha Ingreso (string) | Fecha Egreso (string) | Estado (string) |
|------------------|------------------|---------------|------------------------|----------------------|-----------------|
| 1                | 1                | 2             | 10/08/2025             | 15/08/2025           | ACTIVO          |
| 2                | 3                | 5             | 01/09/2025             | 05/09/2025           | ACTIVO          |
| 3                | 2                | 1             | 20/08/2025             | 25/08/2025           | ACTIVO          |
| 4                | 4                | 4             | 18/08/2025             | 22/08/2025           | ACTIVO          |
| 5                | 5                | 3             | 10/09/2025             | 15/09/2025           | ACTIVO          |

## Convenciones de Codificación

### 1. Estructura General del Proyecto
```
Sistema-Alquileres/
├── main.py                              # Punto de entrada, menús e interfaz
├── README.md                            # Esta documentación facherita

└── ui/                                  # Ayudas para UI
    ├── presentacion_clientes.py         # Presentacion de UI para clientes
    ├── presentacion_departamentos.py    # Presentacion de UI para departamentos
    
└── common/                              # Funcionalidades comunes a las entidades.
    ├── utils.py                         # Utilidades basicas y validaciones
    ├── constantes.py                    # Constantes varias
    
└── domain/                              # Lógica de negocio
    ├── clientes.py                      # CRUD de clientes (diccionarios)
    ├── departamentos.py                 # CRUD de departamentos (diccionarios)
    └── reservas.py                      # CRUD de reservas (matriz)
```

### 2. Estructuras de Datos
- **Clientes**: Lista de diccionarios
- **Departamentos**: Lista de diccionarios 
- **Reservas**: Matriz (lista de listas) con constantes para índices
- **Fechas**: Se almacenan como strings en formato "dd/mm/yyyy"
- **IDs**: Se generan como números enteros únicos de 5 dígitos

#### Estructura de Cliente (Diccionario):
```python
cliente = {
    "id": 12345,
    "nombre": "Juan",
    "apellido": "Perez",
    "dni": "12345678",
    "telefono": "1122334455",
    "activo": True
}
```

#### Estructura de Departamento (Diccionario):
```python
departamento = {
    "id": 12345,
    "ubicacion": "Centro",
    "ambientes": 3,
    "capacidad": 4,
    "estado": "Disponible",
    "precio_noche": 100.0,
    "activo": True
}
```

#### Estructura de Reserva (Lista con constantes):
```python
# Constantes para acceso a indices
INDICE_ID_RESERVA = 0
INDICE_ID_CLIENTE = 1
INDICE_ID_DEPARTAMENTO = 2
INDICE_FECHA_INGRESO = 3
INDICE_FECHA_EGRESO = 4
INDICE_ESTADO = 5

reserva = [12345, 67890, 54321, "25/08/2025", "30/08/2025", "ACTIVO"]
```

### 3. Convenciones de Nomenclatura
- **Variables y funciones**: snake_case (ej: `agregar_cliente`, `lista_clientes`)
- **Constantes**: UPPER_CASE (ej: `ESTADO_ACTIVO`, `INDICE_ID_RESERVA`)
- **Archivos**: snake_case con extensión .py (ej: `clientes.py`, `utils.py`)

### 4. Funciones de Dominio
- **Retornan valores booleanos**: `True` para éxito, `False` para error
- **No imprimen mensajes**: Los mensajes se manejan en el archivo `main.py`
- **Validación de entrada**: Se realiza antes de llamar a las funciones de dominio
- **Encapsulación**: Las listas no se pasan como parámetros (excepto para ID generation en utils)

#### Ejemplo de función de dominio:
```python
def agregar_cliente(nombre, apellido, dni, telefono):
    """Agrega un nuevo cliente verificando que el DNI no se repita"""
    i = 0
    while i < len(clientes):
        if clientes[i][DNI_CLIENTE] == dni:
            return False
        i = i + 1

    id_cliente = generar_id_unico_diccionario(clientes, ID_CLIENTE)
    nuevo_cliente = {
        ID_CLIENTE: id_cliente,
        NOMBRE_CLIENTE: nombre,
        APELLIDO_CLIENTE: apellido,
        DNI_CLIENTE: dni,
        TELEFONO_CLIENTE: telefono,
        ACTIVO_CLIENTE: True
    }
    clientes.append(nuevo_cliente)
    return True

```

### 5. Validaciones
- **Campos obligatorios**: Se valida que no sean None (Null o nulos) ni strings vacíos
- **Fechas**: Formato obligatorio dd/mm/yyyy, validación de fecha real
- **IDs únicos**: Generación automática de 5 dígitos, verificación de unicidad (que sean unicos)
- **Tipos de datos**: Validación específica para enteros y decimales

### 6. Estados del Sistema
#### Estados de Reserva:
- `ESTADO_ACTIVO`: Reserva vigente
- `ESTADO_CANCELADO`: Reserva cancelada (puede reactivarse)
- `ESTADO_ELIMINADO`: Reserva eliminada (baja lógica)

#### Estados de Departamento:
- `"Disponible"`: Listo para reservar
- `"Ocupado"`: Con reserva activa
- `"Mantenimiento"`: No disponible temporalmente

### 7. Manejo de Fechas
- **Almacenamiento**: Strings en formato "dd/mm/yyyy"
- **Validación**: Función `validar_fecha()` en utils.py
- **Comparación**: Función `comparar_fechas_string()` convierte a formato numérico
- **Entrada del usuario**: Solo se acepta formato dd/mm/yyyy

### 8. Arquitectura de la Aplicación
- **main.py**: Interfaz de usuario, menús, entrada/salida, manejo de errores
- **domain/**: Lógica de negocio pura, sin interfaz de usuario
- **ui/**: Funciones de ayuda para la interfaz de usuario
- **common/**: Funciones de utilidad que pueden ser reutilizadas

### 9. Principios de Programación Aplicados
- **Separación de responsabilidades**: UI separada de lógica de negocio
- **Funciones puras**: Las funciones de dominio no tienen efectos secundarios de impresión
- **Validación temprana**: Se valida entrada antes de procesar
- **Consistencia**: Mismo patrón para todas las operaciones CRUD
- **Encapsulación estratégica**: Datos "privados" en módulos de dominio

### 10. Generación de IDs
- **Dos funciones especializadas** en utils.py:
  - `generar_id_unico_lista(lista)`: Para reservas (matriz)
  - `generar_id_unico_diccionario(lista, clave_id)`: Para clientes y departamentos
- **Excepción a encapsulación**: Solo utils accede a las estructuras de datos para evitar duplicación de código
- **Rango**: IDs de 5 dígitos (10000-99999)

### 11. Comentarios y Documentación
- **Docstrings**: Una línea descriptiva para cada función
- **Comentarios inline**: Explicar índices en las listas y lógica compleja
- **Formato**: Claro y conciso, enfocado en qué hace la función

#### Ejemplo de comentarios:
```python
def buscar_cliente_por_id(id_cliente):
    """Busca un cliente por su ID"""
    i = 0
    while i < len(clientes):
        if clientes[i]["id"] == id_cliente:
            return clientes[i]
        i = i + 1
    return None
```

### 12. Constantes para Matrices
Para mejorar la legibilidad del código que maneja matrices, se utilizan constantes descriptivas:

```python
# En lugar de usar números mágicos
reserva[1] = nuevo_id  # ❌ No claro

# Se utilizan constantes descriptivas
reserva[INDICE_ID_CLIENTE] = nuevo_id  # ✅ Claro y mantenible
```

### 13. Manejo de Errores
- **Validación previa**: Todos los datos se validan antes de procesamiento
- **Valores de retorno**: Funciones retornan `True`/`False` para indicar éxito/fallo, o equivalente
- **Mensajes informativos**: Solo en main.py, nunca en funciones de dominio
- **Estados consistentes**: El sistema siempre mantiene un estado válido

## Cómo Ejecutar
1. Asegurarse de tener Python 3.6+ instalado
2. Descargar todos los archivos en un directorio
3. Ejecutar: `python main.py`
4. Seguir las instrucciones del menú interactivo

## Autor
Grupo VII - Programacion I 

Fecha: Agosto 2025