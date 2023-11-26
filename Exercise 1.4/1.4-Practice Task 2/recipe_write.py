import pickle

recipe = {
  'Ingredient_Name': 'Tea',
  'Ingredients': ['Tea Leaves', 'Water', 'Sugar'],
  'Cooking_Time': 5,
  'Difficulty': 'Easy'
}

my_file = open('recipe_binary.bin', 'wb')
pickle.dump(recipe, my_file)
my_file.close()
