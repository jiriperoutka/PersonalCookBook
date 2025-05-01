from nicegui import ui
from frontend.components.top_bar import render_top_bar
import requests

from frontend.service.auth import get_current_user

API_BASE = "http://localhost:8000"

def home_page():
    def delete_recipe(recipe_id):
        #user = get_current_user()
        #render_top_bar(user)

        response = requests.delete(f"{API_BASE}/recipe/{recipe_id}")
        if response.ok:
            ui.notify("🗑️ Recept smazán")
            ui.navigate.to('/')
        else:
            ui.notify("❌ Chyba při mazání receptu")

    with ui.column().classes("w-full items-center p-4"):
        ui.label("Všechny recepty").classes("text-xl font-semibold mb-2")
        with ui.row().classes("flex-wrap justify-center"):
            response = requests.get(f"{API_BASE}/recipes")
            if response.status_code == 200:
                for recipe in response.json():
                    with ui.card().classes("w-96 m-4 shadow-lg rounded-2xl relative"):
                        if recipe.get("image_data"):
                            ui.image(f"data:image/jpeg;base64,{recipe['image_data']}") \
                                .classes("w-full h-48 object-cover rounded-t-2xl")
                        with ui.column().classes("p-4"):
                            ui.link(recipe["title"], f"/recipe/{recipe['_id']}").classes("text-lg font-bold text-blue-600 hover:underline")
                            ui.label(recipe.get("description", "")).classes("text-sm text-gray-600")

                        # Tlačítko delete
                        ui.button("\u274c", on_click=lambda r=recipe: delete_recipe(r['_id'])) \
                            .classes("absolute top-2 right-2 bg-red-600 text-white rounded-full w-8 h-8 flex items-center justify-center hover:bg-red-700")