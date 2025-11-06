# Sistema de Gestión de Alquileres Temporarios

## Informe Final del Proyecto - Programación I

**Grupo VII**
**Fecha**: Noviembre 2025

---

## 1. Definición del Proyecto

El Sistema de Gestión de Alquileres Temporarios es una aplicación de consola desarrollada en Python que permite administrar eficientemente el alquiler temporal de departamentos. El sistema facilita el control de unidades disponibles, la gestión integral de clientes y la organización de reservas con validaciones exhaustivas.

### Objetivos Principales
- Automatizar el proceso de registro, asignación y seguimiento de estadías
- Garantizar la integridad de datos mediante validaciones múltiples
- Proporcionar persistencia robusta de información
- Implementar arquitectura modular y mantenible
- Demostrar técnicas avanzadas de programación funcional

### Alcance del Sistema
- **Entidades**: Clientes, Departamentos, Reservas
- **Operaciones**: CRUD completo para todas las entidades
- **Persistencia**: Archivos JSON y TXT delimitado
- **Interfaz**: Consola con colores ANSI
- **Validaciones**: Sintácticas, semánticas y de negocio

---

## 2. Arquitectura del Sistema

### Estructura de Directorios
```
sistema-alquileres/
├── main.py                    # Punto de entrada y autenticación
├── README.md                  # Documentación del proyecto
├── data/                      # Archivos de persistencia
│   ├── clientes.json          # Clientes en formato JSON
│   ├── departamentos.json     # Departamentos en formato JSON
│   └── reservas.txt           # Reservas en TXT delimitado
├── domain/                    # Lógica de negocio (capa dominio)
│   ├── clientes.py            # Operaciones CRUD de clientes
│   ├── departamentos.py       # Operaciones CRUD de departamentos
│   ├── reservas.py            # Operaciones CRUD de reservas
│   └── servicios.py           # Coordinación entre entidades (evita imports circulares)
├── ui/                        # Interfaz de usuario (capa presentación)
│   ├── menu_clientes.py       # Menús de gestión de clientes
│   ├── menu_depto.py          # Menús de gestión de departamentos
│   ├── menu_reservas.py       # Menús de gestión de reservas
│   └── menu_estadisticas.py   # Menús de estadísticas y reportes
├── common/                    # Utilidades compartidas
│   ├── constantes.py          # Constantes y configuraciones
│   ├── interfaz.py            # Funciones de presentación UI
│   ├── entrada_datos.py       # Validación y entrada de datos
│   ├── validaciones.py        # Validaciones específicas
│   ├── generadores.py         # Generadores de IDs únicos
│   ├── poblador.py            # Datos de ejemplo iniciales
│   └── manejo_errores.py      # Gestión centralizada de errores
├── repository/                # Capa de persistencia
│   ├── persistence_json.py    # Lectura/escritura JSON
│   └── persistence_txt.py     # Lectura/escritura TXT con append
└── tests/                     # Pruebas unitarias
    ├── conftest.py            # Configuración de pruebas
    ├── test_common/           # Pruebas de utilidades
    │   └── test_validacion.py # Pruebas de validaciones
    └── test_domain/           # Pruebas de dominio
        ├── test_clientes.py   # Pruebas CRUD clientes
        └── test_reservas.py   # Pruebas CRUD reservas
```

### Principios Arquitectónicos
- **Separación de responsabilidades**: Cada capa tiene un propósito definido
- **Inversión de dependencias**: Las capas superiores no dependen de las inferiores
- **Modularidad**: Funciones cohesivas y acopladas de manera flexible
- **Abstracción**: Interfaces claras entre capas
- **Resolución de imports circulares**: Módulo `servicios.py` centraliza operaciones que cruzan múltiples entidades

### 2.3 Módulo de Servicios (Coordinación entre Entidades)

El módulo `domain/servicios.py` fue diseñado para resolver imports circulares y centralizar operaciones que cruzan múltiples entidades del dominio. Actúa como una capa de coordinación que orquesta interacciones complejas.

#### Funciones Principales:

**Gestión de Reservas Activas:**
- `cancelar_reservas_activas_de_cliente(id_cliente) -> int`
  - Cancela todas las reservas activas de un cliente antes de su baja lógica
  - Retorna el número de reservas canceladas
  - Usado por: `domain.clientes.baja_logica_cliente()`

- `cancelar_reservas_activas_de_departamento(id_departamento) -> int`
  - Cancela todas las reservas activas de un departamento antes de su baja lógica
  - Retorna el número de reservas canceladas
  - Usado por: `domain.departamentos.baja_logica_departamento()`

**Verificación de Estado:**
- `verificar_reservas_activas_de_departamento(id_departamento) -> bool`
  - Verifica si un departamento tiene reservas activas (bloquea eliminación física)
  - Retorna `True` si hay reservas activas, `False` en caso contrario
  - Usado por: `domain.departamentos.eliminar_departamento()`

**Control de Disponibilidad:**
- `verificar_disponibilidad_departamento_en_fechas(id_depto, fecha_ini, fecha_fin) -> bool`
  - Verifica si un departamento está disponible en un rango de fechas
  - Detecta solapamiento con reservas activas existentes
  - Retorna `True` si está disponible, `False` si hay conflicto
  - Usado por: `domain.departamentos.verificar_disponibilidad_departamento()`


---

## 3. Estructuras de Datos

### 3.1 Clientes (Lista de Diccionarios)
Los clientes se almacenan como una lista de diccionarios JSON con la siguiente estructura:

```python
[
    {
        "id": 81519,           # ID único (5 dígitos)
        "nombre": "Jhon",      # Solo caracteres alfabéticos
        "apellido": "Rororo",  # Solo caracteres alfabéticos
        "dni": "12345678",     # 7-8 dígitos numéricos
        "telefono": "45325432", # 10 dígitos numéricos
        "activo": true         # Estado lógico (boolean)
    }
]
```

### 3.2 Departamentos (Lista de Diccionarios)
Los departamentos se almacenan como una lista de diccionarios JSON:

```python
[
    {
        "id": 50505,              # ID único (5 dígitos)
        "codigo": "DPTO-0001",    # Código único con formato específico
        "ubicacion": "Recoleta",  # Ubicación geográfica
        "precio": 15000.0,        # Precio por noche (float)
        "capacidad": 4,           # Capacidad máxima (int)
        "num_habitaciones": 2,    # Número de habitaciones (int)
        "descripcion": "Moderno", # Descripción textual
        "activo": true,           # Estado lógico (boolean)
        "estado": "Disponible"    # Estado operativo
    }
]
```

### 3.3 Reservas (Lista de Listas)
Las reservas se almacenan como lista de listas en archivo TXT delimitado:

```python
[
    [44910, 11325, 50505, "14/11/2025", "18/11/2025", "ACTIVO"],  # ID, Cliente, Depto, Inicio, Fin, Estado
    [96565, 50220, 92646, "19/11/2025", "24/11/2025", "ACTIVO"],
    [16780, 39253, 38076, "17/10/2025", "22/10/2025", "ACTIVO"]
]
```

**Índices de acceso:**
- `INDICE_ID_RESERVA = 0`        # ID único de la reserva
- `INDICE_ID_CLIENTE = 1`        # ID del cliente
- `INDICE_ID_DEPARTAMENTO = 2`   # ID del departamento
- `INDICE_FECHA_INGRESO = 3`     # Fecha de ingreso (DD/MM/YYYY)
- `INDICE_FECHA_EGRESO = 4`      # Fecha de egreso (DD/MM/YYYY)
- `INDICE_ESTADO = 5`            # Estado de la reserva

---

## 4. Funcionalidades Principales

### 4.1 Gestión de Clientes
- **Alta**: Registro con validación completa de datos personales
- **Consulta**: Búsqueda por DNI con visualización detallada
- **Modificación**: Actualización de datos con preservación de ID
- **Baja lógica**: Desactivación con cancelación automática de reservas activas
- **Baja física**: Eliminación permanente con validación de integridad referencial
- **Listado**: Visualización filtrada por estado (activos/inactivos/todos)

### 4.2 Gestión de Departamentos
- **Alta**: Registro con código único y características completas
- **Consulta**: Búsqueda por código con historial de reservas
- **Modificación**: Actualización controlada de datos
- **Baja lógica**: Desactivación con cancelación de reservas activas
- **Baja física**: Eliminación con verificación de integridad
- **Listado**: Visualización por estado y disponibilidad dinámica
- **Disponibilidad**: Cálculo en tiempo real basado en reservas activas

### 4.3 Gestión de Reservas
- **Alta**: Creación con validaciones múltiples:
  - Cliente y departamento activos
  - Formato de fechas válido
  - No solapamiento con reservas existentes
  - Fechas coherentes (ingreso < egreso)
- **Consulta**: Búsqueda por ID con detalles completos
- **Modificación**: Actualización con revalidación completa
- **Cancelación**: Cambio de estado a CANCELADO
- **Eliminación**: Baja física permanente
- **Listado**: Visualización por cliente, departamento, estado o rango de fechas

### 4.4 Estadísticas y Reportes
- **Estadísticas de clientes**:
  - Totales por estado
  - Promedio de reservas por cliente
  - Cliente con más reservas activas
- **Estadísticas de departamentos**:
  - Totales por estado y disponibilidad
  - Promedio de reservas por departamento
  - Departamento más reservado
- **Estadísticas de reservas**:
  - Totales por estado
  - Promedio de días por reserva
  - Reserva más larga
  - Distribución temporal

---

## 5. Técnicas Avanzadas Implementadas

### 5.1 Programación Funcional
- **Comprensiones de listas**: `[c for c in clientes if c['activo']]`
- **Funciones de orden superior**:
  - `map()`: `list(map(lambda c: c['id'], clientes))`
  - `filter()`: `list(filter(lambda r: r[INDICE_ESTADO] == 'ACTIVO', reservas))`
  - `reduce()`: Acumuladores para estadísticas y conteos
- **Expresiones lambda**: Transformaciones inline y criterios de filtrado
- **Funciones puras**: Separación de efectos secundarios

### 5.2 Estructuras de Datos Avanzadas
- **Listas de listas**: Representación matricial de reservas
- **Diccionarios**: Mapeos para configuración y contadores
- **Tuplas**: Retornos múltiples e inmutabilidad
- **Sets**: Validación de unicidad y operaciones de conjuntos

### 5.3 Expresiones Regulares
```python
DNI_PATTERN = r'^\d{7,8}$'                    # 7-8 dígitos
TELEFONO_PATTERN = r'^\d{10}$'                # 10 dígitos exactos
CODIGO_DEPTO_PATTERN = r'^DPTO-\d{4}$'        # Formato específico
FECHA_PATTERN = r'^\d{2}/\d{2}/\d{4}$'       # DD/MM/YYYY
```

### 5.4 Operaciones con Strings
- **Concatenación**: `f"{cliente['nombre']} {cliente['apellido']}"`
- **Slicing**: `fecha.split('/')`, `linea.strip()`
- **Métodos**: `.upper()`, `.lower()`, `.replace()`, `.startswith()`
- **Formateo**: f-strings para presentación tabular

### 5.5 Búsquedas Relacionales
- **Departamentos disponibles**: Filtra departamentos sin reservas solapadas
- **Clientes con reservas**: Encuentra clientes con reservas en período
- **Reservas por cliente/departamento**: Búsquedas cruzadas eficientes
- **Validaciones FK**: Verificación de integridad referencial

---

## 6. Módulo de Persistencia

### 6.1 Estrategias de Almacenamiento

#### JSON (Clientes y Departamentos)
- **Formato**: Lista de diccionarios serializados
- **Ventajas**: Mantiene tipos de datos automáticamente, legible
- **Operaciones**: Sobrescritura completa en cada guardado
- **Archivos**: `clientes.json`, `departamentos.json`

#### TXT Delimitado (Reservas)
- **Formato**: Valores separados por punto y coma
- **Estructura**: `id;id_cliente;id_depto;fecha_ini;fecha_fin;estado`
- **Ventajas**: Ligero, eficiente para append
- **Archivo**: `reservas.txt`

### 6.2 Operaciones de Escritura

#### JSON: Sobrescritura Total
```python
with open(ruta, 'w', encoding='utf-8') as archivo:
    json.dump(datos, archivo, indent=4, ensure_ascii=False)
```

#### TXT: Append para Agregar
```python
with open(ruta, 'a', encoding='utf-8') as archivo:
    archivo.write(f"{nueva_linea}\n")
```

#### TXT: Archivo Temporal para Modificar
```python
# Crear archivo temporal
with open(temp_ruta, 'w', encoding='utf-8') as temp:
    for linea in lineas_filtradas:
        temp.write(f"{linea}\n")

# Reemplazar archivo original
os.replace(temp_ruta, ruta_original)
```

### 6.3 Lectura de Datos

#### JSON: Carga Completa
```python
with open(ruta, 'r', encoding='utf-8') as archivo:
    datos = json.load(archivo)
```

#### TXT: Lectura Línea por Línea
```python
reservas = []
with open(ruta, 'r', encoding='utf-8') as archivo:
    for linea in archivo:
        if linea.strip():  # Ignorar líneas vacías
            reserva = parsear_reserva_txt(linea.strip())
            reservas.append(reserva)
```

### 6.4 Manejo de Errores
- **FileNotFoundError**: Archivos inexistentes (normal en primera ejecución)
- **json.JSONDecodeError**: JSON corrupto o mal formateado
- **OSError/PermissionError**: Problemas de permisos de archivo
- **UnicodeDecodeError**: Problemas de codificación
- **Bloque finally**: Asegura cierre de archivos siempre

---

## 7. Validaciones Implementadas

### 7.1 Validaciones Sintácticas (Formato)
- **DNI**: Patrón regex `^\d{7,8}$`
- **Teléfono**: Patrón regex `^\d{10}$`
- **Código departamento**: Patrón regex `^DPTO-\d{4}$`
- **Fechas**: Patrón regex `^\d{2}/\d{2}/\d{4}$` + validación de calendario

### 7.2 Validaciones Semánticas (Lógica)
- **Unicidad**: DNI y códigos de departamento únicos en el sistema
- **Rangos**: Valores positivos para precios y capacidades
- **Coherencia**: Fecha de ingreso < fecha de egreso
- **Existencia**: Verificación de IDs válidos

### 7.3 Validaciones de Negocio
- **Estados activos**: Cliente y departamento deben estar activos para reservas
- **No solapamiento**: Reservas no pueden superponerse en mismo departamento
- **Integridad referencial**: No eliminar entidades con dependencias activas
- **Cascada**: Cancelación automática de reservas al desactivar entidades

### 7.4 Validaciones de Fecha
- **Formato válido**: DD/MM/YYYY con días y meses correctos
- **Fechas futuras**: No permitir reservas en fechas pasadas
- **Períodos válidos**: Duración mínima de 1 día
- **No solapamiento**: Algoritmo de comparación de rangos de fechas

---

## 8. Interfaz de Usuario

### 8.1 Características Generales
- **Consola ANSI**: Colores para mejorar experiencia visual
- **Menús numerados**: Navegación intuitiva con validación de entrada
- **Tablas formateadas**: Presentación prolija de datos
- **Confirmaciones**: Diálogos para operaciones críticas
- **Mensajes contextuales**: Feedback claro para cada operación

### 8.2 Sistema de Colores
```python
COLOR_RESET = "\033[0m"
COLOR_AZUL = "\033[94m"      # Títulos y encabezados
COLOR_VERDE = "\033[92m"     # Éxitos y confirmaciones
COLOR_AMARILLO = "\033[93m"  # Advertencias
COLOR_ROJO = "\033[91m"      # Errores
COLOR_MAGENTA = "\033[95m"   # Información destacada
COLOR_CYAN = "\033[96m"      # Entrada de usuario
```

### 8.3 Estructura de Menús
- **Menú principal**: 5 opciones principales
- **Submenús**: Operaciones CRUD específicas por entidad
- **Navegación**: Retorno automático al menú anterior
- **Validación**: Entrada numérica con rangos definidos

---

## 9. Autenticación y Seguridad

### 9.1 Sistema de Login
- **Usuarios predefinidos**: Tupla de credenciales válidas
- **Máximo 3 intentos**: Bloqueo después de fallos consecutivos
- **Validación case-sensitive**: Usuario y contraseña exactos
- **Mensaje de bienvenida**: Confirmación de sesión iniciada

### 9.2 Credenciales del Sistema
```python
USUARIOS = (
    ("evecent", "evecent1234"),
    ("baltaa", "baltaa1234"),
    ("valen", "valen1234"),
    ("juanagus", "juanagus1234"),
    ("a", "a") # Solo utilizar para pruebas inmediatas o presentaciones
)
```

---

## 10. Pruebas Unitarias

### 10.1 Framework Utilizado
- **pytest**: Framework de testing moderno para Python
- **Fixtures**: Configuración reutilizable en `conftest.py`
- **Cobertura**: Validación de rutas de ejecución

### 10.2 Casos de Prueba Implementados

#### Validaciones (`test_validacion.py`)
- `test_validar_dni()`: DNI válido e inválido
- `test_validar_telefono()`: Teléfonos de 10 dígitos
- `test_validar_decimal()`: Validacion de formato decimal apropiado
- `test_comparar_fechas()`: Validacion de anterioridad, posterioridad, o igualdad de fechas, con excepciones

#### Entrada de datos (`test_entrada_datos.py`)
- `test_validar_alfabetico()`: Validaciond e input en formato solo alfabetico

#### Clientes (`test_clientes.py`)
- `test_buscar_dni()`: Busqueda de DNI en clientes
- `test_buscar_dni_con_excepcion()`: Consulta de fallo con excepcion en busqueda de DNI

#### Reservas (`test_reservas.py`)
- `test_solapamiento_mismo_dia()`: Validacion de funcionamiento de funcion de solapamientos para reservas

### 10.3 Cobertura de Pruebas
- **Total de tests**: 8 pruebas unitarias
- **Casos borde**: Validaciones de límites y errores

---

## 11. Control de Versiones

### 11.1 Git Workflow
- **Repositorio**: `tpo-grupo7` en GitHub
- **Rama principal**: `main`
- **Commits estructurados**: Mensajes descriptivos por funcionalidad
- **Historial completo**: Desarrollo incremental documentado en el gitlog

### 11.2 .gitignore
```
__pycache__/
*.pyc
*.pyo
.Python
*.log
.DS_Store
.vscode/
.idea/
```

---

## 12. Checklist de Requisitos del Trabajo Práctico

### Primera Entrega - Fundamentos

**✓ Operaciones CRUD**
- Alta, baja, modificación y consulta para clientes, departamentos y reservas
- Validaciones completas en todas las operaciones
- Integridad referencial y estados consistentes

**✓ Matrices (listas de listas)**
- Reservas implementadas como lista de listas
- Acceso por índices numéricos (INDICE_ID_RESERVA, etc.)
- Manipulación matricial en operaciones CRUD

**✓ Listas avanzadas y comprensiones**
- `[c for c in clientes if c['activo']]` - filtrado de activos
- `[r[INDICE_ID_CLIENTE] for r in reservas]` - extracción de IDs
- Comprensiones anidadas para búsquedas complejas

**✓ Operaciones con strings**
- Concatenación: `f"{nombre} {apellido}"`
- Slicing: `fecha.split('/')`, `linea.strip()`
- Métodos: `.upper()`, `.lower()`, `.replace()`
- Formateo tabular con f-strings

**✓ Funciones lambda (map, filter, reduce)**
- `map(lambda c: c['id'], clientes)` - extracción de IDs
- `filter(lambda r: r[INDICE_ESTADO] == 'ACTIVO', reservas)` - filtrado
- `reduce(lambda acc, r: acc + r[INDICE_DIAS], reservas, 0)` - acumuladores

**✓ Modularización**
- 4 capas claramente separadas (domain, ui, repository, common)
- 20 módulos especializados
- Imports organizados al inicio de cada archivo (a excepcion de `funciones_compartidas.py` para evitar import circulares)
- Funciones cohesivas y responsabilidades bien definidas

**✓ Expresiones regulares**
- DNI: `r'^\d{7,8}$'` - validación de 7-8 dígitos
- Teléfono: `r'^\d{10}$'` - exactamente 10 dígitos
- Código departamento: `r'^DPTO-\d{4}$'` - formato específico
- Fecha: `r'^\d{2}/\d{2}/\d{4}$'` - DD/MM/YYYY

**✓ Diccionarios avanzados**
- Contadores: `{estado: cantidad}` para estadísticas
- Mapeos: `COLORES = {"AZUL": "\033[94m", ...}`
- Acumuladores: `reduce()` para frecuencias
- Configuración: diccionarios para opciones de menú

**✓ Tuplas y sets**
- Tuplas: `USUARIOS = (("user", "pass"), ...)` - credenciales inmutables
- Sets: `{r[INDICE_ID_CLIENTE] for r in reservas}` - IDs únicos
- Retornos múltiples: `return (exito, mensaje)`
- Operaciones: unión, intersección para validaciones

**✓ Búsquedas relacionales**
- `listar_departamentos_disponibles(fecha_ini, fecha_fin)` - sin solapamientos
- `listar_clientes_con_reservas_en_periodo()` - clientes activos en rango
- `buscar_reservas_por_cliente(id_cliente)` - todas las reservas de un cliente
- `buscar_reservas_por_departamento(id_depto)` - historial completo

**✓ Funciones estadísticas**
- Promedios: `sum(dias) / len(reservas)` - duración promedio
- Máximos: `max(reservas, key=lambda r: r[DIAS])` - reserva más larga
- Conteos: totales por estado y distribuciones
- Rankings: cliente/departamento más frecuente

**✓ Control de versiones Git**
- Repositorio creado e inicializado
- Commits con mensajes descriptivos
- Historial de desarrollo documentado
- .gitignore configurado correctamente

### Segunda Entrega - Mejoras Avanzadas

**✓ CRUD basado en archivos**
- JSON: `persistence_json.py` - `leer_clientes()`, `guardar_clientes()`
- TXT: `persistence_txt.py` - `leer_reservas()`, `guardar_reservas_txt()`
- Append eficiente para reservas: `agregar_reserva_txt()`

**✓ Manejo de excepciones**
- `manejo_errores.py` - `manejar_error_inesperado()`
- Captura específica: `FileNotFoundError`, `JSONDecodeError`, `OSError`
- Bloques `try-except-finally` en toda la capa repository
- Mensajes de error descriptivos al usuario

**✓ Pruebas unitarias**
- 8 tests implementados (supera mínimo de 3)
- `pytest` como framework
- Fixtures en `conftest.py`
- Cobertura de algunas funciones críticas y casos borde

**✓ Archivos de texto plano**
- `reservas.txt` - formato delimitado por `;`
- Lectura línea por línea: `readline()` en bucle
- Modo append: `'a'` para agregar sin reescribir
- Archivo temporal para modificaciones seguras

**✓ Archivos JSON**
- `clientes.json`, `departamentos.json`
- `json.load()` para lectura completa
- `json.dump()` con `indent=4` y `ensure_ascii=False`
- Mantiene tipos de datos automáticamente

**✓ Recursión (4 funciones)**
1. `buscar_dni(lista_clientes, dni, indice=0)` - Búsqueda recursiva de DNI en lista de clientes (domain/clientes.py)
2. `listar_clientes_activos(indice=0, resultado=None)` - Listado recursivo de clientes activos con acumulador (domain/clientes.py)
3. `buscar_departamento_por_id(id_departamento, indice=0)` - Búsqueda recursiva de departamento por ID (domain/departamentos.py)
4. `verificar_disponibilidad(lista_reservas, id_depto, fecha_ing, fecha_eg, id_reserva_excluir, indice=0)` - Verificación recursiva de disponibilidad de departamento en rango de fechas (domain/reservas.py)

---

## 13. Instalación y Ejecución

### Requisitos del Sistema
- **Python**: Versión 3.6 o superior
- **Sistema operativo**: Windows 10+, Linux, macOS
- **Terminal**: Soporte para códigos de color ANSI

### Instrucciones de Instalación
1. Descargar todos los archivos manteniendo la estructura de directorios
2. Abrir terminal en el directorio raíz del proyecto
3. Ejecutar: `python main.py`
4. Ingresar credenciales de usuario válidas
5. Navegar por los menús interactivos

### Primera Ejecución
Al ejecutar por primera vez, el sistema:
- Detecta archivos de datos vacíos
- Carga automáticamente datos de ejemplo
- 5 clientes de prueba
- 5 departamentos de prueba
- 7 reservas de prueba (pasadas, actuales y futuras)

### Comandos de Ejecución
```bash
# Desde el directorio raíz
python main.py
```

---

## 14. Características Técnicas

### Robustez
- **Validación exhaustiva**: Múltiples capas de validación de entrada
- **Manejo de errores**: Sistema centralizado de excepciones
- **Consistencia de datos**: Estados siempre válidos
- **Recuperación**: Manejo de entradas incorrectas sin crash

### Escalabilidad
- **Arquitectura modular**: Fácil extensión de funcionalidades
- **Separación de responsabilidades**: Lógica independiente de UI
- **Reutilización**: Funciones comunes centralizadas
- **Mantenibilidad**: Código claro y bien documentado

### Rendimiento
- **Lectura eficiente**: Procesamiento línea por línea para archivos grandes
- **Búsquedas optimizadas**: Índices y algoritmos eficientes
- **Memoria controlada**: Procesamiento por lotes cuando necesario

---

**Grupo VII - Programación I**  
**Juan Arias**
**Baltazar**
**Evelyn Centurion**
**Valen**
**Noviembre 2025**