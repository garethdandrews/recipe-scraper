# recipe-scraper

View example_recipe.json for an example recipe that the scraper pulls

PROJECT OBJECTIVE:
A RECIPE COMPARISON MACHINE LEARNING MODEL THAT TAKES A SET OF FOOD ITEMS AND FINDS A LIST
OF RECIPES THAT USE THOSE INGREDIENTS, SORTED BY MOST SUITABLE. ALSO ADD FILTERS TO SPECIFY 
THINGS LIKE CUISINE, SERVINGS, AND COOKING TIME.
USE DEEP LEARNING MODEL TO EXTRACT THE FOOD ITEMS FROM THE INGREDIENTS LIST.
USE KNN TO FIND THE SIMILARITY BETWEEN RECIPES.


AIM 1:
COLLECT A DATABASE OF RECIPES

- Scrape recipes from various sources and store in a common JSON structure
    - BBC Good Food 
    - Jamie Oliver
    - etc... 

- Store recipes to MongoDB collection as this is a very fast, unstructured database


AIM 2:
FIND THE CORE INGREDIENTS OF A RECIPE

- Process the ingredient lists of each recipe into a more machine friendly format
    e.g. '12 sausages' will be split into the quantity (12) and the food item (sausages)
    This becomes a little more difficult with items like
    '800g boneless and skinless chicken thighs, cut into bite-sized pieces'
    as we only want '800g' and 'chicken thighs'
    we can discard the instruction as this isnt necessary for this part


AIM 3:
CLASSIFY RECIPES INTO CUISINE BASED ON THEIR INGREDIENTS






###########################################################################################################################
References:
https://www.irjet.net/archives/V6/i3/IRJET-V6I328.pdf