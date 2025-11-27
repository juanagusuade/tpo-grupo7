import flet as ft

def vista_home(page: ft.Page):
    """
    Vista principal (Home).
    """
    usuario = page.session.get("usuario") or "Usuario"

    return ft.View(
        "/home",
        [
            ft.AppBar(title=ft.Text("Sistema de Gestión"), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(f"Bienvenido, {usuario}!", size=30),
                        ft.Text("Seleccione una opción del menú para comenzar.", size=16),
                        ft.Row(
                            [
                                ft.ElevatedButton("Gestionar Clientes", on_click=lambda _: page.go("/clientes"), height=50),
                                ft.ElevatedButton("Gestionar Departamentos", on_click=lambda _: page.go("/deptos"), height=50),
                                ft.ElevatedButton("Gestionar Reservas", on_click=lambda _: page.go("/reservas"), height=50),
                                ft.ElevatedButton("Ver Estadísticas", on_click=lambda _: page.go("/estadisticas"), height=50),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            wrap=True,
                            spacing=20
                        ),
                        ft.ElevatedButton("Cerrar Sesión", on_click=lambda _: page.go("/login"), color=ft.Colors.RED)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=30
                ),
                alignment=ft.alignment.center,
                expand=True
            )
        ]
    )
