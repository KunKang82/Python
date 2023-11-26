# Imports pickle to work with binary files
import pickle

# Initializes two empty lists
recipes_list = []
all_ingredients= []

# Defines take_recipe function
def take_recipe():  
  # Asks the user to input recipe name, cooking time, and ingredients
  name = str(input("Enter the recipe name: "))
  cooking_time = int(input("Enter the cooking time(min): "))
  ingredients = str(input("Enter ingredients, each seperated by a comma: ")).split( ", ")
  
  # Calls the calc_difficulty() function to define the recipe level of difficulty
  difficulty = calc_difficulty(cooking_time, ingredients)
  
  # Creates and dictionary that stores recipe details
  recipe = {
    "name": name,
    "cooking_time": cooking_time,
    "ingredients": ingredients,
    "difficulty": difficulty,
  }
  return recipe

# Defines the recipe level of difficulty based on cooking time and number of ingredients
def calc_difficulty(cooking_time, ingredients):
  if cooking_time < 10 and len(ingredients) < 4:
    difficulty = "Easy"
  elif cooking_time < 10 and len(ingredients) >= 4:
    difficulty = "Medium"
  elif cooking_time >= 10 and len(ingredients) < 4:
    difficulty = "Intermediate"
  elif cooking_time >= 10 and len(ingredients) >= 4:
    difficulty = "Hard"
  return difficulty

# Asks user to enter a file name
filename = str(input("Enter a filename to save your recipes to: "))

# Attempts to open a binary file in read mode
try:
  file = open(filename, "rb")
  data = pickle.load(file)
  print("File loaded successfully!")
  
except FileNotFoundError:
  print("File doesn't exist. Creating a new file.")
  
  # Create a new dictionary
  data = {
    "recipes_list": [],
    "all_ingredients": []
  }

except:
  print("Unexpected error. Creating a new file.")
  
  # Creating a new dictionary
  data = {
    "recipes_list": [],
    "all_ingredients": []
  }

else:
  # Close the binary file
  file.close()

finally:
  # Extract the values from the dictionary into two separate lists
  recipes_list = data["recipes_list"]
  all_ingredients = data["all_ingredients"]

# Asks the user how many recipes they'd like to enter 
n = int(input("How many recipes would you like to enter?: "))

# For loop that calls the take_recipe() function
for i in range(n):
  recipe = take_recipe()
  print(recipe)
  
  # Inner loop that scans through the recipe’s ingredients and adds them to all_ingredients if they’re not already there
  for ingredient in recipe["ingredients"]:
    if ingredient not in all_ingredients:
      all_ingredients.append(ingredient)
  # Append the output    
  recipes_list.append(recipe)

# Gather the updated recipes_list and all_ingredients into the dictionary called data  
data = {"recipes_list": recipes_list, "all_ingredients": all_ingredients}

# Opens file and update with new data
updated_file = open(filename, "wb")
# Update
pickle.dump(data, updated_file)
# Close
updated_file.close()
print("Recipe file has been updated: " + str(data))