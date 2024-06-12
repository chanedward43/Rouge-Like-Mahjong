from PIL import Image
import os

# Load the base tile image
base_image = Image.open("tile2.png")

# Define the suits and special tiles
suits = ['bam', 'cir', 'cha']  # bamboo, circle, character
specials = ['east', 'south', 'west', 'north', 'white', 'green', 'red']

# Create the output directory if it doesn't exist
output_dir = "assets/tiles/"
os.makedirs(output_dir, exist_ok=True)

# Generate tile images for suits
for suit in suits:
    for value in range(1, 10):
        tile_name = f"{suit}_{value}.png"
        output_path = os.path.join(output_dir, tile_name)
        base_image.save(output_path)

# Generate tile images for special tiles
for special in specials:
    tile_name = f"special_{special}.png"
    output_path = os.path.join(output_dir, tile_name)
    base_image.save(output_path)

print("Tile images generated successfully!")
