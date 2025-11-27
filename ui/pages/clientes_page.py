import flet as ft
import domain.clientes as clientes
import domain.reservas as reservas
from common.constantes import *

def vista_clientes(page: ft.Page):
    """
    Vista de Gestión de Clientes.
    """
    
    # Tabla de clientes
    tabla_clientes = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Apellido")),
            ft.DataColumn(ft.Text("DNI")),
            ft.DataColumn(ft.Text("Teléfono")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[]
    )

    def cargar_clientes():
        tabla_clientes.rows.clear()
        lista = clientes.obtener_copia_clientes()
        for cliente in lista:
            id_c = cliente[ID_CLIENTE]
            es_activo = cliente.get(ACTIVO_CLIENTE, True)
            estado_texto = "Activo" if es_activo else "Inactivo"
            color_estado = ft.Colors.GREEN if es_activo else ft.Colors.RED
            
            # Botones de acción
            acciones = []
            
            # Editar
            btn_editar = ft.IconButton(
                icon=ft.Icons.EDIT, 
                tooltip="Editar", 
                on_click=lambda e, id=id_c: abrir_dialogo_editar(id)
            )
            acciones.append(btn_editar)

            if es_activo:
                # Baja Lógica
                btn_baja = ft.IconButton(
                    icon=ft.Icons.DELETE, 
                    tooltip="Dar de baja (Lógica)", 
                    icon_color=ft.Colors.ORANGE,
                    on_click=lambda e, id=id_c: confirmar_baja(id)
                )
                acciones.append(btn_baja)
            else:
                # Alta Lógica
                btn_alta = ft.IconButton(
                    icon=ft.Icons.RESTORE, 
                    tooltip="Reactivar (Alta Lógica)", 
                    icon_color=ft.Colors.GREEN,
                    on_click=lambda e, id=id_c: dar_alta(id)
                )
                acciones.append(btn_alta)
                
                # Eliminación Física
                btn_eliminar = ft.IconButton(
                    icon=ft.Icons.DELETE_FOREVER, 
                    tooltip="Eliminar Físicamente", 
                    icon_color=ft.Colors.RED,
                    on_click=lambda e, id=id_c: confirmar_eliminar_fisico(id)
                )
                acciones.append(btn_eliminar)

            tabla_clientes.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(id_c))),
                        ft.DataCell(ft.Text(cliente[NOMBRE_CLIENTE])),
                        ft.DataCell(ft.Text(cliente[APELLIDO_CLIENTE])),
                        ft.DataCell(ft.Text(cliente[DNI_CLIENTE])),
                        ft.DataCell(ft.Text(cliente[TELEFONO_CLIENTE])),
                        ft.DataCell(ft.Text(estado_texto, color=color_estado)),
                        ft.DataCell(ft.Row(acciones)),
                    ]
                )
            )
        page.update()

    # --- Funciones de ABM ---
    def dar_alta(id_c):
        if clientes.alta_logica_cliente(id_c):
            page.open(ft.SnackBar(ft.Text("Cliente reactivado exitosamente")))
            cargar_clientes()
        else:
            page.open(ft.SnackBar(ft.Text("Error al reactivar cliente")))

    def ejecutar_baja_logica(id_c):
        if clientes.baja_logica_cliente(id_c):
             page.open(ft.SnackBar(ft.Text("Cliente dado de baja (Reservas canceladas)")))
             page.close(dialogo_confirmar)
             cargar_clientes()
        else:
             page.open(ft.SnackBar(ft.Text("No se pudo dar de baja")))

    def ejecutar_eliminacion_fisica(id_c):
        # Verificar si tiene reservas (históricas o activas)
        reservas_cliente = reservas.buscar_reservas_por_cliente(id_c)
        if reservas_cliente:
             page.open(ft.SnackBar(ft.Text("No se puede eliminar: Tiene reservas asociadas.")))
             page.close(dialogo_confirmar)
             return

        if clientes.eliminar_cliente(id_c):
             page.open(ft.SnackBar(ft.Text("Cliente eliminado permanentemente")))
             page.close(dialogo_confirmar)
             cargar_clientes()
        else:
             page.open(ft.SnackBar(ft.Text("Error al eliminar cliente")))

    # --- Diálogos de Confirmación ---
    dialogo_confirmar = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar Acción"),
        content=ft.Text("¿Está seguro?"),
        actions=[],
    )

    def confirmar_baja(id_c):
        dialogo_confirmar.content = ft.Text("¿Dar de baja? Se cancelarán sus reservas activas.")
        dialogo_confirmar.actions = [
            ft.TextButton("Cancelar", on_click=lambda e: page.close(dialogo_confirmar)),
            ft.TextButton("Confirmar Baja", on_click=lambda e: ejecutar_baja_logica(id_c), style=ft.ButtonStyle(color=ft.Colors.RED)),
        ]
        page.open(dialogo_confirmar)

    def confirmar_eliminar_fisico(id_c):
        dialogo_confirmar.content = ft.Text("¿Eliminar PERMANENTEMENTE? Esta acción no se puede deshacer.")
        dialogo_confirmar.actions = [
            ft.TextButton("Cancelar", on_click=lambda e: page.close(dialogo_confirmar)),
            ft.TextButton("ELIMINAR", on_click=lambda e: ejecutar_eliminacion_fisica(id_c), style=ft.ButtonStyle(color=ft.Colors.RED)),
        ]
        page.open(dialogo_confirmar)

    # --- Diálogo Agregar ---
    txt_nombre = ft.TextField(label="Nombre")
    txt_apellido = ft.TextField(label="Apellido")
    txt_dni = ft.TextField(label="DNI")
    txt_telefono = ft.TextField(label="Teléfono")

    def guardar_nuevo_cliente(e):
        if not txt_nombre.value or not txt_apellido.value or not txt_dni.value:
            page.open(ft.SnackBar(ft.Text("Complete los campos obligatorios")))
            return

        if clientes.agregar_cliente(txt_nombre.value, txt_apellido.value, txt_dni.value, txt_telefono.value):
            page.open(ft.SnackBar(ft.Text("Cliente agregado exitosamente")))
            page.close(dialogo_agregar)
            cargar_clientes()
        else:
            page.open(ft.SnackBar(ft.Text("Error: DNI ya existe o datos inválidos")))

    dialogo_agregar = ft.AlertDialog(
        title=ft.Text("Agregar Cliente"),
        content=ft.Column([txt_nombre, txt_apellido, txt_dni, txt_telefono], height=300),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: page.close(dialogo_agregar)),
            ft.TextButton("Guardar", on_click=guardar_nuevo_cliente),
        ],
    )

    def abrir_dialogo_agregar(e):
        txt_nombre.value = ""
        txt_apellido.value = ""
        txt_dni.value = ""
        txt_telefono.value = ""
        page.open(dialogo_agregar)

    # --- Diálogo Editar ---
    edit_id = ft.Text()
    edit_nombre = ft.TextField(label="Nombre")
    edit_apellido = ft.TextField(label="Apellido")
    edit_dni = ft.TextField(label="DNI")
    edit_telefono = ft.TextField(label="Teléfono")

    def guardar_edicion_cliente(e):
        try:
            id_c = int(edit_id.value)
            if clientes.actualizar_cliente(id_c, edit_nombre.value, edit_apellido.value, edit_dni.value, edit_telefono.value):
                page.open(ft.SnackBar(ft.Text("Cliente actualizado")))
                page.close(dialogo_editar)
                cargar_clientes()
            else:
                page.open(ft.SnackBar(ft.Text("Error: DNI repetido o datos inválidos")))
        except ValueError:
             pass

    dialogo_editar = ft.AlertDialog(
        title=ft.Text("Editar Cliente"),
        content=ft.Column([edit_id, edit_nombre, edit_apellido, edit_dni, edit_telefono], height=300),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: page.close(dialogo_editar)),
            ft.TextButton("Guardar", on_click=guardar_edicion_cliente),
        ],
    )

    def abrir_dialogo_editar(id_c):
        cliente = clientes.buscar_cliente_por_id(id_c)
        if cliente:
            edit_id.value = str(id_c)
            edit_id.visible = False
            edit_nombre.value = cliente[NOMBRE_CLIENTE]
            edit_apellido.value = cliente[APELLIDO_CLIENTE]
            edit_dni.value = cliente[DNI_CLIENTE]
            edit_telefono.value = cliente[TELEFONO_CLIENTE]
            
            page.open(dialogo_editar)

    # Carga inicial
    cargar_clientes()

    return ft.View(
        "/clientes",
        [
            ft.AppBar(
                title=ft.Text("Gestión de Clientes"), 
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/home"))
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.ElevatedButton("Agregar Cliente", icon=ft.Icons.ADD, on_click=abrir_dialogo_agregar),
                        ft.Row([tabla_clientes], scroll=ft.ScrollMode.AUTO, expand=True)
                    ],
                    expand=True,
                    scroll=ft.ScrollMode.AUTO
                ),
                padding=20,
                expand=True
            )
        ]
    )
