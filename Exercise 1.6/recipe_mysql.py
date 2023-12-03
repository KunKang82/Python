# Import the mysql.connector module
import mysql.connector

# Initialize a connection object called conn
conn = mysql.connector.connect(host='localhost', user='cf-python', passwd='password')

# Initialize a cursor object from conn
cursor = conn.cursor()

# Create a database called task_database
# and make sure it's the only database with this name on the server by using the EXISTS statement
cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

# Have script access my database with the USE statement
cursor.execute("USE task_database")

# Create a table called Recipes
cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(50),
  ingredients VARCHAR(255),
  cooking_time INT,
  difficulty VARCHAR(20)
  )''')

# Calculates the difficulty of the recipe 
def calculate_difficulty(cooking_time, ingredients):
    print("Number of Ingredients:", len(ingredients))
    
    if (cooking_time < 10) and (len(ingredients) < 4):
      difficulty_level = "Easy"
    elif (cooking_time < 10) and (len(ingredients) >= 4):
      difficulty_level = "Medium"
    elif (cooking_time >= 10) and (len(ingredients) < 4):
      difficulty_level = "Intermediate"
    elif (cooking_time >= 10) and (len(ingredients) >= 4):
      difficulty_level = "Hard"
    else:
      print("There was an error, please try again.")
      
    print("Difficulty level: ", difficulty_level)  
    return difficulty_level
  
# Create a new recipe
def create_recipe(conn, cursor):
  recipe_ingredients = []
  name = input("\nEnter the name of the recipe: ")
  print("You have entered: ", name, " for the Recipe name." )
  cooking_time = int(input("Enter the cooking time(min): "))
  print("You have entered: ", cooking_time, " for the cooking time." )
  ingredients_input = input("Enter the ingredients(each separated by a comma followed by a space): ")
  print("You have entered: " , ingredients_input, " for the ingredients." )
  
  # Split the input string into a list of ingredients
  recipe_ingredients = [ingredient.strip() for ingredient in ingredients_input.split(',')]
  
  difficulty = calculate_difficulty(cooking_time, recipe_ingredients)
  recipe_ingredients_str = ", ".join(recipe_ingredients)
  sql = 'INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)'
  val = (name, recipe_ingredients_str, cooking_time, difficulty)
  
  cursor.execute(sql, val)
  conn.commit()
  print("Recipe saved into the database successfully.")

# Search recipes based on ingredients
def search_recipe(conn, cursor):
  all_ingredients = []
  
  # Stores the entire list of ingredients available into results
  cursor.execute("SELECT ingredients FROM Recipes")
  results = cursor.fetchall()
  
  # Iterates through the results list and for each recipe ingredients tuple
  for recipe_ingredients_list in results:
    # Iterate through recipe ingredients tuple
    for recipe_ingredients in recipe_ingredients_list:
      # Split each recipe ingredients tuple
      recipe_ingredient_split = recipe_ingredients.split(", ")
      all_ingredients.extend(recipe_ingredient_split)
  
  # Remove all duplicates from the list    
  all_ingredients = list(dict.fromkeys(all_ingredients))
  
  # Shows the user all the available ingredients contained in all_ingredients
  all_ingredients_list = list(enumerate(all_ingredients))
  
  print("\nAll ingredients list:")
  
  for index, tup in enumerate(all_ingredients_list):
    print(str(tup[0]+1) + ". " + tup[1])
    
  try:
    # User to pick a number from the all_ingredients_list. 
    # This number is used as the index to retrieve the corresponding ingredient, which is then store into a variable called ingredient_searched
    ingredient_searched_nber = input("\nEnter the number corresponding to the ingredient you want to select from the above list: ")
    
    ingredient_searched_index = int(ingredient_searched_nber) - 1
    
    ingredient_searched = all_ingredients_list[ingredient_searched_index][1]
    
    print("\nYou selected the ingredient: ", ingredient_searched)
    
  except:
    print("An unexpected error occurred. Make sure to select a number from the list.")
    
  else:
    # Searches fro rows in the table that contain search_ingredient within the ingredients column
    print("\nThe recipe(s) below include(s) the selected ingredient: ")
    print("-------------------------------------------------------")
    
    # cursor.execute("SELECT * FROM Recipes WHERE ingredients LIKE %s", ('%' + ingredient_searched + '%'))
    cursor.execute("SELECT * FROM Recipes WHERE ingredients LIKE %s", ('%' + ingredient_searched + '%',))

    results_recipes_with_ingredient = cursor.fetchall()
    
    # Displays the data from each recipe found
    for row in results_recipes_with_ingredient:
      print("\nRecipe number: ", row[0])
      print("name: ", row[1])
      print("ingredients: ", row[2])
      print("cooking_time: ", row[3])
      print("difficulty: ", row[4])

# Update recipes    
def update_recipe(conn, cursor):
  # Display every recipe to the user to allow him to update the one he wants
  view_all_recipes(conn, cursor)
  
  # Asks the user to input the ID of the recipe he wants to update
  recipe_id_for_update = int(input("\nEnter the recipe number of the recipe you want to update: "))
  
  # Asks the user to input which column he wnats to update among name, cooking_time and ingredients
  column_for_update = str(input("\nEnter the data you want to update among 'name', 'cooking time' and 'ingredients': "))
  updated_value = (input("\nEnter the new value for the recipe: "))
  print("Choice: ", updated_value)
  
  if column_for_update == "name":
    cursor.execute("UPDATE Recipes SET name = %s WHERE id = %s", (updated_value, recipe_id_for_update))
    print("Updated!")
    
  elif column_for_update == "cooking time":
    cursor.execute("UPDATE Recipes SET cooking_time = %s WHERE id = %s", (updated_value, recipe_id_for_update))
    # As cooking_time was chagned, it is needed to recalculate the difficulty
    # At first we need to fetch the recipe parameters
    cursor.execute("SELECT * FROM Recipes WHERE id = %s", (recipe_id_for_update,))
    result_recipe_for_update = cursor.fetchall()
    
    name = result_recipe_for_update[0][1]
    recipe_ingredients = tuple(result_recipe_for_update[0][2].split(','))
    cooking_time = result_recipe_for_update[0][3]
    
    updated_difficulty = calculate_difficulty(cooking_time, recipe_ingredients)
    print("Updated difficulty: ", updated_difficulty)
    cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (updated_difficulty, recipe_id_for_update))
    print("Updated!")
    
  elif column_for_update == "ingredients":
    cursor.execute("UPDATE Recipes SET ingredients = %s WHERE id = %s", (updated_value, recipe_id_for_update))
    # As ingredients where changed, it is needed to recalculate the difficulty
    # At first we need to fetch the recipe parameters
    cursor.execute("SELECT * FROM Recipes WHERE id = %s", (recipe_id_for_update,))
    result_recipe_for_update = cursor.fetchall()
    
    print("Recipe update result: ", result_recipe_for_update)
    
    name = result_recipe_for_update[0][1]
    recipe_ingredients = tuple(result_recipe_for_update[0][2].split(','))
    cooking_time = result_recipe_for_update[0][3]
    difficulty = result_recipe_for_update[0][4]
    
    updated_difficulty = calculate_difficulty(cooking_time, recipe_ingredients)
    print("Updated diffculty: ", updated_difficulty)
    cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (updated_difficulty, recipe_id_for_update))
    print("Updated!")
    
  conn.commit()

def delete_recipe(conn, cursor):
  # Display every recipe to the user to allow him to delete the one he wants
  view_all_recipes(conn, cursor)
  
  ## Asks the user to input the recipe number to delete
  recipe_number_for_deletion = input("\nEnter the recipe number you want to delete: ")
  
  # Delete the corresponding recipe into result
  cursor.execute("DELETE FROM Recipes WHERE id = %s", (recipe_number_for_deletion,))
  
  # Reset the auto-increment counter to ensure consecutive IDs
  cursor.execute("ALTER TABLE Recipes AUTO_INCREMENT = 1") 
  
  # Commits changes made to the Recipes table
  conn.commit()
  print("\nRecipe successfully deleted from the database.")

def view_all_recipes(conn, cursor):
    # Retrieve all recipes from the database
    cursor.execute("SELECT * FROM Recipes")
    results = cursor.fetchall()

    # Check if there are any entries
    if not results:
        print("\nThere aren't any entries in the database.")
        return None

    print("\nAll recipes can be found below:")
    print("-------------------------------------------")

    # Loop through the list of recipes and display each recipe
    for row in results:
        recipe = Recipe(row[0], row[1], row[2], row[3], row[4])  # Assuming you have a Recipe class with appropriate __init__ method
        print(recipe.__str__())  # Assuming you have a __str__ method in your Recipe class

# Example Recipe class with __init__ and __str__ methods
class Recipe:
    def __init__(self, id, name, ingredients, cooking_time, difficulty):
        self.id = id
        self.name = name
        self.ingredients = ingredients
        self.cooking_time = cooking_time
        self.difficulty = difficulty

    def __str__(self):
        return f"\nRecipe number: {self.id}\nname: {self.name}\ningredients: {self.ingredients}\ncooking time: {self.cooking_time}\ndifficulty: {self.difficulty}"

# Usage of the view_all_recipes function
view_all_recipes(conn, cursor)


# Main menu that loops until the user types 'quit'
def main_menu(conn, cursor):
  choice = ""
  while (choice != "quit"):
    print("\nMain Menu:")
    print("\n======================================================")
    print("Pick a choice:")
    print("   1. Create a new recipe")
    print("   2. Search for a recipe by ingredient")
    print("   3. Update an existing recipe")
    print("   4. Delete a recipe")
    print("   5. View all recipes")
    print("   Type 'quit' to exit the program.")
    choice = input("\nYour choice: ")
    if choice == "1":
      create_recipe(conn, cursor)
    elif choice == "2":
      search_recipe(conn, cursor)
    elif choice == "3":
      update_recipe(conn, cursor)
    elif choice == "4":
      delete_recipe(conn, cursor)
    elif choice == "5":
      view_all_recipes(conn, cursor)

# Calls the main_menu() function
main_menu(conn, cursor)
print("Goodbye!\n")
  