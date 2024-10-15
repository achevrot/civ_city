from city import City, Tile, Settler


class CivManager() :
    
    cities: list[City] = ['']
    n_settlers = 1
    
    def __init__(self, civ_name = "Maya"):
        
        City(1, civ_manager = self, is_capital=True)
        self.current_turn : int = 0
    
    def pass_turn(self):
        self.current_turn += 1
        for city in self.cities:
            city.next_turn()
            
    def add_new_city(self, city: City):
        self.cities[city.id - 1] = city
    
    def get_total_population(self):
        total_pop = 0
        for city in self.cities:
            if isinstance(city, City):
                total_pop += city.population
        return total_pop
    
            
    def get_capital(self):
        return self.cities[0]
        
    def add_new_settler(self, settler: Settler):
        self.cities.append(settler)
        
# Usage example:
if __name__ == "__main__":
    # Create some tile instances with multiple yields
    tile1 = Tile("Grassland Hill", [("Food", 2), ("Production", 2)])
    tile2 = Tile("Grassland Hill", [("Food", 2), ("Production", 2)])
    tile3 = Tile("Grassland Hill", [("Food", 4), ("Production", 2)])

    # Create a city
    CM = CivManager()

    i = 1
    while(i <= 30):
        print(f"Turn {i}:")
        CM.pass_turn()
        input()
        i += 1
    print(CM.get_total_population())