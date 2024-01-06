class Parameters:
    """
    This classs contains all the simulation parameters.
    """

    ocean_width = 20
    ocean_height = 20
    occupacy_rate = 50
    predator_rate = 3
    prey_rate = 100 - predator_rate
    predator_energy = 4
    predator_gain_energy = 2
    predator_reproduction_time = 8
    prey_reproduction_time = 4
    simulation_speed = 500