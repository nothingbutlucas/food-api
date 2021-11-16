from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional, List
from pydantic import BaseModel
from recipes import *

tags_metadata = [
    {
        "name": "Foods",
        "description": "Here u can obtain the complete foods using the ID or the Name",
    },
    {
        "name": "Ingredients",
        "description": "Obtain all the foods you can do with the ingredient"
    },
    {
        "name": "Recipes",
        "description": "Obtain all the recipes available in the API"
    }
]

description = """
🍽 Food API for the food bot and console app 🍅

## Foods

You can know **what to cook**.

"""

app = FastAPI(
    title="Food App",
    description=description,
    version="0.1.1",
    contact={
        "name": "lucasdev",
        "url": "https://bio.link/lucasdev",
        "email": "food-app@telegmail.com",
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