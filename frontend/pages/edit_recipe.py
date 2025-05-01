from nicegui import ui
import json
import httpx
import requests

API_BASE = "http://localhost:8000/recipes"

def edit_recipe_page(recipe_id: str):
    response = requests.get(f"{API_BASE}/{recipe_id}")
    if response.status_code != 200:
        ui.label("❌ Recept nebyl nalezen").classes("text-red-600 text-xl")
        return

    recipe = response.json()
    uploaded_image = {}

    ui.label("📝 Úprava receptu").classes("text-3xl font-bold my-4")

    # === Název a popis ===
    title_input = ui.input("Název receptu", value=recipe.get("title", "")).classes("w-full max-w-2xl")
    description_input = ui.textarea("Popis", value=recipe.get("description", "")).classes("w-full max-w-2xl")

    # === Upload obrázku ===
    ui.label("📸 Obrázek (volitelné)").classes("mt-6")
    def handle_upload(e):
        uploaded_image["name"] = e.name
        uploaded_image["content"] = e.content.read()
        uploaded_image["content_type"] = e.type or "application/octet-stream"

    ui.upload(label="Vyber soubor", auto_upload=True, on_upload=handle_upload).classes("w-full max-w-2xl")

    ui.separator().classes("my-4")

    # === Suroviny ===
    ui.label("🧂 Suroviny").classes("text-xl font-semibold mt-6")
    ingredient_inputs = []
    ingredient_container = ui.column().classes("gap-2 w-full max-w-2xl")

    def add_ingredient(amount_val="", name_val=""):
        with ingredient_container:
            row_container = ui.row().classes("items-center gap-4")
            with row_container:
                amount = ui.input("Množství", value=amount_val).classes("flex-1 min-w-[100px]")
                name = ui.input("Název", value=name_val).classes("flex-[2] min-w-[200px]")

                def delete_ingredient():
                    ingredient_inputs.remove((amount, name))
                    row_container.clear()

                ui.button("🗑️", on_click=delete_ingredient).props("flat color=red").classes("w-10")

            ingredient_inputs.append((amount, name))

    for ing in recipe.get("ingredients", []):
        add_ingredient(ing["amount"], ing["name"])

    ui.button("➕ Přidat surovinu", on_click=lambda: add_ingredient()).classes("mt-2")

    # === Kroky ===
    ui.label("👨‍🍳 Postup").classes("text-xl font-semibold mt-6")
    step_inputs = []
    step_container = ui.column().classes("gap-2 w-full max-w-2xl")

    def add_step(order_val="", text_val=""):
        with step_container:
            row_container = ui.row().classes("items-center gap-4")
            with row_container:
                order = ui.input("Pořadí", value=str(order_val)).classes("w-1/5 min-w-[60px]")
                text = ui.input("Popis", value=text_val).classes("flex-1 min-w-[200px]")

                def delete_step():
                    step_inputs.remove((order, text))
                    row_container.clear()

                ui.button("🗑️", on_click=delete_step).props("flat color=red").classes("w-10")

            step_inputs.append((order, text))

    for step in sorted(recipe.get("steps", []), key=lambda s: s.get("order", 0)):
        add_step(step["order"], step["text"])

    ui.button("➕ Přidat krok", on_click=lambda: add_step()).classes("mt-2")

    ui.separator().classes("my-4")

    # === Uložení ===
    def save_changes():
        updated_recipe = {
            "title": title_input.value,
            "description": description_input.value,
            "ingredients": [
                {"amount": a.value, "name": n.value} for a, n in ingredient_inputs
            ],
            "steps": [
                {"order": int(o.value), "text": t.value} for o, t in step_inputs if o.value.isdigit()
            ],
        }

        files = {
            "recipe": (None, json.dumps(updated_recipe), "application/json")
        }

        if uploaded_image:
            files["image"] = (
                uploaded_image["name"],
                uploaded_image["content"],
                uploaded_image["content_type"],
            )

        try:
            with httpx.Client() as client:
                response = client.put(
                    f"{API_BASE}/{recipe_id}",
                    files=files,
                )

            if response.status_code == 200:
                ui.notify("✅ Recept byl úspěšně upraven")
                ui.navigate.to(f"/recipe/{recipe_id}")
            else:
                ui.notify(f"❌ Chyba při ukládání: {response.text}")
        except Exception as e:
            ui.notify(f"❌ Výjimka při ukládání: {e}")

    ui.button("💾 Uložit změny", on_click=save_changes).classes("mt-6 bg-green-600 text-white px-6 py-3 rounded-xl hover:bg-green-700")