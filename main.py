from models.ocean import Ocean
from ui.simulation_screen import SimulationScreen

screen = SimulationScreen()

Ocean.get_instance().attach_observer(screen)
Ocean.get_instance().init_ecosystem()
screen.action_reset = Ocean.get_instance().init_ecosystem
screen.action_start = Ocean.get_instance().move_fishes

screen._root.mainloop()