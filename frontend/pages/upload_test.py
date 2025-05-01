#Tady jsem jen testoval upload funkcionalitu

from nicegui import ui
import requests
import json

API_URL = "http://localhost:8000/recipes"

def upload_test_page():
    def handle_upload(e):
        content = e.content.read()
        print("📤 Upload spuštěn:", len(content), "bajtů")

        # 🔧 Dummy recept
        recipe_data = {
            "title": "Testovací upload",
            "description": "Recept vytvořený přes testovací upload stránku",
            "ingredients": [{"name": "Test", "amount": "1 ks"}],
            "steps": [{"text": "Test krok", "type": "regular", "order": 1}],
            "tags": ["upload", "test"]
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

    ui.label("Testovací nahrání a odeslání na /recipes").classes("text-xl font-bold mb-4")
    ui.upload(label="Vyber obrázek").on_upload(handle_upload).classes("mb-4")