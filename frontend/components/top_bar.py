from nicegui import ui

def render_top_bar(user):
    with ui.row().classes("w-full px-6 py-4 justify-between items-center bg-white shadow"):
        # Logo + název vlevo
        with ui.row().classes("items-center gap-3"):
            ui.image("https://cdn-icons-png.flaticon.com/512/3075/3075977.png").classes("w-8 h-8")
            ui.label("CookBook").classes("text-2xl font-bold")

        # Tlačítka vpravo
        with ui.row().classes("items-center gap-3"):
            if user:
                ui.button("➕ Přidat recept", on_click=lambda: ui.navigate.to("/new")) \
                    .classes("bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700")

                ui.button("Odhlásit", on_click=lambda: ui.navigate.to("/logout")) \
                    .classes("bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600")
            else:
                ui.button("🔐 Přihlásit se", on_click=lambda: ui.navigate.to("/login")) \
                    .classes("bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700")