from schedule import MakeRandomSchedule, PrintSchedule, MakeShoppingList, PrintShoppingList, MakeScheduleFromList
from dotenv import load_dotenv
from notion import EMOKI, WritePage, GetRecipePageIDs
from datetime import date

import requests


if __name__ == '__main__':
    load_dotenv()

    allRecipes = GetRecipePageIDs()

    # schedule = MakeRandomSchedule(10, allRecipes)

    test = {
        "dal": True,
        "squashta": False
        }

    schedule = MakeScheduleFromList(allRecipes, test)

    body = PrintSchedule(schedule)

    shoppingList = MakeShoppingList(schedule["recipes"])

    body += PrintShoppingList(shoppingList)
    today = date.today()

    print(body)

    # WritePage(body, f'{today}')

    # for idx in range(len(EMOKI)):
    #     print(EMOKI[idx])
    pass
