from google import genai
from google.genai import types
from dotenv import load_dotenv
from pydantic import BaseModel

class RecipeOutput(BaseModel):
    meat: str
    title: str
    recipe: str

class AIManipulation:
    def __init__(self, description):
        if not description: raise ValueError("Missing value.")
        self.description = description
        self.client = genai.Client()
        

    def generate_response(self):

        response = self.client.models.generate_content(
                model = "gemini-3.5-flash",
                contents=(
                    f'''Read recipe = {self.description}
                    It can be written in russian or english.
                    If this recipe in english translate it to russian.
                    After that is done, fill in these categories:
                    1. meat should be type of meat used in the recipe. Format it all lower case and should be in english.
                    2. title should be name of the dish. (If it is not stated clearly in the text, write a suitable name that suits this dish.) Format it all lower case and should be in english.
                    3. recipe should consist of 2 parts: ingredients and instruction.
                    3.1 Ingredients. List them in a column with name of the ingredient, amount and measurement. (All measurments should be in EU metrics, except tablespoon or teaspoon.)
                    3.2 Instruction. Write down an instruction or proceedure of how this meal is made. Divide it into multiple steps for easier read.
                    
                '''
                ),
                config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=RecipeOutput,
      ),
            )
        return response.parsed


if __name__== "__main__":
    desc = '''
    Caption: 655 ккал • 55 г белка • 54 г углеводов • 24 г жира

Курица томат-альфредо с пастой

8 контейнеров — ужины на неделю

🔥 КБЖУ (на порцию)
* Калории: 655
* Белки: 55 г
* Углеводы: 54 г
* Жиры: 24 г

Список покупок
• 1,0 кг филе куриной грудки
• 800 г томатного соуса (Napoletana, 2 банки)
• «Альфредо»: 400 мл сливок 10% + 120 г творожного сыра Hochland Protein+ + 60 г пармезана + 530 г TEOS 2% (в конце)
• 450 г фузилли из твёрдых сортов (Barilla)
• 250 г лёгкого сыра 30% (половина внутрь, половина сверху)
• Ложка чеснока; луковый порошок, перец, копчёная паприка — щедро
• Зелёный лук для подачи

Приготовление
Шаг 1: Грудки ЦЕЛИКОМ в толстодонную кастрюлю: томатный соус + сливки + творожный сыр + пармезан + чеснок + приправы. Тушить под крышкой 40–50 минут.
Шаг 2: Разобрать курицу вилками прямо в соусе.
Шаг 3: Пасту отварить и вмешать.
Шаг 4: TEOS вмешать на малом огне, не кипятить. Половину сыра внутрь, половиной посыпать, крышка 15 минут.
Шаг 5: Зелёный лук, 8 контейнеров по весам.

Хранение: порции на 3 дня — в холодильник, остальное в морозилку.
Разогрев: из холодильника — 1:30 в микроволновке + перемешать. Из морозилки — с вечера переложить в холодильник, утром 1:30 в микроволновке.

Сохрани, чтобы не потерять 💪
'''
    load_dotenv()
    client = AIManipulation(desc.strip())
    print(client.generate_response())


