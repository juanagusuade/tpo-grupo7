# Sistema de Gestión de Alquileres Temporarios

## Definición de la temática del proyecto
Este sistema permite administrar eficientemente el alquiler temporal de distintos departamentos, facilitando el control de las unidades disponibles, la gestión de clientes y la organización de reservas. Está orientado a propietarios o administradores que deseen automatizar el proceso de registro, asignación y seguimiento de estadías.

Las entidades principales son:
- **Clientes**: contienen los datos personales de los inquilinos.
- **Departamentos**: representan cada unidad disponible para alquiler con sus características (ubicación, número de ambientes, capacidad, estado, precio por noche).
- **Reservas**: vinculan a un cliente con un departamento en un período determinado.

## Funcionalidades principales

### Gestión de Clientes
- Agregar nuevos clientes con validación de DNI único
- Listar clientes activos
- Modificar información de clientes existentes
- Dar de baja lógica a clientes (eliminación no destructiva)
- Validación completa de datos (nombres alfabéticos, DNI 7-8 dígitos, teléfono)

### Gestión de Departamentos
- Crear departamentos con todos sus atributos
- Actualización parcial de departamentos (mantener valores actuales opcionales)
- Reemplazo completo de departamentos
- Eliminación física de departamentos
- Baja y alta lógica de departamentos
- Búsqueda por ID individual
- Listado de departamentos activos y todos los departamentos
- Estados: Disponible, Ocupado, Mantenimiento

### Gestión de Reservas
- **Crear reservas** con validación automática de disponibilidad
- **Modificar reservas** activas (fechas de ingreso y egreso)
- **Cancelar reservas** con confirmación del usuario
- **Búsqueda de reservas** por cliente o por departamento
- **Listar todas las reservas activas** con formato de tabla
- **Consulta directa de disponibilidad** de departamentos para fechas específicas
- Validación automática de solapamiento de fechas
- Verificación de que fecha de egreso sea posterior a ingreso

### Reportes y Estadísticas
- **Porcentaje de ocupación por departamento** en los últimos 365 días
- **Duración promedio de reservas** activas en el sistema
- Formato de tablas profesionales para presentación de datos

### Sistema de Autenticación
- Sistema de login con múltiples usuarios válidos
- Máximo 3 intentos de autenticación
- Credenciales predefinidas para 4 usuarios diferentes
- Bloqueo del sistema tras superar intentos

### Interfaz y Experiencia de Usuario
- Interfaz colorizada con códigos ANSI para mejor visualización
- Menús numerados intuitivos con validación de opciones
- Confirmaciones explícitas para operaciones críticas
- Mensajes de éxito, error e información diferenciados
- Separadores visuales y formato de tablas profesional
- Sistema de pausa entre operaciones

## Arquitectura del Sistema

### Estructura de Directorios
```
Sistema-Alquileres/
├── main.py                          # Punto de entrada y autenticación
├── README.md                        # Documentación del proyecto

├── ui/                              # Módulos de interfaz de usuario
│   ├── menu_clientes.py            # Interfaz para gestión de clientes
│   ├── menu_depto.py               # Interfaz para gestión de departamentos
│   ├── menu_reservas.py            # Interfaz para gestión de reservas
│   └── menu_estadisticas.py        # Interfaz para reportes y estadísticas

├── domain/                          # Lógica de negocio
│   ├── clientes.py                 # CRUD de clientes
│   ├── departamentos.py            # CRUD de departamentos
│   └── reservas.py                 # CRUD de reservas y validaciones

└── common/                          # Funcionalidades comunes
    ├── constantes.py               # Constantes del sistema
    ├── interfaz.py                 # Funciones de presentación UI
    ├── entrada_datos.py            # Validaciones y entrada de datos
    ├── validaciones.py             # Validaciones específicas y fechas
    ├── generadores.py              # Generadores de IDs únicos
    └── poblador.py                 # Datos de ejemplo inicial
```

## Estructuras de Datos Implementadas

### Clientes (Lista de Diccionarios)
```python
cliente = {
    "id": 12345,                    # ID único de 5 dígitos
    "nombre": "Juan",               # Solo caracteres alfabéticos
    "apellido": "Pérez",            # Solo caracteres alfabéticos
    "dni": "12345678",              # 7-8 dígitos numéricos
    "telefono": "1122334455",       # Formato validado
    "activo": True                  # Estado lógico
}
```

### Departamentos (Lista de Diccionarios)
```python
departamento = {
    "id": 12345,                    # ID único de 5 dígitos
    "ubicacion": "Buenos Aires, Centro",  # Texto descriptivo
    "ambientes": 3,                 # Número entero ≥ 1
    "capacidad": 4,                 # Número entero ≥ 1
    "estado": "Disponible",         # Disponible/Ocupado/Mantenimiento
    "precio_noche": 100.50,         # Decimal ≥ 0.01
    "activo": True                  # Estado lógico
}
```

### Reservas (Lista de Listas)
```python
# Índices definidos por constantes para mejor legibilidad
INDICE_ID_RESERVA = 0          # ID único de la reserva
INDICE_ID_CLIENTE = 1          # ID del cliente
INDICE_ID_DEPARTAMENTO = 2     # ID del departamento
INDICE_FECHA_INGRESO = 3       # Fecha formato "dd/mm/yyyy"
INDICE_FECHA_EGRESO = 4        # Fecha formato "dd/mm/yyyy"
INDICE_ESTADO = 5              # ACTIVO/CANCELADO/ELIMINADO

reserva = [12345, 67890, 54321, "25/08/2025", "30/08/2025", "ACTIVO"]
```

## Validaciones Implementadas

### Validaciones de Datos Generales
- **Campos obligatorios**: Verificación de valores no nulos ni vacíos
- **Texto alfabético**: Solo letras y espacios para nombres
- **Números enteros**: Validación de rango con mínimos configurables
- **Números decimales**: Formato y valor mínimo validados
- **Opciones de menú**: Validación numérica dentro de rangos válidos

### Validaciones Específicas
- **DNI**: 7-8 dígitos numéricos, verificación de unicidad
- **Teléfono**: Mínimo 7 caracteres, permite números, espacios, guiones, paréntesis
- **Fechas**: Formato dd/mm/yyyy obligatorio, validación de fechas reales incluyendo años bisiestos
- **IDs únicos**: Generación automática de 5 dígitos con verificación de unicidad

### Validaciones de Negocio
- **Reservas**: Fecha egreso posterior a ingreso, verificación de disponibilidad
- **Solapamiento**: Algoritmo que verifica conflictos de fechas entre reservas
- **Estados consistentes**: Validación de transiciones de estado válidas

## Funcionalidades Avanzadas

### Sistema de Fechas
- **Conversión a días**: Algoritmo que convierte fechas a número total de días desde año 0
- **Comparación de fechas**: Función especializada para comparar fechas en formato string
- **Validación de años bisiestos**: Cálculo correcto de días por mes
- **Cálculos de estadísticas**: Duración de reservas en días

### Generación de IDs
- **IDs únicos**: Rango 10000-99999 con verificación automática de unicidad
- **Dos estrategias**: Función específica para listas vs diccionarios
- **Prevención de duplicados**: Verificación exhaustiva antes de asignación

### Poblado Automático de Datos
- **Datos de ejemplo**: Generación automática de clientes, departamentos y reservas al inicio
- **Datos realistas**: Nombres, ubicaciones y fechas con sentido
- **Prevención de conflictos**: Verificación de disponibilidad al generar reservas ejemplo

## Convenciones de Programación

### Nomenclatura
- **Variables y funciones**: snake_case (ej: `agregar_cliente`, `lista_clientes`)
- **Constantes**: UPPER_CASE (ej: `ESTADO_ACTIVO`, `INDICE_ID_RESERVA`)
- **Archivos**: snake_case con extensión .py

### Principios de Diseño
- **Separación de responsabilidades**: UI separada de lógica de negocio
- **Funciones puras**: Las funciones de dominio no manejan interfaz
- **Validación temprana**: Datos validados antes del procesamiento
- **Consistencia**: Mismo patrón para todas las operaciones CRUD
- **Manejo de errores**: Valores de retorno booleanos consistentes

### Estados del Sistema
#### Estados de Reserva
- `ACTIVO`: Reserva vigente y válida
- `CANCELADO`: Reserva cancelada (puede reactivarse)
- `ELIMINADO`: Reserva eliminada (baja fisica)

#### Estados de Departamento
- `"Disponible"`: Listo para nuevas reservas
- `"Ocupado"`: Con reserva activa actual
- `"Mantenimiento"`: Temporalmente no disponible

## Credenciales de Acceso

El sistema incluye 4 usuarios predefinidos:
- **Usuario**: `evecent` | **Contraseña**: `evelamaspiola123`
- **Usuario**: `baltaa` | **Contraseña**: `baltalocuradelcodigo`
- **Usuario**: `valen` | **Contraseña**: `valentiburondelatlantico`
- **Usuario**: `juanagus` | **Contraseña**: `password1234noolvidar`

## Instalación y Ejecución

### Requisitos
- Python 3.6 o superior
- Sistema operativo compatible con códigos de color ANSI (Windows 10+, Linux, macOS)

### Instrucciones
1. Descargar todos los archivos manteniendo la estructura de directorios
2. Abrir terminal en el directorio principal
3. Ejecutar: `python main.py`
4. Usar credenciales proporcionadas para autenticarse
5. Seguir los menús interactivos

### Primera Ejecución
Al ejecutar por primera vez, el sistema detectará que está vacío y cargará automáticamente:
- 5 clientes de ejemplo
- 5 departamentos de ejemplo  
- 7 reservas de ejemplo

Los valores mencionados pueden cambiarse en el archivo `poblador.py`.
## Características Técnicas

### Interfaz de Usuario
- **Colores ANSI**: Código de colores para mejor experiencia visual
- **Menús interactivos**: Validación en tiempo real de opciones
- **Tablas formateadas**: Presentación profesional de datos
- **Confirmaciones**: Diálogos de confirmación para operaciones críticas

### Robustez
- **Validación exhaustiva**: Múltiples capas de validación de datos
- **Manejo de errores**: Gestión elegante de situaciones imprevistas
- **Consistencia de datos**: El sistema mantiene siempre un estado válido
- **Recuperación**: Capacidad de manejar entradas incorrectas sin crash

### Escalabilidad
- **Arquitectura modular**: Fácil extensión de funcionalidades
- **Separación de responsabilidades**: Lógica de negocio independiente de UI
- **Reutilización**: Funciones comunes centralizadas
- **Mantenibilidad**: Código claro y bien documentado

## Autor
**Grupo VII - Programación I**  
**Fecha**: Septiembre 2025

