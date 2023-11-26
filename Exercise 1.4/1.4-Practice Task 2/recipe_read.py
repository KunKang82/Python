import pickle

with open('recipe_binary.bin', 'rb') as my_file:
  recipe = pickle.load(my_file)

print("Recipe after unpickling:", recipe)  # Debugging line

print('\nRecipe Details:')
print('---------------')
print('Ingredient Name: ' + (recipe['Ingredient_Name']))
print('Ingredients: ')
for Ingredients in recipe ['Ingredients']:
  print(Ingredients)

print('Cooking Time: ' + str(recipe['Cooking_Time']))
print('Difficulty: ' + recipe['Difficulty'])