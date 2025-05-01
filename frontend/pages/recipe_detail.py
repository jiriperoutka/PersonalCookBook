from nicegui import ui
import requests

API_BASE = "http://localhost:8000/recipes"

def recipe_detail_page(recipe_id: str):
    response = requests.get(f"{API_BASE}/{recipe_id}")
    if response.status_code != 200:
        ui.label("❌ Recept nebyl nalezen").classes("text-red-600 text-xl")
        return

    recipe = response.json()

    # Horní lišta s ikonou a tlačítkem Edit
    with ui.row().classes("bg-white shadow-md px-6 py-4 justify-between items-center w-full"):
        with ui.row().classes("items-center gap-4"):
            ui.image("https://cdn-icons-png.flaticon.com/512/3075/3075977.png").classes("w-10 h-10 cursor-pointer").on("click", lambda: ui.navigate.to("/"))
            ui.label("CookBook").classes("text-2xl font-extrabold text-gray-800 cursor-pointer").on("click", lambda: ui.navigate.to("/"))
        ui.button("✏️ Upravit", on_click=lambda: ui.navigate.to(f"/edit/{recipe_id}")) \
            .classes("bg-yellow-500 text-white text-md px-5 py-2 rounded-xl hover:bg-yellow-600")

    # Obrázek v horní části + název jako overlay
    with ui.column().classes("w-full items-center"):
        if recipe.get("image_data"):
            with ui.column().classes("relative w-full"):
                ui.image(f"data:image/jpeg;base64,{recipe['image_data']}") \
                    .classes("w-full max-h-96 object-cover rounded-b-xl")
                ui.label(recipe["title"]).classes(
                    "absolute bottom-4 left-4 text-white text-4xl font-bold bg-black bg-opacity-50 px-6 py-2 rounded-xl")

    # Popis zarovnaný na střed a vizuálně odlišený
    if recipe.get("description"):
        with ui.column().classes("items-center w-full"):
            ui.label(recipe["description"]).classes("italic text-center text-lg text-gray-700 mt-6 mb-6 max-w-3xl")

    # AI Tip karta
    ai_tip_response = requests.get(f"{API_BASE}/{recipe_id}/ai-tip")
    if ai_tip_response.status_code == 200:
        ai_tip = ai_tip_response.json().get("tip", "")
        with ui.card().classes("bg-purple-100 border-l-4 border-purple-500 shadow-md p-6 mb-8 max-w-3xl mx-auto"):
            ui.label("💡 AI tip").classes("text-xl font-bold text-purple-800 mb-2")
            ui.label(ai_tip).classes("text-md text-purple-900")

    # Postup a suroviny jako dvě vedlejší karty
    with ui.row().classes("w-full justify-center gap-8 px-8 items-start"):
        with ui.card().classes("w-full max-w-lg shadow-md p-4 flex-1"):
            ui.label("Postup").classes("text-xl font-semibold mb-4")
            for step in sorted(recipe.get("steps", []), key=lambda s: s.get("order", 0)):
                with ui.card().classes("mb-2 p-3 bg-gray-100 shadow-sm"):
                    ui.label(f"{step['order']}. {step['text']}").classes("text-base")

        with ui.card().classes("w-full max-w-lg shadow-md p-4 flex-1"):
            ui.label("Suroviny").classes("text-xl font-semibold mb-4")
            for ing in recipe.get("ingredients", []):
                ui.label(f"{ing['amount']} {ing['name']}").classes("mb-1 text-base")