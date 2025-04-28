from .observability import UISubject
from .fishes import Fish, Shark, Tuna
from .parameters import Parameters
import random

class Ocean(UISubject):
    """
    This classs represents the ecosystem of the simulation.
    It follows the Singleton pattern
    """

    _instance = None
    _ecosystem = {}
    _chronon = 1

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Ocean, cls).__new__(cls)
            cls.empty_ecosystem(cls)
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    @property
    def existing_fishes(self) -> [Fish]:
        fishes = [fish_instance for _, fish_instance in self._ecosystem.items() if fish_instance is not None]
        return fishes
    
    @property
    def chronon(self):
        return self._chronon

    @chronon.setter
    def chronon(self, value):
        self._chronon = value
        self.notify_chronon(self._chronon)

    @property
    def existing_fishes(self) -> [Fish]:
        fishes = [fish_instance for _, fish_instance in self._ecosystem.items() if fish_instance is not None]
        return fishes

    def empty_ecosystem(self):
        self._ecosystem = {(x, y): None for x in range(Parameters.ocean_width) for y in range(Parameters.ocean_height)}

    def init_ecosystem(self):
        self.empty_ecosystem()

        self._chronon = 1
        
        fishes_max = (Parameters.ocean_width * Parameters.ocean_height) * Parameters.occupacy_rate / 100

        # Generate fishes
        nb_of_sharks = round((Parameters.predator_rate / 100) * fishes_max)
        nb_of_tunas = round((Parameters.prey_rate / 100) * fishes_max)
        self.generate_fishes(nb_of_sharks, nb_of_tunas)

        # Update UI
        self.notify_chronon(self._chronon)
        self.notify_stats(self.get_nb_of_fishes())
        self.notify_fishes(self.existing_fishes)

    def generate_fishes(self, max_sharks, max_tunas):
        sharks_count = 0
        tunas_count = 0
        while sharks_count < max_sharks or tunas_count < max_tunas:
            available_positions = [key for key, value in self._ecosystem.items() if value is None]
            random_position = random.choice(available_positions)

            randomChoice = random.choice([1,2])
            if randomChoice == 1 and sharks_count < max_sharks:
                self._ecosystem[random_position] = Shark(position=random_position)
                sharks_count += 1
            elif randomChoice == 2 and tunas_count < max_tunas:
                self._ecosystem[random_position] = Tuna(position=random_position)
                tunas_count += 1
    
    def get_nb_of_fishes(self) -> (int, int):
        nb_of_sharks = 0
        nb_of_tunas = 0
        for _, fish_instance in self._ecosystem.items():
            if isinstance(fish_instance, Shark):
                nb_of_sharks += 1
            elif isinstance(fish_instance, Tuna):
                nb_of_tunas += 1
        return nb_of_sharks, nb_of_tunas
        
    def move_fishes(self):
        # Stop simulation if the ecosystem is empty or completly full
        nb_exisiting_fishes = len(self.existing_fishes)
        should_end_simulation = nb_exisiting_fishes <= 0 or nb_exisiting_fishes >= (Parameters.ocean_width * Parameters.ocean_width) 
        
        if should_end_simulation:
            self.notify_end_simulation()
            return

        for i in range(Parameters.ocean_width):
            for j in range(Parameters.ocean_height):
                fish = self._ecosystem[(i,j)]
                if fish is not None and not fish.has_moved:
                    fish.move(self._ecosystem)
                    fish.reproduce(self._chronon, self._ecosystem)
            
        for fish in self.existing_fishes:
            fish.has_moved = False

        self.chronon += 1
        self.notify_fishes(self.existing_fishes)
        self.notify_stats(self.get_nb_of_fishes())
