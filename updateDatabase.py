# =====  This reads all the balance files from the official github  =====
# =====    It links all the data between evolutions and forms       =====
# ===== It saves the data in an optimized format as pokedex_data.js =====
# After running, you should use git to compare changes made to pokedex_data.js
# There are rules at the bottom of this file for how pokedex_data.js is structured

pathBal  = './game_files/src/data/balance' # Path to the balance folder
pathJSON = './game_files/wiki-output' # Path to the exported game data Json files
pathImg = './website/images' # Path to read processed images from updateImages.py

import re, os, json
def is_numeric(value): # Function to determine if a value is numeric
    return re.match(r'^-?\d+(\.\d+)?$', str(value)) is not None
def format_for_disp(arg): # Remove spaces, and convert _ and - to spaces, then capitalize
    if arg == None: return None
    return arg.replace('_',' ').replace('-',' ').title()
def format_for_attr(arg): # Remove spaces, all lower case
    if arg == None: return None
    return arg.replace(' ','').lower()
def throwError(text = ''):
    print(f'***** Major Error Found ¯\_(ツ)_/¯\n***** {text}')
    breakpoint()
    print('***** Ignoring error...')

#region Read Game Data
print("\n=========== START OF MAIN SCRIPT ===========\n")
with open(f"{pathJSON}/species.json", "r", encoding="utf-8", errors="replace") as f:
    species_data = json.load(f)
with open(f"{pathJSON}/evolutions.json", "r", encoding="utf-8", errors="replace") as f:
    evolution_data = json.load(f)
with open(f"{pathJSON}/tm-tiers.json", "r", encoding="utf-8", errors="replace") as f:
    tm_tier_data_raw = json.load(f)
tmTierValues = { "COMMON":209, "GREAT":210, "ULTRA":211 }
tm_tier_data = { line["move"]: tmTierValues[line["tier"]] for line in tm_tier_data_raw }
with open(f"{pathJSON}/level-moves.json", "r", encoding="utf-8", errors="replace") as f:
    level_data_raw = json.load(f)
level_move_data = {} # Rearrange level moves data to [dexNum][form] = [ [move,level] , ... ]
for moveLine in level_data_raw:
    speciesName = format_for_disp(moveLine["id"])
    if speciesName not in level_move_data:
        level_move_data[speciesName] = {}
    formName = format_for_disp(moveLine["form"])
    if formName == 'Dusk Wings' and speciesName == 'Necrozma':
        formName = 'Dawn Wings' # !!!!!!!!!!!!!!!!!!!!!!
    if formName not in level_move_data[speciesName]:
        level_move_data[speciesName][formName] = []
    level_move_data[speciesName][formName].append([moveLine["move"],moveLine["level"]])
with open(f"{pathJSON}/tms.json", "r", encoding="utf-8", errors="replace") as f:
    tms_data_raw = json.load(f)
tm_move_data = {} # Rearrange tm moves data to [id][form] = [tms,...]
for moveLine in tms_data_raw:
    speciesName = format_for_disp(moveLine["id"])
    if speciesName not in tm_move_data:
        tm_move_data[speciesName] = {}
    formName = format_for_disp(moveLine["form"])
    if formName == 'Normal' and speciesName == 'Calyrex':
        formName = '' # !!!!!!!!!!!!!!!!!!!!!!
    if formName not in tm_move_data[speciesName]:
        tm_move_data[speciesName][formName] = []
    tm_move_data[speciesName][formName].append(moveLine["move"])
print('Finished reading main data')

# Open and read the biomes file ************************************
#region Read Biomes
biome_data_raw = {}
allBiomes = [file.replace('.ts','') for file in os.listdir(f"{pathBal}/biomes") if '.ts' in file]
allBiomes.sort()
for biome in allBiomes: # For each biome file in the biome folder, parse the encounter data
    with open(f"{pathBal}/biomes/{biome}.ts", "r", encoding="utf-8", errors="replace") as file:
        content = file.read()
    # Use a regular expression to extract text between "BiomePokemonPools = {" and "};"
    inputBiomeData = re.findall(r'BiomePokemonPools = {(.*?)};', content, re.DOTALL)[0]
    biome_data_raw[biome] = { # biome_data_raw[biome][tier][timeOfDay] = [speciesNames]
        tierLine.split(']:')[0]: {
            timeLine.split(']:')[0]: re.findall(r'SpeciesId.(.*?)[,\]]', timeLine.split(']:')[1], re.DOTALL)
            for timeLine in tierLine.split('TimeOfDay.')[1:]
        }
        for tierLine in inputBiomeData.split('BiomePoolTier.')
    }
biomeTierValues = { 'COMMON':20, 'UNCOMMON':40, 'BOSS':60, 'RARE':80, 'BOSS_RARE':100, 'SUPER_RARE':120, 'BOSS_SUPER_RARE':140, 'ULTRA_RARE':160, 'BOSS_ULTRA_RARE':180 }
biomeTimeValues = { 'ALL':0, 'DAWN':1, 'DAY':2, 'DUSK':4, 'NIGHT':8 }
biome_data = {} # All biome data [speciesName] = [ [biome,code], ... ]
for biome, biomeLine in biome_data_raw.items():
    for tier, tierLine in biomeLine.items():
        for time, timeLine in tierLine.items():
            for species in timeLine:
                species = format_for_disp(species)
                if species not in biome_data:
                    biome_data[species] = []
                tierCode = biomeTierValues[tier] + biomeTimeValues[time]
                biome_data[species].append([biome, tierCode])           
# Structure of biome_data[species] is like [ ['abyss', 23], ['abyss', 41], ['beach', 160], [...] ]
# Same tier at multiple times of day are combined in a later step
print('Finished reading biome data')

#region Read Egg Moves
egg_move_data = {}
with open(f"{pathBal}/moves/egg-moves.ts", "r", encoding="utf-8", errors="replace") as file: # Egg moves **************************
    content = file.read()
# Use a regular expression to extract text between "speciesEggMoves = {" and "} satisfies"
inputMoveData = re.findall(r'speciesEggMoves\s*=\s*{(.*?)}\ssatisfies', content, re.DOTALL)[0]
inputMoveData = re.split(r',\n', inputMoveData)
# Egg moves are added to egg_move_data[species], encoded as 204(common) or 208(rare)
for eggLine in inputMoveData:
    speciesName = format_for_disp(re.findall(r'SpeciesId\.(.*?)\]', eggLine)[0])
    eggMoves = [ format_for_disp(line) for line in re.findall(r'MoveId\.(.*?)\s?[\],]', eggLine) ]
    if len(eggMoves) != 4:
        print(f'Weird number of egg moves found in {speciesName}')
    if speciesName not in egg_move_data:
        egg_move_data[speciesName] = {}
    for eggMove in eggMoves:
        egg_move_data[speciesName][eggMove] = ( 208 if eggMove==eggMoves[-1] else 204 )
print('Finished reading egg move data')

poke_data = []
#region Assign Pokemon Data
print("\nStarting to assign pokemon data\n")
for i, thisData in enumerate(species_data): # Function for reading from game data
    line = ['' for _ in range(47)] 

    line[0] = i # row number [0]
    line[1] = format_for_disp(thisData["formKey"]) # Form Name [1] (used for actual name)
    line[2] = format_for_disp(thisData["id"]) # Species Name [2] is the text of just the Species
    # Species Name is used for "Related" filters, biome data, and translation lookup. Includes regional name, but not form name.
    line[3] = thisData["dexNum"] # dex number [3]
    line[4] = thisData["spriteKey"] # image filename [4]
    line[5] = f'{line[1]} {line[2]}' if line[1] else line[2] # Display Name [5]
    line[6] = format_for_disp(thisData["category"]) # Species description (unused) [6]

    # Remove unobtainable pokemon, and "Complete 10% Zygarde"
    if thisData["isUnobtainable"] or '10 Complete' in line[5]:
        if 'Revavroom' not in line[5]: # Keep Starmobiles
            print(f'Unobtainable {line[5]}')
            continue # Skip the rest of parsing

    line[7] = format_for_disp(thisData["type1"]) # Type 1 [7]
    typeTwo = format_for_disp(thisData["type2"]) # Type 2 [8]
    line[8] = '' if typeTwo == line[7] or typeTwo == None else typeTwo
    line[9] = format_for_disp(thisData["ability1"])    # Ability 1 [9]
    abilityTwo = format_for_disp(thisData["ability2"]) # Ability 2 [10]
    line[10] = '' if abilityTwo == line[9] or abilityTwo == "None" else abilityTwo
    abilityHidden = format_for_disp(thisData["hiddenAbility"]) # Hidden ability [11]
    line[11] = '' if abilityHidden == line[9] or abilityHidden == "None" else abilityHidden
    line[12] = format_for_disp(thisData["passive"]) # Passive [12]

    stats = ['bst','hp','atk','def','spatk','spdef','spd','catchRate','growthRate','maleRatio','genderDiffs']
    for j, stat in enumerate(stats): # Stats [13-19], Catch rate [20], growthRate [21], malePercent [22], genderDiffs [23]
        line[13+j] = thisData[stat]
    line[29] = thisData["startercost"] # Cost [29]
    line[32] = thisData["generation"] # Generation [32]

    eggTier = thisData["eggTier"] # Egg Tier [30]
    eggTierValues = { None:'', 'COMMON':0, 'RARE':1, 'EPIC':2, 'LEGENDARY':4 }
    line[30] = 3 if line[5] in ['Phione','Manaphy'] else eggTierValues[eggTier]
    
    line[40] = [] # biomes [40]
    if line[2] in biome_data: # If specKey is listed in biome data
        line[40] = biome_data[line[2]] # Take the full list of biomes
    
    line[46] = format_for_disp(thisData["starter"]) # Starter Species Name [46]
    if line[46] == line[2] or 'Pikachu' in line[5]: # If starter species matches this species
        line[33] = 1 # isStartable [33] ( 1 = species available in starter select (i.e. has not evolved yet), '' = not available )
        line[34] = len(poke_data) # starterRow [34] is the row of starter evo
    line[44] = 1 # Fully Evolved [44] ( '' = can evolve, 1 = fully evolved )
    if line[46] == 'Pikachu': line[46] = 'Pichu'

    # Form exclusive [41] ( '' = starter, 1 = mega, 2 = new mega, 3 = giga, 4 = transformed )
    formExclusive = '' # By default, the form is selectable in starter select
    # Check for mega, giga, or other transformed (Zacian, Mimikyu, etc.)
    if line[1] != None and not thisData["isStartSelectable"]: formExclusive = 4 # If form and not selectable
    megaList = ['Mega Clefable','Mega Victreebel','Mega Starmie','Mega Dragonite','Mega Meganium','Mega Feraligatr','Mega Skarmory','Mega Froslass','Mega Emboar','Mega Excadrill','Mega Scolipede','Mega Scrafty','Mega Eelektross','Mega Chandelure','Mega Chesnaught','Mega Delphox','Mega Greninja','Mega Pyroar','Mega Floette','Mega Malamar','Mega Barbaracle','Mega Dragalge','Mega Hawlucha','Mega Zygarde','Mega Drampa','Mega Falinks','Mega Raichu X','Mega Raichu Y','Mega Chimecho','Mega Baxcalibur']
    speciesName = line[5]
    if 'Mega ' in speciesName:      formExclusive = 1 # Mega (needs the space)
    if speciesName in megaList:     formExclusive = 2 # New Mega
    if 'Gigantamax' in speciesName: formExclusive = 3 # Giga
    # In-game, the form is chosen from getSpeciesFormIndex in src/battle-scene.ts
    # Some forms have the wrong isStarterSelectable in the species definition (error with the game code)
    if 'Minior'   in speciesName and 'Meteor' not in speciesName: formExclusive = 4  # Force minior core to count as transformed
    if 'Maushold' in speciesName or 'Dudunsparce' in speciesName: formExclusive = '' # Force those forms to be not exclusive
    line[41] = formExclusive

    # Many attributes are given the default values of '', and filled in later, including:
    # Egg Moves [24-27], Shiny Variants [31], familyFID [38], freshStart [39], Newly Added Variants [43]
    # Exclusive class [45] ( '' = regular, 1 = eggExc, 2 = baby, 3 = paradox, 4 = eterna, 5 = starmobile )

    #region Assign Moves
    line[28] = {} # Add dictionary for all moves [28] { 'Move Name':src, ... }
    # src = -1:mushroom, 0:evo, 1-200:level, 201-203:egg&TM, 204:egg, 205-207:rare&TM, 208:rare, 209-211:comm/great/ultra TM
    def assignMoveCode(code):
        currentCode = None
        if format_for_disp(moveName) in line[28]: currentCode = line[28][format_for_disp(moveName)]
        if code == 'EVOLVE_MOVE' : code = 0
        if code == 'RELEARN_MOVE': code = -1
        if 100 < code < 200: throwError(f'High level move found in {line[5]}: Level {code}')
        if code > 208: # If a TM move
            if currentCode in [204,208]: code += currentCode - 212 # Combine egg moves and TM moves
            if currentCode != None and currentCode < 200: return # Don't replace level moves with TM moves
        if code < 200 and currentCode != None: return # Don't replace egg moves with level moves
        line[28][format_for_disp(moveName)] = code
    # Import egg moves from the starterName [46] **********
    line[24:28] = egg_move_data[line[46]].keys() # Put egg moves in [24-27]
    for move in egg_move_data[line[46]].keys(): # Add egg moves to the move dictionary [28]
        line[28][move] = egg_move_data[line[46]][move] # Add the egg move to the move dict
    # Import level moves from the speciesName [2] **********
    for moveName, moveCode in level_move_data[line[2]][None]: # For all forms
        assignMoveCode(moveCode)
    if line[1] != None and line[1] in level_move_data[line[2]]: # Uses form key
        for moveName, moveCode in level_move_data[line[2]][line[1]]: # For specific forms
            assignMoveCode(moveCode)
        print(f"Imported unique level moves for {line[5]}")
        level_move_data[line[2]][line[1]] = []
    if line[2] in tm_move_data: # If species is listed, add TM moves **********
        for moveName in tm_move_data[line[2]][None]: # For all forms
            assignMoveCode(tm_tier_data[moveName])
        if line[1] != None and line[1] in tm_move_data[line[2]]:
            for moveName in tm_move_data[line[2]][line[1]]: # For specific forms
                assignMoveCode(tm_tier_data[moveName])
            print(f"Imported unique TM moves for {line[5]}")
            tm_move_data[line[2]][line[1]] = []

    poke_data.append(line)
print("\nFinished assigning pokemon data\n")

#region Propagate Cost & Egg
for line in poke_data:
    if '' in line[29:31]: # If blank entry for cost or egg tier, inherit from starter
        for starterLine in poke_data:
            if line[46] == starterLine[2]: # If starterName [46] equals starter's Species Name [2]
                line[29:31] = starterLine[29:31] # Cost [29], egg tier [30]
                line[34] = starterLine[34]       # Starter row [34]
                break
for evoLine in evolution_data: # Find pokemon that are not fully evolved
    preEvo = format_for_disp(evoLine["id"])
    for childLine in poke_data:
        if preEvo == childLine[2]:
            childLine[44] = '' # Set the child to not be fullyEvolved
#region Propagate Biomes
for stages in range(2): # Propagate biomes via up to 2 evolutions **************************
    for evoLine in evolution_data:
        preEvo = format_for_disp(evoLine["id"])
        for childLine in poke_data:
            if preEvo == childLine[2]: # Find the childLine, break when matching
                break
        else: # If the child search loop fails to break
            throwError(f'Failed to find pre-evo: {preEvo}')
        parentName = format_for_disp(evoLine["evoId"])
        for parentLine in poke_data:
            if parentName == parentLine[2]: # Copy properties from child to parent
                for biomeLine in childLine[40]:
                    parentLine[40].append(biomeLine)
# The game usually only provides biome data to one species per evolution line
# The evolution stage is upgraded/downgraded by determineEnemySpecies in file:///\.\game_files\src\data\pokemon-species.ts
# Biome propagation (line[40]) in my code must be done in a particular way: forward twice, then backward twice
# That prevents split evolutions from influencing each other (e.g. Dustox/Beautifly)
# Structure of line[40] is like [ ['abyss', 23], ['abyss', 41], ['beach', 160], [...] ]
for stages in range(2): # Up to 2 evolutions
    for evoLine in evolution_data: # Assign biome data backwards
        parentName = format_for_disp(evoLine["evoId"])
        for parentLine in poke_data:
            if parentName == parentLine[2]: # Find the parent line, to copy biomes from
                break
        else: # If the parent search loop fails to break
            throwError(f'Failed to find post-evo: {preEvo}')
        preEvo = format_for_disp(evoLine["id"])
        for childLine in poke_data:
            if preEvo == childLine[2]: # Find the childLine, break when matching
                for biomeLine in parentLine[40]:
                    childLine[40].append(biomeLine)
        # TODO: tyrogue,smoochum,elekid,magby,wynaut,toxel
        # These babies can appear in the wild, because they are level evolutions
        # Friendship evolutions cannot devolve at low levels
print('Finished propagating data to evolutions and forms')

#region Empty Checks
for line in poke_data: # Check for empty properties in full_data
    if line[12] == '':
        throwError(f'Missing Passives: {line[5]}')
    if line[24:28] == '':
        throwError(f'Missing Egg Moves: {line[5]}')
    if line[29] == '' or line[29] == 0:
        throwError(f'Missing Cost: {line[5]}')
    if line[30] == '':
        throwError(f'Missing Egg Tier: {line[5]}')
    if line[34] == '': # Check for invalid starter row
        throwError(f'Unassigned starter row for {line[5]}')
    if line[40] == []:
        line[45] = 1 # Exclusive to egg
        if 'Pichu' in line[5]: # Manual override for spiky pichu bc it is missing evo hookup
            line[45] = 2 # Exclusive to baby
        for evoLine in evolution_data:
            if format_for_disp(evoLine["id"]) == line[2]:
                parentName = evoLine["evoId"]
                for parentLine in poke_data:
                    # Make sure Meltan doesn't count as a baby
                    if parentName == parentLine[2] and parentLine[40] != []: # Check if parent has biomes
                        line[45] = 2 # Exclusive to baby
                        break
        # if line[45] == 1: print('Egg Exclusive:',line[5])
        # if line[45] == 2: print('Baby Egg Exclusive:',line[5])
    elif line[40] != [] and line[40][0][0] == 'end':
        if 'Eternatus' in line[5]:
            # print('Eternatus:',line[5])
            line[45] = 4
        else:
            # print('Paradox:',line[5])
            line[45] = 3
    if 'Starmobile' in line[5]:
        line[40] = []
        line[41] = '' # Set form exclusive [41] to blank, not a "transformed" form
        line[45] = 5  # Set exclusive class [45] to unobtainable
        # print('Starmobile:',line[5])
    if line[40] == [] and line[45] not in [1,2,5]: # If no biomes, and not egg exclusive
        throwError(f'Missing Biomes: {line[5]}')

# Determine which pokemon are available for "Fresh Start"
gen, freshThisGen, freshStarterIndices = 1, 0, []
for line in poke_data:
    if int(line[32]) == gen and (line[34] not in freshStarterIndices) and freshThisGen < 3:
        if line[29] < 6: # Exclude Victini
            freshStarterIndices.append(line[34]) # Add that starter line to the Fresh Start list
            freshThisGen += 1
    if freshThisGen == 3: # Go to next gen after finding 3 starter lines
        gen = gen + 1 
        freshThisGen = 0
    if line[34] in freshStarterIndices:
        line[39] = 1 # Set all pokemon in that starter line to be Fresh Start

# Error checking **************************************************************************************
# region Error Checking
print('\n==============================\n')
print('Checking for errors...')

for speciesName in level_move_data:
    for formName in level_move_data[speciesName]:
        if formName != None and level_move_data[speciesName][formName] != []:
            print(f"** Failed to assign Level Moves for {formName} {speciesName}")
for speciesName in tm_move_data:
    for formName in tm_move_data[speciesName]:
        if formName != None and tm_move_data[speciesName][formName] != []:
            print(f"** Failed to assign TM Moves for {formName} {speciesName}")

# Use the default image if unique form image does not exist
for i in range(len(poke_data)):
    if not os.path.isfile(f'{pathImg}/{poke_data[i][4]}_0.png'): # Check if the given img does not exist
        # print(f'{poke_data[i][5]}: Could not find {poke_data[i][4]}')
        if os.path.isfile(f'{pathImg}/{poke_data[i][3]}_0.png'): # Check if the base img exists
            # print(f'{poke_data[i][5]}: Replaced {poke_data[i][4]} with base image')
            poke_data[i][4] = f'{poke_data[i][3]}' # Get base image from dexno
        elif poke_data[i][3] == poke_data[i-1][3]: # If same species as one above
            poke_data[i][4] = poke_data[i-1][4] # Take image from form above
            if int(poke_data[i][3]) not in [1012,1013]: # Report if not Sinistcha family
                print(f'{poke_data[i][5]}: Replaced {poke_data[i][4]} with {poke_data[i-1][4]}')
        else:
            throwError(f'Could not find any image {poke_data[i][4]}_0.png for {poke_data[i][5]}')
# Check for the existence of variant shinies
for line in poke_data:
    if os.path.isfile(f'{pathImg}/{line[4]}_3.png'): # Check if the tier 3 shiny exists
        line[31] = 3 # Shiny variants [31]           # Need to run updateImages.py first *****
    else:
        line[31] = 1 # Shiny variants [31]
    if os.path.isfile(f'{pathImg}/{line[4]}_0f.png'): # Check if the base female sprite exists
        line[23] = 1 # Mark as female sprite difference
        femlist = ['','f']
    else:
        if 'Female' in line[5] or line[5] == 'Nidoran F':
            line[23] = 2 # Mark as a distinct female form (Nidoran, Meowstic, etc.)
        else:
            line[23] = ''
        femlist = ['']
    for back in ['','b']: 
        for fem in femlist: 
            for shiny in range(line[31]+1):
                # Check for existence of all images (all shiny, all back, optionally female)
                if not os.path.isfile(f'{pathImg}/{line[4]}_{shiny}{fem}{back}.png'):
                    throwError(f"The file {pathImg}/{line[4]}_{shiny}{fem}{back}.png does not exist.")

# Check that each Pokemon has level up moves, egg moves, and TM moves
for line in poke_data:
    check = [0,0,0]
    for value in line[28].values():
        if value < 100: # Level moves
            check[0] = 1
        if 200 < value < 209: # Egg moves (and Egg/TM moves)
            check[1] += 1
        if value > 208: # TM moves
            check[2] = 1
    if check[0] != 1:
        throwError(f'Missing level-up entries in {line[5]}')
    if check[1] != 4:
        throwError(f'Missing egg move entries in {line[5]}')
    if check[2] != 1 and line[3] not in [132, 201, 202, 235, 360, 789, 790]:
        throwError(f'Missing TM move entries in {line[5]}') # If a pokemon is supposed to have TM moves
    if int(line[32]) not in range(1,10):
        throwError(f'Generation Error in {line[5]}')

# Check that every pokemon has at least one pickable form        
dexNo, isStartable = 1, False
for line in poke_data:
    if line[3] != dexNo:
        if not isStartable: # Show error if a pokemon has no startable forms
            throwError(f'No startable forms found for {line[2]}')
        dexNo, isStartable = line[3], False # Restart the search on the next dex number
    if not line[41]: # If not form exclusive, it is startable
        isStartable = True

# Check that dex numbers are sequential up to 1025
dexNo = 1
for line in poke_data:
    if line[3] == dexNo: dexNo += 1
    if line[3] >  dexNo: throwError(f'Could not find Dex #{dexNo}')
    if dexNo == 1026: break
if poke_data[-1][5] != "Bloodmoon Ursaluna": throwError('Final dex entry is not correct') # Check final pokemon
if len(poke_data) != 1452: throwError('Total number of entries is not correct') # Check number of pokemon

# Check that Normal Deoxys has Swift, Icy Wind, and Cosmic Power (and speed, speed, attack)
# Check that Normal/Ice Calyrex has Body Press

# Assemble lists of all filters of each category *****************************
#region Define Filters
allTypes = ['Bug','Dark','Dragon','Electric','Fairy','Fighting','Fire','Flying','Ghost','Grass','Ground','Ice','Normal','Poison','Psychic','Rock','Steel','Water']
allAbilities = []
allMoves = {}
for line in poke_data:
    for ability in line[9:13]:
        if ability != '' and ability not in allAbilities:
            allAbilities.append(ability)
    for moveName in line[28].keys():
        allMoves[moveName] = ''
allAbilities.sort()
allMoves = sorted([*allMoves]) # Get a list of moves from the move dict
allBiomes = sorted([format_for_disp(biome) for biome in allBiomes])

# Assign filter ID numbers (FID) to each filter *****************************
allFilters = []  # List of all filters, in numerical order: FID: ['Category','Filter Name']
filterToFID = {} # Get FID from name: e.g. filterToFID('typebug') = FID
# All strings from poke_data are encoded as FID before writing to the website data
for type in allTypes:
    filterToFID[f'type{format_for_attr(type)}'] = len(allFilters)
    allFilters.append(['Type',type])
for line in allAbilities:
    filterToFID[f'ability{format_for_attr(line)}'] = len(allFilters)
    allFilters.append(['Ability',line])
for line in allMoves:
    filterToFID[f'move{format_for_attr(line)}'] = len(allFilters)
    allFilters.append(['Move',line])
for j in range(1,10):
    allFilters.append(['Gen',j])
for j in range(1,11):
    allFilters.append(['Cost',j])
for j in range(2,10):
    allFilters.append(['Cost',f'≤ {j}'])
for j in range(2,10):
    allFilters.append(['Cost',f'≥ {j}'])
for j in ['Common','Rare','Epic','Manaphy','Legendary','Exclusive']:
    allFilters.append(['Egg Tier',j])
for j in ['Starter Select','Fresh Start','Flipped Stats']:
    allFilters.append(['Mode',j])
for j in ['Starter','Fully Evolved']:
    allFilters.append(['Evolution',j])
for j in ['Base','Mega','New Mega','Giga','Transformed','Female']:
    allFilters.append(['Form',j])
for line in allBiomes:
    filterToFID[f'biome{format_for_attr(line)}'] = len(allFilters)
    allFilters.append(['Biome',line])
for j in ['Mega','New Mega','Giga']:
    allFilters.append(['Related To',j])
for starterIndex in sorted(list(set([ line[34] for line in poke_data ]))):
    allFilters.append(['Related To',poke_data[starterIndex][2]])
    for line in poke_data:
        if line[34] == starterIndex: # If starterIndex is equal to the one in starterList
            line[38] = len(allFilters)-1 # Set familyFID to this fid
for j in ['New','All','None']:
    allFilters.append(['Shiny Variants',j])
for j in [71,37,48,49,50,56,57,58,59,60,61,62,63,64,65,66,67]: # TagID of the tag filters
    allFilters.append(['Tag',j])                               # en.py has the full list of tags

#region Combine Biomes
# Structure of line[40] is like [ ['abyss', 23], ['abyss', 41], ['beach', 160], [...] ]
# This step encodes that data as [ ['abyss', fid, [23,41]], ['beach', fid, [160]], [...] ]
# Multiple encounters in the same biome are put into a list in that biome (instead of a separate line)
biomeForms = { # manually updated from getSpeciesFormIndex in file:///\.\game_files\src\field\arena.ts
    'Plant Burmy':    'Forest', 'Sandy Burmy':    'Beach', 'Trash Burmy':    'Slum',
    'Plant Wormadam': 'Forest', 'Sandy Wormadam': 'Beach', 'Trash Wormadam': 'Slum',
}   
biomeFormsTime = { # 1=dawn, 2=day, 4=dusk, 8=night
    'Midday Lycanroc': [1,2], 'Dusk Lycanroc': [4], 'Midnight Lycanroc': [8]
}
for line in poke_data:
    encoded = []
    if line[40] != []: # If there are biomes
        for biomeLine in line[40]:
            # If a species is limited by biome/time, it must pass a check before the biomes are written
            if line[5] in biomeForms: # Enforce specific BIOME FORMS by matching biome name
                if format_for_disp(biomeLine[0]) != biomeForms[line[5]]:
                    continue # Abort if not the right biome for this form
            if line[5] in biomeFormsTime: # Enforce TIME OF DAY forms by checking remainder of encounter code
                if all(not(i & (biomeLine[1]%20)) for i in biomeFormsTime[line[5]]):
                    continue # Abort if not the right time of day for this form
            newFID = filterToFID[f'biome{format_for_attr(format_for_disp(biomeLine[0]))}'] # Find filter ID
            for encLine in encoded: # Find existing encounters in that biome
                if encLine[0] == newFID: # If the biome already exists, add this encounter to the list
                    for index,existingEncoding in enumerate(encLine[2]):
                        if biomeLine[1]//20 == existingEncoding//20: # Check entry of same rarity
                            # Add the time of day together with bitwise OR
                            # If no times are active, it counts as ALL times (15)
                            # If the combination is ALL times, do mod 15 to not show any times
                            timeOfDayEncoding = ( ( biomeLine[1]%20 or 15 ) | ( existingEncoding%20 or 15 ) ) % 15
                            encLine[2][index] = timeOfDayEncoding + existingEncoding//20*20
                            break
                    else: # Add the encounter code as a new rarity
                        encLine[2].append(biomeLine[1])
                    break # Break if biome has been processed
            else: # Create a new FID entry for that biome
                encoded.append([newFID, biomeLine[0], [biomeLine[1]]])
    line[40] = encoded
    # for encLine in encoded:
    #     if len(encLine[1]) > 2:
    #         print('** More than 2 biome rarites in {line[5]}: {encLine}')
    # if len(encoded) > 3:
    #     print(f'** Many biomes ({len(encoded)}) in {line[5]}: {line[40]}')
# Sort each biome entry to be [norm, boss, rarerNorm, rarerBoss]
# This is important for the website quickly sorting by biome rarity
# If a pokemon is all Boss or all non-Boss, the whole list is just in ascending order
for line in poke_data:
    if isinstance(line[40],list):
        for biomeLine in line[40]:
            encoded = []
            # First entry is the most common non-Boss encounter
            entry = min((x for x in biomeLine[2] if x-x%20 not in [60,100,140,180]), default=None)
            if entry: encoded.append(entry)
            # Second entry is the most common Boss encounter
            entry = min((x for x in biomeLine[2] if x-x%20 in [60,100,140,180]), default=None)
            if entry: encoded.append(entry)
            # Remaining entries are in ascending order
            for entry in sorted(biomeLine[2]):
                if entry not in encoded:
                    encoded.append(entry)
            biomeLine[2] = encoded       

#region Export Filter Lists
fidThreshold = []
catName = allFilters[0][0]
for index,line in enumerate(allFilters):
    if line[0] != catName:
        catName = line[0]
        fidThreshold.append(index) # Find the threshold of each filter category
fidThreshold.append(len(allFilters))
if fidThreshold[0] != 18:  throwError('Wrong number of types')
if fidThreshold[1] != 328: throwError('Wrong number of abilities')
# Write some variables to files, which are read by my other scripts, and some are written to the website
with open("local_files/my_json/allFilters.json", "w") as f:
    json.dump(allFilters, f, indent=4)
with open("local_files/my_json/fidThreshold.json", "w") as f:
    json.dump(fidThreshold, f, indent=4)
with open("local_files/my_json/filterToFID.json", "w") as f:
    json.dump(filterToFID, f, indent=4)
# Save all the names: [displayname/formkey/species] (regional is included in species)
allSpecies = [[line[5],line[1],line[2]] for line in poke_data]
with open("local_files/my_json/allSpecies.json", "w") as f:
    json.dump(allSpecies, f, indent=4)

input('No Major Errors Found\n\nContinue to patch review?')
print('\n==============================\n')
print("Reviewing patch changes...\n")

# Patch note creating **********************************************************************************
# region Review Patch Notes
# This makes it easy to see what has changed in the new data, by comparing to poke_data_prev.json
# To re-base the comparison, you must manually replace poke_data_prev.json with data from poke_data.json
# poke_data_prev_shvar.json should only be re-based right before adding new variants
with open("local_files/poke_data.json", "w", encoding="utf-8") as f:
    json.dump(poke_data, f, ensure_ascii=False, indent=4) # Write all the trimmed data to a json file
with open("local_files/poke_data_prev.json", "r", encoding="utf-8", errors="replace") as fp:
    poke_data_prev = json.load(fp) # Load the previous trimmed data for comparison
with open("local_files/poke_data_prev_shvar.json", "r", encoding="utf-8", errors="replace") as fp:
    poke_data_shvar = json.load(fp) # Older version for detecting new variants
# Look for changes and report them in a patch notes format
# Github may detect more changes in pokedex_data.js because of how fid are assigned
attNames = ['rowno','form','species','dexno','img','fullName','desc','type1','type2','ab1','ab2','hab','Passive',
           #   0      1        2        3      4       5        6       7       8      9    10    11    12
            'bst','HP','Atk','Def','SpAtk','SpDef','Speed','catchrate','exp','mpc','fem','Egg Move 1','Egg Move 2','Egg Move 3','Rare Egg Move',
           # 13    14   15    16     17      18      19        20      21    22    23        24           25           26        27
            'movedict','cost','eggtier','shvar','gen','startable','startRow','startInd','specInd','specKey','famFID',
           #    28       29      30       31     32       33          34         35         36        37       38
            'freshStart','biomes','formExclusive','unobtainable','newVariants','evoClass','exclusiveClass','starterName']
           #    39          40           41             42             43           44            45             46
omitAttr = [0, 1, 2, 6, 20, 21, 22, 34, 35, 36, 37, 38, 42]
soloAttr = [] # Put an attribute here to only show changes to that, and ignores changes to others
for i in soloAttr:                              # You can use strings for ranges (inclusive)
    if isinstance(i, str) and '-' in i: # i.e. [1,'3-5',8] becomes [1,3,4,5,8]
        for j in range(int(i.split('-')[0]),int(i.split('-')[1])):
            soloAttr.append(j)
        i = j+1
attPatchCount = [0 for arg in attNames] # How many times each attribute was changed
eggPatchCount = [0 for arg in poke_data] # How many times any egg move was changed
patch_review = [] # Readable review of patch notes in the console
patch_data = {} # Numerical patch data imported to the SearchDex
def MoveSrcText(value):
    if value == -1: return "mushroom"
    if value == 0: return "evolution"
    if value < 200: return f"level {value}"
    return { 201:"Egg & Common TM", 202:"Egg & Great TM", 203:"Egg & Ultra TM", 204:"Egg Move", 205:"Rare Egg & Common TM", 206:"Rare Egg & Great TM", 207:"Rare Egg & Ultra TM", 208:"Rare Egg Move", 209:"Common TM", 210:"Great TM", 211:"Ultra TM" }[value]           
for i,line in enumerate(poke_data):
    # Find where the species is, in _prev (the index may be different)
    for ii in range(i-10,min(i+10,len(poke_data_prev))):
        if line[5] == poke_data_prev[ii][5]:
            prevLine = poke_data_prev[ii]
            prevLine[4] = format_for_attr(prevLine[4])
            prevLine[40] = [ [biomeLine[1], biomeLine[0], biomeLine[2]] for biomeLine in prevLine[40] ] # !!!!!!!!!!!!
            break
    else:
        print('Could not find',line[5],'in previous data')
        continue
    if line[5] == prevLine[5]: # Make sure species is the same
        # Find where the species is, in _prev_shvar (which may be different length from _prev)
        for iii in range(i-10,min(i+10,len(poke_data_shvar))):
            if line[5] == poke_data_shvar[iii][5]: # Find matching name
                if line[31] != poke_data_shvar[iii][31]: # If shvar has changed
                    line[43] = 1 # Mark as newly added shiny variants
                break
        else:
            print(f'Could not find previous data for {line[5]}')
        # Loop through all attributes for comparison
        for j in range(0,min(len(line),len(prevLine))):
            # For all the main values, they are only 'changed'
            if (not soloAttr and j not in omitAttr) or j in soloAttr: 
                if j == 28: # For the move dict, they are either 'added' or 'removed'
                    for key,value in line[28].items():
                        if value not in [204,208]: # Ignore egg moves
                            if key in prevLine[28] and prevLine[28][key] not in [204,208]:
                                valuePrev = prevLine[28][key]
                                if valuePrev != value: # If move is different in new vs old data
                                    patch_review.append(f'{line[5]}: {key} changed from {MoveSrcText(valuePrev)} to {MoveSrcText(value)}')
                            else: # If new move is not in old data
                                moveKind = "Level" if value < 200 else "TM"
                                patch_review.append(f'{line[5]}: {key} added to {moveKind} moves')
                    for key,value in prevLine[28].items():
                        if key not in line[28] and value not in [204,208]: # If old move missing from new data
                            moveKind = "Level" if value < 200 else "TM"
                            patch_review.append(f'{line[5]}: {key} removed from {moveKind} moves')
                elif str(line[j]) != str(prevLine[j]): # Compare all other attributes
                    if j not in [24,25,26,27] or ( line[33] and not line[41] ): # Don't show egg moves, except on starter select mons
                        patch_review.append(f'{line[5]}: {attNames[j]} changed from {prevLine[j]} to {line[j]}')
                    if j in [12,24,25,26,27,29,30]:
                        if j == 12: # Passive
                            preFID = filterToFID[f'ability{format_for_attr(prevLine[j])}']
                            postFID = filterToFID[f'ability{format_for_attr(line[j])}']
                        if j in [24,25,26,27]: # Egg moves
                            preFID = filterToFID[f'move{format_for_attr(prevLine[j])}']
                            postFID = filterToFID[f'move{format_for_attr(line[j])}']
                        if j == 29: # Cost
                            preFID = fidThreshold[3]-1+prevLine[j]
                            postFID = fidThreshold[3]-1+line[j]
                        if j == 30: # Egg tier
                            preFID = fidThreshold[4]+prevLine[j]
                            postFID = fidThreshold[4]+line[j]
                        for specID,thisData in patch_data.items(): # Check patch data for redundant entries
                            if poke_data[specID][38] == line[38]: # If same family
                                if j in thisData and thisData[j][0] == preFID and thisData[j][1] == postFID:
                                    break
                        else:
                            if i not in patch_data:
                                patch_data[i] = {}
                            patch_data[i][j] = [preFID, postFID]
                    attPatchCount[j] += 1
                    if j in [24,25,26,27]:
                        eggPatchCount[i] = 1
for line in patch_review:
    print(line)
print('\nSummary of patch notes:')
for j in range(len(attNames)):
    if attPatchCount[j] > 0:
        print(f'{attNames[j]} changed: {attPatchCount[j]}')
print('Total Egg Moves changed:',sum(eggPatchCount))
# Format the patch notes and save to a file
with open("local_files/patch_review.txt", "w") as file:
    file.writelines("\n".join(patch_review))
with open("website/patch_data.js", "w") as file:
    file.writelines("patchData = {")
    for specID in patch_data.keys():
        file.writelines(f"\n{specID}: {{")
        textList = [f"{attID}:[{line[0]},{line[1]}]" for attID, line in patch_data[specID].items()]
        file.writelines(",".join(textList))
        file.writelines("},")
    file.writelines('\n};')

input('\nContinue to writing website database?')
print('\n==============================\n')
print("Writing to website database...")

#region Write Website Data
# Write all the main data to a Javascript file *********************************************
# Names are short to reduce database file size
attributes = ['row','form','spec','dex','img','name','desc','t1','t2','a1','a2','ha','pa',
             #  0     1      2      3     4     5      6     7    8    9    10   11   12    
              'bst','hp','atk','def','spa','spd','spe','catchrate','exp','mpc','fe','e1','e2','e3','e4','movedict',
             #  13   14    15    16    17    18    19       20       21    22   23   24   25   26   27      28
              'co','et','sh','ge','st','startRow','startInd','specInd','specKey','fa',
             # 29   30   31   32   33      34         35         36        37     38
              'fs','biomes','fx','unobtainable','nv','ev','ex']
             # 39     40     41        42        43   44   45
# Some attributes are not written to the SearchDex database
omitAttr = [0, 1, 2, 5, 6, 20, 21, 22, 28, 34, 35, 36, 37, 40, 42]
# Key text to convert type/ability/move to filterID (FID) via filterToFID
keyText = {7:'type', 8:'type', 9:'ability', 10:'ability', 11:'ability', 12:'ability', 24:'move', 25:'move', 26:'move', 27:'move'}

jsdict = ['// pokedex_data.js\nconst items=[']
for line in poke_data:
    text = '{' # Start the entry of that Pokemon
    # Write all the main attributes as {text}:{value}
    for i in range(len(attributes)): 
        if i not in omitAttr and line[i] != '':
            if i in [7,8,9,10,11,12,24,25,26,27]: # Types/Abilities/Moves are listed as Names in poke_data
                fid = filterToFID[format_for_attr(f'{keyText[i]}{line[i]}')] # Convert to filter ID (fid)
                text = f'{text}{attributes[i]}:{fid},'
            elif i == 4:
                text = f'{text}{attributes[i]}:"{format_for_attr(line[i])}",' # For img path
            elif is_numeric(line[i]):
                text = f'{text}{attributes[i]}:{line[i]},' # For numbers
            else:
                throwError(f"Unknown attribute format: {i}")

    # Prepare all filters to be written as {fid}:{source}
    fidToWrite = [
        *[ # Types and Abilities
            [ filterToFID[format_for_attr(f'{keyText[i]}{line[i]}')], 300+i ] for i in range(7,13) if line[i] != ""
        ], *[ # Moves
            [ filterToFID[format_for_attr(f'move{moveName}')], line[28][moveName] ] for moveName in line[28].keys()
        ], *[ # Biomes as fid:[code1,code2,...]
            [ biomeLine[0], f'[{",".join(str(b) for b in biomeLine[2])}]' ] for biomeLine in line[40]
        ]
    ]
    for filterLine in sorted(fidToWrite):
        text = f'{text}{filterLine[0]}:{filterLine[1]},'

    # End the entry of that Pokemon and remove unnecessary commas
    text = f'{text}}},'.replace(',]',']').replace(',}','}')
    jsdict.append(text)
jsdict.append('];')

# Open the file in write mode ('w') - this will overwrite the file if it exists
with open("website/pokedex_data.js", "w") as file:
    # Add a newline character to each string and write it to the file
    file.writelines(f"{line}\n" for line in jsdict)
print("Data writing complete")

# Here are the rules for how pokedex_data.js is structured:
#     The data contains the full data on every Pokemon, and the structure allows for fast lookups of information.
#     The pokemon must be in the same order as speciesNames in the lang file. This is also the default sort option.
#     The entries for each pokemon can be in any order.
#     dex:    Pokedex number
#     img:    File name of the image
#             Gets the actual image as "ui/{img}_0.png" for tier 0 (non-shiny)
#     t1, t2, a1, a2, ha, pa: Types, Abilities, Hidden Ability, Passive
#             Contains the Filter ID (FID) that corresponds to the type/ability described
#             An entry is omitted if it does not apply to the pokemon
#     bst, hp, atk, def, spa, spd, spe: Stats
#     e1, e2, e3, e4: Egg moves
#             Contains the Filter ID (FID) of the corresponding move
#     co: Base cost of the pokemon
#     et: Egg tier      
#             0 = common, 1 = rare, 2 = epic, 3 = manaphy, 4 = legendary
#     sh: Number of shiny variants the Pokemon has
#             Either 1 (no variants), or 3 (all variants)
#     ge: Which generation the pokemon is in
# vvv All the remaining entries are omitted if not applicable to the pokemon
#     fe: If the Pokemon has a female form
#             Value is 1 if they have traditional sprite differences, like Venusaur
#             Value is 2 if they have named female forms, like Meowstic
#     fa: Which family the pokemon is in
#             This is used for the "Related To" filters
#             Contains the FID that corresponds to that family filter
#     st: Value is 1 if the Pokemon is available from starter select (i.e. being the lowest evolution)
#     ev: Value is 1 if the Pokemon is fully evolved (single stage pokemon have 'st' and 'ev')
#     fs: Value is 1 if the Pokemon is available in fresh start (i.e. being a first partner pokemon)
#     nv: Value is 1 if the Pokemon had new variants recently added
#     fx: If the Pokemon is form exclusive
#             Value is 1 for Mega
#             Value is 2 for New mega
#             Value is 3 for Giga
#             Value is 4 for item form changes or temporary form changes
#     ex: If the Pokemon is egg exclusive
#             Value is 1 for traditional egg exclusives, like Arceus
#             Value is 2 for baby Pokemon, like Pichu
#             Value is 3 for paradox egg exclusives, like Scream Tail
#             Value is 4 only for Eternatus
#             Value is 5 only for Starmobile Revavroom
#     numerical entries: These are like FID:value
#             FID is the Filter ID, which can be a type, ability, move, biome
#             value is how that pokemon relates to that FID (this is different depending on the FID)
#             Do not include entries that don't apply to that pokemon
#             For Moves: (i.e. 876:204, 328:1, 1125:209, or anything like that)
#                     fidThreshold[1] <= FID < fidThreshold[2]
#                     value shows how the pokemon learns the move
#                             -1:mushroom, 0:evo, 1-200:level, 
#                             201:egg&commonTM, 202:egg&greatTM, 203:egg&ultraTM, 204:egg,
#                             205:rareEgg&commonTM, 206:rareEgg&greatTM, 205:rareEgg&ultraTM, 208:rareEgg,
#                             209:commonTM, 210:greatTM, 211: ultraTM
#             For Types: (i.e. 9:307)
#                     fidThreshold[0] <= FID < fidThreshold[1]
#                     value shows which slot the pokemon has that type (307 = type1, 308 = type2)
#                     This data is technically redundant but allows for faster lookups
#             For Abilities: (i.e. 18:309)
#                     fidThreshold[1] <= FID < fidThreshold[2]
#                     value shows which slot the pokemon has that ability (309 = ab1, 310 = ab2, 311 = ha, 312 = pa)
#                     This data is technically redundant but allows for faster lookups
#             For Biomes: (i.e. 1197:[80,100])
#                     fidThreshold[8] <= FID < fidThreshold[9]
#                     value is an array describing the encounter types in that biome
#                             Each of those entries encodes the encounter rarity and time of day
#                             Each rarity is a number:
#                                     20 = COMMON,  40 = UNCOMMON,  60 = BOSS,  80 = RARE,  100 = BOSS_RARE,
#                                     120 = SUPER_RARE,  140 = BOSS_SUPER_RARE,  160 = ULTRA_RARE,  180 = BOSS_ULTRA_RARE
#                             If a pokemon is only available at a certain time of day, it has a modifier added to that number
#                                     +1 for dawn, +2 for day, +4 for dusk, +8 for night
#                                     Modifiers are added together if the Pokemon is available during more than one time of day
#                             If there is more than one entry for encounter types that are always put in a predictable order
#                                     The first entry is the most common nonboss encounter
#                                     The second entry is the most common boss encounter
#                                     Entries beyond the second can be in any order
#                                     If a pokemon is only Boss encounters, the first entry is the lowest number
#                     For example, Amoonguss has 1201:[32,72,83,103]
#                             This means it is in the Jungle (FID = 1201)
#                             The rarities are Common (Dusk, Night), Boss Common (Dusk, Night), Rare (Dawn, Day), Boss Rare (Dawn, Day)

print("Filter writing complete\n\n=========== ALL DONE ===========\n")