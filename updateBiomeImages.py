import os, json
from PIL import Image

source_dir = "./game_files/assets/images/arenas"
dest_dir = "./website/ui"

with open("local_files/my_json/allFilters.json", "r") as file:
    allFilters = json.load(file)
with open("local_files/my_json/fidThresholds.json", "r") as fp:
    fidThresholds = json.load(fp)
biomeNames = [filter[1].lower().replace(' ','_') for filter in allFilters if filter[0] == 'Biome']
thisFID = fidThresholds[8]-1

for thisBiome in biomeNames:

    background_filename = f"{thisBiome}_bg.png"
    thisFID += 1
    output_filename = f"biomes/{thisFID}.png"

    bg_path = os.path.join(source_dir, background_filename) # Load background image
    background = Image.open(bg_path).convert("RGBA")
    overlay_filenames = [ # Get overlay image paths
        f for f in os.listdir(source_dir) if f.startswith(f"{thisBiome}_b") and f.endswith(".png") and f != background_filename
    ]
    overlay_filenames.sort() # Sort for consistent layering

    # Paste each overlay image on top of the background
    for filename in overlay_filenames:
        # Open the image
        overlay_path = os.path.join(source_dir, filename)
        overlay = Image.open(overlay_path).convert("RGBA")
        bg_pos = [0, 0] # Where to paste the overlay image on the background

        # If json data exists, crop the image
        if os.path.isfile(f'{source_dir}/{filename[:-4]}.json'):
            with open(f'{source_dir}/{filename[:-4]}.json', "r") as f:
                json_data = json.load(f)
            frame_data = json_data['textures'][0]['frames'][0]
            bg_pos = [frame_data["spriteSourceSize"]["x"], frame_data["spriteSourceSize"]["y"]]
            crop_box = [val for val in frame_data["frame"].values()] # Get x, y, w, h
            crop_box[2] += crop_box[0] # Add w to x
            crop_box[3] += crop_box[1] # Add h to y
            overlay = overlay.crop(crop_box)

        # Overlay the image on the bg
        background.paste(overlay, bg_pos, overlay)

    background = background.crop((150, 20, 282, 110))
    background.save(os.path.join(dest_dir, output_filename))
    print(f"Composite image saved as: {output_filename}")