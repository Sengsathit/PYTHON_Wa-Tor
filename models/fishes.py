from .parameters import Parameters
import random

# Parent class 
class Fish():
    def __init__(self, position: tuple = (0,0)):
        super().__init__()
        self.position = position
        self.old_position = self.position
        self.can_reproduce = False
        self.has_moved = False

    def set_new_position(self, new_position):
        self.old_position = self.position
        self.position = new_position

    @property
    def north_neighboor_position(self):
        return ((self.pos_y - 1) % Parameters.ocean_height, self.pos_x)

    @property
    def south_neighboor_position(self):
        return ((self.pos_y + 1) % Parameters.ocean_height, self.pos_x)
    
    @property
    def east_neighboor_position(self):
        return (self.pos_y, (self.pos_x - 1) % Parameters.ocean_width)

    @property
    def west_neighboor_position(self):
        return (self.pos_y, (self.pos_x + 1) % Parameters.ocean_width)
    
    @property
    def pos_x(self):
        return self.position[1]

    @property
    def pos_y(self):
        return self.position[0]
    
    def get_neighbors(self, ecosystem):
        return {
                self.north_neighboor_position: ecosystem[self.north_neighboor_position],
                self.east_neighboor_position: ecosystem[self.east_neighboor_position],
                self.south_neighboor_position: ecosystem[self.south_neighboor_position],
                self.west_neighboor_position: ecosystem[self.west_neighboor_position]
        }

# Child class 
class Shark(Fish):
    def __init__(self, position):
        super().__init__(position)
        self.energy = Parameters.predator_energy

    def move(self, ecosystem):
        self.energy -= 1
        if self.energy <= 0:
            ecosystem[self.position] = None
            return
        
        neighbors = self.get_neighbors(ecosystem)
        tunas_positions = [position for position, neighboor in neighbors.items() if isinstance(neighboor, Tuna)]
        available_positions = [position for position, neighboor in neighbors.items() if neighboor is None]

        if len(tunas_positions) > 0:
            random_tuna_position = random.choice(tunas_positions)
            self.set_new_position(random_tuna_position)
            ecosystem[self.position] = self
            ecosystem[self.old_position] = None
            self.energy += Parameters.predator_gain_energy
            self.has_moved = True
        elif len(available_positions) > 0:
            random_available_position = random.choice(available_positions)
            self.set_new_position(random_available_position)
            ecosystem[self.position] = self
            ecosystem[self.old_position] = None
            self.has_moved = True



    def reproduce(self,chronon, ecosystem):
        if chronon % Parameters.predator_reproduction_time == 0 and self.has_moved:
            ecosystem[self.old_position] = Shark(self.old_position)

# Child class 
class Tuna(Fish):

    def move(self, ecosystem):
        neighbors = self.get_neighbors(ecosystem)
        available_positions = [position for position, neighboor in neighbors.items() if neighboor is None]
        if len(available_positions) > 0:
            random_available_position = random.choice(available_positions)
            self.set_new_position(random_available_position)
            ecosystem[self.position] = self
            ecosystem[self.old_position] = None
            self.has_moved = True
    
    def reproduce(self,chronon, ecosystem):
        if chronon % Parameters.prey_reproduction_time == 0 and self.has_moved:
            ecosystem[self.old_position] = Tuna(self.old_position)