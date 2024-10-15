from base_cost import Costs
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
        
class Settler():
    def __init__(self, id, civ_manager, turn_to_settle = 4):
        self.civ_manager = civ_manager
        self.civ_manager.add_new_settler(self)
        self.turn_left_to_settle = turn_to_settle
        self.id = id
        self.settled = False
        
    def next_turn(self):
        self.turn_left_to_settle -= 1
        try: 
            self.settle() 
        except AssertionError: 
            return
        
    def settle(self):
        assert self.turn_left_to_settle == 0
        self.settled = True
        self.city = City(self.id, civ_manager = self.civ_manager)
        
    def __call__(self) -> None:
        if self.settled:
            return self.city
        else: 
            print(f"Turn left to settle : {self.turn_left_to_settle}")
        
class City():
    def __init__(self, id, civ_manager, population=1,  is_capital = False, production_stack=None, tiles=None):
        self.id = id
        self.civ_manager = civ_manager
        self.civ_manager.add_new_city(self)
        self.population = population
        self.is_capital = is_capital
        self.total_resources = {"Food": 0, "Production": 0}  # Track total resources
        self.turn_ressources = {"Food": 0, "Production": 0}
        
        if not production_stack:
            self.production_stack = [Costs.settler, Costs.settler, Costs.settler, Costs.settler, Costs.settler, Costs.scout, Costs.scout]
        else:
            self.production_stack = production_stack
            
        if not tiles:
            tile1 = Tile("Grassland Hill", [("Food", 2), ("Production", 2)])
            self.tiles = [tile1, tile1, tile1, tile1, tile1, tile1, tile1, tile1, tile1, tile1, tile1, tile1]
        else:
            self.tiles = tiles
            
        self.overflow = 0
        self.in_production = None
        self.food_basket = 0
        self.production = {}
        

    def add_tile(self, tile):
        self.tiles.append(tile)
        
    def pick_production(self):
        if not self.in_production:
            self.in_production =  [self.production_stack.pop(), self.overflow]
            x = self.civ_manager.n_settlers  # noqa: F841
            self.requ_prod = eval(self.in_production[0].value)
            self.overflow = 0

    def produce(self):        
        self.in_production[1] += self.turn_ressources["Production"]
        
        if self.in_production[1] >= self.requ_prod:
            self.overflow = (self.in_production[1] - self.requ_prod)
            if self.in_production[0].name == "settler":
                self.produce_settler()
            self.in_production = None
    
    def next_turn(self):
        self.turn_ressources = {"Food": 0, "Production": 0}
        self.work_tiles()
        self.pick_production()
        self.display_info()
        self.produce()
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
            print(f"{self.id} doesn't have enough tiles for its population!")

    def grow_population(self):
        if self.food_basket >= (food_cost := required_food[self.population]):
            self.food_basket -= food_cost 
            self.population += 1
    
    def produce_settler(self, *args):
        assert self.population > 1
        self.population -= 1
        self.grow_population()
        self.civ_manager.n_settlers += 1
        Settler(len(self.civ_manager.cities) + 1, self.civ_manager)   

    def display_tiles(self):
        for i, tile in enumerate(self.tiles):
            yield_string = ", ".join([f"{yield_amount} {yield_type}" for yield_type, yield_amount in tile.yields])
            print(f"{i + 1}. {tile.resource} - {yield_string}")

    def display_info(self):
        total_resource_info = ", ".join([f"{yield_type}: {yield_amount}" for yield_type, yield_amount in self.total_resources.items()])
        turn_resource_info = ", ".join([f"{yield_type}: {yield_amount}" for yield_type, yield_amount in self.turn_ressources.items()])
        surplus = self.turn_ressources["Food"] - self.population*2
        food_left = required_food[self.population] - self.food_basket + surplus
        print(f"""B_{self.id} Population: {self.population}
              Turn Resources: {turn_resource_info}
              Turn Overflow: {self.overflow}
              Total Food Surplus: {surplus}
              Food Before Growth: {food_left}
              Total Resources: {total_resource_info}
              Production: {self.in_production[0].name} ({self.in_production[1]}/{self.requ_prod})""")
