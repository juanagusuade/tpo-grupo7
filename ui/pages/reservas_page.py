import flet as ft
import domain.reservas as reservas
import domain.clientes as clientes
import domain.departamentos as departamentos
from common.constantes import *

def vista_reservas(page: ft.Page):
    """
    Vista de Gestión de Reservas.
    """
    
    tabla_reservas = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Cliente")),
            ft.DataColumn(ft.Text("Depto")),
            ft.DataColumn(ft.Text("Ingreso")),
            ft.DataColumn(ft.Text("Egreso")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[]
    )

    def cargar_reservas():
        tabla_reservas.rows.clear()
        lista = reservas.obtener_todas_las_reservas()
        lista = [r for r in lista if r[INDICE_ESTADO] != ESTADO_ELIMINADO]
        
        for res in lista:
            id_r = res[INDICE_ID_RESERVA]
            estado = res[INDICE_ESTADO]
            color_estado = ft.Colors.GREEN if estado == ESTADO_ACTIVO else ft.Colors.ORANGE
            
            # Obtener nombres
            cli = clientes.buscar_cliente_por_id(res[INDICE_ID_CLIENTE])
            nombre_cli = f"{cli[NOMBRE_CLIENTE]} {cli[APELLIDO_CLIENTE]}" if cli else "Desc."
            
            depto = departamentos.buscar_departamento_por_id(res[INDICE_ID_DEPARTAMENTO])
            nombre_depto = depto[UBICACION_DEPARTAMENTO] if depto else "Desc."

            acciones = []

            if estado == ESTADO_ACTIVO:
                btn_cancelar = ft.IconButton(
                    icon=ft.Icons.CANCEL, 
                    tooltip="Cancelar Reserva", 
                    icon_color=ft.Colors.ORANGE,
                    on_click=lambda e, id=id_r: confirmar_cancelacion(id)
                )
                acciones.append(btn_cancelar)
            elif estado == ESTADO_CANCELADO:
                btn_reactivar = ft.IconButton(
                    icon=ft.Icons.RESTORE, 
                    tooltip="Reactivar Reserva", 
                    icon_color=ft.Colors.GREEN,
                    on_click=lambda e, id=id_r: reactivar(id)
                )
                acciones.append(btn_reactivar)
                
                btn_eliminar = ft.IconButton(
                    icon=ft.Icons.DELETE_FOREVER, 
                    tooltip="Eliminar Físicamente", 
                    icon_color=ft.Colors.RED,
                    on_click=lambda e, id=id_r: confirmar_eliminar_fisico(id)
                )
                acciones.append(btn_eliminar)
            
            tabla_reservas.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(id_r))),
                        ft.DataCell(ft.Text(nombre_cli)),
                        ft.DataCell(ft.Text(nombre_depto)),
                        ft.DataCell(ft.Text(res[INDICE_FECHA_INGRESO])),
                        ft.DataCell(ft.Text(res[INDICE_FECHA_EGRESO])),
                        ft.DataCell(ft.Text(estado, color=color_estado)),
                        ft.DataCell(ft.Row(acciones)),
                    ]
                )
            )
        page.update()

    # --- Funciones ABM ---
    def reactivar(id_r):
        if reservas.reactivar_reserva(id_r):
             page.open(ft.SnackBar(ft.Text("Reserva reactivada")))
             cargar_reservas()
        else:
             page.open(ft.SnackBar(ft.Text("Error al reactivar (¿Fechas ocupadas?)")))

    def ejecutar_cancelacion(id_r):
        if reservas.cancelar_reserva(id_r):
             page.open(ft.SnackBar(ft.Text("Reserva cancelada")))
             page.close(dialogo_confirmar)
             cargar_reservas()
        else:
             page.open(ft.SnackBar(ft.Text("No se pudo cancelar")))

    def ejecutar_eliminacion_fisica(id_r):
        if reservas.eliminar_reserva(id_r):
             page.open(ft.SnackBar(ft.Text("Reserva eliminada permanentemente")))
             page.close(dialogo_confirmar)
             cargar_reservas()
        else:
             page.open(ft.SnackBar(ft.Text("Error al eliminar")))

    # --- Diálogos Confirmación ---
    dialogo_confirmar = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar Acción"),
        content=ft.Text("¿Está seguro?"),
        actions=[],
    )

    def confirmar_cancelacion(id_r):
        dialogo_confirmar.content = ft.Text("¿Cancelar esta reserva?")
        dialogo_confirmar.actions = [
            ft.TextButton("Volver", on_click=lambda e: page.close(dialogo_confirmar)),
            ft.TextButton("Cancelar Reserva", on_click=lambda e: ejecutar_cancelacion(id_r), style=ft.ButtonStyle(color=ft.Colors.ORANGE)),
        ]
        page.open(dialogo_confirmar)

    def confirmar_eliminar_fisico(id_r):
        dialogo_confirmar.content = ft.Text("¿Eliminar PERMANENTEMENTE del historial?")
        dialogo_confirmar.actions = [
            ft.TextButton("Volver", on_click=lambda e: page.close(dialogo_confirmar)),
            ft.TextButton("ELIMINAR", on_click=lambda e: ejecutar_eliminacion_fisica(id_r), style=ft.ButtonStyle(color=ft.Colors.RED)),
        ]
        page.open(dialogo_confirmar)

    # --- Diálogo Agregar ---
    dd_cliente = ft.Dropdown(label="Cliente")
    dd_depto = ft.Dropdown(label="Departamento")
    txt_fecha_ingreso = ft.TextField(label="Fecha Ingreso (dd/mm/aaaa)", max_length=10)
    txt_fecha_egreso = ft.TextField(label="Fecha Egreso (dd/mm/aaaa)", max_length=10)

    def formatear_fecha(e, campo):
        """Auto-formatea la fecha agregando las barras mientras el usuario escribe"""
        texto = campo.value or ""
        # Remover barras para trabajar solo con numeros
        numeros = texto.replace("/", "")
        
        # Solo permitir nunmeros
        if not all(c.isdigit() for c in numeros):
            numeros = ''.join(c for c in numeros if c.isdigit())
        
        # Formatear según la longitud
        if len(numeros) <= 2:
            campo.value = numeros
        elif len(numeros) <= 4:
            campo.value = f"{numeros[:2]}/{numeros[2:]}"
        else:
            campo.value = f"{numeros[:2]}/{numeros[2:4]}/{numeros[4:8]}"
        
        campo.update()

    txt_fecha_ingreso.on_change = lambda e: formatear_fecha(e, txt_fecha_ingreso)
    txt_fecha_egreso.on_change = lambda e: formatear_fecha(e, txt_fecha_egreso)

    def guardar_nueva_reserva(e):
        try:
            if not dd_cliente.value or not dd_depto.value or not txt_fecha_ingreso.value or not txt_fecha_egreso.value:
                 page.open(ft.SnackBar(ft.Text("Complete todos los campos")))
                 return

            id_c = int(dd_cliente.value)
            id_d = int(dd_depto.value)
            
            if reservas.agregar_reserva(id_c, id_d, txt_fecha_ingreso.value, txt_fecha_egreso.value):
                page.open(ft.SnackBar(ft.Text("Reserva creada exitosamente")))
                page.close(dialogo_agregar)
                cargar_reservas()
            else:
                page.open(ft.SnackBar(ft.Text("Error: Verifique disponibilidad y fechas")))
        except (ValueError, TypeError):
             page.open(ft.SnackBar(ft.Text("Error: Datos inválidos")))

    dialogo_agregar = ft.AlertDialog(
        title=ft.Text("Nueva Reserva"),
        content=ft.Column(
            [
                ft.Text("Seleccione un cliente:", weight=ft.FontWeight.BOLD, size=12),
                dd_cliente,
                ft.Text("Seleccione un departamento:", weight=ft.FontWeight.BOLD, size=12),
                dd_depto,
                ft.Divider(),
                txt_fecha_ingreso,
                txt_fecha_egreso
            ],
            height=450,
            scroll=ft.ScrollMode.AUTO
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: page.close(dialogo_agregar)),
            ft.TextButton("Guardar", on_click=guardar_nueva_reserva),
        ],
    )

    def abrir_dialogo_agregar(e):
        # Cargar opciones de clientes y deptos
        dd_cliente.options = []
        lista_clientes = clientes.listar_clientes_activos()
        
        # Usar texto corto y agregar hint text
        dd_cliente.hint_text = f"{len(lista_clientes)} clientes disponibles - busque escribiendo"
        
        for c in lista_clientes:
            dd_cliente.options.append(
                ft.dropdown.Option(
                    key=str(c[ID_CLIENTE]), 
                    text=f"{c[ID_CLIENTE]} - {c[NOMBRE_CLIENTE]} {c[APELLIDO_CLIENTE]}"
                )
            )
        
        dd_depto.options = []
        lista_deptos_disponibles = []
        
        for d in departamentos.listar_departamentos_activos():
             if d[ESTADO_DEPARTAMENTO] == ESTADO_DISPONIBLE:
                lista_deptos_disponibles.append(d)
                dd_depto.options.append(
                    ft.dropdown.Option(
                        key=str(d[ID_DEPARTAMENTO]), 
                        text=f"{d[ID_DEPARTAMENTO]} - {d[UBICACION_DEPARTAMENTO]} (${d[PRECIO_DEPARTAMENTO]})"
                    )
                )
        
        dd_depto.hint_text = f"{len(lista_deptos_disponibles)} departamentos disponibles"

        txt_fecha_ingreso.value = ""
        txt_fecha_egreso.value = ""
        
        page.open(dialogo_agregar)

    cargar_reservas()    

    return ft.View(
        "/reservas",
        [
            ft.AppBar(
                title=ft.Text("Gestión de Reservas"), 
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/home"))
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.ElevatedButton("Nueva Reserva", icon=ft.Icons.ADD, on_click=abrir_dialogo_agregar),
                        ft.Row([tabla_reservas], scroll=ft.ScrollMode.AUTO, expand=True)
                    ],
                    expand=True,
                    scroll=ft.ScrollMode.AUTO
                ),
                padding=20,
                expand=True
            )
        ]
    )
