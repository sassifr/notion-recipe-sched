import requests
import os
import json
import random
import re
from dotenv import load_dotenv


# get page IDs for all recipes from recipe datasource
def getAllRecipes():
    url = f"https://api.notion.com/v1/data_sources/{os.environ['NOTION_DATA_SOURCE']}/query"

    payload = {}

    headers = {
        "Notion-Version": "2026-03-11",
        "Authorization": f'Bearer {os.environ['NOTION_KEY']}',
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)

    parsed_data = []

    json_response = json.loads(response.text)

    for page in json_response["results"]:
        parsed_page = {
            "id": page["id"],
            "name": page["properties"]["Name"]["title"][0]["plain_text"],
            "can_double": True,
            "servings": 1
        }

        parsed_data.append(parsed_page)

    return parsed_data

# get ingredients list datasource ID from recipe page
def getIngredientsDB(dataSource):

    url = f"https://api.notion.com/v1/pages/{dataSource}/markdown"

    headers = {
        "Notion-Version": "2026-03-11",
        "Authorization": f'Bearer {os.environ['NOTION_KEY']}'
    }

    response = requests.get(url, headers=headers)

    ingListID = re.split('">ingredients', re.split("collection://", response.text)[1])[0][:-1]

    return ingListID

# get list of ingredients from a recipe datasource ID
def getIngredientsList(dataSource):
    url = f"https://api.notion.com/v1/data_sources/{dataSource}/query"

    headers = {
        "Notion-Version": "2026-03-11",
        "Authorization": f'Bearer {os.environ['NOTION_KEY']}',
        "Content-Type": "application/json"
    }

    response = requests.post(url, json={}, headers=headers)

    parsed_data = []
    
    json_response = json.loads(response.text)

    for ing in json_response["results"]:
        parsed_ing = {
            "ingredient": ing["properties"]["ingredient"]["title"][0]["plain_text"],
            "amount": ing["properties"]["amount"]["number"],
            "unit": ing["properties"]["unit"]["select"]["name"]
        }

        parsed_data.append(parsed_ing)

    return parsed_data

# get list of ingredients from recipe page
def GetIngredients(recipe):
    recipeDB = getIngredientsDB(recipe['id'])
    return getIngredientsList(recipeDB)


'''
recipe format:
[
    {
        "name": str,
        "servings": int,
        "can_double": bool
    },
]
'''
# from list of recipes, create a random shorlist schedule (incl total servings)
def makeSchedule(serv, recipes):
    # keep adding recipes until we run out of options OR we have enough servings
    seen = set()
    doubled = False
    double_threshold = 15
    schedule = {
        "servings": 0,
        "recipes": []
        }

    while len(seen) < len(recipes) and schedule["servings"] < serv:
        idx  = random.randrange(len(recipes))

        # fix this lollll
        while idx in seen:
            idx  = random.randrange(len(recipes))

        curr = recipes[idx]

        schedule["recipes"].append(curr)

        # if we can double it, lets do it!
        if serv > double_threshold and doubled == False and curr["can_double"]:
            doubled = True
            schedule["recipes"][-1]["name"] = "(doubled) " + schedule["recipes"][-1]["name"]
            schedule["recipes"][-1]["servings"] = schedule["recipes"][-1]["servings"] *2

        schedule["servings"] += schedule["recipes"][-1]["servings"] 
        seen.add(idx)

    return schedule

# create shopping list from a list of recipes
def makeShoppingList(recipes):

    shoppingList = dict()

    # for each recipe in scheudle
    for recipe in recipes:
        # get ingredients db
        # getIngredientsDB(recipe['id'])
        ingredientsList = GetIngredients(recipe)

        # for each ingredient
        for ing in ingredientsList:
            # check if the ingredient is in the shopping list
            key = f"{ing['ingredient']}_{ing['unit']}"
            if key in shoppingList:
                # yes -> then add to the existing one
                shoppingList[key] += ing['amount']
            else:
                shoppingList[key] = ing['amount']

    print(shoppingList)
            



if __name__ == '__main__':
    load_dotenv()

    allRecipes = getAllRecipes()

    schedule = makeSchedule(16, allRecipes)

    makeShoppingList(schedule["recipes"])