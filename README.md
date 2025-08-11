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
- Implementar una interfaz sencilla y comprensible, acorde al nivel de un proyecto de Programación 1.

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

### Tabla: Clientes
| ID Cliente (int) | Nombre (string) | Apellido (string) | DNI (string) | Teléfono (string) |
|------------------|-----------------|-------------------|--------------|-------------------|
| 1                | Juan            | Pérez             | 30111222     | 1122334455        |
| 2                | María           | Gómez             | 29888777     | 1144455566        |
| 3                | Lucas           | Fernández         | 28444555     | 1177788899        |
| 4                | Ana             | Martínez          | 31222333     | 1133344455        |
| 5                | Pedro           | López             | 29999111     | 1199988877        |

### Tabla: Departamentos
| ID Dpto (int) | Ubicación (string)      | Ambientes (int) | Capacidad (int) | Estado (string) | Precio/Noche (float) |
|---------------|-------------------------|-----------------|-----------------|-----------------|----------------------|
| 1             | Buenos Aires, Centro    | 2               | 4               | Disponible      | 75.50                |
| 2             | Córdoba, Nueva Córdoba  | 1               | 2               | Ocupado         | 50.00                |
| 3             | Mendoza, Ciudad         | 3               | 6               | Disponible      | 120.00               |
| 4             | Rosario, Centro         | 2               | 4               | Disponible      | 80.00                |
| 5             | Mar del Plata, Playa    | 1               | 2               | Ocupado         | 65.00                |

### Tabla: Reservas
| ID Reserva (int) | ID Cliente (int) | ID Dpto (int) | Fecha Ingreso (date) | Fecha Egreso (date) |
|------------------|------------------|---------------|----------------------|---------------------|
| 1                | 1                | 2             | 2025-08-10           | 2025-08-15          |
| 2                | 3                | 5             | 2025-09-01           | 2025-09-05          |
| 3                | 2                | 1             | 2025-08-20           | 2025-08-25          |
| 4                | 4                | 4             | 2025-08-18           | 2025-08-22          |
| 5                | 5                | 3             | 2025-09-10           | 2025-09-15          |
