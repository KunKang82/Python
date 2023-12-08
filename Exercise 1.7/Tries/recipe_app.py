#recipe_app.py

# Import the create_engine function from SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import or_

# Connecting to database
engine = create_engine("mysql://cf-python:password@localhost/my_database")

# Bring in a function from SQLAlchemy that generates the declarative base class
from sqlalchemy.ext.declarative import declarative_base
# Generate the class from this function. Call this class Base
Base = declarative_base()

# Import the Column type
from sqlalchemy import Column
# Import Integer and String types
from sqlalchemy.types import Integer, String

# Declares new class
class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    # Add a __repr__ method to this class to help identify your objects easily from the terminal
    def __repr__(self):
      return "<Recipe ID: " + str(self.id) + "-" + self.name + ">"
      
    # Method to prting a well-formatted version of the recipes
    def __str__(self):
      output = ("\nID: " + str(self.id) +
              "\nName: " + str(self.name) +
              "\nCooking time (minutes): " + str(self.cooking_time) +
              "\nDifficulty: " + str(self.difficulty) +
              "\nIngredients: " + str(self.ingredients))
      return output


# Use the create_all() method in the base class to create tables of all the models that you’ve defined
Base.metadata.create_all(engine)

# To create a session on my database, start by importing a method called sessionmaker() from SQLAlchemy
from sqlalchemy.orm import sessionmaker

# Connecting Session class to the engine created earlier through a keyword argument called bind
Session = sessionmaker(bind=engine)

# Initialize the session object that I'll be using for the rest of my operations
session = Session()

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

# Return ingredients_as_list() function retrieves the ingredients string inside Recipe object as a list
def return_ingredients_as_list():
  # Assign all recipes to recipes_list
  recipes_list = session.query(Recipe).all()
  for recipe in recipes_list:
    print("Recipe: ", recipe)
    print("recipe.ingredients: ", recipe.ingredients)
    # Split the input string into a list of ingredients
    recipe_ingredients_list = recipe.ingredients.split(", ")
    print(recipe_ingredients_list)

def create_recipe():
    recipe_ingredients = []

    # Keep prompting the user until they enter a name < 50 with only alphabetical characters and numeric cooking time
    correct_input_name = False
    while not correct_input_name:
        # Asks the user to input recipe name
        name = input("\nEnter the name of the recipe: ")
        print("You have entered:", name, "for the Recipe name.")
        if len(name) < 50:
            correct_input_name = True
        else:
            print("Please enter a name that contains less than 50 characters.")

    # Asks the user to input cooking time
    correct_input_cooking_time = False
    while not correct_input_cooking_time:
        cooking_time_str = input("Enter the cooking time(min): ")
        print("You have entered:", cooking_time_str, "(min) for the cooking time.")
        if cooking_time_str.isnumeric():
            cooking_time = int(cooking_time_str)
            if cooking_time > 0:  # Check if it's a positive integer
                correct_input_cooking_time = True
            else:
                print("Please enter a positive number.")
        else:
            print("Please enter a valid number.")

    # Asks the user to enter the number of ingredients he wants to add then asks the user to input ingredients
    correct_input_number = False
    while not correct_input_number:
        ingredient_count = input("How many ingredients do you want to enter?: ")
        print("You have entered:", ingredient_count, "for the number of ingredients.")
        if ingredient_count.isnumeric():
            correct_input_number = True

            for _ in range(int(ingredient_count)):
                ingredient = input("Enter an ingredient: ")
                recipe_ingredients.append(ingredient)

        else:
            correct_input_number = False
            print("Please enter a positive number.")

    # Converts recipe_ingredients into comma-separated strings as MySQL doesn't fully support arrays
    recipe_ingredients_str = ", ".join(recipe_ingredients)
    print(recipe_ingredients_str)

    # Call calculate_difficulty() that calculates the difficulty of the recipe by taking in cooking_time and ingredients
    # as arguments, and returning one of the following strings: Easy, Medium, Intermediate, or Hard
    difficulty = calculate_difficulty(cooking_time, recipe_ingredients)

  
    recipe_entry = Recipe(
      name = name,
      cooking_time = int(cooking_time),
      ingredients = recipe_ingredients_str,
      difficulty = difficulty
    )
  
    print("You have entered:", recipe_entry)
    
    # Add the new recipe to the session
    session.add(recipe_entry)

    # Commit the changes to the database
    session.commit()

    # Print the ID after adding the recipe to the database
    print("Recipe successfully added to the database with ID:", recipe_entry.id)

def view_all_recipes():
  all_recipes = []
  all_recipes = session.query(Recipe).all()
  
  # If there aren't any entries, inform the user that there aren't any entries in your database
  if len(all_recipes) == 0:
    print("There is no recipe in the database.")
    return None
  
  # Else, print all the recipes entered in the database
  else:
    print("\nAll recipes can be found below: ")
    print("-"*40)
    
    for recipe in all_recipes:
      print(recipe)

def search_by_ingredients():
    # Check if your table has any entries. If there aren't any entries, notify the user, and exit the function.
    if session.query(Recipe).count() == 0:
        print("There is no recipe in the database.")
        return None

    # Retrieve only the values from the ingredients column of the table, and store them into a variable called results.
    results = session.query(Recipe.ingredients).all()

    # Initialize an empty list called all_ingredients.
    all_ingredients = [ingredient for recipe_ingredients_list in results for ingredient in recipe_ingredients_list[0].split(", ")]
    all_ingredients = list(set(all_ingredients))  # Remove duplicates

    # Shows the user all the available ingredients contained in all_ingredients
    all_ingredients_list = list(enumerate(all_ingredients, start=1))

    print("\nAll ingredients list:")
    print("-" * 25)

    for index, ingredient in all_ingredients_list:
        print(f"{index}. {ingredient}")

    try:
        # User to pick a number from all_ingredients_list.
        ingredient_searched_nber = input("""
Enter the numbers corresponding to the ingredients you want to select from the above list.
You can enter several numbers. In this case, numbers shall be separated by a space: """)

        # Create a list to identify the different ingredients user wants to search
        ingredients_nber_list_searched = ingredient_searched_nber.split(" ")

        # Validate user input
        if not all(1 <= int(n) <= len(all_ingredients_list) for n in ingredients_nber_list_searched):
            print("Invalid input. Please enter valid numbers.")
            return None

        ingredient_searched_list = [all_ingredients_list[int(n) - 1][1] for n in ingredients_nber_list_searched]

        print("\nYou selected the ingredient(s): ", ingredient_searched_list)

        # Initialize an empty list called conditions.
        conditions = [Recipe.ingredients.like(f"%{ingredient}%") for ingredient in ingredient_searched_list]

        # Combine all conditions using the OR operator
        search_condition = or_(*conditions)

        # Retrieve all recipes from the database using the filter() query, containing the combined conditions
        searched_recipes = session.query(Recipe).filter(search_condition).all()

        print(searched_recipes)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

        
def edit_recipe():
  # Check if your table has any entries. If there aren't any entries, notify the user, and exit the function.
  if session.query(Recipe).count() == 0:
    print("There is no recipe in the database.")
    return None
  
  else:
    # Retrieve only the values from the id and name columns of the table, and store them into a variable called results.
    results = session.query(Recipe).with_entities(Recipe.id, Recipe.name).all()
    print("List of available recipes:")
    for recipe in results:
      print("\nID: ", recipe[0])
      print("Name: ", recipe[1])
      
    # Asks the user to input the ID of the recipe he wants to edit
    recipe_id_for_edit = int(input("\nEnter the ID of the recipe you want to edit: "))
    
    print(session.query(Recipe).with_entities(Recipe.id).all())
    
    recipes_id_tup_list = session.query(
            Recipe).with_entities(Recipe.id).all()
    recipes_id_list = []
    
    for recipe_tup in recipes_id_tup_list:
      print(recipe_tup[0])
      recipes_id_list.append(recipe_tup[0])
      
    print(recipes_id_list)
    
    if recipe_id_for_edit not in recipes_id_list:
      print("Not in the ID list, please try again later.")
    else:
      print("Ok you can continue.")
      # Look for the object associated with the ID and retrieve it
      recipe_to_edit = session.query(Recipe).filter(Recipe.id == recipe_id_for_edit).one()
      
      print("\nWARNING: You are about to edit the following recipe: ")
      print(recipe_to_edit)
      
      # Asks the user to input which column he wants to update among name, cooking_time and ingredients
      column_for_update = int(input("\nEnter the number corresponding to the attribute you want to update:\n1. Name\n2. Cooking time\n3. Ingredients\nChoice: "))

      # Asks the user to input the new value
      updated_value = (input("\nEnter the new value for the recipe: "))
      print("Choice: ", updated_value)
      
      if column_for_update == 1: 
        print("You want to update the name of the recipe")
        session.query(Recipe).filter(Recipe.id == recipe_id_for_edit).update({Recipe.name: updated_value})
        session.commit()

      elif column_for_update == 2: 
        print("You want to update the cooking time of the recipe")
        session.query(Recipe).filter(Recipe.id == recipe_id_for_edit).update({Recipe.cooking_time: updated_value})
        session.commit()

      elif column_for_update == 3: 
        print("You want to update the ingredients of the recipe")
        session.query(Recipe).filter(Recipe.id == recipe_id_for_edit).update({Recipe.ingredients: updated_value})
        session.commit()
        
      else:
        print("Wrong input, please try again.")
        
      # Recalculate the difficulty
      updated_difficulty = calculate_difficulty(recipe_to_edit.cooking_time, recipe_to_edit.ingredients)
      print("Updated difficulty: ", updated_difficulty)
      
      # Assign the updated difficulty to edited recipe
      recipe_to_edit.difficulty = updated_difficulty
      
      # Commit changes to the database
      session.commit()
      print("Modification done.")
        
def delete_recipe():
  # Check if your table has any entries. If there aren't any entries, notify the user, and exit the function.
  if session.query(Recipe).count() == 0:
    print("There is no recipe in the database.")
    return None
  
  else:
    # Retrieve only the values from the id and name columns of the table, and store them into a variable called results.
    results = session.query(Recipe).with_entities(Recipe.id, Recipe.name).all()
    print("List of available recipes: ")
    for recipe in results:
      print("\nID: ", recipe[0])
      print("Name: ", recipe[1])
      
    # Asks the user to input the ID of the recipe he wants to delete
    recipe_id_for_deletion = input("\nEnter the ID of the recipe you want to delete: ")
    
    # Look for object associated with the ID and retrieve it
    recipe_to_be_deleted = session.query(Recipe).filter(Recipe.id == recipe_id_for_deletion).one()
    
    print("\nWARNING: you are about to delete the following recipe: ")
    print(recipe_to_be_deleted)
    
    # Confirm with the user he wants to delete this entry
    deletion_confirmed = input("\nPlease confirm you want to delete the entry above (y/n): ")
    if  deletion_confirmed == "y":
      # Delete the corresponding recipe into result
      session.delete(recipe_to_be_deleted)
      
      # Commits changes made to the final_recipes table
      session.commit()
      print("\nRecipe successfully deleted from the database.")
    
    else:
      return None
    
def main_menu()  :
  # Loops until the user decides to type "quit"
  choice = ""
  while(choice != "quit"):
    print("\n" + "=" * 50)
    print("\nMain Menu:")
    print("-"*15)
    print("Pick a choice:")
    print("\t1. Create a new recipe")
    print("\t2. Search for a recipe by ingredient")
    print("\t3. Edit an existing recipe")
    print("\t4. Delete a recipe")
    print("\t5. View all recipes")
    print("\n\tType 'quit' to exit the program.")
    choice = input("\nYour choice: ")
    print("\n" + "=" * 50)
    
    if choice == "1":
      create_recipe()
    elif choice == "2":
      search_by_ingredients()
    elif choice == "3":
      edit_recipe()
    elif choice == "4":
      delete_recipe()
    elif choice == "5":
      view_all_recipes()
    else:
      if choice == "quit":
        print("Bye!\n")
      else:
        print("WARNING... Wrong entry, please try again.")
        
# Calls the main_menu() function
main_menu()
session.close()
