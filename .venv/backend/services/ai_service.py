import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_ai_tip(recipe: dict) -> str:
    prompt = f"""
    Dej mi jeden praktický tip nebo zlepšení pro následující recept:

    Název: {recipe.get('title')}
    Ingredience: {', '.join(i['name'] for i in recipe.get('ingredients', []))}
    Kroky: {" | ".join(step['text'] for step in recipe.get('steps', []))}

    Tip:
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=80,
        temperature=0.7
    )

    return response.choices[0].message.content.strip()