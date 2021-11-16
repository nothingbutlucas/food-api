from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional, List
from pydantic import BaseModel
from recipes import *

tags_metadata = [
    {
        "name": "Foods",
        "description": "Here u can obtain the complete foods using the ID or the Name"
    },
    {
        "name": "Ingredients",
        "description": "Obtain all the foods you can do with the ingredient"
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
    version="0.0.1",
    contact={
        "name": "lucasdev",
        "url": "https://bio.link/lucasdev",
        "email": "food-app@telegmail.com",
    },
    openapi_tags=tags_metadata
)

# gt => Greater than
# lt => less than


class Item(BaseModel):
    name: str
    ingredients: List


@app.get("/")
def home_view():
    return food


@app.get("/foods-id/{item_id}", tags=["Foods"])
def get_food_id(item_id: int = Path(None, description="The ID of the item u like to see :)", gt=-1, lt=len(food))):
    return food[item_id]


# The * says something like: Accept that this function has unlimited positional arguments
@app.get("/foods/{name}", tags=["Foods"])
def get_foods(name: str):
    for item_id in food:
        if food.get(item_id).get("name") == name:
            return food[item_id]
    # found in /get-by-name/?name=name
    # raise HTTPException(status_code=404, detail="Item ID not found.")
    return {"Data": "Error 4🍅4 - Recipe not Found :("}


@app.get("/foods/ingredients/{ingredient_}", tags=["Ingredients"])
def get_ingredient(ingredient_: str):
    foods = list()
    for item_id in food:
        capture_ingredients = food.get(item_id).get("ingredients")
        for ingredient in capture_ingredients:
            if ingredient == ingredient_:
                foods.append(food[item_id])
    if len(foods) > 0:
        return foods
    else:
        return {"Data": "Error 4🍊4 - Ingredient not Found :("}


'''
@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        return {"Error": "Item ID already exists."}

    inventory[item_id] = item
    return inventory[item_id]


@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        return {"Error": "Item ID does not exists."}

    if item.name != None:
        inventory[item_id].name = item.name

    if item.price != None:
        inventory[item_id].price = item.price

    if item.brand != None:
        inventory[item_id].brand = item.brand

    return inventory[item_id]


@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="The ID of the item to delete"), gt = 0):
    if item_id not in inventory:
        return {"Error": "ID does not exists"}

    del inventory[item_id]
    return {"Success": "Item deleted!"}

'''