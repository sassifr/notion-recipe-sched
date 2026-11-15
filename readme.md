# Weekly recipe scheduler 

borne out of my laziness to pick ts every week

tldr; creates a randomized recipe/shopping list for the week, in notion.

reads from notion db of recipes, each containing a db of ingredients. randomly selects unique recipes based on the number of servings requested, and produced a markdown formatted list of recipes and corresponding sorted shopping list, and writes to a new notion page

### how to use
must populate `.env` with 
- `NOTION_DATA_SOURCE` (database containing recipes)
- `NOTION_KEY` (notion key with read access to the aforementioned data source)
- `SCHEDULES_DATA_SOURCE` (parent page to write new shopping list to)
- `SCHEDULES_BLOCK` (block in parent page under which new shopping list will be added)

```bash
$ python main.py
```

