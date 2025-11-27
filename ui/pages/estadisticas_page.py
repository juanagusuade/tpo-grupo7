import flet as ft
import domain.clientes as clientes
import domain.departamentos as departamentos
import domain.reservas as reservas
from common.constantes import *

def vista_estadisticas(page: ft.Page):
    """
    Vista de Estadísticas.
    """
    
    # 1. Cantidad total de clientes activos
    total_clientes = len(clientes.listar_clientes_activos())
    
    # 2. Cantidad total de departamentos (activos)
    total_deptos = len(departamentos.listar_departamentos_activos())
    
    # 3. Cantidad de reservas activas
    reservas_activas = reservas.obtener_reservas_activas()
    total_reservas_activas = len(reservas_activas)
    
    # 4. Duración promedio de reservas
    promedio_dias = reservas.calcular_duracion_promedio_reservas()
    
    # 5. Ocupación por departamento
    tabla_ocupacion = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Departamento")),
            ft.DataColumn(ft.Text("Días Ocupados")),
            ft.DataColumn(ft.Text("% Ocupación (Anual)")),
        ],
        rows=[]
    )
    
    deptos = departamentos.listar_departamentos_activos()
    for d in deptos:
        dias = reservas.calcular_dias_ocupados_depto(d[ID_DEPARTAMENTO])
        porcentaje = reservas.calcular_porcentaje_ocupacion_depto(d[ID_DEPARTAMENTO])
        
        tabla_ocupacion.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(d[UBICACION_DEPARTAMENTO])),
                    ft.DataCell(ft.Text(str(dias))),
                    ft.DataCell(ft.Text(f"{porcentaje:.1f}%")),
                ]
            )
        )

    return ft.View(
        "/estadisticas",
        [
            ft.AppBar(
                title=ft.Text("Estadísticas del Sistema"), 
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/home"))
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                tarjeta_estadistica("Clientes Activos", str(total_clientes), ft.Icons.PEOPLE),
                                tarjeta_estadistica("Deptos. Activos", str(total_deptos), ft.Icons.APARTMENT),
                                tarjeta_estadistica("Reservas Activas", str(total_reservas_activas), ft.Icons.CALENDAR_MONTH),
                                tarjeta_estadistica("Promedio Días", f"{promedio_dias:.1f}", ft.Icons.TIMELAPSE),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=20
                        ),
                        ft.Divider(),
                        ft.Text("Ocupación por Departamento", size=20, weight=ft.FontWeight.BOLD),
                        ft.Row([tabla_ocupacion], scroll=ft.ScrollMode.AUTO, expand=True)
                    ],
                    spacing=10,
                    scroll=ft.ScrollMode.AUTO
                ),
                expand=True,
                padding=20
            )
        ]
    )

def tarjeta_estadistica(titulo, valor, icono):
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icono, size=40, color=ft.Colors.PRIMARY),
                    ft.Text(valor, size=30, weight=ft.FontWeight.BOLD),
                    ft.Text(titulo, size=14),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=20,
            width=150,
            height=150,
        )
    )
