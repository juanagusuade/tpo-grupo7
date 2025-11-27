import flet as ft
import domain.departamentos as departamentos
import domain.reservas as reservas
from common.constantes import *

def vista_deptos(page: ft.Page):
    """
    Vista de Gestión de Departamentos.
    """
    
    tabla_deptos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Ubicación")),
            ft.DataColumn(ft.Text("Amb.")),
            ft.DataColumn(ft.Text("Cap.")),
            ft.DataColumn(ft.Text("Precio")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[]
    )

    def cargar_deptos():
        tabla_deptos.rows.clear()
        # Mostrar todos los departamentos para permitir reactivación
        lista = departamentos.departamentos # Acceso directo a la lista global o crear funcion obtener_todos
        
        for depto in lista:
            id_d = depto[ID_DEPARTAMENTO]
            es_activo = depto.get(ACTIVO_DEPARTAMENTO, True)
            estado_logico = "Activo" if es_activo else "Inactivo"
            color_estado = ft.Colors.GREEN if es_activo else ft.Colors.RED
            
            # Estado de ocupación (Disponible/Ocupado/Mantenimiento)
            estado_ocupacion = depto[ESTADO_DEPARTAMENTO]

            acciones = []
            
            # Editar
            btn_editar = ft.IconButton(
                icon=ft.Icons.EDIT, 
                tooltip="Editar", 
                on_click=lambda e, id=id_d: abrir_dialogo_editar(id)
            )
            acciones.append(btn_editar)
            
            # Consultar disponibilidad 
            btn_disponibilidad = ft.IconButton(
                icon=ft.Icons.CALENDAR_TODAY,
                tooltip="Consultar Disponibilidad",
                icon_color=ft.Colors.BLUE,
                on_click=lambda e, id=id_d: abrir_dialogo_disponibilidad(id)
            )
            acciones.append(btn_disponibilidad)

            if es_activo:
                btn_baja = ft.IconButton(
                    icon=ft.Icons.DELETE, 
                    tooltip="Dar de baja (Lógica)", 
                    icon_color=ft.Colors.ORANGE,
                    on_click=lambda e, id=id_d: confirmar_baja(id)
                )
                acciones.append(btn_baja)
            else:
                btn_alta = ft.IconButton(
                    icon=ft.Icons.RESTORE, 
                    tooltip="Reactivar", 
                    icon_color=ft.Colors.GREEN,
                    on_click=lambda e, id=id_d: dar_alta(id)
                )
                acciones.append(btn_alta)
                
                btn_eliminar = ft.IconButton(
                    icon=ft.Icons.DELETE_FOREVER, 
                    tooltip="Eliminar Físicamente", 
                    icon_color=ft.Colors.RED,
                    on_click=lambda e, id=id_d: confirmar_eliminar_fisico(id)
                )
                acciones.append(btn_eliminar)

            tabla_deptos.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(id_d))),
                        ft.DataCell(ft.Text(depto[UBICACION_DEPARTAMENTO])),
                        ft.DataCell(ft.Text(str(depto[AMBIENTES_DEPARTAMENTO]))),
                        ft.DataCell(ft.Text(str(depto[CAPACIDAD_DEPARTAMENTO]))),
                        ft.DataCell(ft.Text(f"${depto[PRECIO_DEPARTAMENTO]}")),
                        ft.DataCell(ft.Column([
                            ft.Text(estado_ocupacion),
                            ft.Text(estado_logico, color=color_estado, size=10)
                        ])),
                        ft.DataCell(ft.Row(acciones)),
                    ]
                )
            )
        page.update()

    # --- Funciones ABM ---
    def dar_alta(id_d):
        if departamentos.alta_logica_departamento(id_d):
            page.open(ft.SnackBar(ft.Text("Departamento reactivado")))
            cargar_deptos()
        else:
            page.open(ft.SnackBar(ft.Text("Error al reactivar")))

    def ejecutar_baja_logica(id_d):
        if departamentos.baja_logica_departamento(id_d):
             page.open(ft.SnackBar(ft.Text("Departamento dado de baja (Reservas canceladas)")))
             page.close(dialogo_confirmar)
             cargar_deptos()
        else:
             page.open(ft.SnackBar(ft.Text("No se pudo dar de baja")))

    def ejecutar_eliminacion_fisica(id_d):
        # Verificar reservas históricas
        reservas_depto = reservas.buscar_reservas_por_departamento(id_d)
        if reservas_depto:
             page.open(ft.SnackBar(ft.Text("No se puede eliminar: Tiene reservas asociadas.")))
             page.close(dialogo_confirmar)
             return

        if departamentos.eliminar_departamento(id_d):
             page.open(ft.SnackBar(ft.Text("Departamento eliminado permanentemente")))
             page.close(dialogo_confirmar)
             cargar_deptos()
        else:
             page.open(ft.SnackBar(ft.Text("Error al eliminar (¿Reservas activas?)")))

    # --- Diálogo Ver Disponibilidad ---
    disp_fecha_ingreso = ft.TextField(label="Fecha Ingreso (dd/mm/aaaa)", max_length=10)
    disp_fecha_egreso = ft.TextField(label="Fecha Egreso (dd/mm/aaaa)", max_length=10)
    disp_resultado = ft.Text()
    disp_id_depto = ft.Text(visible=False)

    def formatear_fecha_disp(e, campo):
        """Auto-formatea la fecha en el diálogo de disponibilidad"""
        texto = campo.value or ""
        numeros = texto.replace("/", "")
        
        if not all(c.isdigit() for c in numeros):
            numeros = ''.join(c for c in numeros if c.isdigit())
        
        if len(numeros) <= 2:
            campo.value = numeros
        elif len(numeros) <= 4:
            campo.value = f"{numeros[:2]}/{numeros[2:]}"
        else:
            campo.value = f"{numeros[:2]}/{numeros[2:4]}/{numeros[4:8]}"
        
        campo.update()

    disp_fecha_ingreso.on_change = lambda e: formatear_fecha_disp(e, disp_fecha_ingreso)
    disp_fecha_egreso.on_change = lambda e: formatear_fecha_disp(e, disp_fecha_egreso)

    def consultar_disponibilidad(e):
        if not disp_fecha_ingreso.value or not disp_fecha_egreso.value:
            disp_resultado.value = "Por favor ingrese ambas fechas"
            disp_resultado.color = ft.Colors.RED
            disp_resultado.update()
            return
        
        import domain.funciones_compartidas as fc
        id_depto = int(disp_id_depto.value)
        
        disponible = fc.verificar_disponibilidad_departamento_en_fechas(
            id_depto,
            disp_fecha_ingreso.value,
            disp_fecha_egreso.value
        )
        
        if disponible:
            disp_resultado.value = "✓ Departamento DISPONIBLE en estas fechas"
            disp_resultado.color = ft.Colors.GREEN
        else:
            disp_resultado.value = "✗ Departamento NO DISPONIBLE (hay conflictos)"
            disp_resultado.color = ft.Colors.RED
        disp_resultado.update()

    dialogo_disponibilidad = ft.AlertDialog(
        title=ft.Text("Consultar Disponibilidad"),
        content=ft.Column([
            disp_id_depto,
            disp_fecha_ingreso, 
            disp_fecha_egreso,
            ft.ElevatedButton("Verificar", on_click=consultar_disponibilidad),
            disp_resultado
        ], height=300),
        actions=[
            ft.TextButton("Cerrar", on_click=lambda e: page.close(dialogo_disponibilidad))
        ],
    )

    def abrir_dialogo_disponibilidad(id_d):
        depto = departamentos.buscar_departamento_por_id(id_d)
        if depto:
            dialogo_disponibilidad.title = ft.Text(f"Disponibilidad - {depto[UBICACION_DEPARTAMENTO]}")
            disp_id_depto.value = str(id_d)
            disp_fecha_ingreso.value = ""
            disp_fecha_egreso.value = ""
            disp_resultado.value = ""
            page.open(dialogo_disponibilidad)

    # --- Diálogos de Confirmación ---
    dialogo_confirmar = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar Acción"),
        content=ft.Text("¿Está seguro?"),
        actions=[],
    )

    def confirmar_baja(id_d):
        dialogo_confirmar.content = ft.Text("¿Dar de baja? Se cancelarán sus reservas activas.")
        dialogo_confirmar.actions = [
            ft.TextButton("Cancelar", on_click=lambda e: page.close(dialogo_confirmar)),
            ft.TextButton("Confirmar Baja", on_click=lambda e: ejecutar_baja_logica(id_d), style=ft.ButtonStyle(color=ft.Colors.RED)),
        ]
        page.open(dialogo_confirmar)

    def confirmar_eliminar_fisico(id_d):
        dialogo_confirmar.content = ft.Text("¿Eliminar PERMANENTEMENTE? Esta acción no se puede deshacer.")
        dialogo_confirmar.actions = [
            ft.TextButton("Cancelar", on_click=lambda e: page.close(dialogo_confirmar)),
            ft.TextButton("ELIMINAR", on_click=lambda e: ejecutar_eliminacion_fisica(id_d), style=ft.ButtonStyle(color=ft.Colors.RED)),
        ]
        page.open(dialogo_confirmar)

    # --- Diálogo Agregar ---
    txt_ubicacion = ft.TextField(label="Ubicación")
    txt_ambientes = ft.TextField(label="Ambientes", keyboard_type=ft.KeyboardType.NUMBER)
    txt_capacidad = ft.TextField(label="Capacidad", keyboard_type=ft.KeyboardType.NUMBER)
    txt_precio = ft.TextField(label="Precio por noche", keyboard_type=ft.KeyboardType.NUMBER)
    dd_estado = ft.Dropdown(
        label="Estado",
        options=[
            ft.dropdown.Option(ESTADO_DISPONIBLE),
            ft.dropdown.Option(ESTADO_OCUPADO),
            ft.dropdown.Option(ESTADO_MANTENIMIENTO),
        ],
        value=ESTADO_DISPONIBLE
    )

    def guardar_nuevo_depto(e):
        try:
            if not txt_ubicacion.value or not txt_ambientes.value:
                page.open(ft.SnackBar(ft.Text("Complete campos obligatorios")))
                return

            amb = int(txt_ambientes.value)
            cap = int(txt_capacidad.value)
            precio = float(txt_precio.value)
            
            if departamentos.agregar_departamento(txt_ubicacion.value, amb, cap, dd_estado.value, precio):
                page.open(ft.SnackBar(ft.Text("Departamento agregado exitosamente")))
                page.close(dialogo_agregar)
                cargar_deptos()
            else:
                page.open(ft.SnackBar(ft.Text("Error al agregar departamento")))
        except ValueError:
             page.open(ft.SnackBar(ft.Text("Error: Verifique los datos numéricos")))

    dialogo_agregar = ft.AlertDialog(
        title=ft.Text("Agregar Departamento"),
        content=ft.Column([txt_ubicacion, txt_ambientes, txt_capacidad, txt_precio, dd_estado], height=400),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: page.close(dialogo_agregar)),
            ft.TextButton("Guardar", on_click=guardar_nuevo_depto),
        ],
    )

    def abrir_dialogo_agregar(e):
        txt_ubicacion.value = ""
        txt_ambientes.value = ""
        txt_capacidad.value = ""
        txt_precio.value = ""
        dd_estado.value = ESTADO_DISPONIBLE
        page.open(dialogo_agregar)

    # --- Diálogo Editar ---
    edit_id = ft.Text()
    edit_ubicacion = ft.TextField(label="Ubicación")
    edit_ambientes = ft.TextField(label="Ambientes")
    edit_capacidad = ft.TextField(label="Capacidad")
    edit_precio = ft.TextField(label="Precio")
    edit_estado = ft.Dropdown(
        label="Estado",
        options=[
            ft.dropdown.Option(ESTADO_DISPONIBLE),
            ft.dropdown.Option(ESTADO_OCUPADO),
            ft.dropdown.Option(ESTADO_MANTENIMIENTO),
        ]
    )

    def guardar_edicion_depto(e):
        try:
            id_d = int(edit_id.value)
            amb = int(edit_ambientes.value)
            cap = int(edit_capacidad.value)
            precio = float(edit_precio.value)

            if departamentos.actualizar_departamento(id_d, edit_ubicacion.value, amb, cap, edit_estado.value, precio):
                page.open(ft.SnackBar(ft.Text("Departamento actualizado")))
                page.close(dialogo_editar)
                cargar_deptos()
            else:
                page.open(ft.SnackBar(ft.Text("Error al actualizar")))
        except ValueError:
             pass

    dialogo_editar = ft.AlertDialog(
        title=ft.Text("Editar Departamento"),
        content=ft.Column([edit_id, edit_ubicacion, edit_ambientes, edit_capacidad, edit_precio, edit_estado], height=400),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: page.close(dialogo_editar)),
            ft.TextButton("Guardar", on_click=guardar_edicion_depto),
        ],
    )

    def abrir_dialogo_editar(id_d):
        depto = departamentos.buscar_departamento_por_id(id_d)
        if depto:
            edit_id.value = str(id_d)
            edit_id.visible = False
            edit_ubicacion.value = depto[UBICACION_DEPARTAMENTO]
            edit_ambientes.value = str(depto[AMBIENTES_DEPARTAMENTO])
            edit_capacidad.value = str(depto[CAPACIDAD_DEPARTAMENTO])
            edit_precio.value = str(depto[PRECIO_DEPARTAMENTO])
            edit_estado.value = depto[ESTADO_DEPARTAMENTO]
            
            page.open(dialogo_editar)

    cargar_deptos()

    return ft.View(
        "/deptos",
        [
            ft.AppBar(
                title=ft.Text("Gestión de Departamentos"), 
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/home"))
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.ElevatedButton("Agregar Departamento", icon=ft.Icons.ADD, on_click=abrir_dialogo_agregar),
                        ft.Row([tabla_deptos], scroll=ft.ScrollMode.AUTO, expand=True)
                    ],
                    expand=True,
                    scroll=ft.ScrollMode.AUTO
                ),
                padding=20,
                expand=True
            )
        ]
    )
