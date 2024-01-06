from models.observability import UIObserver
from models.fishes import Shark
from models.parameters import Parameters
import tkinter as tk

class SimulationScreen(UIObserver):
    """
    This classs is responsible of the UI display
    """
    _root = tk.Tk()
    _tags = {}
    _should_run_simulation = False
    
    def __init__(self):
        super().__init__()

        self._root.title("Wa-Tor")
        self.action_reset = None
        self.action_start = None

        button = tk.Button(self._root, text="Reset", command=self.on_reset_click)
        button.grid(row=0, column=Parameters.ocean_width, sticky="ns") 

        button = tk.Button(self._root, text= "Play - Pause", command=self.on_start_click)
        button.grid(row=10, column=Parameters.ocean_width, sticky="ns")

        for i in range(Parameters.ocean_height):
            self._root.grid_rowconfigure(i, minsize=40)
        for i in range(Parameters.ocean_width):
            self._root.grid_columnconfigure(i, minsize=40)

    def on_reset_click(self):
        if self.action_reset is not None:
            self.clear_screen()
            self.action_reset()

    def on_start_click(self):
        self._should_run_simulation = not self._should_run_simulation
        self.run_simulation()

    def run_simulation(self):
        if self._should_run_simulation:
            if self.action_start is not None:
                self.action_start()
            self._root.after(Parameters.simulation_speed, self.run_simulation)

    def refresh_chronon(self, value):
        self._tags['chronon_stats'] = tk.Label(self._root, text=f"Chronon = {value}", font=("Arial Unicode MS", 20))
        self._tags['chronon_stats'].grid(row=1, column=Parameters.ocean_width, sticky="ns")

    def refresh_stats(self, values):
        nb_sharks, nb_tunas = values
        self._tags['sharks_stats'] = tk.Label(self._root, text=f"Sharks = {nb_sharks}", font=("Arial Unicode MS", 20))
        self._tags['sharks_stats'].grid(row=2, column=Parameters.ocean_width, sticky="ns")

        self._tags['tunas_stats'] = tk.Label(self._root, text=f"Tunas = {nb_tunas}", font=("Arial Unicode MS", 20))
        self._tags['tunas_stats'].grid(row=3, column=Parameters.ocean_width, sticky="ns") 

    def refresh_fishes(self, fishes):
        self.clear_screen()
        for fish in fishes:
            emoji = f"🦈" if isinstance(fish, Shark) else f"🐟"
            emoji_size = 25 if isinstance(fish, Shark) else 20
            label = tk.Label(self._root, text=emoji, font=("Arial Unicode MS", emoji_size))
            label.grid(row=fish.position[0], column=fish.position[1], sticky="nsew")

    def stop_simulation(self):
        self._should_run_simulation = False

    def clear_screen(self):
        for widget in self._root.winfo_children():
            if isinstance(widget, tk.Label) and widget not in self._tags.values():
                widget.destroy()
        
