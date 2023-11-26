import pickle

def display_recipe(recipe):
  print('Recipe name: ', recipe['name'])
  print('Cooking time(min): ', recipe['cooking_time'])
  print('Ingredients: ', ', '.join(recipe['ingredients']))
  print('Difficulty: ', recipe['difficulty'])
  
# Function to search ingredients
def search_ingredient(data):
  ingredients_list = data['all_ingredients']
  indexed_ingredients_list = list(enumerate(ingredients_list, 1))
  
  for ingredient in indexed_ingredients_list:
    print('No.', ingredient[0], '-', ingredient[1])
    
  try:
    chosen_num = int(input('Enter the corresponding number of your chosen ingredient: '))
    # -1 to adjust the pick for 0-based indexing
    index = chosen_num - 1
    ingredient_searched = ingredients_list[index].lower()
    
  except IndexError:
    print('The number you entered is not on the list.')
  except:
    print('An error occured while finding your ingredient.')
  else:
    # Iterate through the list of recipes in the data dictionary
    for recipe in data['recipes_list']:       
      # Convert each recipe ingredient to lowercase for case-insensitive comparison
      recipe_ingredients_lower = [ing.lower() for ing in recipe['ingredients']]

      if ingredient_searched in recipe_ingredients_lower:
        print('\nThe Following recipe includes the searched ingredient: ')
        print('------------------------------------------------------')
        display_recipe(recipe)
          
# Enter the file name
filename = (input('Enter the filename where you\'ve stored your recipes: '))
try:
  recipes_file = open(filename, 'rb')
  data = pickle.load(recipes_file)
  print("File loaded successfully!")
  
except FileNotFoundError:
  print('File doesn\'t exist in the current directory')
  data = {'recipes_list': [], 'all_ingredients': []}
  
except:
  print('An unexpected error occured')
  data = {'recipes_list': [], 'all_ingredients': []}

# Calls search_ingredient() while passing data into it as an argument
else:
  search_ingredient(data)
  recipes_file.close()