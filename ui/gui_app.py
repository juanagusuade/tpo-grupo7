import flet as ft
from ui.pages.login_page import vista_login
from ui.pages.home_page import vista_home
from ui.pages.clientes_page import vista_clientes
from ui.pages.deptos_page import vista_deptos
from ui.pages.reservas_page import vista_reservas
from ui.pages.estadisticas_page import vista_estadisticas

def iniciar_app(page: ft.Page):
    """
    Función principal de la aplicación Flet.
    Configura el título, tema y el enrutamiento.
    """
    page.title = "Sistema de Gestión de Alquileres"
    page.theme_mode = ft.ThemeMode.DARK
    
    def route_change(route):
        page.views.clear()
        
        # Ruta por defecto o Login
        if page.route == "/login" or page.route == "/":
            page.views.append(vista_login(page))
            
        elif page.route == "/home":
            # Verificar si hay usuario en sesión (mokead)
            if not page.session.get("usuario"):
                page.go("/login")
                return
            page.views.append(vista_home(page))
            
        elif page.route == "/clientes":
            if not page.session.get("usuario"):
                page.go("/login")
                return
            page.views.append(vista_clientes(page))

        elif page.route == "/deptos":
            if not page.session.get("usuario"):
                page.go("/login")
                return
            page.views.append(vista_deptos(page))

        elif page.route == "/reservas":
            if not page.session.get("usuario"):
                page.go("/login")
                return
            page.views.append(vista_reservas(page))

        elif page.route == "/estadisticas":
            if not page.session.get("usuario"):
                page.go("/login")
                return
            page.views.append(vista_estadisticas(page))
        
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # Iniciar en login
    page.go("/login")
