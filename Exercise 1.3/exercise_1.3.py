recipes_list = []
ingredients_list = []

def take_recipe():
  name = input("Recipe name: ")
  cooking_time = int(input("Cooking time (min): "))
  ingredients = input("Ingredients for this recipe ")
  ingredients = ingredients.split(", ")
  recipe = { "Name": name,
            "Cooking_Time": cooking_time,
            "Ingredients": ingredients
            }
  return recipe

n = int(input("How many recipes would you like to enter?: "))

for i in range(n):
  recipe = take_recipe()
  for ingredient in recipe["Ingredients"]:
    if not ingredient in ingredients_list:
      ingredients_list.append(ingredient)
  recipes_list.append(recipe)
  
for recipe in recipes_list:
  if recipe["Cooking_Time"] < 10 and len(recipe["Ingredients"]) < 4:
    recipe["difficulty"] = "easy"
  elif recipe["Cooking_Time"] < 10 and len(recipe["Ingredients"]) >= 4:
    recipe["difficulty"] = "medium"
  elif recipe["Cooking_Time"] >= 10 and len(recipe["Ingredients"]) < 4:
    recipe["difficulty"] = "intermediate"
  elif recipe["Cooking_Time"] >= 10 and len(recipe["Ingredients"]) >= 4:
    recipe["difficulty"] = "hard"
    
  print("\nRecipe: ", recipe["Name"]) #Add \n before "Recipe"
  print("Cooking Time (min): ", recipe["Cooking_Time"])
  for ingredient in recipe["Ingredients"]:
    print(ingredient)
  print("Difficulty level: ", recipe["difficulty"])

def print_ingredients():
  ingredients_list.sort()  
  print("\nIngredients Available Across All Recipes\n----------------------------------------")
  for ingredient in ingredients_list:
    print(ingredient)
print_ingredients()

    