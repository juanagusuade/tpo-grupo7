# Sistema de Gestión de Alquileres Temporarios

## Definición de la temática del proyecto
Este sistema permite administrar eficientemente el alquiler temporal de distintos departamentos, facilitando el control de las unidades disponibles, la gestión de clientes y la organización de reservas. Está orientado a propietarios o administradores que deseen automatizar el proceso de registro, asignación y seguimiento de estadías.

Las entidades principales son:
- **Clientes**: contienen los datos personales de los inquilinos.
- **Departamentos**: representan cada unidad disponible para alquiler con sus características (ubicación, número de ambientes, capacidad, estado, precio por noche).
- **Reservas**: vinculan a un cliente con un departamento en un período determinado.

## Técnicas Avanzadas Implementadas

### Programación Estructurada
El sistema utiliza técnicas de programación estructurada:
- **`any()`**: Búsqueda eficiente de elementos (DNI duplicados)
- **`map()`**: Transformación de listas para extracción de IDs
- **`filter()`**: Filtrado de elementos activos en clientes y departamentos
- **`reduce()`**: Cálculos acumulativos para estadísticas de reservas
- **Comprensiones de lista**: Uso extensivo para operaciones de filtrado y transformación
- **Expresiones lambda**: Funciones anónimas en filter y map
- **Ciclos for**: Validación de campos y caracteres

### Persistencia de Datos (Módulo Repository)
Implementación de persistencia con **dos estrategias diferentes**:
- **JSON** para clientes y departamentos (formato estructurado, mantiene tipos)
- **TXT delimitado** para reservas (append eficiente, archivo temporal para seguridad)
- Manejo robusto de errores y estrategias de recuperación

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
- Validación de solapamiento de fechas (permite check-in/check-out el mismo día)
- Verificación de que fecha de egreso sea posterior a ingreso

### Reportes y Estadísticas
- **Porcentaje de ocupación por departamento**: Calcula el porcentaje de días ocupados sobre un período de 365 días
- **Días ocupados por departamento**: Suma total de días que un departamento estuvo reservado
- **Duración promedio de reservas**: Usa `reduce()` de programación funcional para calcular promedio de estadías
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
- **Reservas**: Fecha egreso posterior a ingreso, verificación automática de disponibilidad del departamento
- **Solapamiento de fechas**: Algoritmo que verifica conflictos, permitiendo check-in/check-out el mismo día
- **Estados consistentes**: Validación de transiciones de estado válidas
- **DNI único**: Verificación con `any()` que evita duplicados al agregar o modificar clientes

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

### Programación Funcional
- **Uso de `map`**: Implementado para la transformación de listas, como la extracción de IDs de clientes y departamentos para el poblador de datos.
- **Uso de `filter`**: Implementado para el filtrado de listas, como en las funciones `listar_clientes_activos` y `listar_departamentos_activos`.
- **Uso de `reduce`**: Importado de `functools` y utilizado para cálculos acumulativos, como en `calcular_duracion_promedio_reservas`.

#### Comparación con Programación Estructurada

**Otras validaciones usan ciclos for tradicionales:**

```python
# Validación de teléfono con ciclo for
def validar_telefono(tel):
    if len(tel) < 7:
        return False
    caracteres_validos = "0123456789 -()+."
    for caracter in tel:
        if caracter not in caracteres_validos:
            return False
    return True
```

### Técnicas de Programación Utilizadas

El sistema utiliza diversas técnicas de programación:

**`any()` - Búsqueda eficiente:**
```python
# En clientes.py
def buscar_dni(lista_clientes, dni):
    return any(cliente[DNI_CLIENTE] == dni for cliente in lista_clientes)

def buscar_dni_diferente_id(lista_clientes, dni, id_excluir):
    return any(
        cliente[DNI_CLIENTE] == dni and cliente[ID_CLIENTE] != id_excluir
        for cliente in lista_clientes
    )
```

**Ciclos `for` - Validación con control de flujo:**
```python
# En validaciones.py
def campos_son_validos(*campos):
    for campo in campos:
        if campo is None:
            return False
        if type(campo) == str and len(campo.strip()) == 0:
            return False
        if type(campo) == list and len(campo) == 0:
            return False
    return True

def validar_telefono(tel):
    if len(tel) < 7:
        return False
    caracteres_validos = "0123456789 -()+."
    for caracter in tel:
        if caracter not in caracteres_validos:
            return False
    return True
```

**`filter()` - Filtrado declarativo:**
```python
# Listar solo clientes activos
clientes_activos = list(filter(lambda c: c[ACTIVO_CLIENTE], clientes))
```

**`map()` y `reduce()` - Transformación y acumulación:**
```python
# Extraer IDs
ids = list(map(lambda c: c[ID_CLIENTE], clientes))

# Sumar días ocupados
from functools import reduce
total_dias = reduce(lambda acc, r: acc + calcular_dias(...), reservas, 0)
```

## Módulo de Persistencia (Repository)

El sistema incluye un módulo para persistencia de datos con dos estrategias:

### Archivos y Responsabilidades

#### `persistence_json.py` - Persistencia en formato JSON
**Responsable de:** Clientes y Departamentos

**Formato:** Listas de diccionarios en JSON
```json
[{"id": 1, "nombre": "Juan", "activo": true}, ...]
```

**Funciones principales:**
- `leer_clientes()`, `guardar_clientes(lista)`
- `leer_departamentos()`, `guardar_departamentos(lista)`

**Características:**
- Formato legible por humanos
- Mantiene tipos de datos automáticamente (bool, int, str)
- Estructura jerárquica con indentación
- Mejor para datos que requieren estructura compleja

#### `persistence_txt.py` - Persistencia en formato TXT delimitado
**Responsable de:** Reservas

**Estructura TXT:**
```
12345;67890;54321;25/08/2025;30/08/2025;ACTIVO
23456;78901;65432;01/09/2025;05/09/2025;ACTIVO
```

**Funciones principales:**
- `leer_reservas()`: Lee todas las reservas línea por línea
- `guardar_reservas_txt(lista)`: Guarda lista completa usando archivo temporal
- `agregar_reserva_txt(reserva)`: Agrega una reserva al final (modo append)

**Funciones auxiliares (traductores):**
- `parsear_reserva_txt(linea)`: Convierte string → lista de reserva
- `formatear_reserva_txt(reserva)`: Convierte lista de reserva → string

**Características:**
- Formato liviano y eficiente
- Modo append para agregar rápidamente sin reescribir todo
- Archivo temporal para seguridad en modificaciones
- Todo se guarda como texto, requiere conversión manual de tipos

### Estrategias de Escritura

#### JSON: Sobrescritura Total
1. Abrir archivo en modo 'w' (write)
2. Usar `json.dump()` para escribir toda la estructura
3. Cerrar archivo

**Ventajas:** Simple, mantiene tipos automáticamente
**Desventajas:** Reescribe todo el archivo en cada guardado

#### TXT: Modo Append (para agregar)
1. Abrir archivo en modo 'a' (append)
2. Agregar nueva línea al final
3. Cerrar archivo

**Ventajas:** Muy rápido, no toca datos existentes
**Desventajas:** No permite modificar líneas anteriores

#### TXT: Archivo Temporal (para modificar/eliminar)
1. Crear archivo `.tmp` temporal
2. Escribir todos los datos en el temporal
3. Si tiene éxito, reemplazar archivo original con `os.replace()`
4. Si falla, el original queda intacto

**Ventajas:** Seguridad, no corrompe datos si falla
**Desventajas:** Más lento, requiere espacio temporal

### Lectura de Archivos

#### JSON: Lectura Completa
```python
archivo = open(ruta, 'r', encoding='UTF-8')
datos = json.load(archivo)  # Carga TODO en memoria
archivo.close()
```

#### TXT: Lectura Línea por Línea
```python
archivo = open(ruta, 'r', encoding='utf-8')
linea = archivo.readline()  # Primera línea
while linea:                # Mientras haya contenido
    procesar(linea)
    linea = archivo.readline()  # Siguiente línea
archivo.close()
```

**Ventaja:** Usa menos memoria, procesa mientras lee

### Manejo de Errores en Persistencia

Ambos módulos implementan manejo robusto de errores:

**Errores capturados:**
- `FileNotFoundError`: Archivo no existe (normal en primera ejecución)
- `json.JSONDecodeError`: JSON corrupto o mal formateado
- `OSError` / `PermissionError`: Problemas de permisos o disco
- `IOError`: Errores de entrada/salida

**Estrategia:**
- Todos los errores se registran con `manejar_error_inesperado()`
- Las funciones retornan valores seguros (lista vacía o False)
- Se usa bloque `finally` para asegurar cierre de archivos

### Comparación: JSON vs TXT

| Característica | JSON | TXT Delimitado |
|----------------|------|----------------|
| Legibilidad | ★★★★★ | ★★★☆☆ |
| Tamaño archivo | Más grande | Más pequeño |
| Mantiene tipos | Automático | Manual |
| Append eficiente | No | Sí |
| Estructura jerárquica | Sí | No |
| Parsing | Automático | Manual |
| Validación | Auto-verificable | Propenso a errores |

### Por Qué Esta Separación

**Clientes y Departamentos en JSON:**
- Estructuras más complejas (diccionarios)
- Se modifican con menos frecuencia
- Beneficio de mantener tipos automáticamente

**Reservas en TXT:**
- Se agregan constantemente (beneficio de append)
- Estructura simple (lista de valores)
- Archivos más livianos
- Demostración de manejo de archivos de texto plano

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
- **Manejo de errores**: Sistema robusto con `try-except` y un manejador de errores centralizado (`manejo_errores.py`).

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
- **Usuario**: `evecent` | **Contraseña**: `evecent1234`
- **Usuario**: `baltaa` | **Contraseña**: `baltaa1234`
- **Usuario**: `valen` | **Contraseña**: `valen1234`
- **Usuario**: `juanagus` | **Contraseña**: `juanagus1234`

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
- **Manejo de errores**: Gestión centralizada de excepciones (`try-except`) para prevenir cierres inesperados (crashes), reportando errores de forma clara al usuario.
- **Consistencia de datos**: El sistema mantiene siempre un estado válido
- **Recuperación**: Capacidad de manejar entradas incorrectas sin crash

### Escalabilidad
- **Arquitectura modular**: Fácil extensión de funcionalidades
- **Separación de responsabilidades**: Lógica de negocio independiente de UI
- **Reutilización**: Funciones comunes centralizadas
- **Mantenibilidad**: Código claro y bien documentado

## Autor
**Grupo VII - Programación I**  
**Fecha**: Noviembre 2025

