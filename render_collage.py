from PIL import Image
import numpy as np
from categorize_images import SourceImage, SourceImagePalette, categorize_all_images
from extract_target_colors import extract_section_color
from color_matching import find_best_match



def render_collage(target_image: Image.Image,
                   palette: SourceImagePalette,
                   tile_size: int = 40,
                   method: str = "euclidean") -> Image.Image:

    # Crop to clean tile grid

    width, height = target_image.size

    width = (width // tile_size) * tile_size
    height = (height // tile_size) * tile_size

    target_image = target_image.crop((0, 0, width, height))



    mosaic = Image.new("RGB", (width, height))



    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            # Extract tile and compute average color

            tile = target_image.crop((x, y, x + tile_size, y + tile_size))
            average_color = extract_section_color(tile, 0, 0, tile_size, tile_size)

            # Use your existing matching function
            find_match = find_best_match(average_color, palette, "euclidean")

            # Load image from filepath
            src_img = Image.open(find_match.filepath).convert("RGB")

            # Resize to tile
            src_img = src_img.resize((tile_size, tile_size), Image.LANCZOS)
            mosaic.paste(src_img, (x, y))

    
    
    return mosaic

palette = categorize_all_images(
    image_directory="data/source_images",
    supported_formats=[".jpg", ".jpeg", ".png", ".webp"]
)
print("Loaded images:", len(palette))
target_image = Image.open("data/target_images/target_pic.png").convert("RGB")
collage = render_collage(target_image, palette, tile_size=15)
collage.save("collage.jpg")

# Render collage for all images in the dataset
