from schedule import MakeSchedule, PrintSchedule, MakeShoppingList, PrintShoppingList
from dotenv import load_dotenv
from notion import EMOKI, WritePage, GetRecipePageIDs
from datetime import date

import requests


if __name__ == '__main__':
    load_dotenv()

    allRecipes = GetRecipePageIDs()

    schedule = MakeSchedule(10, allRecipes)
    body = PrintSchedule(schedule)

    shoppingList = MakeShoppingList(schedule["recipes"])

    body += PrintShoppingList(shoppingList)
    today = date.today()

    WritePage(body, f'{today}')

    # for idx in range(len(EMOKI)):
    #     print(EMOKI[idx])
    pass
