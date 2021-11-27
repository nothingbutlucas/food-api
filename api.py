from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional, List
from pydantic import BaseModel
from recipes import *

tags_metadata = [
    {
        "name": "Foods | Comidas",
        "description": "Here u can obtain the complete foods using the ID or the Name | Con este metodo podes obtener las recetas usando el ID o el nombre de la comida",
    },
    {
        "name": "Ingredients | Ingredientes",
        "description": "Obtain all the foods you can do with the ingredient | Con este metodo podes obtener todas las comidas que podes hacer con determinado ingrediente"
    },
    {
        "name": "Recipes | Recetas",
        "description": "Obtain all the recipes available in the API | Con este metodo podes ver todas las recetas disponibles en la API"
    }
]

description = """
## 🍽 Food API for the food_bot and console app 🍅

### What can I cook with what I have?

The food bot and the food console app know's the answer ;)

It happened to you from finding yourself in the situation where you have things to cook, but you don't know what you can do with what you have?

To us too, that's why we developed this API with plant-based food recipes, together with the telegram bot [@plant_base_food_bot](https://t.me/plant_base_food_bot) and with the app to run on the console: food app console that can be found on [GitHub](https://github.com/lucaslucasprogram/food) of [@lucasdev](https://bio.link/lucasdev)


### Recipes made by [@cosoycosas](https://bio.link/cosoycosas) developed by [@lucasdev](https://bio.link/lucasdev)

<:3)~~~~ 

## 🍽 Food API para food_bot y la app de consola 🍅

### Que puedo cocinar con lo que tengo?

¿Te paso de encontrarte en la situación donde tenes cosas para cocinar, pero no sabes que podes hacer con lo que tenes?

A nosotros también, por eso desarrollamos esta API con recetas de comidas basadas en plantas, junto con el bot de telegram [@plant_base_food_bot](https://t.me/plant_base_food_bot) y con la app para correr en consola: food app console que se puede encontrar en el [GitHub](https://github.com/lucaslucasprogram/food) de [@lucasdev](https://bio.link/lucasdev)

### Recetas hechas por [@cosoycosas](https://bio.link/cosoycosas) codeado por [@lucasdev](https://bio.link/lucasdev)
"""

app = FastAPI(
    title="Food API",
    description=description,
    # Version X.Y.Z -> X= Versión mayor, versión principal | Y= Versión menor, nuevas funcionalidades | Z= Revisión por fallos y detalles
    version="0.1.6",
    contact={
        "name": "lucasdev & cosoycosas",
        "url": "https://bio.link/devycoso",
        "email": "devycoso@gmail.com",
    },
    openapi_tags=tags_metadata,
    docs_url=None,
    redoc_url="/"
)

# gt => Greater than
# lt => less than


class Item(BaseModel):
    name: str
    main_ingredients: List
    secondary_ingredients: List


@app.get("/foods/recipes", tags=["Recipes"])
def get_recipes():
    recipes = list()
    for item_id in food:
        recipes.append(food[item_id].get("name"))
    return recipes


@app.get("/foods", tags=["Foods"])
def get_all_foods():
    return food


@app.get("/foods/id/{item_id}", tags=["Foods"])
def get_food_id(item_id: int = Path(None, description="The ID of the item u like to see :)", gt=-1, lt=len(food))):
    return food[item_id]


# The * says something like: Accept that this function has unlimited positional arguments
@app.get("/foods/{name}", tags=["Foods"])
def get_specific_food(name: str = Path(None, description="The name of the food u like to see :)")):
    for item_id in food:
        if food.get(item_id).get("name") == name:
            return food[item_id]
    # found in /get-by-name/?name=name
    # raise HTTPException(status_code=404, detail="Item ID not found.")
    return {"Data": "Error 4🍅4 - Food not Found :("}


@app.get("/foods/ingredients/{ingredient_}", tags=["Ingredients"])
def get_all_ingredients(ingredient_: str = Path(None, description="Capture main and secondary ingredients")):
    foods = list()
    for item_id in food:
        capture_ingredients = food.get(item_id).get("main-ingredients")
        for ingredient in capture_ingredients:
            if ingredient == ingredient_:
                foods.append(food[item_id])
    if len(foods) > 0:
        return foods
    else:
        return {"Data": "Error 4🍊4 - Ingredient not Found :("}


@app.get("/foods/main-ingredients/{ingredient_}", tags=["Ingredients"])
def get_main_ingredient(ingredient_: str = Path(None, description="Capture main ingredients")):
    foods = list()
    for item_id in food:
        capture_ingredients = food.get(item_id).get("main-ingredients")
        for ingredient in capture_ingredients:
            if ingredient == ingredient_:
                foods.append(food[item_id])
    if len(foods) > 0:
        return foods
    else:
        return {"Data": "Error 4🍊4 - Main Ingredient not Found :("}


@app.get("/foods/secondary-ingredients/{ingredient_}", tags=["Ingredients"])
def get_secondary_ingredient(ingredient_: str = Path(None, description="Capture secondary ingredients")):
    foods = list()
    for item_id in food:
        capture_ingredients = food.get(item_id).get("secondary-ingredients")
        if capture_ingredients:
            for ingredient in capture_ingredients:
                if ingredient == ingredient_:
                    foods.append(food[item_id])
    if len(foods) > 0:
        return foods
    else:
        return {"Data": "Error 4🍊4 - Secondary Ingredient not Found :("}
