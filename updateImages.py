# ======================== Image Updating Script ===========================
# ========================= Written by Sandstorm ===========================
# It assembles all the shiny pokemon, and warns of any palette swap issues
# This script will take ~2 minutes to run all images (depending on your CPU)

source_dir = "game_files/assets/images/pokemon"
# The official files from github must be in "game_files" folder, in same directory as this script
# That folder will be created when you run updateGameFiles.py

dest_dir = "website/images"
# Where to put all the processed images

# =============================== Options ==================================

overrideSpriteList = ['']
# Specify a subset of images, rather than running the entire list
# Each entry must be a string, like this: overrideSpriteList = ['692','3-mega']
# Leave blank to run all the images that are found in source_dir

warnMissingColors = 0
# Warns if at least x different colors listed in the json are NOT found in the image
# This helps find redundant or incorrect entries in the json
# Set to 0 to ignore this check, or set to 1 to report all missing colors

warnSimilarColors = 0
# Warns if colors exist that are less than x bits different on all channels (R/G/B)
# This was important when 'fuzzy color matching' was in the game, however, it is no longer relevant
# Set to 0 to ignore this check

warnPureBlackJson = 0
# Warns if pure black is found on a json
# Set to 0 to ignore this check

closeToBlackThreshold = 16
# Warns of colors that are less than x on all channels (R/G/B)
# To ignore this check, set this to 0, or set warnPureBlackJson to 0

warnIdenticalColors = 1
# Warns if a color is listed more than once in the json
# Set to 0 to ignore this check

warnVariantDimensions = 1
# Warns if variants of the same pokemon have different dimensions
# This usually happens if the animations are packed differently, not a big problem

# Since there is no official static frame, one must be chosen
# By default, it chooses the most common frame of the animation 
# However, you can override here to choose a specific frame
overrideFrame = {
    '4':-1,
    '12':0,
    '49':0,
    '68':0,
    '781':99, # Dhelmise at (574,243)
    '890':-8,
}

# ===================== Do not touch below this line =======================

import os, json
import numpy as np
from PIL import Image

# Function to convert hex to RGBA
def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip("#") # Remove '#' if present
    hex_code = hex_code[:6]
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def getBestFrame(thisImgPath, altJsonPath=''):
    # This looks at all the frames in the animation sheet, and crops to the most common one
    thisImage = Image.open(f'{thisImgPath}.png')
    if not os.path.isfile(f'{thisImgPath}.json'): # If there is no specific json
        thisImgPath = altJsonPath
    if not os.path.isfile(f'{thisImgPath}.json'): # If there is no default json
        input('***** Error: Could not find any JSON file for',thisImgPath)
    with open(f'{thisImgPath}.json', "r") as f:
        jsonLoad = json.load(f)
    if 'textures' in jsonLoad:
        allFrames = jsonLoad['textures'][0]['frames']
    else:
        allFrames = jsonLoad['frames']

    if (isinstance(allFrames, list)):    
        indFrames = [list(line['frame'].values()) for line in allFrames] # Each frame [x,y,w,h]
    else:
        indFrames = [list(line['frame'].values()) for line in allFrames.values()] # Each frame [x,y,w,h]
    
    # If the pokemon has an override frame, only use that frame
    if thisImgPath.split('/')[-1] in overrideFrame:
        if abs(overrideFrame[thisImgPath.split('/')[-1]]) <= len(indFrames):
            indFrames = [indFrames[overrideFrame[thisImgPath.split('/')[-1]]]]

    # Count how many times each frame occurs
    frameCount = [sum([lineA==lineB for lineB in indFrames]) for lineA in indFrames]
    x,y,w,h = indFrames[np.argmax(frameCount)] # Choose the first most common frame
    return thisImage.crop((x, y, x+w, y+h))

# Function to do palette swap
def palette_swap(image, json_path, tier):
    if not os.path.isfile(json_path):
        return None
    with open(json_path, "r") as f:
        data = json.load(f)
    tier_key = str(tier - 1)
    if tier_key not in data:
        return None
    hexDict = data[tier_key]
    rgb2rgbDict = {hex_to_rgb(key): hex_to_rgb(hexDict[key]) for key in hexDict}

    # Check for similar color keys
    if warnSimilarColors or warnPureBlackJson:
        for index, color in enumerate(rgb2rgbDict.keys()):
            if warnPureBlackJson:
                if color == (0,0,0):
                    print(f"Pure black found in: {json_path.split('/')[-1]}")
                elif all(col <= closeToBlackThreshold for col in color):
                    print(f"Near black color {color} found in: {json_path.split('/')[-1]}")
            if warnSimilarColors:
                for index2, color2 in enumerate(rgb2rgbDict.keys()):
                    if color != color2 and index2 > index:
                        diff = [abs(color[i] - color2[i]) <= warnSimilarColors for i in [0,1,2]]
                        if all(diff):
                            print('Similar colors:', color, color2, 'in', json_path.split('/')[-1])
            if warnIdenticalColors:
                for index2, color2 in enumerate(rgb2rgbDict.keys()):
                    if color == color2 and index2 > index:
                        print('Identical colors:', color, color2, 'in', json_path.split('/')[-1])

    # Access the palette (returns a flat list of RGB triples)
    palette = image.getpalette() # length is 256*3 internally

    # Modify the first few colors (used colors)
    usedColors = {}
    for i in range(0,len(palette),3):
        key = tuple(palette[i:i+3])
        if key in rgb2rgbDict:
            palette[i:i+3] = rgb2rgbDict[key]
            usedColors[key] = True
    
    # Check for colors in the JSON that are not in the image
    if warnMissingColors:
        missingColorReport = []
        for key in rgb2rgbDict.keys():
            if key not in usedColors:
                missingColorReport.append(f"Missing color: {key} in {json_path.split('/')[-1]}")
        if len(missingColorReport) >= warnMissingColors:
            for line in missingColorReport:
                print(line)

    # Apply the modified palette back
    image.putpalette(palette)
    return image

def addPartnerHeart(img): # Adds a heart image onto the partner pokemon image
    # Expand the original image width, more for eevee
    widthAdd = 5+10*(img.width < 40) 
    new_size = (img.width + widthAdd, img.height)
    expanded_image = Image.new("RGBA", new_size, (0, 0, 0, 0))
    expanded_image.paste(img, (0, 0))
    # Open the second image to paste
    overlay_image = Image.open("website/ui/partnerheart.png")
    overlay_pos = (new_size[0] - overlay_image.width, new_size[1] - overlay_image.height)
    # Create a temporary layer for blending
    temp_layer = Image.new("RGBA", expanded_image.size, (0, 0, 0, 0))  # Transparent layer
    temp_layer.paste(overlay_image, overlay_pos)  # Paste the image onto the temp layer
    expanded_image = Image.alpha_composite(expanded_image, temp_layer)
    return expanded_image

def convert_to_exact_palette(img: Image.Image) -> Image.Image:
    """
    Convert an RGBA/RGB image into P mode with an exact palette.
    Preserves all unique colors, avoids quantization shifts.
    """

    # Ensure RGBA
    arr = np.array(img.convert("RGBA"))
    h, w, _ = arr.shape
    pixels = arr.reshape(-1, 4)
    for i in range(len(pixels)): # Make transparent pixels actually zero
        if pixels[i][3] == 0:
            pixels[i][:3] = np.array([0,0,0])

    # Collect unique colors
    unique_colors = np.unique(pixels, axis=0)
    if len(unique_colors) > 256:
        raise ValueError(f"Too many colors ({len(unique_colors)}). Cannot fit into P-mode (max 256).")
    for col in unique_colors:
        if col[3] == 0 and any(x != 0 for x in col):
            print("Fully transparent color found other than (0,0,0)")

    # Build palette (R,G,B only)
    palette = [x for row in unique_colors for x in row[:3]]

    # Pad palette to 256 entries (768 values) (doesn't affect file size)
    while len(palette) < 768:
        palette.extend([0, 0, 0])

    # Create P image
    p_img = Image.new("P", (w, h))
    p_img.putpalette(palette)

    # Map colors to indices
    color_to_index = {tuple(rgba): idx for idx, rgba in enumerate(unique_colors)}
    indices = np.array([color_to_index[tuple(rgba)] for rgba in pixels], dtype=np.uint8)
    indices = indices.reshape(h, w)
    p_img.putdata(indices.flatten())

    # Handle transparency
    if (0, 0, 0, 0) in color_to_index:
        p_img.info['transparency'] = color_to_index[(0, 0, 0, 0)]

    return p_img

def processImage(spriteIndex, shinyIndex, femIndex, backIndex):
    # Priority in paths is variant > back > shiny > female
    thisPath = source_dir
    if shinyIndex > 1:  thisPath = f'{thisPath}/variant'
    if backIndex == 1:  thisPath = f'{thisPath}/back'
    if shinyIndex == 1: thisPath = f'{thisPath}/shiny'
    femExt = '/female' if femIndex else ''
    backExt = '/back' if backIndex else ''
    thisPath = f'{thisPath}{femExt}/{spriteIndex}' # Standard image path
    varPath = f'{source_dir}/variant{backExt}{femExt}/{spriteIndex}' # Palette swap image path
    defPath = f'{source_dir}{backExt}{femExt}/{spriteIndex}' # Fallback image path
    simpleName = f'{spriteIndex}_{shinyIndex}{femExt}{backExt}'.replace('/female','f').replace('/back','b')
    savePath = f'{dest_dir}/{simpleName}' # Name for SearchDex

    kind = 0 # Read the master list, to know which kind of image to look for in the game files
    masterListPart = masterList
    if backIndex: masterListPart = masterListPart['back']
    if femIndex:  masterListPart = masterListPart['female']
    if shinyIndex and spriteIndex in masterListPart:
        kind = masterListPart[spriteIndex][shinyIndex-1]

    sliced_img = None
    if shinyIndex and os.path.isfile(f'{varPath}_{shinyIndex}.png') and kind == 2: # Check for custom shiny first
        sliced_img = getBestFrame(f'{varPath}_{shinyIndex}',defPath)
    elif shinyIndex and os.path.isfile(f'{varPath}.json') and kind == 1: # Check for palette swap (sometimes even T1)
        sliced_img = getBestFrame(defPath)
        if sliced_img.mode != 'P':
            sliced_img = convert_to_exact_palette(sliced_img)
        sliced_img = palette_swap(sliced_img, f'{varPath}.json', shinyIndex)
    if not sliced_img and os.path.isfile(f'{thisPath}.png') and kind == 0: # If not custom, use official shiny
        sliced_img = getBestFrame(thisPath,defPath)
    if not sliced_img:
        if shinyIndex < 2 and femIndex == 0: # If it should exist, show an error
            print('Could not find image for',simpleName)
        return # Stop if there is no image

    if 'partner' in spriteIndex:
        sliced_img = addPartnerHeart(sliced_img) # Add partner heart to pika and eevee

    # Crop to a bounding box of solid pixels
    pixels = np.array(sliced_img)
    if sliced_img.mode == 'P':
        for x in range(len(pixels)):
            for y in range(len(pixels[x])):
                pixels[x][y] = (pixels[x][y] != sliced_img.info['transparency'])
    sliced_img = sliced_img.crop(Image.fromarray(pixels, mode=sliced_img.mode).getbbox())

    # Strip the color profile to save space (it is useless for pixel art)
    sliced_img.info.pop('icc_profile', None)

    # Convert to palette mode, with exact colors
    if sliced_img.mode != 'P':
        sliced_img = convert_to_exact_palette(sliced_img)

    # Check for differences with the previous image
    global changedList
    if os.path.isfile(f"{savePath}.png"):
        prev_img = Image.open(f"{savePath}.png")
        arr_new = np.array(sliced_img.convert("RGBA"))
        arr_old = np.array(prev_img.convert("RGBA"))
        if arr_new.shape != arr_old.shape:
            print('Image size changed in',simpleName)
            changedList.append(simpleName)
        else:
            changed_mask = np.any(arr_new[:, :, :3] != arr_old[:, :, :3], axis=-1)  # Compare RGB only
            alpha_mask = arr_new[:, :, 3] > 0  # Only count pixels that are not fully transparent
            pixelsChanged = np.sum(changed_mask & alpha_mask)
            if pixelsChanged: 
                print(pixelsChanged,'pixels changed in',simpleName)
                changedList.append(simpleName)

    sliced_img.save(f"{savePath}.png", optimize=True, compress_level=9) # Save the image to the website folder
    
    global biggestH, biggestW, thisH, thisW 
    # Update the largest dimensions among all images
    biggestH = max(biggestH, sliced_img.height)
    biggestW = max(biggestW, sliced_img.width)
    # Check that the size is the same between variants
    # It's okay if this shows for a few images, due to animation differences
    if thisH == 0 and thisW == 0:
        thisH = sliced_img.height
        thisW = sliced_img.width
    elif sliced_img.height != thisH or sliced_img.width != thisW:
        if warnVariantDimensions:
            print(f'Different variant dimensions for {simpleName}')

# ======================= Process all the pokemon images =======================

os.makedirs(dest_dir, exist_ok=True) # Ensure the directory exists

# Load the masterlist, it also has ['back'], ['female'], and ['back']['female']
with open(f'game_files/assets/images/pokemon/variant/_masterlist.json', "r") as f:
    masterList = json.load(f)

# Assemble the list of all images to be processed
spriteNames = [file.replace('.png','') for file in os.listdir(source_dir) if '.png' in file and 'sub.png' not in file]
# Use override list if applicable, instead of the full list
if overrideSpriteList != [] and overrideSpriteList != ['']: 
    spriteNames = [str(name) for name in overrideSpriteList]
    print('\n***** Running with override sprite list *****')
    print(f'\nProcessing {len(overrideSpriteList)} species...\n')
else:
    print('\nProcessing all images...\n')

# Loop through each sprite in the list
progressCount = 0
biggestW, biggestH = 0, 0
changedList = []
for index, thisSpriteName in enumerate(spriteNames):
    for thisBackIndex in [0,1]:
        for thisFemIndex in [0,1]:
            thisW, thisH = 0, 0
            for thisShinyIndex in [0,1,2,3]:
                processImage(thisSpriteName, thisShinyIndex, thisFemIndex, thisBackIndex)
    if (index+1)/len(spriteNames) >= (progressCount+1)*0.05:
        progressCount = int((index+1)/len(spriteNames)*20)
        print(f'{progressCount*5}% complete...')

if overrideSpriteList != [] and overrideSpriteList != ['']: 
    print(f'\nFinished processing {len(overrideSpriteList)} pokemon species')
else:
    print('\nFinished processing all pokemon images')
print('Largest width:' ,biggestW) # usually 115
print('Largest height:',biggestH) # usually 119

print('\nList of actually changed images:')
print("\n".join(changedList))

print('\n=========== ALL DONE ===========\n')

# ********* Reminder for what colors and indices are used
# color     yellow      blue        red   
# hex       0xf8c020    0x20f8f0    0xe81048
# rgb       (248,192,32)(32,248,240)(232,16,72)
# tier      1           2           3
# _#.png    1           2           3
# json[#]   0           1           2