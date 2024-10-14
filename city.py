
from math import floor
from typing import Any


required_food = {
    1:7,
2:12,
3:16,
4:22,
5:27,
6:33,
7:38,
8:44,
9:50.5,
10:57,
11:63,
}

class Tile:
    def __init__(self, resource, yields):
        self.resource = resource
        self.yields = yields  # List of tuples (yield_type, yield_amount)
        
class Settler:
    def __init__(self, name, turn_to_settle = 4):
        self.turn_left_to_settle = turn_to_settle
        self.name = name
        self.settled = False
        
    def settle(self):
        assert self.turn_left_to_settle == 0
        self.settled = True
        self.city = City(self.name)
        
    def __call__(self) -> None:
        if self.settled:
            return self.city
        else: 
            print(f"Turn left to settle : {self.turn_left_to_settle}")
        
class City:
    def __init__(self, name, population=1, is_capital = False):
        self.name = name
        self.population = population
        self.tiles = []
        self.is_capital = is_capital
        self.total_resources = {"Food": 0, "Production": 0}  # Track total resources
        self.turn_ressources = {"Food": 0, "Production": 0}
        self.food_basket = 0

    def add_tile(self, tile):
        self.tiles.append(tile)

    def pass_turn(self):
        self.turn_ressources = {"Food": 0, "Production": 0}
        self.work_tiles()
        self.display_info()
        self.grow_population()
        
    def work_tiles(self):
        if self.population <= len(self.tiles) + 1:
            for i in range(self.population + 1): # Adding one for the city Center
                for yield_type, yield_amount in self.tiles[i].yields:
                    self.turn_ressources[yield_type] += yield_amount
                    self.total_resources[yield_type] += yield_amount
                    if yield_type == "Food":
                        self.food_basket += yield_amount
                # print(f"{self.name} is working the {self.tiles[i].resource}.")
            
            # Food consumed by population
            self.food_basket -= self.population*2
            # production given by Palace
            if self.is_capital:
                self.total_resources["Production"] += 2
                self.turn_ressources["Production"] += 2
        else:
            print(f"{self.name} doesn't have enough tiles for its population!")

    def grow_population(self):
        if self.food_basket >= (food_cost := required_food[self.population]):
            self.food_basket -= food_cost 
            self.population += 1

    def display_tiles(self):
        for i, tile in enumerate(self.tiles):
            yield_string = ", ".join([f"{yield_amount} {yield_type}" for yield_type, yield_amount in tile.yields])
            print(f"{i + 1}. {tile.resource} - {yield_string}")

    def display_info(self):
        total_resource_info = ", ".join([f"{yield_type}: {yield_amount}" for yield_type, yield_amount in self.total_resources.items()])
        turn_resource_info = ", ".join([f"{yield_type}: {yield_amount}" for yield_type, yield_amount in self.turn_ressources.items()])
        surplus = self.turn_ressources["Food"] - self.population*2
        food_left = required_food[self.population] - self.food_basket + surplus
        print(f"""{self.name} Population: {self.population}
              Turn Resources: {turn_resource_info}
              Total Food Surplus: {surplus}
              Food Before Growth: {food_left}
              Total Resources: {total_resource_info}""")

# Usage example:
if __name__ == "__main__":
    # Create some tile instances with multiple yields
    tile1 = Tile("Grassland Hill", [("Food", 2), ("Production", 2)])
    tile2 = Tile("Grassland Hill", [("Food", 3), ("Production", 1)])

    # Create a city
    my_city = City("MyCity", 1, True)

    # Add tiles to the city
    my_city.add_tile(tile1)
    my_city.add_tile(tile1)
    my_city.add_tile(tile2)
    my_city.add_tile(tile2)
    my_city.add_tile(tile1)
    my_city.add_tile(tile1)
    my_city.add_tile(tile1)
    my_city.add_tile(tile1)
    my_city.add_tile(tile1)

    for i in range(30):
        print(f"Turn {i+1}:")
        my_city.pass_turn()
