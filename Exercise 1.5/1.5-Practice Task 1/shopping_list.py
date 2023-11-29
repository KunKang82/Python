class ShoppingList(object):
  # Method to create a list
  def __init__(self, list_name):
    self.list_name = list_name
    self.shopping_list = []
  
  # Method to add an item to self.shopping_list only if the item isn't already there
  def add_item(self, item):
    self.item = item
    if (item in self.shopping_list):
      print('Item is already in the list')
    else:
      self.shopping_list.append(item)
      print("Item added to the list")
      
  # Method to remove an item from the list
  def remove_item(self, item):
    self.item = item
    if (item in self.shopping_list):
      self.shopping_list.remove(item)
      print("Item is removed from the list")
    else:
      print("Item is not in the list")
  
  # Prints the contents of self.shopping_list    
  def view_list(self):
    print(self.shopping_list)
    print("Items in the " + self.list_name )
    for item in self.shopping_list:
      print(item)
      
# Initialize a new list
pet_store_list = ShoppingList("Pet Store Shopping List")

# Add items to the shopping list
pet_store_list.add_item("dog food")
pet_store_list.add_item("frisbee")
pet_store_list.add_item("bowl")
pet_store_list.add_item("collars")
pet_store_list.add_item("flea collars")
  
# Remove flea collars using the remove_item() method
pet_store_list.remove_item("flea collars")
  
# Add frisbee again using the add_item() method
pet_store_list.add_item("frisbee")
  
# Display the entire shopping list through the view_list() method
pet_store_list.view_list()