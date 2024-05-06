import numpy as np
import matplotlib.pyplot as plt
from noise import snoise2
import random

# Set the size of the heightmap
width = 200
height = 200

# Set the scale of the noise (affects the level of detail)
scale = 125.0

# Set a random seed for the noise generation
seed = random.randint(0, 1000000)
random.seed(seed)
np.random.seed(seed)

# Generate the heightmap using Perlin noise
heightmap = np.zeros((width, height))
for i in range(width):
    for j in range(height):
        heightmap[i][j] = snoise2(i/scale, j/scale, octaves=6, persistence=0.5, lacunarity=2.0, repeatx=1024, repeaty=1024, base=seed)

# Normalize the values to the range [0, 1]
heightmap = (heightmap - np.min(heightmap)) / (np.max(heightmap) - np.min(heightmap))

# Define color gradients based on elevation
colors = [
    (0, 0, 0.5),    # Deep water
    (0, 0, 1),       # Shallow water
    (0.8, 0.8, 0.2), # Beach
    (0.2, 0.8, 0.2), # Land
    (0.3, 0.2, 0.1), # Mountain (marron foncé)
    (1, 1, 1)        # Snow
]

# Interpolate colors based on elevation
def interpolate_color(value, color_map):
    value = max(0, min(1, value))
    index = int(value * (len(color_map) - 1))
    return np.array(color_map[index])

# Generate colored heightmap
colored_heightmap = np.zeros((width, height, 3))
for i in range(width):
    for j in range(height):
        colored_heightmap[i][j] = interpolate_color(heightmap[i][j], colors)

# Add a beach based on elevation threshold
beach_threshold = 0.2
beach_color = (0.8, 0.8, 0.2)  # Color for the beach

beach_mask = heightmap < beach_threshold
colored_heightmap[beach_mask] = beach_color

# Random Viking city names
viking_city_names = ["Asgard", "Valhalla", "Niflheim", "Midgard", "Jotunheim", "Helheim", "Svartalfheim", "Alfheim", "Vanaheim", "Muspelheim", "Yggdrasil", "Ragnarok", "Bifrost", "Fenrir", "Nidavellir"]

# Generate random city coordinates and names
num_cities = 10
city_coordinates = []
city_names = []

while len(city_coordinates) < num_cities:
    x, y = np.random.randint(0, width), np.random.randint(0, height)
    if not beach_mask[x, y]:  # Check if the city is not on the beach
        city_coordinates.append((x, y))
        city_names.append(random.choice(viking_city_names))
        # Add a light brown point under the city
        colored_heightmap[x, y] = (0.8, 0.6, 0.4)

# Add city names to the plot
for city_coord, city_name in zip(city_coordinates, city_names):
    plt.text(city_coord[1], city_coord[0], city_name, color='black', fontsize=13, ha='center', va='center', fontfamily='cursive')

# Display the colored heightmap in 2D
plt.imshow(colored_heightmap, origin='lower')
plt.title(f'2D Random Map (Seed: {seed})')
plt.show()
