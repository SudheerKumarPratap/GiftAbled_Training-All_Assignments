
class Player:
    def __init__(self, name):
        self.name = name
        self.bag = []

    def collect(self, item):
        if item in self.bag:
            print(f"{self.name} already has a {item} in the bag!")
        else:
            self.bag.append(item)
            print(f"{self.name} picked up a {item}.")

    def show_bag(self):
        if not self.bag:
            print(f"{self.name}'s bag is empty.")
        else:
            print(f"{self.name} is carrying: {', '.join(self.bag)}")


# 2. Place Class (Supports regular and locked places)
class Place:
    def __init__(self, name, description, required_item=None,item_inside=None):
        self.name = name
        self.description = description
        self.required_item = required_item
        self.item_inside= item_inside

    def visit(self, player):
        print(f"\n---------- {self.name.upper()} ---")
        if self.required_item and (self.required_item not in player.bag):
            print("Access Denied! This place is locked.")
            print(f"You need a '{self.required_item}' to enter in  bag.")
            return False
        
        if self.required_item:
            print(f"(You unlocked the entry using your {self.required_item}!)")
        print(self.description)
        #return True
        if self.item_inside:
            print(" then,Look!there is something here--- ")
            player.collect(self.item_inside)
            self.item_inside= None
        return True    

# 3. Chest Class
class Chest:
    def __init__(self, code, trophy_name="Golden Goblet"):
        """Initializes the chest with a specific code and the prize it holds inside."""
        self.code = code
        self.trophy_name = trophy_name
        self.is_opened = False

    def open(self, player):
        """Checks if the player has the correct code in their bag to claim the trophy."""
        print(f"\n--- Attempting to open the Mysterious Chest ---")
        
        if self.is_opened:
            print(f"The chest is already open and empty! You already claimed the {self.trophy_name}.")
            return True

        if self.code in player.bag:
            print(f" Click! The code '{self.code}' matched perfectly.")
            print(f"Success! Inside the chest, you found the legendary trophy: [{self.trophy_name}]!")
            self.is_opened = True
            player.collect(self.trophy_name)
            return True
        else:
            print(f" The chest stays tightly shut. You do not have the correct code ('{self.code}') in your bag.")
            return False

if __name__ == "__main__":
     p1 = Player("Mohan")
      
     cant=Place("Canteen",f"the dinning area, It is quite but something shiny catches {p1.name}'s eyes",item_inside = "key")
     lab= Place("Lab", "A high Tech Research Facility ", required_item= "key",  item_inside="code")
     stage=Place("stage", "a large  auditorium stage with  an old chest resting  right in the middle.")
     ch=Chest(code ="code",trophy_name="Golden_Global_hockey")

     print(" Starting Scenario-1: The failed Route---")
     p1.show_bag()
     stage.visit(p1) 
     ch.open(p1)
     p1.show_bag()
     lab.visit(p1)
     p1.show_bag()
     print("\n----- Resetting Scenario-2: The winning Route---")
     cant.visit(p1)
     lab.visit(p1)
     







    