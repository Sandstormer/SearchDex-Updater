# =====  This reads all the balance files from the official github  =====
# =====    It links all the data between evolutions and forms       =====
# ===== It saves the data in an optimized format as pokedex_data.js =====
# After running, you should use git to compare changes made to pokedex_data.js
# There are rules at the bottom of this file for how pokedex_data.js is structured

pathBal  = './game_files/src/data/balance' # File path to the balance files
pathImg = './website/images' # Path to read processed images from updateImages.py

import re, os, copy, json
def is_numeric(value): # Function to determine if a value is numeric
    return re.match(r'^-?\d+(\.\d+)?$', str(value)) is not None
def format_for_disp(arg): # Remove spaces, and convert _ and - to spaces, then capitalize
    return arg.replace(' ','').replace('_',' ').replace('-',' ').title()
def format_for_attr(arg): # Remove spaces, all lower case
    return arg.replace(' ','').lower()
def throwError(text = ''):
    print(f'***** Major Error Found ¯\_(ツ)_/¯\n***** {text}')
    breakpoint()
    print('***** Ignoring error...')

# Open and read the file of main data *******************************
with open(f"{pathBal}/pokemon-species.ts", "r", encoding="utf-8", errors="replace") as file:
    content = file.read()
# Use a regular expression to extract text between the markers
raw_data = re.findall(r'PokemonSpecies\[\]\)\.push\((.*?)\);\n}', content, re.DOTALL)[0]
print('\nLoading data...')

# Counter to keep track of incrementing numbers
species_counter = [1]  # Use a list to allow updates within a nested function
# Replacement function to substitute "Species." with incremented numbers
def replace_species(_):
    current_number = species_counter[0]
    species_counter[0] += 1
    return f"{current_number}, {current_number}, "
raw_data = re.sub(r'SpeciesId\.', replace_species, raw_data)
# Replace object prefixes
raw_data = re.sub(r'\bPokemonType\.', '', raw_data)
raw_data = re.sub(r'\bAbilityId\.', '', raw_data)
raw_data = re.sub(r'\bGrowthRate\.', '', raw_data)
raw_data = re.sub(r'\bSpeciesFormKey\.', '', raw_data)
raw_data = re.sub(r'\s+new\sPokemonSpecies\(', '\nrow, , ,', raw_data)
raw_data = re.sub(r'\s+new\sPokemonForm\(', '\nrow,form,parent,', raw_data)
raw_data = re.sub(r'\s+\),', '', raw_data)
raw_data = re.sub(r'\"', '', raw_data)
raw_data = raw_data.strip().split('\n') # Split lines
raw_data = [re.split(r'\),|,', line) for line in raw_data] # Split arguments on each line
raw_data = [[format_for_disp(arg) for arg in line] for line in raw_data] # Format the text

# Assign the parent rows to the alternate forms
parentCurrent = 0
for i in range(len(raw_data)):
    raw_data[i][0] = i # Add the row number at the start of all rows
    if raw_data[i][2] == 'Parent': # If it has been marked as needing a parent row
        raw_data[i][2] = parentCurrent
    else:
        parentCurrent = raw_data[i][0] # Parent is the row of base form
print('Finished reading species')

# Open and read the evolutions file ************************************
with open(f"{pathBal}/pokemon-evolutions.ts", "r", encoding="utf-8", errors="replace") as file:
    content = file.read()
# Use a regular expression to extract text between "PokemonEvolutions = {" and "};"
inputEvoData = re.findall(r'PokemonEvolutions = {(.*?)};', content, re.DOTALL)[0]
inputEvoData = re.sub(r'\[SpeciesId\.', '[', inputEvoData)
inputEvoLines = re.split('],\n', inputEvoData)
result = []
for line in inputEvoLines:
    row = [re.findall(r'\[(\w+)\]:', line)[0]]  # First entry is the species name
    row.extend(re.findall(r'SpeciesId\.(\w+),', line)) # Grab the evolutions from the text 
    result.append(row)
# Apply formatting to all arguments
evolution_data = [[format_for_disp(arg) for arg in line] for line in result]
print('Finished reading evolutions')

# Open and read all the moves files ************************************
with open(f"{pathBal}/pokemon-level-moves.ts", "r", encoding="utf-8", errors="replace") as file: # Level up moves for species ***********************
    content = file.read()
# Use a regular expression to extract text between "pokemonSpeciesLevelMoves = {" and "PokemonSpeciesLevelMoves"
inputMoveData = re.findall(r'pokemonSpeciesLevelMoves\s*=\s*\{(.*?)PokemonSpeciesLevelMoves', content, re.DOTALL)[0]
inputMoveData = re.sub(r'\[.*SpeciesId\.', '[', inputMoveData)
inputMoveData = re.sub(r'MoveId\.', '', inputMoveData)
inputMoveData = re.split(r'\n\s*],', inputMoveData)
levelMoveData = [re.findall(r'\[(.*)\]', line) for line in inputMoveData]
levelMoveData = [[format_for_disp(arg) for arg in line] for line in levelMoveData]
levelMoveData = [[re.split(',', arg) for arg in line] for line in levelMoveData]
# Put all move data into a unified 4D list
# [species, [[levelmove,src],[]], [[eggmove,src],[]], [[tmmove,src],[]]]
# src = -1:mushroom, 0:evo, 1-200:level, 201-203:egg&TM, 204:egg, 205-207:rare&TM, 208:rare, 209-211:comm/great/ultra TM
# Moves learned by egg AND by TM are encoded later
moveBySpecToCat = {}
for line in levelMoveData:
    moveBySpecToCat[line[0][0]] = [[],[],[]]
    for j in range(1,len(line)):
        if line[j][0] == 'Evolve Move':
            line[j][0] = 0
        if line[j][0] == 'Relearn Move':
            line[j][0] = -1
        if int(line[j][0]) > 100:
            throwError(f'High level move found: {line[0][0]} {line[j]}')
        # Level moves are added to [0] in moveBySpecToCat[species], along with their level
        moveBySpecToCat[line[0][0]][0].append([line[j][1], int(line[j][0])])
print('Finished reading level moves')
with open(f"{pathBal}/moves/egg-moves.ts", "r", encoding="utf-8", errors="replace") as file: # Egg moves **************************
    content = file.read()
# Use a regular expression to extract text between "speciesEggMoves = {" and "} satisfies"
inputMoveData = re.findall(r'speciesEggMoves\s*=\s*{(.*?)}\ssatisfies', content, re.DOTALL)[0]
inputMoveData = re.sub(r'\[.*SpeciesId\.', '[', inputMoveData)
inputMoveData = re.sub(r'MoveId\.', '', inputMoveData)
inputMoveData = re.split(r',\n', inputMoveData)
eggMoveData = [re.findall(r'\[(.*)\]', line) for line in inputMoveData]
eggMoveData = [format_for_disp(line[0]) for line in eggMoveData]
eggMoveData = [re.split('\]:\[', line) for line in eggMoveData]
eggMoveData = [[line[0], re.split(',', line[1])] for line in eggMoveData]
for eggLine in eggMoveData:
    if eggLine[0] in moveBySpecToCat:
        for k in range(4):
            # Egg moves are added to [1] in moveBySpecToCat[species], encoded as 204(common) or 208(rare)
            moveBySpecToCat[eggLine[0]][1].append([eggLine[1][k],204+(k==3)*4])
    else:
        print('egg species not found')
print('Finished reading egg moves')
with open(f"{pathBal}/tm-species-map.ts", "r", encoding="utf-8", errors="replace") as file: # Read the file of TM moves ************************
    content = file.read()
# Use a regular expression to extract text of each TM separately
inputMoveData = re.findall(r'\[(MoveId\..*?)\n\s\s\],', content, re.DOTALL)
inputMoveData = [re.split(r'\]:\s?\[', line) for line in inputMoveData]
inputMoveData = [[line[0], re.split('\n', line[1])] for line in inputMoveData]
with open(f"{pathBal}/tms.ts", "r", encoding="utf-8", errors="replace") as file: # Read the file of TM tiers
    content = file.read()
# Use a regular expression to extract text between "TmPoolTiers = {" and "};" from TM Tier data
tierData = re.findall(r'TmPoolTiers\s*=\s*{(.*?)\n};', content, re.DOTALL)[0]
tierData = re.split(r',\n', tierData)
tierData = [[format_for_disp(re.findall(r'MoveId\.(.*?)\]',line)[0]),format_for_disp(re.split(r'ModifierTier\.',line)[1])] for line in tierData]
for line in tierData:
    if "Common" in line[1]:
        line[1] = 209
    elif "Great" in line[1]:
        line[1] = 210
    elif "Ultra" in line[1]:
        line[1] = 211
    else:
        throwError(f'Could not parse TM tier {line}')
TMtier_dict = {thisTierLine[0]: thisTierLine[1] for thisTierLine in tierData}
for line in inputMoveData:
    moveName = format_for_disp(line[0].split("MoveId.")[1].strip()) # Get the move name
    baseSpecies = ''
    speciesListForThisTM = []
    prevSpecLine = ''
    # Format the list of species and forms that can learn it
    for specLine in line[1]:
        if "SpeciesId." in specLine:
            specLine = format_for_disp(re.findall(r'SpeciesId\.(.*?),\s*',specLine)[0])
            if "[" in prevSpecLine:
                baseSpecies = specLine.replace(' ','-') # Set this as the species for forms listed below it
            else:
                speciesListForThisTM.append(specLine)
        elif '"' in specLine:
            specLine = specLine.split('"')[1] # Get the form key
            specLine = specLine.replace('low-key','lowkey') # Override for toxtricity
            if specLine == "":
                specLine = 'Normal' # Add 'normal' to species name if form key is blank
            speciesListForThisTM.append(format_for_disp(f"{specLine}-{baseSpecies}")) # Add form name and species name
        prevSpecLine = specLine
    # For each species, add the TM to the big move dict
    for species in speciesListForThisTM:
        if species not in moveBySpecToCat: # Forms with unique TM learnset will not have an entry yet
            moveBySpecToCat[species] = [[],[],[]] 
        moveBySpecToCat[species][2].append([moveName, TMtier_dict[moveName]]) # Add the TM to each pokemon's compatible moves
print('Finished reading TM moves')
print('Finished reading all moves')

# Currently, base species and forms have different formats in raw_data
# full_data puts base species and forms into a consistent data format
full_data = [] 
for i,line in enumerate(raw_data):
    full_data.append([])
    newLine = full_data[-1]
    parentLine = raw_data[ i if line[2] == '' else int(line[2]) ] # Get the parent row (itself for base species)
    # I always use [2] (parent row) to tell if an entry is a form (it will be blank for base species)
    if line[2] == '': # For base species, not forms
        # row number [0], form key [1], parent row number [2], dex number [3], image filename [4], display name [5]
        newLine.extend(line[0:6]) 
        newLine.append(line[10]) # Species description (unused) [6]
        newLine.append(line[11]) # Type 1 [7]
        newLine.append('' if line[12] == 'Null' else line[12]) # Type 2 [8]
        newLine.append(line[15]) # Ability 1 [9]
        newLine.append('' if line[16] == line[15] or line[16] == 'None' else line[16]) # Ability 2 [10]
        newLine.append('' if line[17] == line[15] or line[17] == 'None' else line[17]) # Hidden ability [11]
        newLine.append('') # [12] Passive (filled in later)
        newLine.extend(line[18:26]) # [13-19] Stats, [20] Catch rate
    else: # For forms
        newLine.append(line[0]) # row number [0]
        newLine.append(line[4]) # form key [1]
        newLine.append(line[2]) # parent row number [2]
        newLine.append(parentLine[3]) # dex number [3]
        if line[4] == '': 
            # If the form key is blank, like a 'normal' form, just use the species name
            newLine.append(parentLine[4]) # image filename [4]
            newLine.append(parentLine[5]) # display name [5]
        else: # If it is a named form
            spriteName = f'{parentLine[4]}-{line[4]}'
            newLine.append(spriteName.replace(" ", "-")) # image filename [4]
            newLine.append(f'{line[4]} {parentLine[5]}') # display name [5]
        newLine.append(parentLine[10]) # Species description (unused) [6]
        newLine.append(line[5]) # Type 1 [7]
        newLine.append('' if line[6] == 'Null' else line[6]) # Type 2 [8]
        newLine.append(line[9]) # Ability 1 [9]
        newLine.append('' if line[10] == line[9] or line[10] == 'None' else line[10]) # Ability 2 [10]
        newLine.append('' if line[11] == line[9] or line[11] == 'None' else line[11]) # Hidden ability [11]
        newLine.append('')          # [12] Passive (filled in later)
        newLine.extend(line[12:19]) # [13-19] Stats
        newLine.append(parentLine[25]) # [20] Catch rate
        
    newLine.extend(parentLine[28:31])  # growthRate [21], malePercent [22], femDiff [23]
    newLine.extend(['','','','']) # Add 4 empty lines for egg moves [24-27]
    newLine.append({}) # Add dict for all moves [28]
    newLine.extend(['','','']) # Add cost [29], egg tier [30], shiny variants [31]
    newLine.append(line[6] if line[2] == '' else parentLine[6]) # Generation [32]

    # isStartable [33] is if that species is available in starter select (i.e. has not evolved yet)
    # This is separate from: form exclusives [41] and fully evolved [44]
    isStartable = ''
    if newLine[5] in moveBySpecToCat: # Anything with egg moves is startable, plus Pikachu
        if moveBySpecToCat[newLine[5]][1] or 'Pikachu' in newLine[5]:
            isStartable = 1
    newLine.append(isStartable)

    newLine.append('') # starterRow [34] is the row of starter evo (similar to [2] being row of parent)
    newLine.append('') # starterIndex [35] is the speciesID [36] of the starter evo
    newLine.append('') # speciesID [36] is the number for lookup on the SearchDex
    newLine.append(parentLine[5]) # specKey [37] is the text of just the Species (no form, except regionals)
    # specKey is used for "Related" filters, and translation lookup of species
    newLine.extend(['','',[]]) # familyFID [38], freshStart [39], biomes [40]
    
    # Form exclusive [41] ('' = starter, 1 = mega, 2 = new mega, 3 = giga, 4 = transformed)
    name = newLine[5]
    formExclusive = '' # Startable by default, for base species and most forms
    # In the game data, argument 24 defaults to False (Forms are exclusive unless marked otherwise)
    # Check for mega, giga, or other transformed (Zacian, Mimikyu, etc.)
    if line[2] != '' and (len(line) < 25 or 'True' not in line[24]): formExclusive = 4
    megaList = ['Mega Clefable','Mega Victreebel','Mega Starmie','Mega Dragonite','Mega Meganium','Mega Feraligatr','Mega Skarmory','Mega Froslass','Mega Emboar','Mega Excadrill','Mega Scolipede','Mega Scrafty','Mega Eelektross','Mega Chandelure','Mega Chesnaught','Mega Delphox','Mega Greninja','Mega Pyroar','Mega Floette','Mega Malamar','Mega Barbaracle','Mega Dragalge','Mega Hawlucha','Mega Zygarde','Mega Drampa','Mega Falinks','Mega Raichu X','Mega Raichu Y','Mega Chimecho','Mega Baxcalibur']
    if 'Mega ' in name:      formExclusive = 1 # Mega (needs the space)
    if name in megaList:     formExclusive = 2 # New Mega
    if 'Gigantamax' in name: formExclusive = 3 # Giga
    # In-game, the form is chosen from getSpeciesFormIndex in src/battle-scene.ts
    # Some forms have the wrong isStarterSelectable in balance/pokemon-species.ts (error with the game code)
    if 'Minior'   in name and 'Meteor' not in name: formExclusive = 4  # Force minior core to count as transformed
    if 'Maushold' in name or 'Dudunsparce' in name: formExclusive = '' # Force those forms to be not exclusive
    newLine.append(formExclusive)

    # Unobtainable [42] (forms must be listed as 'True' in raw_data[i][25])
    unobtainable = 0 # Can be obtained, by default
    if line[2] != '' and len(line) > 25 and 'True' in line[25]: unobtainable = 1
    if 'Revavroom' in parentLine[5]: unobtainable = 0 # Keep Starmobiles
    if '10 Complete' in line[4]: unobtainable = 1 # Remove "Complete 10% Zygarde"
    if 'Mega Starmie' in line[4]: unobtainable = 1 # Remove "Mega Starmie"
    newLine.append(unobtainable) # Unobtainable [42]

    newLine.append('') # Newly added variants [43]
    newLine.append(1)  # Fully Evolved [44] ('' = can evolve, 1 = fully evolved)
    newLine.append('') # Exclusive class [45] ('' = regular, 1 = eggExc, 2 = baby, 3 = paradox, 4 = eterna, 5 = starmobile)
print('Finished normalizing data')

# Parse the data for starter costs ****************************
with open(f"{pathBal}/starters.ts", "r", encoding="utf-8", errors="replace") as file:
    content = file.read()
# Use a regular expression to extract text between "speciesStarterCosts = {" and "};"
inputCostData = re.findall(r'speciesStarterCosts = {(.*?)};', content, re.DOTALL)
if not inputCostData: throwError('Could not find cost data')
costSpecies = re.findall(r'\[SpeciesId\.(.*)\]:', inputCostData[0])
costValues  = re.findall(r'\]: (.*),', inputCostData[0])
for i in range(len(costSpecies)):
    isFound = False
    for line in full_data:
        if line[5] == format_for_disp(costSpecies[i]):
            isFound = True
            line[29] = int(costValues[i])
    if not isFound:
        throwError(f'Could not assign cost of {costSpecies[i]}')
print('Finished assigning base costs')
# Parse the data for starter egg tiers ****************************
with open(f"{pathBal}/species-egg-tiers.ts", "r", encoding="utf-8", errors="replace") as file:
    content = file.read()
# Use a regular expression to extract text between "speciesEggTiers = {" and "};"
inputTierData = re.findall(r'speciesEggTiers\s*=\s*{(.*?)};', content, re.DOTALL)
if not inputTierData: throwError('Could not find tier data')
tierSpecies = re.findall(r'\[SpeciesId\.(.*)\]:', inputTierData[0])
tierValues  = re.findall(r'EggTier\.(.*)\n', inputTierData[0])
for i,tierLine in enumerate(tierSpecies):
    isFound = False
    for line in full_data: # Find the species name
        if line[5] == format_for_disp(tierLine) and line[2] == '':
            isFound = True
            line[34] = line[0] # starterRow equals this row
            line[30] = re.sub(',','',tierValues[i])
            if line[5] == 'Phione' or line[5] == 'Manaphy':
                line[30] = 3
            elif line[30] == 'COMMON':
                line[30] = 0
            elif line[30] == 'RARE':
                line[30] = 1
            elif line[30] == 'EPIC':
                line[30] = 2
            elif line[30] == 'LEGENDARY':
                line[30] = 4
            else:
                print('Could not parse tier')
    if not isFound:
        print(f'Could not assign egg tier of {tierLine}')
print('Finished assigning base egg tiers')

# Open and read the biomes file ************************************
# Find the file of each biome in the biome folder, and parse the encounter data
biomeData = {}
allBiomes = [file.replace('.ts','') for file in os.listdir(f"{pathBal}/biomes") if '.ts' in file]
allBiomes.sort()
for biome in allBiomes:
    with open(f"{pathBal}/biomes/{biome}.ts", "r", encoding="utf-8", errors="replace") as file:
        content = file.read()
    # Use a regular expression to extract text between "BiomePokemonPools = {" and "};"
    inputBiomeData = re.findall(r'BiomePokemonPools = {(.*?)};', content, re.DOTALL)[0]
    biomeData[biome] = { # biomeData[biome][tier][timeOfDay] = [speciesNames]
        tierLine.split(']:')[0]: {
            timeLine.split(']:')[0]: re.findall(r'SpeciesId.(.*?)[,\]]', timeLine.split(']:')[1], re.DOTALL)
            for timeLine in tierLine.split('TimeOfDay.')[1:]
        }
        for tierLine in inputBiomeData.split('BiomePoolTier.')
    }
biomeTierValues = { 'COMMON':20, 'UNCOMMON':40, 'BOSS':60, 'RARE':80, 'BOSS_RARE':100, 'SUPER_RARE':120, 'BOSS_SUPER_RARE':140, 'ULTRA_RARE':160, 'BOSS_ULTRA_RARE':180 }
biomeTimeValues = { 'ALL':0, 'DAWN':1, 'DAY':2, 'DUSK':4, 'NIGHT':8 }
for biome, biomeLine in biomeData.items():
    for tier, tierLine in biomeLine.items():
        for time, timeLine in tierLine.items():
            for species in timeLine:
                tierCode = biomeTierValues[tier] + biomeTimeValues[time]
                for specLine in full_data:
                    if format_for_disp(species) == specLine[5]: # Assign biome data to base species
                        specLine[40].append([biome, tierCode]) # New entry for that biome
# Structure of line[40] is like [ ['abyss', 23], ['abyss', 41], ['beach', 160], [...] ]
# Same tier at multiple times of day are combined in a later step
print('Finished assigning base biomes')

# Open and read the file of passives ***********************************
with open(f"{pathBal}/passives.ts", "r", encoding="utf-8", errors="replace") as file:
    content = file.read()
# Use a regular expression to extract text between the markers
inputPassiveData = re.findall(r'StarterPassiveAbilities\s*=\s*{\n(.*?)\n};', content, re.DOTALL)[0]
inputPassiveData = re.split('\n',inputPassiveData)
inputPassiveData = [line for line in inputPassiveData if 'SpeciesId.' in line]
passive_species = [re.findall(r'SpeciesId\.(.*?)]', line)[0] for line in inputPassiveData]
passive_species = [format_for_disp(line) for line in passive_species]
passive_abilities = [re.findall(r'AbilityId\.(.*?)[,\s]', line) for line in inputPassiveData]
passive_abilities = [[format_for_disp(arg) for arg in line] for line in passive_abilities]
print('Finished reading passives')
for passiveIndex in range(len(passive_species)): # Assign passives from list of passives *****
    for i in range(len(full_data)): # Find the base species that matches that passive
        if passive_species[passiveIndex] == full_data[i][5] and full_data[i][2] == '':
            full_data[i][12] = passive_abilities[passiveIndex][0] # Assign the passive to the base species
            if len(passive_abilities[passiveIndex]) > 1:
                # If the passive is a list (for those Pokemon's forms)
                for formInd in range(len(passive_abilities[passiveIndex])):
                    if full_data[i+1+formInd][2] != '': # It has to be a form
                        # Assign the passive to the forms in order
                        # Reminder that full_data has the base species, and then form0, form1, etc.
                        # (base species and form0 will use the same passive)
                        # (base species is trimmed later in this script)
                        full_data[i+1+formInd][12] = passive_abilities[passiveIndex][formInd]
                    else:
                        throwError(f'Passive error: {passive_species[passiveIndex]} {passive_abilities[passiveIndex]}')
            break
print('Finished assigning passives')

# Add only egg moves to the attributes and dictionary
for line in full_data:
    if line[5] in moveBySpecToCat and line[2] == '': # Only for base species
        if moveBySpecToCat[line[5]][1]:
            if len(moveBySpecToCat[line[5]][1]) != 4:
                print(f'Weird number of egg moves found in {line[5]}')
            line[24:28] = [eggLine[0] for eggLine in moveBySpecToCat[line[5]][1]] # Put egg moves in [24-27]
            for move in moveBySpecToCat[line[5]][1]:
                if move[0] not in line[28]:
                    line[28][move[0]] = move[1] # Add the move to the dict
print('Finished assigning egg moves')

# Propagate egg moves and other data via evolution **************************
for stages in range(2): # Up to 2 evolutions
    for evoLine in evolution_data: # Assign data through evolution **********
        for childLine in full_data:
            if evoLine[0] == childLine[5]: # Find the childLine, break when matching
                childLine[44] = '' # Set the child to not be fullyEvolved
                break
        else: # If the child search loop fails to break
            throwError(f'Failed to find pre-evo {evoLine[0]}')
        for parentName in evoLine[1:]:
            for parentLine in full_data:
                if parentName == parentLine[5]: # Copy properties from child to parent
                    parentLine[24:28] = childLine[24:28]          # Egg moves
                    parentLine[28] = copy.deepcopy(childLine[28]) # All moves
                    parentLine[29:31] = childLine[29:31]          # Cost, egg tier
                    parentLine[34] = childLine[34]                # Starter row
                    for biomeLine in childLine[40]:
                        parentLine[40].append(biomeLine)
                    break # Break the parent search loop
            else: # If the parent search loop fails to break
                throwError(f'Failed to find post-evo: {parentName}')
# The game usually only provides biome data to one species per evolution line
# The evolution stage is upgraded/downgraded by determineEnemySpecies in file:///\.\game_files\src\data\pokemon-species.ts
# Biome propagation (line[40]) in my code must be done in a particular way: forward twice, then backward twice
# That prevents split evolutions from influencing each other (e.g. Dustox/Beautifly)
# Structure of line[40] is like [ ['abyss', 23], ['abyss', 41], ['beach', 160], [...] ]
for stages in range(2): # Up to 2 evolutions
    for evoLine in evolution_data: # Assign biome data backwards
        for childLine in full_data:
            if evoLine[0] == childLine[5]: # Find the childLine, break when matching
                break
        else: # If the child search loop fails to break
            throwError(f'Failed to find pre-evo {evoLine[0]}')
        for parentName in evoLine[1:]:
            for parentLine in full_data:
                if parentName == parentLine[5]: # Copy biomes from parent to child (reverse)
                    # tyrogue,smoochum,elekid,magby,wynaut,toxel
                    # These babies can appear in the wild, because they are level evolutions
                    # Friendship evolutions cannot devolve at low levels
                    for biomeLine in parentLine[40]:
                        childLine[40].append(biomeLine)
                    break # Break the parent search loop
            else: # If the parent search loop fails to break
                throwError(f'Failed to find post-evo: {parentName}')

for line in full_data: # Assign data through forms **********************
    if line[2] != '': # Only for forms
        parentLine = full_data[int(line[2])]
        if line[12] == '':
            line[12] = parentLine[12]
            print('** Assigned parent passive to',line[5])
        line[24:28] = parentLine[24:28]
        line[28] = copy.deepcopy(parentLine[28])
        line[29:31] = parentLine[29:31]
        line[33] = parentLine[33] # isStartable
        line[34] = parentLine[34] # starterRow
        line[40] = parentLine[40] # Inherit biomes, even on exclusive forms
        line[44] = parentLine[44] # Inherit fullyEvolved
print('Finished propagating data to evolutions and forms')
for line in full_data: # Check for empty properties in full_data
    if line[12] == '':
        throwError(f'Missing Passives: {line[5]}')
    if line[24:28] == '':
        throwError(f'Missing Egg Moves: {line[5]}')
    if line[29] == '' or line[29] == 0:
        throwError(f'Missing Cost: {line[5]}')
    if line[30] == '' or line[30] == -1:
        throwError(f'Missing Egg Tier: {line[5]}')
    if line[40] == []:
        line[45] = 1 # Exclusive to egg
        if 'Pichu' in line[5]: # Manual override for spiky pichu bc it is missing evo hookup
            line[45] = 2 # Exclusive to baby
        for evoLine in evolution_data:
            if evoLine[0] == line[5]:
                for parentName in evoLine[1:]:
                    for parentLine in full_data:
                        # Make sure Meltan doesn't count as a baby
                        if parentName == parentLine[5] and parentLine[40] != []:
                            line[45] = 2 # Exclusive to baby
                            break
        if line[45] == 1:
            print('Egg Exclusive:',line[5])
        if line[45] == 2:
            print('Baby Egg Exclusive:',line[5])
    elif line[40] != [] and line[40][0][0] == 'end':
        if 'Eternatus' in line[5]:
            # print('Eternatus:',line[5])
            line[45] = 4
        else:
            # print('Paradox:',line[5])
            line[45] = 3
    if 'Starmobile' in line[5]:
        line[40] = []
        line[41] = '' # Not form exclusive
        line[45] = 5  # Just unobtainable
        # print('Starmobile:',line[5])
    # if line[41] and line[45]:
    #     print('Double exclusive:',line[5],line[41],line[45])
    if line[40] == [] and line[45] == -1:
        throwError(f'Missing Biomes: {line[5]}')

# How assigning moves is done:
    # Assign egg moves to first evolution
    # Propagate egg moves through evolutions and forms
    # Add level up moves and TM moves to base species
    # Add unique level up moves to forms
        # If those don't exist, get the level up moves from base species
    # Inherit TM moves from base species to forms
    # Also add unique TM moves to forms
    
# Add level up and TM moves to all the base species
# src = -1:mushroom, 0:evo, 1-200:level, 201-203:egg&TM, 204:egg, 205-207:rare&TM, 208:rare, 209-211:TM
for line in full_data:
    if line[2] == '': # Only for base species
        if line[5] in moveBySpecToCat:
            moveBySpecToCat[line[5]].append('done')
            for move in moveBySpecToCat[line[5]][0]+moveBySpecToCat[line[5]][2]:
                if move[0] not in line[28]:
                    line[28][move[0]] = move[1] # Add level and TM moves to base species
                else:
                    if line[28][move[0]] in [204,208] and move[1] > 208:
                        line[28][move[0]] += move[1]-212 # Encode the move as an egg move and a TM
                        # print('Multi-source move',move[0],'on',line[5],': source',line[28][move[0]],'and',move[1])
        else:
            throwError(f'Failed to find base species {line[5]}')

# Parse the level up moves for alternate forms
with open(f"{pathBal}/pokemon-level-moves.ts", "r", encoding="utf-8", errors="replace") as file: # Level up moves for alt forms ****
    content = file.read()
# Use a regular expression to extract text between "pokemonFormLevelMoves = {" and "} as PokemonSpeciesFormLevelMoves"
inputMoveData = re.findall(r'pokemonFormLevelMoves = {(.*?)} as PokemonSpeciesFormLevelMoves', content, re.DOTALL)[0]
inputMoveData = re.sub(r'\[.*SpeciesId\.', '[', inputMoveData)
inputMoveData = re.sub(r'MoveId\.', '', inputMoveData)
inputMoveData = re.split(r'\n\s*},', inputMoveData)
formLevelSpecies = [re.findall(r'\[(.*)\]:', line) for line in inputMoveData]
formLevelSpecies = [format_for_disp(line[0]) for line in formLevelSpecies]
formLevelMoveData = [re.split(': \[', line) for line in inputMoveData]
formLevelMoveData = [[re.findall(r'\s\s\s\s\[(.*)\]', arg) for arg in line] for line in formLevelMoveData]
formLevelMoveData = [[[format_for_disp(u) for u in arg] for arg in line] for line in formLevelMoveData]
formLevelMoveData = [[[re.split(',', u) for u in arg] for arg in line] for line in formLevelMoveData]
# If an alternate form has different level-up moves, add them to the move list (egg moves are there)
for specInd,specLine in enumerate(formLevelMoveData):
    for formInd,formLine in enumerate(specLine):
        if formInd > 0: # The first form (base form) is always blank
            for i in range(len(full_data)):
                # Find the matching base species entry (it will have a blank parent index [2])
                if full_data[i][5] == formLevelSpecies[specInd] and full_data[i][2] == '':
                    thisEntry = full_data[i+formInd+1]
                    # Forms with unique levelup may not have an entry yet
                    if thisEntry[5] not in moveBySpecToCat and len(formLine): 
                        moveBySpecToCat[thisEntry[5]] = [[],[],[]]
                    for move in formLine:
                        if move[0] == 'Evolve Move':
                            move[0] = 0
                        elif move[0] == 'Relearn Move':
                            move[0] = -1
                        move[0], move[1] = move[1], int(move[0])
                        moveBySpecToCat[thisEntry[5]][0].append([move[0], move[1]]) # Add to level up moves
# Assign TM moves and level moves to forms: ==================
# If the form doesn't have a unique moveset, inherit that from the base species
    # If it does, only inherit TM moves
# Either way, add TM moves that are unique to forms (in addition to the inherited TM moves)
for line in full_data: 
    if line[2] != '': # Only for forms
        # Determine the name of the form, for lookup in moveBySpecToCat
        # TMs are only given from the base species (not from the 'normal' form) to their forms
        if line[1] == '': 
            formName = f'Normal {line[5]}' # Add 'Normal' to distinguish from base species, like Normal Calyrex
        else:
            formName = line[5]
        parentName = full_data[int(line[2])][5]

        if formName in moveBySpecToCat: # If that form has specific moves (either level or TM)

            # If there are unique level up moves, import them =======
            if len(moveBySpecToCat[formName][0]):
                for move in moveBySpecToCat[formName][0]:
                    if move[0] not in line[28]:
                        line[28][move[0]] = move[1] # Add unique level moves
                print('Imported unique level moves for',formName)
            else: # If there are NOT unique level up moves =======
                if parentName in moveBySpecToCat: 
                    for move in moveBySpecToCat[parentName][0]:
                        if move[0] not in line[28]:
                            line[28][move[0]] = move[1] # Add level moves from parent
                else:
                    throwError(f'Failed to find parent species {parentName}')

            # If there are unique TM moves, import them =======
            if len(moveBySpecToCat[formName][2]): 
                for move in moveBySpecToCat[formName][2]:
                    if move[0] not in line[28]:
                        line[28][move[0]] = move[1] # Add unique TM moves
                    else:
                        if line[28][move[0]] in [204,208] and move[1] > 208:
                            line[28][move[0]] += move[1]-212 # Encode as TM and egg move
                print('Imported unique TMs for',formName)
            # Import parent TMs even if there were unique TMs =======
            if parentName in moveBySpecToCat: 
                for move in moveBySpecToCat[parentName][2]:
                    if move[0] not in line[28]:
                        line[28][move[0]] = move[1] # Add TM moves from parent
                    else:
                        if line[28][move[0]] in [204,208] and move[1] > 208:
                            line[28][move[0]] += move[1]-212 # Encode as TM and egg move
            else:
                throwError(f'Failed to find parent species {parentName}')
            moveBySpecToCat[formName].append('done')

        else: # If that form can't be looked up, it doesn't have unique level/TM moves
            # Copy all moves from parent (level, egg, TM)
            line[28] = copy.deepcopy(full_data[line[2]][28]) 
            
# Check that every entry in moveBySpecToCat was assigned
# A correct moveBySpecToCat[key] looks like [[[levelmove,src],[]], [[eggmove,src],[]], [[tmmove,src],[]], 'done']
for key, value in moveBySpecToCat.items():
    if len(value) > 4:
        throwError(f'Double counted moves in {key}') # Base species will have value[3] = 'done'
    elif len(value) < 4: # If moves could not be assigned from moveBySpecToCat (form-unique moves)
        throwError(f'Failed to assign unique moves to form - Species: {key} - Moves: {value}')

# Species specific manual overrides
for line in full_data:
    if line[3] == '718': # 718 Zygarde override
        for text in ['10','50','Complete']:
            if text in line[5]:
                line[4] = re.sub('-50','',f'718-{text}') # Image path
                line[5] = re.sub('Pc','PC',line[5])      # Species

# Convert full_data into trimmed_data by removing base species and unobtainables
trimmed_data = []
print('\nTrimming base species and unobtainable pokemon...')
for i in range(len(full_data)-1):
    # Keep entries under two scenarios:
    #   If it IS A FORM: because we want to keep all forms
    #   If the next is NOT A FORM: this ensures we keep base species that do not have forms
    # The result is that any base species at the top of form lists get removed
    if full_data[i][2] != "" or full_data[i+1][2] == "": # If it is a form, or next is not
        if not full_data[i][42]: 
            trimmed_data.append(full_data[i]) # Keep everything except for unobtainables
        else:
            print('Unobtainable:',full_data[i][5]) # Should be 2: Unknown Arceus, Zenith Marshadow
    elif full_data[i][3] != full_data[i+1][3]:
        throwError(f"Ignored {full_data[i][5]}") # Show error if removing unique species
trimmed_data.append(full_data[-1]) # Add the last entry

# If the pokemon is from a region, find the original species, to calculate the regional dex number
for line in trimmed_data:
    allRegionValues = { "Alola":2000, "Eternal":2000, "Galar":4000, "Hisui":6000, "Paldea":8000, "Bloodmoon":8000 }
    for regionText, regionValue in allRegionValues.items():
        if regionText in line[5]:
            # Look for a name [5] that matches the regional name with the region removed
            for parentLine in trimmed_data:
                # Floette must be searched for differently because it only has colored forms (not just "Floette")
                if parentLine[5] == line[5].split(f'{regionText} ')[1] or (regionText=="Eternal" and "Floette" in parentLine[5]):
                    line[3] = int(parentLine[3]) + regionValue
                    break
            else:
                print(f'***** Error: Could not find regional dex number for {line[5]}')
            line[3] = str(line[3]) # Set dex number back to a string
            line[4] = line[3] # Replace img with new dex number
            if line[1] != "": line[4] = f'{line[3]}-{line[1]}' # If there is a formKey [1], add that to the image name

# Reminder: isStartable [33], starterRow [34], starterIndex [35], speciesID [36]
for i, line in enumerate(trimmed_data): 
    if line[34] == '': # Check for invalid starter row
        throwError(f'Unassigned starter row for {line[5]}')
    # Trimmed data no longer has base species or unobtainable forms
    # So now we rebase the row numbers as speciesID [36] to be sequential
    # This is the speciesID (SID) on the SearchDex, used to look up data for that species
    line[36] = i
    # Also rebase to sequential numbers for starterIndex [35]
    # This requires finding which row the child is in
    if line[34] == line[0]:
        line[35] = i
    else: # Find which row the child is in
        for j, childLine in enumerate(trimmed_data):
            # If the child is a form, the base row will be gone
            if line[34] == childLine[0] or line[34] == childLine[0]-1:
                line[35] = j
                break
        else:
            throwError(f'Could not find starter row {line[34]} for {line[5]}')
familyList = sorted(list(set([ line[35] for line in trimmed_data ])))

# Determine which pokemon are in fresh start
gen, freshThisGen, freshStarterIndices = 1, 0, []
for line in trimmed_data:
    if int(line[32]) == gen and (line[35] not in freshStarterIndices) and freshThisGen < 3:
        if line[29] < 6:
            freshStarterIndices.append(line[35])
            freshThisGen += 1
    if freshThisGen == 3:
        gen = gen + 1 
        freshThisGen = 0
    if line[35] in freshStarterIndices:
        line[39] = 1

# Error checking **************************************************************************************
print('\n==============================\n')
print('Checking for errors...')

# Use the default image if unique form image does not exist
for i in range(len(trimmed_data)):
    if not os.path.isfile(f'{pathImg}/{trimmed_data[i][4]}_0.png'): # Check if the given img does not exist
        # print(f'{trimmed_data[i][5]}: Could not find {trimmed_data[i][4]}')
        if os.path.isfile(f'{pathImg}/{trimmed_data[i][3]}_0.png'): # Check if the base img exists
            # print(f'{trimmed_data[i][5]}: Replaced {trimmed_data[i][4]} with base image')
            trimmed_data[i][4] = f'{trimmed_data[i][3]}' # Get base image from dexno
        elif trimmed_data[i][3] == trimmed_data[i-1][3]: # If same species as one above
            trimmed_data[i][4] = trimmed_data[i-1][4] # Take image from form above
            if int(trimmed_data[i][3]) not in [1012,1013]: # Report if not Sinistcha family
                print(f'{trimmed_data[i][5]}: Replaced {trimmed_data[i][4]} with {trimmed_data[i-1][4]}')
        else:
            throwError(f'Could not find any image for {trimmed_data[i][4]}_0.png')
# Check for the existence of variant shinies
for line in trimmed_data:
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
for line in trimmed_data:
    check = [0,0,0]
    for value in line[28].values():
        if value < 100:
            check[0] = 1
        if 200 < value < 209:
            check[1] += 1
        if value > 208:
            check[2] = 1
    if check[0] != 1:
        throwError(f'Missing level-up entries in {line[5]}')
    if check[1] != 4:
        throwError(f'Missing egg move entries in {line[5]}')
    if check[2] != 1 and int(line[3]) not in [132, 201, 202, 235, 360, 789, 790] and line[2] == '':
        # If there is a base species that is supposed to have TM moves
        throwError(f'Missing TM move entries in {line[5]}')
    if int(line[32]) not in range(1,10):
        throwError(f'Generation Error in {line[5]}')

# Check that every pokemon has at least one pickable form        
dexNo = -1
for i,line in enumerate(trimmed_data):
    hasStartableForms = 0
    if line[3] != dexNo:
        dexNo = line[3]
        familyNames = []
        for j in range(i, len(trimmed_data)):
            if trimmed_data[j][3] == dexNo:
                familyNames.append(trimmed_data[j][5])
                if not trimmed_data[j][41]: # If not form exclusive, it is startable
                    hasStartableForms = 1
            else:
                break
        if not hasStartableForms:
            if line[5] in moveBySpecToCat and moveBySpecToCat[line[5]][1]: 
                # Show error if a pokemon has egg moves, but no startable forms
                throwError(f'No startable forms found in {familyNames}')
            else:
                print(f'No evolved startable forms in {familyNames}') # Not a problem

# Check that dex numbers are sequential up to 1025
for i in range(1,1026):
    for j in range(i-1,len(trimmed_data)):
        if i == int(trimmed_data[j][3]):
            break
        if j == len(trimmed_data)-1:
            throwError(f'Could not find Dex #{i}')
# Check the final entries
if trimmed_data[-1][5] != "Bloodmoon Ursaluna":
    print(trimmed_data[-5:])
    throwError('Final dex entry is not correct')
if len(trimmed_data) != 1452:
    print(trimmed_data[-5:])
    throwError('Total number of entries is not correct')

# Check that Normal Deoxys has Swift, Icy Wind, and Cosmic Power (and speed, speed, attack)
# Check that Normal/Ice Calyrex has Body Press

# Assemble lists of all filters of each category *****************************
allTypes = ['Bug','Dark','Dragon','Electric','Fairy','Fighting','Fire','Flying','Ghost','Grass','Ground','Ice','Normal','Poison','Psychic','Rock','Steel','Water']
allAbilities = []
for line in full_data:
    for ab_slot in [9,10,11,12]:
        if line[ab_slot] != '' and line[ab_slot] not in allAbilities:
            allAbilities.append(line[ab_slot])
allAbilities.sort()
allMovesDict = {}
for specLine in moveBySpecToCat.values():
    for moveCat in specLine[0:3]:
        for moveLine in moveCat:
            if moveLine[0] not in allMovesDict:
                allMovesDict[moveLine[0]] = ''
allMoves = [*allMovesDict] # Get a list of moves from the move dict
allMoves.sort()
allBiomes = [format_for_disp(biome) for biome in allBiomes]
allBiomes.sort()

# Assign filter ID numbers (FID) to each filter *****************************
allFilters = []  # List of all filters, in numerical order: FID: ['Category','Filter Name']
filterToFID = {} # Get FID from name: e.g. filterToFID('typebug') = FID
# All strings from trimmed_data are encoded as FID before writing to the website data
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
for starterIndex in familyList:
    allFilters.append(['Related To',trimmed_data[starterIndex][37]])
    for line in trimmed_data:
        if line[35] == starterIndex: # If starterIndex is equal to the one in starterList
            line[38] = len(allFilters)-1 # Set familyFID to this fid
for j in ['New','All','None']:
    allFilters.append(['Shiny Variants',j])
for j in ['Lure Ability','Ignores Abilities',"Can't be suppressed","Can't be replaced","Can't be ignored",'Electric Immunity','Fire Immunity','Ground Immunity','Water Immunity','Rain Synergy','Creates Rain','Sand Synergy','Creates Sand','Snow Synergy','Sun Synergy','Creates Sun']:
    allFilters.append(['Tag',j])

# Process the biome data:
# Structure of line[40] is like [ ['abyss', 23], ['abyss', 41], ['beach', 160], [...] ]
# This step encodes that data as [ ['abyss', fid, [23,41]], ['beach', fid, [160]], [...] ]
# Multiple encounters in the same biome are put into a list in that biome (instead of a separate line)
# fid is the numerical filter ID of the biome
biomeForms = [ # manually updated from getSpeciesFormIndex in file:///\.\game_files\src\field\arena.ts
    ['Plant Burmy','Forest'],
    ['Sandy Burmy','Beach'],
    ['Trash Burmy','Slum'],
    ['Plant Wormadam','Forest'],
    ['Sandy Wormadam','Beach'],
    ['Trash Wormadam','Slum'],
]   
biomeFormsTime = [ # manually updated from getSpeciesFormIndex in arena.ts
    ['Midday Lycanroc',[1,2]], # 1=dawn, 2=day, 4=dusk, 8=night
    ['Dusk Lycanroc',[4]],
    ['Midnight Lycanroc',[8]],
]   
for line in trimmed_data:
    encoded = []
    if line[40] != []: # If there are biomes
        for biomeLine in line[40]:
            abort = 0
            # If a species is limited by biome/time, it must pass a check before the biomes are written
            for speciesLine in biomeForms: # Enforce specific BIOME FORMS by matching biome name
                if line[5] == speciesLine[0]:
                    if format_for_disp(biomeLine[0]) != speciesLine[1]:
                        abort = 1
                        # print(line[5],biomeLine[0])
            for speciesLine in biomeFormsTime: # Enforce TIME OF DAY forms by checking remainder of encounter code
                if line[5] == speciesLine[0]:  # Abort if none of the valid times are in the encounter code
                    if all(not(i & (biomeLine[1]%20)) for i in speciesLine[1]):
                        abort = 1
            if not abort:
                # Multiple rarites in the same biome will be grouped together
                newFID = filterToFID[f'biome{format_for_attr(format_for_disp(biomeLine[0]))}']
                for encLine in encoded:
                    if encLine[1] == newFID: # If the biome already exists, add this encounter to the list
                        # In the encounter codes for that biome, check for an entry that matches the rarity
                        for index,existingEncoding in enumerate(encLine[2]):
                            if biomeLine[1]//20 == existingEncoding//20:
                                # Add the time of day together with bitwise OR
                                # If no times are active, it counts as ALL times (15)
                                # If the combination is ALL times, do mod 15 to not show any times
                                timeOfDayEncoding = ( ( biomeLine[1]%20 or 15 ) | ( existingEncoding%20 or 15 ) ) % 15
                                encLine[2][index] = timeOfDayEncoding + existingEncoding//20*20
                                break
                        else: # Add the encounter code as a new rarity
                            encLine[2].append(biomeLine[1])
                        break
                else: # Create a new FID entry for the biome
                    encoded.append([biomeLine[0], newFID, [biomeLine[1]]])
        # for encLine in encoded:
        #     if len(encLine[1]) > 2:
                # print('** More than 2 biome rarites in {line[5]}: {encLine}')
        # if len(encoded) > 3:
            # print(f'** Many biomes ({len(encoded)}) in {line[5]}: {line[40]}')
        line[40] = encoded
# Sort each biome entry to be [norm, boss, rarerNorm, rarerBoss]
# This is important for the website quickly sorting by biome rarity
    # The first entry is the most common nonboss encounter
    # The second entry is the most common boss encounter
    # Entries beyond the second can be in any order
    # If a pokemon is only Boss encounters, the first entry is the lowest number
for line in trimmed_data:
    if isinstance(line[40],list):
        for biomeLine in line[40]:
            encoded = []
            entry = min((x for x in biomeLine[2] if x-x%20 not in [60,100,140,180]), default=None)
            if entry: encoded.append(entry)
            entry = min((x for x in biomeLine[2] if x-x%20 in [60,100,140,180]), default=None)
            if entry: encoded.append(entry)
            for entry in biomeLine[2]:
                if entry not in encoded:
                    encoded.append(entry)
            # print('Changed',biomeLine[1],'to',encoded)
            biomeLine[2] = encoded       

# Find the threshold of types and abilities
fidThreshold = []
catName = allFilters[0][0]
for index,line in enumerate(allFilters):
    if line[0] != catName:
        catName = line[0]
        fidThreshold.append(index)
fidThreshold.append(len(allFilters))
if fidThreshold[0] != 18: throwError('Wrong number of types')
if fidThreshold[1] != 328: throwError('Wrong number of abilities')
if allTypes[-1] != allFilters[fidThreshold[0]-1][1]: throwError('Name error with types')
if allAbilities[-1] != allFilters[fidThreshold[1]-1][1]: throwError('Name error with abilities')
if allMoves[-1] != allFilters[fidThreshold[2]-1][1]: throwError('Name error with moves')

# Write some variables to files
# These are read by my other scripts, and some are written to the website
with open("local_files/my_json/allFilters.json", "w") as f:
    json.dump(allFilters, f, indent=4)
with open("local_files/my_json/fidThreshold.json", "w") as f:
    json.dump(fidThreshold, f, indent=4)
with open("local_files/my_json/filterToFID.json", "w") as f:
    json.dump(filterToFID, f, indent=4)
# Save all the names: [displayname/form/species] (regional is included in species)
allSpecies = [[line[5],line[1],line[37]] for line in trimmed_data]
with open("local_files/my_json/allSpecies.json", "w") as f:
    json.dump(allSpecies, f, indent=4)

input('\nNo Major Errors Found\nContinue to patch review?')
print('\n==============================\n')
print("Reviewing patch changes...\n")

# Patch note creating **********************************************************************************
# This makes it easy to see what has changed in the new data, by comparing to trimmed_data_prev.json
# To re-base the comparison, you must manually replace trimmed_data_prev.json with data from trimmed_data.json
# trimmed_data_prev_shvar.json should only be re-based right before adding new variants
with open("local_files/trimmed_data.json", "w", encoding="utf-8") as f:
    json.dump(trimmed_data, f, ensure_ascii=False, indent=4) # Write all the trimmed data to a json file
with open("local_files/trimmed_data_prev.json", "r", encoding="utf-8", errors="replace") as fp:
    trimmed_data_prev = json.load(fp) # Load the previous trimmed data for comparison
with open("local_files/trimmed_data_prev_shvar.json", "r", encoding="utf-8", errors="replace") as fp:
    trimmed_data_shvar = json.load(fp) # Older version for detecting new variants
# Look for changes and report them in a patch notes format
# Github may detect more changes in pokedex_data.js because of how fid are assigned
attNames = ['rowno','form','parno','dexno','img','spec','desc','type1','type2','ab1','ab2','hab','Passive',
           #   0      1       2       3      4     5      6       7       8      9    10    11    12
            'bst','HP','Atk','Def','SpAtk','SpDef','Speed','catchrate','exp','mpc','fem','Egg Move 1','Egg Move 2','Egg Move 3','Rare Egg Move',
           # 13    14   15    16     17      18      19        20      21    22    23        24           25           26        27
            'movedict','cost','eggtier','shvar','gen','startable','startRow','startInd','specInd','specKey','famFID',
           #    28       29      30       31     32       33          34         35         36        37       38
            'freshStart','biomes','formExclusive','unobtainable','newVariants','evoClass','exclusiveClass','fullyEvolved']
           #    39          40           41             42             43           44            45             46
omitAttr = [0, 1, 2, 20, 21, 22, 28, 34, 35, 36, 37, 38]
soloAttr = [] # Put an attribute here to only show changes to that, and ignores changes to others
for i in range(len(soloAttr)):                              # You can use strings for ranges (inclusive)
    if isinstance(soloAttr[i], str) and '-' in soloAttr[i]: # i.e. [1,'3-5',8] becomes [1,3,4,5,8]
        for j in range(int(soloAttr[i].split('-')[0]),int(soloAttr[i].split('-')[1])):
            soloAttr.append(j)
        soloAttr[i] = j+1
attPatchCount = [0 for arg in attNames] # How many times each attribute was changed
eggPatchCount = [0 for arg in trimmed_data] # How many times any egg move was changed
patch_review = [] # Readable review of patch notes in the console
patch_data = {} # Numerical patch data imported to the SearchDex
for i,line in enumerate(trimmed_data):
    # Find where the species is, in _prev (the index may be different)
    for ii in range(i-10,min(i+10,len(trimmed_data_prev))):
        if line[5] == trimmed_data_prev[ii][5]:
            prevLine = trimmed_data_prev[ii]
            break
    else:
        print('Could not find',line[5],'in previous data')
        continue
    if line[5] == prevLine[5]: # Make sure species is the same
        # Find where the species is, in _prev_shvar (which may be different length from _prev)
        for iii in range(i-10,min(i+10,len(trimmed_data_shvar))):
            if line[5] == trimmed_data_shvar[iii][5]: 
                if line[31] != trimmed_data_shvar[iii][31]:
                    line[43] = 1 # Mark as newly added shiny variants
                break
        # Loop through all attributes for comparison
        for j in range(0,min(len(line),len(prevLine))):
            # For all the main values, they are only 'changed'
            if (not soloAttr and j not in omitAttr) or j in soloAttr: 
                if line[j] != prevLine[j]:
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
                        for specID,specLine in patch_data.items(): # Check patch data for redundant entries
                            if trimmed_data[specID][38] == line[38]: # If same family
                                if j in specLine and specLine[j][0] == preFID and specLine[j][1] == postFID:
                                    break
                        else:
                            if i not in patch_data:
                                patch_data[i] = {}
                            patch_data[i][j] = [preFID, postFID]
                    attPatchCount[j] += 1
                    if j in [24,25,26,27]:
                        eggPatchCount[i] = 1
            elif j == 28: # For the move dict, they are either 'added' or 'removed'
                # src = -1:mushroom, 0:evo, 1-200:level, 201-203:egg&TM, 204:egg, 205-207:rare&TM, 208:rare, 209-211:TM
                for key,value in line[28].items():
                    if 209 < value < 200: # Ignore egg moves
                        if key in prevLine[28]:
                            if prevLine[28][key] != value:
                                print(line[5],'move',key,'changed from',prevLine[28][key],'to',value)
                                if line[33] and not [41]:
                                    patch_review.append(f'{key}: {prevLine[28][key]} > {value}')
                        else:
                            print('Move',key,'added to',line[5])
                            if line[33] and not [41]:
                                patch_review.append(f'{key}: Added ({value})')
                for key,value in prevLine[28].items():
                    if key not in line[28] and 209 < value < 200:
                        print('Move',key,'removed from',line[5])
                        if line[33] and not [41]:
                            patch_review.append(f'{key}: Removed ({value})')
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

# Write all the main data to a Javascript file *********************************************
# Names are short to reduce database file size
attributes = ['row','form','parno','dex','img','sp','desc','t1','t2','a1','a2','ha','pa',
             #  0     1       2      3     4    5     6     7    8    9    10   11   12    
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
for line in trimmed_data:
    text = '{' # Start the entry of that Pokemon
    # Write all the main attributes as {text}:{value}
    for i in range(len(attributes)): 
        if i not in omitAttr and line[i] != '':
            if i in [7,8,9,10,11,12,24,25,26,27]:
                # Types/Abilities/Moves are listed as Names in trimmed_data
                # They are converted to filter ID (fid) before writing
                fid = filterToFID[format_for_attr(f'{keyText[i]}{line[i]}')]
                text = f'{text}{attributes[i]}:{fid},'
            elif i == 4:
                text = f'{text}{attributes[i]}:"{format_for_attr(line[i])}",' # For img path
            elif is_numeric(line[i]):
                text = f'{text}{attributes[i]}:{line[i]},' # For numbers
            else:
                throwError(f"***** Unknown attribute format: {i}")
    # Write all moves as {fid}:{source}
    for moveName,moveSrc in line[28].items():
        fid = filterToFID[format_for_attr(f'move{moveName}')]
        text = f'{text}{fid}:{moveSrc},'
    # Write types/abilities as {fid}:{source}
    # This is for faster lookups, and for the ability restriction filter to know which slot
    for i in range(7,13):
        if line[i] != '':
            fid = filterToFID[format_for_attr(f'{keyText[i]}{line[i]}')]
            text = f'{text}{fid}:{300+i},'
    # Write biome data as fid:'[code1,code2,...]'
    for biomeLine in line[40]: # Biomes
        text = f'{text}{biomeLine[1]}:[{",".join(str(b) for b in biomeLine[2])}],'
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