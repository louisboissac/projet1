import numpy as np
from PIL import Image, ImageTk, ImageDraw
import noise
import tkinter as tk
from tkinter import ttk
import random

# Constants
IMAGE_SIZE = (900, 900)
SCALE = 50  # Adjust this to change the scale of the noise
OCTAVES = 6  # Number of octaves for Perlin noise
PERSISTENCE = 0.5  # Persistence parameter for Perlin noise
LACUNARITY = 2.0  # Lacunarity parameter for Perlin noise
ROAD_WIDTH = 3
DIRT_ROAD_DENSITY = 0.2
PRIMARY_ROAD_DENSITY = 0.2
SECONDARY_ROAD_DENSITY = 0.2


class TerrainGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Terrain Generator")

        self.scale_var = tk.DoubleVar(value=SCALE)
        self.octaves_var = tk.IntVar(value=OCTAVES)
        self.persistence_var = tk.DoubleVar(value=PERSISTENCE)
        self.lacunarity_var = tk.DoubleVar(value=LACUNARITY)
        self.water_threshold_var = tk.DoubleVar(value=-0.2)
        self.dark_grass_threshold_var = tk.DoubleVar(value=0.3)
        self.medium_grass_threshold_var = tk.DoubleVar(value=0.6)
        self.road_density_var = tk.DoubleVar(value=0.2)
        self.highway_spacing_var = tk.DoubleVar(value=50)  # Define highway spacing variable
        self.road_width_var = tk.IntVar(value=ROAD_WIDTH)
        self.dirt_road_density_var = tk.DoubleVar(value=DIRT_ROAD_DENSITY)
        self.primary_road_density_var = tk.DoubleVar(value=PRIMARY_ROAD_DENSITY)
        self.secondary_road_density_var = tk.DoubleVar(value=SECONDARY_ROAD_DENSITY)
        self.driveway_density_var = tk.DoubleVar(value=0.2)
        self.driveway_spacing_var = tk.DoubleVar(value=50)
        self.driveway_length_var = tk.IntVar(value=12)
        self.create_widgets()

    def create_widgets(self):
        # Scale slider
        scale_label = ttk.Label(self, text="Scale:")
        scale_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        scale_slider = ttk.Scale(self, from_=10, to=100, orient="horizontal", variable=self.scale_var)
        scale_slider.grid(row=0, column=1, padx=5, pady=5)

        # Octaves slider
        octaves_label = ttk.Label(self, text="Octaves:")
        octaves_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        octaves_slider = ttk.Scale(self, from_=1, to=10, orient="horizontal", variable=self.octaves_var)
        octaves_slider.grid(row=1, column=1, padx=5, pady=5)

        # Persistence slider
        persistence_label = ttk.Label(self, text="Persistence:")
        persistence_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        persistence_slider = ttk.Scale(self, from_=0, to=1, orient="horizontal", variable=self.persistence_var)
        persistence_slider.grid(row=2, column=1, padx=5, pady=5)

        # Lacunarity slider
        lacunarity_label = ttk.Label(self, text="Lacunarity:")
        lacunarity_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        lacunarity_slider = ttk.Scale(self, from_=1, to=4, orient="horizontal", variable=self.lacunarity_var)
        lacunarity_slider.grid(row=3, column=1, padx=5, pady=5)

        # Water threshold slider
        water_threshold_label = ttk.Label(self, text="Water Threshold:")
        water_threshold_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
        water_threshold_slider = ttk.Scale(self, from_=-1, to=1, orient="horizontal", variable=self.water_threshold_var)
        water_threshold_slider.grid(row=4, column=1, padx=5, pady=5)

        # Dark grass threshold slider
        dark_grass_threshold_label = ttk.Label(self, text="Dark Grass Threshold:")
        dark_grass_threshold_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
        dark_grass_threshold_slider = ttk.Scale(self, from_=-1, to=1, orient="horizontal",
                                                variable=self.dark_grass_threshold_var)
        dark_grass_threshold_slider.grid(row=5, column=1, padx=5, pady=5)

        # Medium grass threshold slider
        medium_grass_threshold_label = ttk.Label(self, text="Medium Grass Threshold:")
        medium_grass_threshold_label.grid(row=6, column=0, padx=5, pady=5, sticky="e")
        medium_grass_threshold_slider = ttk.Scale(self, from_=-1, to=1, orient="horizontal",
                                                  variable=self.medium_grass_threshold_var)
        medium_grass_threshold_slider.grid(row=6, column=1, padx=5, pady=5)

        # Seed entry
        seed_label = ttk.Label(self, text="Seed:")
        seed_label.grid(row=7, column=0, padx=5, pady=5, sticky="e")
        self.seed_entry = ttk.Entry(self)
        self.seed_entry.grid(row=7, column=1, padx=5, pady=5)

        # Generate button
        generate_button = ttk.Button(self, text="Generate", command=self.generate_terrain)
        generate_button.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

        # Image display for terrain
        self.image_label = ttk.Label(self)
        self.image_label.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

        # New label for vegetation map
        veg_label = ttk.Label(self, text="Vegetation Map")
        veg_label.grid(row=10, column=0, columnspan=2, padx=5, pady=5)

        # Image display for vegetation
        self.image_label_veg = ttk.Label(self)
        self.image_label_veg.grid(row=11, column=0, columnspan=2, padx=5, pady=5)

        # Road controls
        road_controls_label = ttk.Label(self, text="Road Controls")
        road_controls_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        # Road density slider
        road_density_label = ttk.Label(self, text="Density:")
        road_density_label.grid(row=1, column=2, padx=5, pady=5, sticky="e")
        road_density_slider = ttk.Scale(self, from_=0, to=1, orient="horizontal", variable=self.road_density_var)
        road_density_slider.grid(row=1, column=3, padx=5, pady=5)

        # Road width slider
        road_width_label = ttk.Label(self, text="Road Width:")
        road_width_label.grid(row=7, column=2, padx=5, pady=5, sticky="e")
        road_width_slider = ttk.Scale(self, from_=1, to=10, orient="horizontal", variable=self.road_width_var)
        road_width_slider.grid(row=7, column=3, padx=5, pady=5)

        # Dirt road density slider
        dirt_road_density_label = ttk.Label(self, text="Dirt Road Density:")
        dirt_road_density_label.grid(row=8, column=2, padx=5, pady=5, sticky="e")
        dirt_road_density_slider = ttk.Scale(self, from_=0, to=1, orient="horizontal",
                                             variable=self.dirt_road_density_var)
        dirt_road_density_slider.grid(row=8, column=3, padx=5, pady=5)

        # Primary road density slider
        primary_road_density_label = ttk.Label(self, text="Primary Road Density:")
        primary_road_density_label.grid(row=9, column=2, padx=5, pady=5, sticky="e")
        primary_road_density_slider = ttk.Scale(self, from_=0, to=1, orient="horizontal",
                                                variable=self.primary_road_density_var)
        primary_road_density_slider.grid(row=9, column=3, padx=5, pady=5)

        # Secondary road density slider
        secondary_road_density_label = ttk.Label(self, text="Secondary Road Density:")
        secondary_road_density_label.grid(row=10, column=2, padx=5, pady=5, sticky="e")
        secondary_road_density_slider = ttk.Scale(self, from_=0, to=1, orient="horizontal",
                                                  variable=self.secondary_road_density_var)
        secondary_road_density_slider.grid(row=10, column=3, padx=5, pady=5)

        # Highway spacing slider
        highway_spacing_label = ttk.Label(self, text="Highway Spacing:")
        highway_spacing_label.grid(row=4, column=2, padx=5, pady=5, sticky="e")
        highway_spacing_slider = ttk.Scale(self, from_=10, to=100, orient="horizontal",
                                           variable=self.highway_spacing_var)
        highway_spacing_slider.grid(row=4, column=3, padx=5, pady=5)

        # Driveway density slider
        driveway_density_label = ttk.Label(self, text="Driveway Density:")
        driveway_density_label.grid(row=11, column=2, padx=5, pady=5, sticky="e")
        driveway_density_slider = ttk.Scale(self, from_=0, to=1, orient="horizontal",
                                            variable=self.driveway_density_var)
        driveway_density_slider.grid(row=11, column=3, padx=5, pady=5)

        # Driveway spacing slider
        driveway_spacing_label = ttk.Label(self, text="Driveway Spacing:")
        driveway_spacing_label.grid(row=12, column=2, padx=5, pady=5, sticky="e")
        driveway_spacing_slider = ttk.Scale(self, from_=10, to=100, orient="horizontal",
                                            variable=self.driveway_spacing_var)
        driveway_spacing_slider.grid(row=12, column=3, padx=5, pady=5)

        # Driveway length slider
        driveway_length_label = ttk.Label(self, text="Driveway Length:")
        driveway_length_label.grid(row=13, column=2, padx=5, pady=5, sticky="e")
        driveway_length_slider = ttk.Scale(self, from_=8, to=16, orient="horizontal", variable=self.driveway_length_var)
        driveway_length_slider.grid(row=13, column=3, padx=5, pady=5)

    def display_image(self, image):
        # Create a new window to display the image
        image_window = tk.Toplevel(self.master)
        image_window.title("Terrain Image")

        # Display the image in a label
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(image_window, image=photo)
        label.image = photo
        label.pack()

    def display_image_vegetation(self, image):
        # Create a new window to display the image
        image_window = tk.Toplevel(self.master)
        image_window.title("Vegetation Image")

        # Display the image in a label
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(image_window, image=photo)
        label.image = photo
        label.pack()

    # Modify the generate_terrain method in TerrainGeneratorApp class to apply road mask to the vegetation map
    def generate_terrain(self):
        scale = self.scale_var.get()
        octaves = self.octaves_var.get()
        persistence = self.persistence_var.get()
        lacunarity = self.lacunarity_var.get()
        water_threshold = self.water_threshold_var.get()
        dark_grass_threshold = self.dark_grass_threshold_var.get()
        medium_grass_threshold = self.medium_grass_threshold_var.get()
        road_density = self.road_density_var.get()
        highway_spacing = self.highway_spacing_var.get()
        road_width = self.road_width_var.get()
        dirt_road_density = self.dirt_road_density_var.get()
        primary_road_density = self.primary_road_density_var.get()
        secondary_road_density = self.secondary_road_density_var.get()

        # New driveway variables
        driveway_density = self.driveway_density_var.get()
        driveway_spacing = self.driveway_spacing_var.get()
        driveway_length = self.driveway_length_var.get()

        # Get the seed value from the entry field
        seed_value = self.seed_entry.get()

        # Convert seed to integer if it's provided and valid
        try:
            seed_value = int(seed_value)
        except ValueError:
            # If invalid or empty, generate a random seed
            seed_value = None

        # Generate terrain map with the provided or random seed
        terrain_map, vegetation_map = generate_terrain_and_vegetation(IMAGE_SIZE[0], IMAGE_SIZE[1], scale, octaves,
                                                                      persistence, lacunarity,
                                                                      water_threshold, dark_grass_threshold,
                                                                      medium_grass_threshold, seed=seed_value)
        # Generate roads with new parameters
        terrain_map_with_roads = generate_roads(terrain_map, road_density, highway_spacing,
                                                road_width, dirt_road_density, primary_road_density,
                                                secondary_road_density,
                                                driveway_density, driveway_spacing, driveway_length)

        # Apply road mask to vegetation map
        vegetation_map = apply_road_mask(terrain_map_with_roads, vegetation_map)

        # Display the generated terrain map with roads
        self.display_image(terrain_map_with_roads)
        # Save the generated image
        output_file_path = "output.png"
        terrain_map_with_roads.save(output_file_path)

        # Display the generated vegetation map
        self.display_image_vegetation(vegetation_map)
        # Save the generated vegetation image
        output_veg_file_path = "output_veg.png"
        vegetation_map.save(output_veg_file_path)


def generate_perlin_noise(width, height, scale, octaves, persistence, lacunarity, seed):
    noise_map = np.zeros((width, height))
    for i in range(width):
        for j in range(height):
            noise_map[i][j] = noise.pnoise2(i / scale,
                                            j / scale,
                                            octaves=octaves,
                                            persistence=persistence,
                                            lacunarity=lacunarity,
                                            repeatx=width,
                                            repeaty=height,
                                            base=seed)  # Using the same seed for all points
    return noise_map


def generate_vegetation_map(width, height, scale, octaves, persistence, lacunarity,
                            water_threshold, dark_grass_threshold, medium_grass_threshold, seed=None):
    if seed is None:
        seed = random.randint(1, 10000)

    # Generate Perlin noise layers for vegetation
    vegetation_noise = generate_perlin_noise(width, height, scale, octaves, persistence, lacunarity, seed=seed + 1)

    # Normalize vegetation values
    vegetation_min = np.min(vegetation_noise)
    vegetation_max = np.max(vegetation_noise)
    vegetation_range = vegetation_max - vegetation_min
    normalized_vegetation = (vegetation_noise - vegetation_min) / vegetation_range

    # Create an empty image
    image = Image.new("RGB", (width, height))

    # Define color ranges for vegetation
    colors = [
        (0, 0, 0),  # None (Black)
        (0, 128, 0),  # Mainly grass, some trees
        (0, 255, 0)  # Light long grass
    ]

    # Generate vegetation based on noise layers
    for x in range(width):
        for y in range(height):
            vegetation_value = normalized_vegetation[x][y]

            # Assign color based on vegetation value
            if vegetation_value < 0.3:
                color = colors[0]  # None (Black)
            elif vegetation_value < 0.6:
                color = colors[1]  # Mainly grass, some trees
            else:
                color = colors[2]  # Light long grass

            # Set pixel color
            image.putpixel((x, y), color)

    return image


# Modify the generate_terrain_map function to return the terrain map
def generate_terrain_map(width, height, scale, octaves, persistence, lacunarity,
                         water_threshold, dark_grass_threshold, medium_grass_threshold, seed=None):
    if seed is None:
        seed = random.randint(1, 10000)

    # Generate Perlin noise layers
    terrain_noise = generate_perlin_noise(width, height, scale, octaves, persistence, lacunarity, seed)

    # Normalize terrain values
    terrain_min = np.min(terrain_noise)
    terrain_max = np.max(terrain_noise)
    terrain_range = terrain_max - terrain_min
    normalized_terrain = (terrain_noise - terrain_min) / terrain_range

    # Create an empty image
    image = Image.new("RGB", (width, height))

    # Define color ranges
    colors = [
        (0, 138, 255),  # Water
        (90, 100, 35),  # Dark grass
        (117, 117, 47),  # Medium grass
        (145, 135, 60)  # Light grass
    ]

    # Generate terrain based on noise layers
    for x in range(width):
        for y in range(height):
            terrain_value = normalized_terrain[x][y]

            # Assign color based on terrain value
            if terrain_value < water_threshold:
                color = colors[0]  # Water
            elif terrain_value < dark_grass_threshold:
                color = colors[1]  # Dark grass
            elif terrain_value < medium_grass_threshold:
                color = colors[2]  # Medium grass
            else:
                color = colors[3]  # Light grass

            # Set pixel color
            image.putpixel((x, y), color)

    return image, normalized_terrain  # Return the terrain map and normalized terrain values


def generate_terrain_and_vegetation(width, height, scale, octaves, persistence, lacunarity,
                                    water_threshold, dark_grass_threshold, medium_grass_threshold, seed=None):
    terrain_map, terrain_values = generate_terrain_map(width, height, scale, octaves, persistence, lacunarity,
                                                       water_threshold, dark_grass_threshold, medium_grass_threshold,
                                                       seed)
    vegetation_map = generate_vegetation_map(width, height, scale, octaves, persistence, lacunarity,
                                             water_threshold, dark_grass_threshold, medium_grass_threshold, seed)

    return terrain_map, vegetation_map


def generate_roads(terrain_map, density=0.2, highway_spacing=50, road_width=6,
                   dirt_road_density=0.2, primary_road_density=0.2, secondary_road_density=0.2,
                   driveway_density=0.2, driveway_spacing=50, driveway_length=12):
    draw = ImageDraw.Draw(terrain_map)
    width, height = terrain_map.size

    # Data structure to store road coordinates
    road_coordinates = set()

    # Generate dirt roads branching off from secondary roads
    for i in range(0, width, int(highway_spacing)):
        for j in range(0, height, int(highway_spacing)):
            if random.random() < dirt_road_density:
                start_x, start_y = i, j
                end_x = random.randint(0, width)
                end_y = random.randint(0, height)

                # Check if the proposed road segment intersects with existing roads
                if ((start_x, start_y, end_x, start_y) in road_coordinates) or \
                        ((end_x, start_y, end_x, end_y) in road_coordinates) or \
                        ((start_x, start_y, start_x, end_y) in road_coordinates) or \
                        ((start_x, end_y, end_x, end_y) in road_coordinates):
                    continue  # Skip this road segment if it intersects

                # Add the road coordinates to the data structure
                road_coordinates.add((start_x, start_y, start_x, end_y))
                road_coordinates.add((start_x, end_y, end_x, end_y))

                # Draw the road segment
                draw.line([(start_x, start_y), (start_x, end_y)], fill=(120, 70, 20), width=road_width)
                draw.line([(start_x, end_y), (end_x, end_y)], fill=(120, 70, 20), width=road_width)

                # Generate driveways
                if random.random() < driveway_density:
                    for k in range(start_y, end_y, int(driveway_spacing)):
                        driveway_start_x = start_x - road_width // 2  # Adjust for the road width
                        driveway_end_x = start_x + road_width // 2  # Adjust for the road width
                        draw.line([(driveway_start_x, k), (driveway_end_x, k)], fill=(120, 70, 20), width=road_width)

    # Generate secondary roads branching off from primary roads
    for i in range(0, width, int(highway_spacing)):
        for j in range(0, height, int(highway_spacing)):
            if random.random() < secondary_road_density:
                start_x, start_y = i, j
                end_x = random.randint(0, width)
                end_y = random.randint(0, height)

                # Check if the proposed road segment intersects with existing roads
                if ((start_x, start_y, end_x, start_y) in road_coordinates) or \
                        ((end_x, start_y, end_x, end_y) in road_coordinates):
                    continue  # Skip this road segment if it intersects

                # Add the road coordinates to the data structure
                road_coordinates.add((start_x, start_y, start_x, end_y))
                road_coordinates.add((start_x, end_y, end_x, end_y))

                # Draw the road segment
                draw.line([(start_x, start_y), (start_x, end_y)], fill=(165, 160, 140), width=road_width)
                draw.line([(start_x, end_y), (end_x, end_y)], fill=(165, 160, 140), width=road_width)

                # Generate driveways
                if random.random() < driveway_density:
                    for k in range(start_x, end_x, int(driveway_spacing)):
                        driveway_start_y = start_y - road_width // 2  # Adjust for the road width
                        driveway_end_y = start_y + road_width // 2  # Adjust for the road width
                        draw.line([(k, driveway_start_y), (k, driveway_end_y)], fill=(165, 160, 140), width=road_width)

    # Generate primary roads branching off from highways
    for i in range(0, width, int(highway_spacing)):
        for j in range(0, height, int(highway_spacing)):
            if random.random() < primary_road_density:
                start_x, start_y = i, j
                end_x = random.randint(0, width)
                end_y = random.randint(0, height)

                # Check if the proposed road segment intersects with existing roads
                if ((start_x, start_y, end_x, start_y) in road_coordinates) or \
                        ((end_x, start_y, end_x, end_y) in road_coordinates):
                    continue  # Skip this road segment if it intersects

                # Add the road coordinates to the data structure
                road_coordinates.add((start_x, start_y, start_x, end_y))
                road_coordinates.add((start_x, end_y, end_x, end_y))

                # Draw the road segment
                draw.line([(start_x, start_y), (start_x, end_y)], fill=(120, 120, 120), width=road_width)
                draw.line([(start_x, end_y), (end_x, end_y)], fill=(120, 120, 120), width=road_width)

    # Generate highways
    for i in range(0, width, int(highway_spacing)):
        for j in range(0, height, int(highway_spacing)):
            if random.random() < density:
                start_x, start_y = i, j
                end_x = random.randint(0, width)
                end_y = random.randint(0, height)

                # Check if the proposed road segment intersects with existing roads
                if ((start_x, start_y, end_x, start_y) in road_coordinates) or \
                        ((end_x, start_y, end_x, end_y) in road_coordinates):
                    continue  # Skip this road segment if it intersects

                # Add the road coordinates to the data structure
                road_coordinates.add((start_x, start_y, end_x, start_y))
                road_coordinates.add((end_x, start_y, end_x, end_y))

                # Draw the road segment
                draw.line([(start_x, start_y), (end_x, start_y)], fill=(100, 100, 100), width=road_width)
                draw.line([(end_x, start_y), (end_x, end_y)], fill=(100, 100, 100), width=road_width)

    return terrain_map


def apply_road_mask(terrain_map_with_roads, vegetation_map):
    # Convert terrain map with roads to numpy array for efficient pixel access
    terrain_array = np.array(terrain_map_with_roads)

    # Define road colors with tolerance for matching
    road_colors = [
        ((120, 70, 20), 20),  # Dirt (with a tolerance of 20 for each channel)
        ((165, 160, 140), 20),  # Light Asphalt
        ((100, 100, 100), 20),  # Dark Asphalt (main roads)
        ((120, 120, 120), 20)  # Medium Asphalt
    ]

    # Iterate over each pixel in the terrain image
    for x in range(terrain_array.shape[1]):  # Iterate over the second dimension first
        for y in range(terrain_array.shape[0]):  # Then iterate over the first dimension
            # Check if the pixel color is close enough to any road color
            for road_color, tolerance in road_colors:
                if np.all(np.abs(terrain_array[y, x] - road_color) <= tolerance):  # Note the swap in x and y
                    # Set the corresponding pixel in the vegetation image to black
                    vegetation_map.putpixel((x, y), (0, 0, 0))  # Black color
                    break  # Stop iterating over road colors once a match is found

    return vegetation_map


if __name__ == "__main__":
    app = TerrainGeneratorApp()
    app.mainloop()