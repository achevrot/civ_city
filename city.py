class Tile:
    def __init__(self, resource, yields):
        self.resource = resource
        self.yields = yields  # List of tuples (yield_type, yield_amount)

class City:
    def __init__(self, name, population):
        self.name = name
        self.population = population
        self.tiles = []
        self.resources = {"Food": 0, "Production": 0, "Gold": 0}  # Track total resources
        self.growth_threshold = 10  # Population increases when food reaches this threshold

    def add_tile(self, tile):
        self.tiles.append(tile)
        for yield_type, yield_amount in tile.yields:
            self.resources[yield_type] += yield_amount

    def work_tiles(self):
        if self.population <= len(self.tiles):
            for _ in range(self.population):
                tile_index = len(self.tiles) - self.population
                tile = self.tiles.pop(tile_index)
                for yield_type, yield_amount in tile.yields:
                    self.resources[yield_type] += yield_amount
                print(f"{self.name} is working the {tile.resource}.")
        else:
            print(f"{self.name} doesn't have enough tiles for its population!")

    def grow_population(self):
        if self.resources["Food"] >= self.growth_threshold:
            self.population += 1
            self.resources["Food"] -= self.growth_threshold
            self.growth_threshold = int(self.growth_threshold * 1.2)  # Increase the growth threshold for the next growth

    def display_tiles(self):
        for i, tile in enumerate(self.tiles):
            yield_string = ", ".join([f"{yield_amount} {yield_type}" for yield_type, yield_amount in tile.yields])
            print(f"{i + 1}. {tile.resource} - {yield_string}")

    def display_info(self):
        resource_info = ", ".join([f"{yield_type}: {yield_amount}" for yield_type, yield_amount in self.resources.items()])
        print(f"{self.name} (Population: {self.population}, Resources: {resource_info}, Growth Threshold: {self.growth_threshold})")

# Usage example:
if __name__ == "__main__":
    # Create some tile instances with multiple yields
    tile1 = Tile("Grassland Hill", [("Food", 2), ("Production", 1)])
    tile2 = Tile("Hill", [("Production", 2)])
    tile3 = Tile("River", [("Gold", 1)])

    # Create a city
    my_city = City("MyCity", 5)

    # Add tiles to the city
    my_city.add_tile(tile1)
    my_city.add_tile(tile2)
    my_city.add_tile(tile3)

    # Simulate working tiles
    my_city.work_tiles()

    # Display city information
    my_city.display_info()

    # Simulate population growth
    my_city.grow_population()
    my_city.display_info()
