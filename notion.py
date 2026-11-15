import requests
import os
import json
from random import randrange
import re
from enum import Enum
from dotenv import load_dotenv


EMOKI = "🍵🍶🍾🍷🍸🍹🍺🍻🥂🥃🍘🍙🍚🍛🍜🍠🍢🍣🍤🥮🍡🥟🍞🥐🥖🥨🥯🥞🧇🧀🍖🍗🥩🍔🍟🍕🌭🥪🌮🌯🫔🥙🧆🥚🍳🍲🫕🥗🥫🍝🍇🍈🍉🍊🍋🍌🍍🥭🍎🍏🍐🍑🍒🍓🫐🥝🍅🫒🥥🥑🍆🥔🥕🌽🫑🥒🥬🥦🧄🧅🥜🫘🌰🫚🫛🍄🫜"

class Category(Enum):
    vegetables = 1
    bread = 2
    dry_goods = 3
    meat = 4
    fridge = 5
    
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


# get page IDs for all recipes from recipe datasource
def GetRecipePageIDs():
    url = f"https://api.notion.com/v1/data_sources/{os.environ['RECIPES_DATA_SOURCE']}/query"

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
        if not page["properties"]["enabled"]["checkbox"]:
            continue
        parsed_page = {
            "id": page["id"],
            "name": page["properties"]["Name"]["title"][0]["plain_text"],
            "can_double": page["properties"]["can_double"]["checkbox"], 
            "servings": page["properties"]["servings"]["number"]
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
            "unit": ing["properties"]["unit"]["select"]["name"],
            "category": Category[ing["properties"]["category"]["select"]["name"]] # so we can sort on this value
        }

        parsed_data.append(parsed_ing)

    return parsed_data

# get list of ingredients from recipe page
def GetIngredients(recipe):
    recipeDB = getIngredientsDB(recipe['id'])
    return getIngredientsList(recipeDB)

# write a page with content, title
def WritePage(pageContent, pageTitle):
    idx = randrange(len(EMOKI))
    emo = EMOKI[idx]

    print(idx, emo) # DEBUG

    url = "https://api.notion.com/v1/pages"

    payload = {
        "parent": {
            "page_id": f"{os.environ['SCHEDULES_DATA_SOURCE']}", # actual page
            "type": "page_id"
        },
        "properties": {
            "title": {
                "title": [{ "text": { "content": pageTitle } }]
                }
        },
          "icon": {
            "type": "emoji",
            "emoji": emo
        },
        "markdown": pageContent,
        "allow_async": True,
        "position": {
            "type": "after_block",
            "after_block": { "id": os.environ['SCHEDULES_BLOCK'] }
        },
        "template": { "type": "none" },
        "markdown_version": "v2"
    }
    headers = {
        "Notion-Version": "2026-03-11",
        "Authorization": f'Bearer {os.environ['NOTION_KEY']}',
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
