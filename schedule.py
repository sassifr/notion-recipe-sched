import random
import notion
# from sortedcontainers import SortedDict

'''
recipe format:
[
    {
        "name": str,
        "servings": int,
        "can_double": bool,
        "category": int # see notion.py Category
    },
]
'''
# from list of recipes, create a random shorlist schedule (incl total servings)
def MakeSchedule(serv, recipes):
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

def PrintSchedule(schedule):
    ret = ""
    ret += ("### Recipes:\n")
    for r in schedule["recipes"]:
        ret += f"- {r['name']}\n"

    # print(ret) DEBUG
    return ret

# create shopping list from a list of recipes
def MakeShoppingList(recipes):

    shoppingList = dict()

    # for each recipe in scheudle
    for recipe in recipes:
        # get ingredients for recipe
        ingredientsList = notion.GetIngredients(recipe)

        doubled = False

        if "doubled" in recipe['name']:
            doubled = True

        # for each ingredient
        for ing in ingredientsList:
            # check if the ingredient is in the shopping list
            key = f"{ing['ingredient']}_{ing['unit']}"

            amnt = ing['amount']
            if doubled:
                amnt *= 2
            
            if key in shoppingList:
                # yes -> then add to the existing one
                newAmnt = shoppingList[key][1] + amnt
                shoppingList[key] = (ing["category"], newAmnt)
            else:
                shoppingList[key] = (ing["category"], amnt)

    return shoppingList

'''
shoppinglist:
{
    "ingredient_unit" : (category, amount (int)),
    ...
}
'''
def PrintShoppingList(shoppingList):  
    # creat a list that we will sort based on the category
    l = []
    ret = ""


    ret+= ("\n### Shopping List:\n")

    # to list add tuple(category [for sorting], print string)
    for key in shoppingList:
        ing, unit = key.split('_')
        amnt = shoppingList[key][1]
        cat = shoppingList[key][0]

        # don't print empty unit
        unit = "" if unit == "-" else unit

        l.append((cat,f"- [ ] {amnt} {unit} {ing}"))

    # sorts based on tuple (category, print string)
    l.sort()

    # also print headers for each category
    curr_category = l[0][0]
    ret +=(f"#### {curr_category.name}\n")

    for i in l:
        if i[0] != curr_category:
            curr_category = i[0]
            ret += (f"#### {curr_category.name}\n")

        ret += f'{i[1]}\n'

    # print(ret) # DEBUG
    return ret


