from nicegui import ui
import requests
import json
from frontend.service.auth import get_current_user
from frontend.components.top_bar import render_top_bar

API_URL = "http://localhost:8000/recipes"

def new_recipe_page():
    user = get_current_user()
    render_top_bar(user)

    def handle_upload(e):
        content = e.content.read()
        print("📤 Upload spuštěn:", len(content), "bajtů")

        recipe_data = {
            "title": title.value,
            "description": description.value,
            "ingredients": [{"name": i.strip(), "amount": "?"} for i in ingredients.value.split("\n") if i.strip()],
            "steps": [{"text": s.strip(), "type": "regular", "order": idx + 1} for idx, s in enumerate(steps.value.split("\n")) if s.strip()],
            "tags": [t.strip() for t in tags.value.split(",") if t.strip()]
        }

        files = {
            "recipe": (None, json.dumps(recipe_data), "application/json"),
            "image": ("image.jpg", content, "image/jpeg")
        }

        try:
            response = requests.post(API_URL, files=files)
            if response.ok:
                ui.notify("✅ Recept úspěšně odeslán na API")
                print("✅ API odpověď:", response.status_code)
            else:
                ui.notify(f"❌ API chyba: {response.status_code}")
                print("❌ Chyba odpovědi:", response.status_code)
        except Exception as ex:
            print("❌ Výjimka při POST:", ex)
            ui.notify("❌ Chyba při komunikaci se serverem")

    ui.label("Nový recept").classes("text-2xl font-bold my-4")

    global title, description, ingredients, steps, tags
    title = ui.input("Název receptu").classes("w-full")
    description = ui.textarea("Popis").classes("w-full")
    ingredients = ui.textarea("Ingredience (např. Mouka)").classes("w-full")
    steps = ui.textarea("Kroky").classes("w-full")
    tags = ui.input("Tagy (oddělené čárkou)").classes("w-full")

    ui.upload(label="Vyber obrázek").on_upload(handle_upload).classes("mb-4")