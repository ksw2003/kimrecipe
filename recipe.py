from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
import google.generativeai as genai

app = Flask(__name__)

cuisines = [
    "",
    "Italian",
    "Mexican",
    "Chinese",
    "Indian",
    "Japanese",
    "Thai",
    "French",
    "Mediterranean",
    "American",
    "Greek"
]

dietary_restrictions = [
    "Gluten-Free",
    "Dairy-Free",
    "Vegan",
    "Pescatarian",
    "Nut-Free",
    "Kosher",
    "Halal",
    "Low-Carb",
    "Organic",
    "Locally Sourced"
]

languages = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Russian": "ru",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Japanese": "ja",
    "Korean": "ko"
}

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-2.5-flash')


@app.route('/')
def index():
    return render_template(
        'index.html',
        cuisines=cuisines,
        dietary_restrictions=dietary_restrictions,
        languages=languages
    )


@app.route('/generate_recipe', methods=['POST'])
def generate_recipe():

    ingredients = [
        request.form['ingredient1'],
        request.form['ingredient2'],
        request.form['ingredient3']
    ]

    selected_cuisine = request.form.get('cuisine')

    selected_restrictions = request.form.getlist(
        'restrictions'
    )

    selected_language = request.form.get('language')

    prompt = f"""
    Create a recipe using:
    {', '.join(ingredients)}

    Return ONLY valid HTML.

    Write the recipe entirely in {selected_language}.

    Required format:

    <h2>Recipe Name</h2>

    <h3>Ingredients</h3>
    <ul>
    <li>Ingredient</li>
    </ul>

    <h3>Instructions</h3>
    <ol>
    <li>Step</li>
    </ol>

    Do NOT use markdown.
    Do NOT use **.
    Do NOT use #.
    Do NOT use ```html.
    Do NOT include explanations before the recipe.
    Return HTML only.
    """

    if selected_cuisine:
        prompt += f"""
        The cuisine should be {selected_cuisine}.
        """

    if selected_restrictions and len(selected_restrictions) > 0:
        prompt += f"""
        The recipe should have the following restrictions:

        {', '.join(selected_restrictions)}
        """

    try:
        response = model.generate_content(prompt)
        recipe = response.text

    except Exception as e:
        recipe = f"Error generating recipe: {str(e)}"

    return render_template(
        'recipe.html',
        recipe=recipe
    )

if __name__ == '__main__':
    app.run(debug=True)