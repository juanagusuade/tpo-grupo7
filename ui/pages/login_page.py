import flet as ft
from common.constantes import USUARIOS

def vista_login(page: ft.Page):
    """
    Vista de inicio de sesión.
    Retorna una lista de controles para la vista o configura la página directamente.
    Retorna un ft.View.
    """
    
    # Contador de intentos (usa una lista para poder modificarlo en la función interna)
    intentos_restantes = [3]
    
    usuario_input = ft.TextField(label="Usuario", width=300)
    pass_input = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
    error_text = ft.Text(color=ft.Colors.RED)
    intentos_text = ft.Text(f"Intentos restantes: {intentos_restantes[0]}", size=12, color=ft.Colors.GREY)

    def login(e):
        user = usuario_input.value
        password = pass_input.value
        
        autenticado = False
        for u, p in USUARIOS:
            if u == user and p == password:
                autenticado = True
                break
        
        if autenticado:
            page.session.set("usuario", user)
            page.go("/home")
        else:
            intentos_restantes[0] -= 1
            
            if intentos_restantes[0] > 0:
                error_text.value = f"Credenciales incorrectas. Intentos restantes: {intentos_restantes[0]}"
                intentos_text.value = f"Intentos restantes: {intentos_restantes[0]}"
                usuario_input.value = ""
                pass_input.value = ""
                page.update()
            else:
                error_text.value = "Ha superado el número de intentos. La aplicación se cerrará."
                error_text.color = ft.Colors.RED
                page.update()
                # Esperar un momento antes de cerrar
                import time
                time.sleep(2)
                page.window.close()

    return ft.View(
        "/login",
        [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Iniciar Sesión", size=30, weight=ft.FontWeight.BOLD),
                        usuario_input,
                        pass_input,
                        ft.ElevatedButton("Ingresar", on_click=login),
                        error_text,
                        intentos_text
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20
                ),
                alignment=ft.alignment.center,
                expand=True
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
