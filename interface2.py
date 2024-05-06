import tkinter as tk
import numpy as np
from world import World_Creator

import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Heightmap Generator")
        self.master.geometry("500x500")

        # Scale X slider
        self.scale_x_label = tk.Label(self.master, text="Scale X")
        self.scale_x_label.grid(row=0, column=0)
        self.scale_x_slider = tk.Scale(self.master, from_=100, to=1000000,resolution=10, orient=tk.HORIZONTAL)
        self.scale_x_slider.grid(row=0, column=1)

        # Scale Y slider
        self.scale_y_label = tk.Label(self.master, text="Scale Y")
        self.scale_y_label.grid(row=1, column=0)
        self.scale_y_slider = tk.Scale(self.master, from_=100, to=1000000,resolution=10, orient=tk.HORIZONTAL)
        self.scale_y_slider.grid(row=1, column=1)

        # Initial shape randomness slider
        self.initial_shape_randomness_label = tk.Label(self.master, text="Initial Shape Randomness")
        self.initial_shape_randomness_label.grid(row=2, column=0)
        self.initial_shape_randomness_slider = tk.Scale(self.master, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL)
        self.initial_shape_randomness_slider.grid(row=2, column=1)

        # Smoothing slider
        self.smoothing_label = tk.Label(self.master, text="Smoothing")
        self.smoothing_label.grid(row=3, column=0)
        self.smoothing_slider = tk.Scale(self.master, from_=0, to=10, orient=tk.HORIZONTAL)
        self.smoothing_slider.grid(row=3, column=1)

        # Heightmap modifier intensity slider
        self.heightmap_modifier_intensity_label = tk.Label(self.master, text="Heightmap Modifier Intensity")
        self.heightmap_modifier_intensity_label.grid(row=4, column=0)
        self.heightmap_modifier_intensity_slider = tk.Scale(self.master, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL)
        self.heightmap_modifier_intensity_slider.grid(row=4, column=1)

        # Heightmap smoothing slider
        self.heightmap_smoothing_label = tk.Label(self.master, text="Heightmap Smoothing")
        self.heightmap_smoothing_label.grid(row=5, column=0)
        self.heightmap_smoothing_slider = tk.Scale(self.master, from_=0, to=10, orient=tk.HORIZONTAL)
        self.heightmap_smoothing_slider.grid(row=5, column=1)

        # Generate button
        self.generate_button = tk.Button(self.master, text="Generate", command=self.generate_heightmap)
        self.generate_button.grid(row=7, column=1)

        add_feature_button = tk.Button(self.master, text="Add Feature")
        add_feature_button.grid(row=6,column=1)

    def generate_heightmap(self):
        # Get slider values and generate heightmap
        scale_x = self.scale_x_slider.get()
        scale_y = self.scale_y_slider.get()
        initial_shape_randomness = self.initial_shape_randomness_slider.get()
        smoothing = self.smoothing_slider.get()
        heightmap_modifier_intensity = self.heightmap_modifier_intensity_slider.get()
        heightmap_smoothing = self.heightmap_smoothing_slider.get()

        # Call World class with slider values to generate heightmap
        # ...

root = tk.Tk()
app = Application(master=root)
app.mainloop()