# ===== This reads all the balance files from the official github   =====
# ===== It links all the data between evolutions and forms          =====
# ===== It saves the data in an optimized format as pokedex_data.js =====

import re, os, copy, json
pathBal  = './game_files/src/data/balance' # File path to the balance files
pathImg = './website/images'

# Function to determine if a value is numeric
def is_numeric(value):
    return re.match(r'^-?\d+(\.\d+)?$', str(value)) is not None
# Function to format arguments
def format_for_disp(arg): # Remove spaces, and convert _ and - to spaces, then capitalize
    return arg.replace(' ','').replace('_',' ').replace('-',' ').title()
def format_for_attr(arg): # Remove spaces
    return arg.replace(' ','').lower()
def throwError(text = ''):
    print(f'***** Major Error Found ¯\_(ツ)_/¯\n***** {text}')
    print('Continuing...') # PUT A BREAKPOINT ON THIS LINE FOR DEBUGGING ****************

megaList = ['Mega Clefable','Mega Victreebel','Mega Starmie','Mega Dragonite','Mega Meganium','Mega Feraligatr','Mega Skarmory','Mega Froslass','Mega Emboar','Mega Excadrill','Mega Scolipede','Mega Scrafty','Mega Eelektross','Mega Chandelure','Mega Chesnaught','Mega Delphox','Mega Greninja','Mega Pyroar','Mega Floette','Mega Malamar','Mega Barbaracle','Mega Dragalge','Mega Hawlucha','Mega Zygarde','Mega Drampa','Mega Falinks','Mega Raichu X','Mega Raichu Y','Mega Chimecho','Mega Baxcalibur']

# Open and read the file of main data *******************************
with open(f"{pathBal}/pokemon-species.ts", "r") as file:
    content = file.read()
# Use a regular expression to extract text between the markers
input_data = re.findall(r'PokemonSpecies\[\]\)\.push\((.*?)\);\n}', content, re.DOTALL)[0]
print('\nLoading data...')

# Counter to keep track of incrementing numbers
species_counter = [1]  # Use a list to allow updates within a nested function
# Replacement function to substitute "Species." with incremented numbers
def replace_species(_):
    current_number = species_counter[0]
    species_counter[0] += 1
    return f"{current_number}, {current_number}, "
input_data = re.sub(r'SpeciesId\.', replace_species, input_data)
# Replace object prefixes
input_data = re.sub(r'\bPokemonType\.', '', input_data)
input_data = re.sub(r'\bAbilityId\.', '', input_data)
input_data = re.sub(r'\bGrowthRate\.', '', input_data)
input_data = re.sub(r'\bSpeciesFormKey\.', '', input_data)
input_data = re.sub(r'\s+new\sPokemonSpecies\(', '\nrow, , ,', input_data)
input_data = re.sub(r'\s+new\sPokemonForm\(', '\nrow,form,parent,', input_data)
input_data = re.sub(r'\s+\),', '', input_data)
input_data = re.sub(r'\"', '', input_data)

# Split arguments and organize into a 2D list, and apply formatting
output_data = input_data.strip().split('\n')
output_data = [re.split(r'\),|,', line) for line in output_data]
output_data = [[format_for_disp(arg) for arg in line] for line in output_data]

# Assign the parent rows to the alternate forms
parentCurrent = 0
for i in range(len(output_data)):
    output_data[i][0] = i # Add the row number at the start of all rows
    if output_data[i][2] == 'Parent': # If it has been marked as needing a parent row
        output_data[i][2] = parentCurrent
    else:
        parentCurrent = output_data[i][0] # Parent is the row of base form
print('Finished reading species')

# Open and read the evolutions file ************************************
with open(f"{pathBal}/pokemon-evolutions.ts", "r") as file:
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
with open(f"{pathBal}/pokemon-level-moves.ts", "r") as file: # Level up moves for species ***********************
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
movesByCategory = []
move_list_dict = {}
for line in levelMoveData:
    movesByCategory.append([line[0][0],[],[],[]])
    for j in range(1,len(line)):
        if line[j][0] == 'Evolve Move':
            line[j][0] = 0
        if line[j][0] == 'Relearn Move':
            line[j][0] = -1
        if int(line[j][0]) > 100:
            throwError(f'High level move found: {line[0][0]} {line[j]}')
        # Level moves are added to [1] in movesByCategory[i], along with their level
        movesByCategory[-1][1].append([line[j][1], int(line[j][0])])
        if line[j][1] not in move_list_dict:
            move_list_dict[line[j][1]] = 'level'
print('Finished reading level moves')
with open(f"{pathBal}/egg-moves.ts", "r") as file: # Egg moves **************************
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
for line in movesByCategory:
    for eggLine in eggMoveData:
        if line[0] == eggLine[0]:
            for k in range(4):
                # Egg moves are added to [2] in movesByCategory[i], encoded as 204(common) or 208(rare)
                line[2].append([eggLine[1][k],204+(k==3)*4])
                if eggLine[1][k] not in move_list_dict:
                    move_list_dict[eggLine[1][k]] = 'egg'
print('Finished reading egg moves')
# Convert movesByCategory to a dictionary for faster lookups
move4D_dict = {speciesMoveLine[0]: speciesMoveLine for speciesMoveLine in movesByCategory}
with open(f"{pathBal}/tm-species-map.ts", "r") as file: # Read the file of TM moves ************************
    content = file.read()
# Use a regular expression to extract text of each TM separately
inputMoveData = re.findall(r'\[(MoveId\..*?)\n\s\s\],', content, re.DOTALL)
inputMoveData = [re.split(r'\]:\s?\[', line) for line in inputMoveData]
inputMoveData = [[line[0], re.split('\n', line[1])] for line in inputMoveData]
with open(f"{pathBal}/tms.ts", "r") as file: # Read the file of TM tiers
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
    # Get the move name
    moveName = format_for_disp(line[0].split("MoveId.")[1].strip())
    if moveName not in move_list_dict: # Add the TM itself to the list of all moves
        move_list_dict[moveName] = TMtier_dict[moveName]
    # Format the list of species and forms that can learn it
    baseSpecies = ''
    speciesListForThisTM = []
    prevSpecLine = ''
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
        if species not in move4D_dict: # Forms with unique TM learnset will not have an entry yet
            move4D_dict[species] = [species,[],[],[]] 
        move4D_dict[species][3].append([moveName, TMtier_dict[moveName]]) # Add the TM to each pokemon's compatible moves
print('Finished reading TM moves')
print('Finished reading all moves')

# Currently, base species and forms have different formats in output_data
# This puts base species and forms into a consistent data format: combined_data
combined_data = [] 
for i in range(len(output_data)):
    combined_data.append([])
    # I always use [2] (parent row) to tell if an entry is a form (it will be blank for base species)
    if output_data[i][2] == '': # For base species, not forms
        par = i
        # row number [0], form key [1], parent row number [2], dex number [3], image filename [4], display name [5]
        combined_data[-1].extend(output_data[i][0:6]) 
        combined_data[-1].append(output_data[i][10]) # Species description (unused) [6]
        combined_data[-1].append(output_data[i][11]) # Type 1 [7]
        if output_data[i][12] == 'Null':
            combined_data[-1].append('')
        else:
            combined_data[-1].append(output_data[i][12]) # Type 2 [8]
        combined_data[-1].append(output_data[i][15]) # Ability 1 [9]
        if output_data[i][16] == output_data[i][15] or output_data[i][16] == 'None':
            combined_data[-1].append('')
        else:
            combined_data[-1].append(output_data[i][16]) # Ability 2 [10]
        if output_data[i][17] == output_data[i][15] or output_data[i][17] == 'None':
            combined_data[-1].append('')
        else:
            combined_data[-1].append(output_data[i][17]) # Hidden ability [11]
        combined_data[-1].append('') # Blank passive combined_data[12]
        combined_data[-1].extend(output_data[i][18:26])
        combined_data[-1].extend(output_data[i][28:31])
    else: # For forms
        combined_data[-1].append(output_data[i][0]) # row number [0]
        combined_data[-1].append(output_data[i][4]) # form key [1]
        combined_data[-1].append(output_data[i][2]) # parent row number [2]
        par = int(output_data[i][2]) # Note which row the parent is
        combined_data[-1].append(output_data[par][3]) # dex number [3]
        if output_data[i][4] == '': 
            # If the form key is blank, like a 'normal' form, just use the species name
            combined_data[-1].append(output_data[par][4])
            combined_data[-1].append(output_data[par][5])
        else: # If it is a named form
            spriteName = f'{output_data[par][4]}-{output_data[i][4]}'
            combined_data[-1].append(spriteName.replace(" ", "-")) # image filename [4]
            combined_data[-1].append(f'{output_data[i][4]} {output_data[par][5]}') # Display name [5]
        combined_data[-1].append(output_data[par][10]) # Species description (unused) [6]
        combined_data[-1].append(output_data[i][5]) # Type 1 [7]
        if output_data[i][6] == 'Null':
            combined_data[-1].append('') # Type 2 [8]
        else:
            combined_data[-1].append(output_data[i][6])
        combined_data[-1].append(output_data[i][9]) # Ability 1 [9]
        if output_data[i][10] == output_data[i][9] or output_data[i][10] == 'None': # Ability 2 [10]
            combined_data[-1].append('')
        else:
            combined_data[-1].append(output_data[i][10])
        if output_data[i][11] == output_data[i][9] or output_data[i][11] == 'None': # [11] Hidden ability
            combined_data[-1].append('')
        else:
            combined_data[-1].append(output_data[i][11])
        combined_data[-1].append('')                      # [12] Passive (filled in later)
        combined_data[-1].extend(output_data[i][12:19])   # [13-19] Stats
        combined_data[-1].append(output_data[par][25])    # [20] Catch rate
        combined_data[-1].extend(output_data[par][28:31]) # [21-23] growthRate, malePercent, femDiff
    combined_data[-1].extend(['','','','']) # Add 4 empty lines for egg moves [24-27]
    combined_data[-1].append({}) # Add dict for all moves [28]
    combined_data[-1].extend(['','','']) # Add cost [29], egg tier [30], shiny variants [31]
    if output_data[i][2] == '':
        combined_data[-1].append(output_data[i][6]) # Generation [32]
    else:
        combined_data[-1].append(output_data[par][6])
    combined_data[-1].extend(['','','','']) # isStartable [33], starterRow [34], starterIndex [35], specIndex[36]
    combined_data[-1].extend([output_data[par][5],'','','']) # specKey [37], familyFID [38], freshStart [39], biomes [40]
    # Form exclusive [41] (if the form is only available via form change, not startable/encounterable)
    # In-game, the form is chosen from getSpeciesFormIndex in src/battle-scene.ts
    # Base species are always startable, argument 24 defaults to True (Forms are exclusive unless marked otherwise)
    if output_data[i][2] == '' or (len(output_data[i]) > 24 and 'True' in output_data[i][24]):
        combined_data[-1].append('')
    else:
        combined_data[-1].append(1)
        # print('Form Change Only:',line[5])
    # Force certain forms to be startable (they still didn't fix this...)
    # These species are missing isStarterSelectable in balance/pokemon-species.ts
    # Also, Minior core forms are marked as selectable there (which makes my biomes show up)
    for spec in ['Maushold','Dudunsparce','Sinistcha']:
        if spec in combined_data[-1][5]:
            combined_data[-1][41] = '' # Force certain forms to startable (not exclusive)
    # Check for unobtainable entries (forms must be listed as 'True' in output_data[i][25])
    unobtainable = 0 # Can be obtained, by default
    if output_data[i][2] != '' and len(output_data[i]) > 25 and 'True' in output_data[i][25]:
        unobtainable = 1
    if 'Revavroom' in output_data[par][5]: # Revavroom is technically unobtainable, but I still want to include it
        unobtainable = 0
    if '10 Complete' in output_data[i][4]: # Remove "Complete 10% Zygarde"
        unobtainable = 1
    combined_data[-1].append(unobtainable) # Unobtainable [42]
    combined_data[-1].append('') # Newly added variants [43]
    combined_data[-1].append('') # Form type [44] (fullevo, mega, giga)
    combined_data[-1].append('') # Exclusive type [45] (regular, eggExc, baby, paradox, eterna, starmobile)
print('Finished normalizing data')

# Parse the data for starter costs ****************************
with open(f"{pathBal}/starters.ts", "r") as file:
    content = file.read()
# Use a regular expression to extract text between "speciesStarterCosts = {" and "};"
inputCostData = re.findall(r'speciesStarterCosts = {(.*?)};', content, re.DOTALL)
if not inputCostData: throwError('Could not find cost data')
costSpecies = re.findall(r'\[SpeciesId\.(.*)\]:', inputCostData[0])
costValues  = re.findall(r'\]: (.*),', inputCostData[0])
for i in range(len(costSpecies)):
    isFound = False
    for line in combined_data:
        if line[5] == format_for_disp(costSpecies[i]):
            isFound = True
            line[29] = int(costValues[i])
    if not isFound:
        throwError(f'Could not assign cost of {costSpecies[i]}')
print('Finished assigning base costs')
# Parse the data for starter egg tiers ****************************
with open(f"{pathBal}/species-egg-tiers.ts", "r") as file:
    content = file.read()
# Use a regular expression to extract text between "speciesEggTiers = {" and "};"
inputTierData = re.findall(r'speciesEggTiers\s*=\s*{(.*?)};', content, re.DOTALL)
if not inputTierData: throwError('Could not find tier data')
tierSpecies = re.findall(r'\[SpeciesId\.(.*)\]:', inputTierData[0])
tierValues  = re.findall(r'EggTier\.(.*)\n', inputTierData[0])
for i,tierLine in enumerate(tierSpecies):
    isFound = False
    for line in combined_data: # Find the species name
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
with open(f"{pathBal}/init-biomes.ts", "r") as file:
    content = file.read()
# Use a regular expression to extract text between "pokemonBiomes = [" and "const trainerBiomes"
inputBiomeData = re.findall(r'pokemonBiomes = \[(.*?)const trainerBiomes', content, re.DOTALL)[0]
inputBiomeData = re.findall(r'\[(SpeciesId.*?)    ]', inputBiomeData, re.DOTALL)
inputBiomeLines = [re.split('\n', line) for line in inputBiomeData]
biome_data = [[format_for_disp(re.findall(r'SpeciesId\.(.*?),',line[0])[0]), line[1:-1]] for line in inputBiomeLines]
rarities = ['COMMON','UNCOMMON','BOSS','RARE','BOSS_RARE','SUPER_RARE','BOSS_SUPER_RARE','ULTRA_RARE','BOSS_ULTRA_RARE']
for line in biome_data:
    for index in range(len(line[1])):
        line[1][index] = [
            re.findall(r'BiomeId\.(.*?),',line[1][index])[0],
            re.findall(r'BiomePoolTier\.(.*?)(?:,|\])',line[1][index])[0],
            re.findall(r'TimeOfDay\.(.*?)(?:,|\])',line[1][index]),
        ]
        for i, rarity in enumerate(rarities): # Encode the rarity
            if line[1][index][1] == rarity: 
                code = (i+1)*20
                break
        else:
            throwError(f'No biome rarity found: {line[1][index][1]}')
        if line[1][index][2]: # Check for time restrictions
            code += 1*('DAWN' in line[1][index][2])
            code += 2*('DAY' in line[1][index][2])
            code += 4*('DUSK' in line[1][index][2])
            code += 8*('NIGHT' in line[1][index][2])
        line[1][index].append(code)
    for specLine in combined_data:
        if line[0] == specLine[5]: # Assign biome data to base species
            specLine[40] = line[1]
            break
# Structure of biome_data[species] is like ['Bulbasaur', ['GRASS', 'RARE', [], 80]]
print('Finished assigning base biomes')

# Open and read the file of passives ***********************************
with open(f"{pathBal}/passives.ts", "r") as file:
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
    for i in range(len(combined_data)): # Find the base species that matches that passive
        if passive_species[passiveIndex] == combined_data[i][5] and combined_data[i][2] == '':
            combined_data[i][12] = passive_abilities[passiveIndex][0] # Assign the passive to the base species
            if len(passive_abilities[passiveIndex]) > 1:
                # If the passive is a list (for those Pokemon's forms)
                for formIndex in range(len(passive_abilities[passiveIndex])):
                    if combined_data[i+1+formIndex][2] != '': # It has to be a form
                        # Assign the passive to the forms in order
                        # Reminder that combined_data has the base species, and then form0, form1, etc.
                        # (base species and form0 will use the same passive)
                        # (base species is trimmed later in this script)
                        combined_data[i+1+formIndex][12] = passive_abilities[passiveIndex][formIndex]
                    else:
                        throwError(f'Passive error: {passive_species[passiveIndex]} {passive_abilities[passiveIndex]}')
            break
print('Finished assigning passives')

# Add only egg moves to the attributes and dictionary
for line in combined_data:
    if line[5] in move4D_dict and line[2] == '': # Only for base species
        if move4D_dict[line[5]][2]:
            line[33] = 1 # Anything with egg moves is startable [33] (forms exclusives [41] are on top of that)
            line[24:28] = [eggLine[0] for eggLine in move4D_dict[line[5]][2]] # Put egg moves in [24-27]
            if len(move4D_dict[line[5]][2]) != 4:
                print(f'Weird number of egg moves found in {line[5]}')
        for move in move4D_dict[line[5]][2]:
            if move[0] not in line[28]:
                line[28][move[0]] = move[1] # Add the move to the dict
print('Finished assigning egg moves')

# Propagate egg moves and other data via evolution **************************
for stages in range(2): # Up to 2 evolutions
    for evoLine in evolution_data: # Assign data through evolution **********
        for childLine in combined_data:
            if evoLine[0] == childLine[5]: # Find the childLine, break when matching
                break
        else: # If the child search loop fails to break
            throwError(f'Failed to find pre-evo {evoLine[0]}')
        for parentName in evoLine[1:]:
            for parentLine in combined_data:
                if parentName == parentLine[5]: # Copy properties from child
                    parentLine[24:28] = childLine[24:28]          # Egg moves
                    parentLine[28] = copy.deepcopy(childLine[28]) # All moves
                    parentLine[29:31] = childLine[29:31]          # Cost, egg tier
                    parentLine[34] = childLine[34]                # Starter row
                    break # Break the parent search loop
            else: # If the parent search loop fails to break
                throwError(f'Failed to find post-evo: {parentName}')
for line in combined_data: # Assign data through forms **********************
    if line[2] != '': # Only for forms
        par = int(line[2])
        if line[12] == '':
            line[12] = combined_data[par][12]
            print('** Assigned parent passive to',line[5])
        line[24:28] = combined_data[par][24:28]
        line[28] = copy.deepcopy(combined_data[par][28])
        line[29:31] = combined_data[par][29:31]
        if not line[41] and (combined_data[par][33] or 'Pikachu' in line[5]):
            line[33] = 1 # If the form is not exclusive, and the base is startable, then it is startable
        line[34] = combined_data[par][34]
        line[40] = combined_data[par][40] # Inherit biomes, even on exclusive forms
print('Finished propagating data to evolutions and forms')
for line in combined_data: # Check for empty properties in combined_data
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
                    for parentLine in combined_data:
                        # Make sure Meltan doesn't count as a baby
                        if parentName == parentLine[5] and parentLine[40] != []:
                            line[45] = 2 # Exclusive to baby
                            break
        if line[45] == 1:
            print('Egg Exclusive:',line[5])
        if line[45] == 2:
            print('Baby Egg Exclusive:',line[5])
    elif line[40] != '' and line[40][0][0] == 'END':
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
        print('Starmobile:',line[5])
    # if line[41] and line[45]:
    #     print('Double exclusive:',line[5])
    #     print(line[5],line[45])
    if line[40] == '' and line[45] == -1:
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
for line in combined_data:
    if line[2] == '': # Only for base species
        if line[5] in move4D_dict:
            move4D_dict[line[5]].append('done')
            for move in move4D_dict[line[5]][1]+move4D_dict[line[5]][3]:
                if move[0] not in line[28]:
                    line[28][move[0]] = move[1] # Add level and TM moves to base species
                else:
                    if line[28][move[0]] in [204,208] and move[1] > 208:
                        line[28][move[0]] += move[1]-212 # Encode the move as an egg move and a TM
                        # print('Multi-source move',move[0],'on',line[5],': source',line[28][move[0]],'and',move[1])
        else:
            throwError(f'Failed to find base species {line[5]}')

# Parse the level up moves for alternate forms
with open(f"{pathBal}/pokemon-level-moves.ts", "r") as file: # Level up moves for alt forms ****
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
for spec_ind in range(len(formLevelMoveData)):
    for index,formLine in enumerate(formLevelMoveData[spec_ind]):
        if index > 0: # The first line is always blank
            for i in range(len(combined_data)):
                if combined_data[i][5] == formLevelSpecies[spec_ind] and combined_data[i][2] == '':
                    # Find the matching base species line (it will not have a parent index [2])
                    for move in formLine:
                        if move[0] == 'Evolve Move':
                            move[0] = 0
                        elif move[0] == 'Relearn Move':
                            move[0] = -1
                        move[0], move[1] = move[1], int(move[0])
                        if move[0] not in combined_data[i+index+1][28]:
                            combined_data[i+index+1][28][move[0]] = move[1] # Add the unique form moves
                        if move[0] not in move_list_dict:
                            move_list_dict[move[0]] = 'formlevel'
# Assign TM moves and level moves to forms:
# If the form doesn't have a unique moveset, inherit that from the base species
    # If it does, only inherit TM moves
# Either way, add TM moves that are unique to forms (in addition to the inherited TM moves)
for line in combined_data: 
    if line[2] != '': # Only for forms
        # TMs are only given from the base species (not from the 'normal' form) to their forms
        if len(line[28]) == 4: # If there are only egg moves, that form doesn't have unique level moves
            # Copy all moves from parent (level, egg, TM)
            # This inherits all the level up moves if the form does not have a unique moveset
            line[28] = copy.deepcopy(combined_data[line[2]][28]) 
        else: # Only try to inherit TMs if the form has unique level moves (if it didn't just inherit moves)
            parentName = combined_data[int(line[2])][5]
            if parentName in move4D_dict: 
                for move in move4D_dict[parentName][3]:
                    if move[0] not in line[28]:
                        line[28][move[0]] = move[1] # Add the TM move to the form's list
                    else:
                        if line[28][move[0]] in [204,208] and move[1] > 208:
                            line[28][move[0]] += move[1]-212 # Encode the move as an egg move and a TM
            else:
                throwError(f'Failed to find parent species {parentName}')
        # Add TM moves that are specific to forms
        if line[1] == '': # Add 'normal' to distinguish from base species, like Normal Calyrex
            normName = f'Normal {line[5]}'
        else:
            normName = line[5]
        if normName in move4D_dict:
            for move in move4D_dict[normName][1]+move4D_dict[normName][2]+move4D_dict[normName][3]:
                if move[0] not in line[28]:
                    line[28][move[0]] = move[1] # Add all level/egg/TM moves
                else:
                    if line[28][move[0]] in [204,208] and move[1] > 208:
                        line[28][move[0]] += move[1]-212
            print('Imported unique TMs for',normName)
            move4D_dict[normName].append('done')
# Check that every entry in move4D_dict was assigned
# A correct move4D_dict[key] looks like [species, [[levelmove,src],[]], [[eggmove,src],[]], [[tmmove,src],[]], 'done']
for key, value in move4D_dict.items():
    if len(value) > 5:
        throwError(f'Double counted moves in {key}') # Base species will have value[3] = 'done'
    elif len(value) < 5: # If moves could not be assigned from move4D_dict (likely for form-unique TMs)
        throwError(f'Failed to assign TM to form - key: {key} - value: {value}')

# Assemble lists of all abilities and biomes *****************************
allAbilities = []
for line in combined_data:
    for ab_slot in [9,10,11,12]:
        if line[ab_slot] != '' and line[ab_slot] not in allAbilities:
            allAbilities.append(line[ab_slot])
allBiomes = []
for line in biome_data:
    for biomeLine in line[1]:
        if biomeLine[0] != '' and format_for_disp(biomeLine[0]) not in allBiomes:
            allBiomes.append(format_for_disp(biomeLine[0]))
allBiomes.sort()

# Species specific manual overrides
for line in combined_data:
    if line[5] == "Apex Build Koraidon":
        line[5] = "Koraidon" # 1007 Koraidon override
    if line[5] == "Ultimate Mode Miraidon":
        line[5] = "Miraidon" # 1008 Miraidon override
    if line[5] == "Hero Of Many Battles Zamazenta":
        line[5] = "Zamazenta" # 888 Zama override
    if line[5] == 'Hero Of Many Battles Zacian':
        line[5] = "Zacian" # 889 Zacian override
    if line[3] == '718': # 718 Zygarde override
        for text in ['10','50','Complete']:
            if text in line[5]:
                line[4] = re.sub('-50','',f'718-{text}') # Image path
                line[5] = re.sub('Pc','PC',line[5])      # Species
    if line[5] == 'Arceus': # 493 Arceus override
        line[4] = f"{line[3]}-normal" # Image path
        line[5] = "Normal Arceus"     # Species

# Don't keep base form of a species with forms
trimmed_data = []
print('\nTrimming base species and unobtainable pokemon...')
for i in range(len(combined_data)-1):
    if combined_data[i][2] != "" or combined_data[i+1][2] == "": # If it is a form, or next is not
        if not combined_data[i][42]: 
            trimmed_data.append(combined_data[i]) # Keep everything except for unobtainables
        else:
            # Should be 2: Unknown Arceus, Zenith Marshadow
            print('Unobtainable:',combined_data[i][5])
    elif combined_data[i][3] != combined_data[i+1][3]: # Remove the base of species with forms
        throwError(f"Ignored {combined_data[i][5]}") # Show error if removing unique species
trimmed_data.append(combined_data[-1]) # Add the last entry

# Regional forms dex number override
with open("./local_files/my_json/regionalformnumbers.txt", "r") as file:
    regionalDexNo = re.split('\n',file.read()) # Generated using sprite names
for i in range(len(regionalDexNo)):
    trimmed_data[-i-1][3] = regionalDexNo[-i-1]
    if trimmed_data[-i-1][2] == "":
        trimmed_data[-i-1][4] = f'{regionalDexNo[-i-1]}' # Replace img with new dex number
    else:
        trimmed_data[-i-1][4] = f'{regionalDexNo[-i-1]}-{trimmed_data[-i-1][1]}' # Add form to img name

# Reminder: isStartable [33], starterRow [34], starterIndex [35], specIndex[36]
for i, line in enumerate(trimmed_data): 
    if line[34] == '': # Check for invalid starter row
        throwError(f'Unassigned starter row for {line[5]}')
    # Trimmed data no longer has base species or unobtainable forms
    # So now we rebase the row numbers as specIndex[36] to be sequential
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
starterList = {}
for line in trimmed_data: # Count how many times each child is listed
    if line[35] not in starterList:
        starterList[line[35]] = 1
    else:
        starterList[line[35]] += 1

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

# Determine the form class [44] of each pokemon
# 0 = not fully evolved, 1 = fully evolved, 2 = mega, 3 = giga ......................

# Error checking **************************************************************************************
print('\n==============================\n')
print('Checking for errors...')

# Use the default image if unique form image does not exist
for i in range(len(trimmed_data)):
    if not os.path.isfile(f'{pathImg}/{trimmed_data[i][4]}_0.png'): # Check if the given img does not exist
        # print(f'{trimmed_data[i][5]}: Could not find {trimmed_data[i][4]}')
        if os.path.isfile(f'{pathImg}/{trimmed_data[i][3]}_0.png'): # Check if the base img exists
            # print(f'{trimmed_data[i][5]}: Replaced {trimmed_data[i][4]} with base image')
            trimmed_data[i][4] = f'{trimmed_data[i][3]}' # Get image from dexno
        elif trimmed_data[i][3] == trimmed_data[i-1][3]: # If same species as one above
            if int(trimmed_data[i][3]) not in [1012,1013]: # Ignore Sinistcha family
                print(f'{trimmed_data[i][5]}: Replaced {trimmed_data[i][4]} with {trimmed_data[i-1][4]}')
            trimmed_data[i][4] = trimmed_data[i-1][4] # Take that image
        else:
            throwError(f'Could not find any image for {trimmed_data[i][4]}_0.png')
# Check for the existence of variant shinies
for line in trimmed_data:
    if os.path.isfile(f'{pathImg}/{line[4]}_3.png'): # Check if the tier 3 shiny exists
        line[31] = 3 # Shiny variants [31]           # Need to run updateImages.py first *****
    else:
        line[31] = 1 # Shiny variants [31]
    if os.path.isfile(f'{pathImg}/{line[4]}_0f.png'): # Check if the base female sprite exists
        line[23] = 1
        femlist = ['','f']
    else:
        if 'Female' in line[5] or line[5] == 'Nidoran F':
            line[23] = 2
        else:
            line[23] = ''
        femlist = ['']
    for fem in femlist: 
        for shiny in range(line[31]+1):
            # Check for existence of all images (all shiny, optionally female)
            if not os.path.isfile(f'{pathImg}/{line[4]}_{shiny}{fem}.png'):
                throwError(f"The file {pathImg}/{line[4]}_{shiny}{fem}.png does not exist.")

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
    if check[2] != 1 and int(line[3]) not in [132, 201, 202, 235, 360, 789, 790]:
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
                if not trimmed_data[j][41]:
                    hasStartableForms = 1
            else:
                break
        if not hasStartableForms:
            if line[5] in move4D_dict and move4D_dict[line[5]][2]: # Only for first-evo base species
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

# Repair names that have punctuation? probably not
    # Zygarde, Farfetch'd, Sirfetch'd, Ho-oh, Porygon-Z, Porygon2, Type: Null, Mr. Mime, Mime Jr., Mr. Rime

# Sort the abilities and moves into order based on frequency?
# They are in arbitrary order. Types are alphabetical.

types = ['Bug','Dark','Dragon','Electric','Fairy','Fighting','Fire','Flying','Ghost','Grass','Ground','Ice','Normal','Poison','Psychic','Rock','Steel','Water']
moveList = [*move_list_dict] # Get a regular list of moves
allFilters = []
filterToFID = {}
# Put all filters into a big list [[Categ, Value], []]
# Get FID with e.g. filterToFID('typebug') = 0
for type in types:
    filterToFID[f'type{format_for_attr(type)}'] = len(allFilters)
    allFilters.append(['Type',type])
for line in allAbilities:
    filterToFID[f'ability{format_for_attr(line)}'] = len(allFilters)
    allFilters.append(['Ability',line])
for line in moveList:
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
allFilters.append(['Gender','Female'])
for j in ['Starter Select','Fresh Start','Flipped Stats']:
    allFilters.append(['Mode',j])
for j in ['Common','Rare','Epic','Manaphy','Legendary','Exclusive']:
    allFilters.append(['Egg Tier',j])
for j in ['New','All','None']:
    allFilters.append(['Shiny Variants',j])
for line in allBiomes:
    filterToFID[f'biome{format_for_attr(line)}'] = len(allFilters)
    allFilters.append(['Biome',line])
for key,value in starterList.items():
    if value > 1:
        allFilters.append(['Related To',trimmed_data[key][37]])
        for line in trimmed_data:
            if line[35] == key: # If starterIndex is equal to the one in starterList
                line[38] = len(allFilters)-1 # Set familyFID to this fid
for j in ['Lure Ability','Ignores Abilities','Ignores Abilities (Move)','Target Switches Out','Spread Moves']:
    allFilters.append(['Tag',j])

# Process the biome data:
# Currently, biome_data[species] is like ['Bulbasaur', ['GRASS', 'RARE', [], 80]]
# Encode the biome data as [Biome Name, fid, [code1,code2,...]]
# Will be written to js file as fid:[code1,code2,...]
biomeForms = [ # manually updated from getSpeciesFormIndex in file:///.\game_files\src\field\arena.ts
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
    if isinstance(line[40],list): # If there are biomes, and pokemon is base or form exclusive
        for biomeLine in line[40]:
            abort = 0
            # If a species is limited by biome/time, it must pass a check before the biomes are written
            for speciesLine in biomeForms: # Enforce biome specific forms by matching biome name
                if line[5] == speciesLine[0]:
                    if format_for_disp(biomeLine[0]) != speciesLine[1]:
                        abort = 1
                        # print(line[5],biomeLine[0])
            for speciesLine in biomeFormsTime: # Enforce time of day forms by checking remainder of encounter code
                if line[5] == speciesLine[0]:  # Abort if none of the valid times are in the encounter code
                    if all(not(i & (biomeLine[3]%20)) for i in speciesLine[1]):
                        abort = 1
            if not abort:
                # Encoded the biome name as its FID *********************
                # Multiple rarites in the same biome are grouped together
                newFID = filterToFID[f'biome{format_for_attr(format_for_disp(biomeLine[0]))}']
                for encLine in encoded:
                    if encLine[1] == newFID: # If the biome already exists, add this encounter to the list
                        encLine[2].append(biomeLine[3])
                        break
                else: # Create a new FID entry for the biome
                    encoded.append([biomeLine[0], newFID, [biomeLine[3]]])
        # for encLine in encoded:
        #     if len(encLine[2]) > 2:
        #         print('** More than 2 biome rarites in',line[5],encLine)
        # if len(encoded) > 3:
        #     print(f'** Many biomes ({len(encoded)}) in',line[5],line[40])
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
            # print('Changed',biomeLine[2],'to',encoded)
            biomeLine[2] = encoded       

# Find the threshold of types and abilities
fidThresholds = []
catName = allFilters[0][0]
for index,line in enumerate(allFilters):
    if line[0] != catName:
        catName = line[0]
        fidThresholds.append(index)
fidThresholds.append(len(allFilters))
if fidThresholds[0] != 18: throwError('Wrong number of types')
if fidThresholds[1] != 328: throwError('Wrong number of abilities')
if types[-1] != allFilters[fidThresholds[0]-1][1]: throwError('Name error with types')
if allAbilities[-1] != allFilters[fidThresholds[1]-1][1]: throwError('Name error with abilities')
if moveList[-1] != allFilters[fidThresholds[2]-1][1]: throwError('Name error with moves')

# Write some variables to files
# These are read by my other scripts, and some are written to the website
with open("local_files/my_json/allFilters.json", "w") as f:
    json.dump(allFilters, f, indent=4)
with open("local_files/my_json/fidThresholds.json", "w") as f:
    json.dump(fidThresholds, f, indent=4)
with open("local_files/my_json/filterToFID.json", "w") as f:
    json.dump(filterToFID, f, indent=4)
allSpecies = []
for line in trimmed_data:
    allSpecies.append([line[5],line[1],line[37]]) # Combined/form/species keys
with open("local_files/my_json/allSpecies.json", "w") as f:
    json.dump(allSpecies, f, indent=4)

input('\nNo Major Errors Found\nContinue to patch review?')
print('\n==============================\n')
print("Reviewing patch changes...")

# Patch note creating **********************************************************************************
# Write all the trimmed data to a json file
with open("local_files/trimmed_data.json", "w") as f:
    json.dump(trimmed_data, f, indent=4)
# Load the previous trimmed data > You need to manually rename the old one to _prev
with open("local_files/trimmed_data_prev.json", "r") as fp:
    trimmed_data_prev = json.load(fp)
with open("local_files/trimmed_data_prev_shvar.json", "r") as fp: # Older version for purpose of new variants
    trimmed_data_shvar = json.load(fp)
# Look for changes and report them in a patch notes format
# Github may detect more changes because of how fid are assigned
attNames = ['rowno','form','parno','dexno','img','spec','desc','type1','type2','ab1','ab2','hab','Passive',
           #   0      1       2       3      4     5      6       7       8      9    10    11    12
            'bst','HP','Atk','Def','SpAtk','SpDef','Speed','catchrate','exp','mpc','fem','Egg Move 1','Egg Move 2','Egg Move 3','Rare Egg Move',
           # 13    14   15    16     17      18      19        20      21    22    23        24           25           26        27
            'movedict','cost','eggtier','shvar','gen','startable','startRow','startInd','specInd','specKey','famFID',
           #    28       29      30       31     32       33          34         35         36        37       38
            'freshStart','biomes','formExclusive','unobtainable','newVariants','formClass','exclusiveClass']
           #    39          40           41             42             43           44            45
omitAttr = [0, 1, 2, 20, 21, 22, 28, 34, 35, 36, 37, 38, 40, 41]
soloAttr = [] # Put an attribute here to only show changes to that, and ignores changes to others
for i in range(len(soloAttr)):                              # You can use strings for ranges (inclusive)
    if isinstance(soloAttr[i], str) and '-' in soloAttr[i]: # i.e. [1,'3-5',8] becomes [1,3,4,5,8]
        for j in range(int(soloAttr[i].split('-')[0]),int(soloAttr[i].split('-')[1])):
            soloAttr.append(j)
        soloAttr[i] = j+1
attPatchCount = [0 for arg in attNames] # How many times each attribute was changed
eggPatchCount = [0 for arg in trimmed_data] # How many times any egg move was changed
patch_lines = ['patchNotes = `']
for i,line in enumerate(trimmed_data):
    patch_lines.append('')
    patch_lines.append(f'{line[5]}:')
    # Find where the species is, in _prev (the index may be different)
    for ii in range(i-10,min(i+10,len(trimmed_data_prev))):
        if line[5] == trimmed_data_prev[ii][5]:
            break
    else:
        print('Could not find',line[5],'in previous data')
        break
    if line[5] == trimmed_data_prev[ii][5]: # Make sure species is the same
        # Find where the species is, in _prev_shvar (which may be different length from _prev)
        for iii in range(i-10,min(i+10,len(trimmed_data_shvar))):
            if line[5] == trimmed_data_shvar[iii][5]: 
                if line[31] != trimmed_data_shvar[iii][31]:
                    line[43] = 1 # Mark as newly added shiny variants
                break
        # Loop through all attributes for comparison
        for j in range(0,min(len(line),len(trimmed_data_prev[ii]))):
            # For all the main values, they are only 'changed'
            if (not soloAttr and j not in omitAttr) or j in soloAttr: 
                if line[j] != trimmed_data_prev[ii][j]:
                    print(line[5],attNames[j],'changed from',trimmed_data_prev[ii][j],'to',line[j])
                    patch_lines.append(f'{attNames[j]}: {trimmed_data_prev[ii][j]} > {line[j]}')
                    attPatchCount[j] += 1
                    if j in [24,25,26,27]:
                        eggPatchCount[i] = 1
            elif j == 28: # For the move dict, they are either 'added' or 'removed'
                # src = -1:mushroom, 0:evo, 1-200:level, 201-203:egg&TM, 204:egg, 205-207:rare&TM, 208:rare, 209-211:TM
                for key,value in line[28].items():
                    if 209 < value < 200:
                        if key in trimmed_data_prev[ii][28]:
                            if trimmed_data_prev[ii][28][key] != value:
                                if line[33] == 1:
                                    print(line[5],'move',key,'changed from',trimmed_data_prev[ii][28][key],'to',value)
                                    patch_lines.append(f'{key}: {trimmed_data_prev[ii][28][key]} > {value}')
                        else:
                            print('Move',key,'added to',line[5])
                            if line[33] == 1:
                                patch_lines.append(f'{key}: Added ({value})')
                for key,value in trimmed_data_prev[ii][28].items():
                    if key not in line[28] and 209 < value < 200:
                        print('Move',key,'removed from',line[5])
                        if line[33] == 1:
                            patch_lines.append(f'{key}: Removed ({value})')
    if patch_lines[-1] == f'{line[5]}:':
        patch_lines.pop()                   
        patch_lines.pop()    
print('Summary of patch notes:')
for j in range(len(attNames)):
    if attPatchCount[j] > 0:
        print(f'{attNames[j]} changed: {attPatchCount[j]}')
print('Total Egg Moves changed:',sum(eggPatchCount))
# Format the patch notes and save to a file
with open("local_files/patch_notes.js", "w") as file:
    file.writelines(f"{line}<br>\n" for line in patch_lines)
    file.writelines('`;')

input('\nContinue to writing website database?')
print('\n==============================\n')
print("Writing to website database...")

# Write all the main data to a Javascript file *********************************************
attributes = ['row','form','parno','dex','img','sp','desc','t1','t2','a1','a2','ha','pa', # Names are short to reduce file size
             #  0     1       2      3     4    5     6     7    8    9    10   11   12    
              'bst','hp','atk','def','spa','spd','spe','catchrate','exp','mpc','fe','e1','e2','e3','e4','movedict',
             #  13   14    15    16    17    18    19       20       21    22   23   24   25   26   27      28
              'co','et','sh','ge','st','startRow','startInd','specInd','specKey','fa',
             # 29   30   31   32   33      34         35         36        37     38
              'fs','biomes','fx','unobtainable','nv','formClass','ex']
             # 39     40     41        42        43      44       45
omitAttr = [0, 1, 2, 5, 6, 20, 21, 22, 28, 34, 35, 36, 37, 40, 42, 44] # Some attributes are not written to the database
keyText = {7:'type', 8:'type', 9:'ability', 10:'ability', 11:'ability', 12:'ability', 24:'move', 25:'move', 26:'move', 27:'move'}
jsdict = ['// pokedex_data.js\nconst items=[']

for line in trimmed_data:
    text = '{' # Start the entry of that Pokemon
    # Write all the main attributes as {text}:{value}
    for j in range(len(attributes)): 
        if j not in omitAttr and line[j] != '':
            if j in [7,8,9,10,11,12,24,25,26,27]:
                # Types/Abilities/Moves are listed as Names in trimmed_data
                # They are converted to filter ID (fid) before writing
                innertext = f'{keyText[j]}{line[j]}'
                text = f'{text}{attributes[j]}:{filterToFID[format_for_attr(innertext)]}'
            elif j == 4:
                text = f'{text}{attributes[j]}:"{format_for_attr(line[j])}"' # For img path
            elif is_numeric(line[j]):
                text = f'{text}{attributes[j]}:{line[j]}' # For numbers
            else:
                text = f'{text}{attributes[j]}:"{line[j]}"' # For all others
            text = f'{text},'
    # Write all moves as {fid}:{source}
    for key,value in line[28].items():
        innertext = f'move{key}'
        text = f'{text}{filterToFID[format_for_attr(innertext)]}:{value},'
    # Write types/abilities as {fid}:{source}
    # This is for faster lookups, and for the ability restriction filter to know which slot
    for i in range(7,13):
        if line[i] != '':
            innertext = f'{keyText[i]}{line[i]}'
            text = f'{text}{filterToFID[format_for_attr(innertext)]}:{300+i}'
            if i < 12:
                text = f'{text},'
    # Write biome data as fid:'[code1,code2,...]'
    # line[40] is like [Biome Name, fid, [code1,code2,...]]
    if isinstance(line[40],list):
        for biomeLine in line[40]: # Biomes
            text = f'{text},{biomeLine[1]}:['
            for source in biomeLine[2]:
                text = f'{text}{source}'
                if source != biomeLine[2][-1]:
                    text = f'{text},'
                else:
                    text = f'{text}]'
    text = f'{text}}},' # End the entry of that Pokemon
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
#     fs: Value is 1 if the Pokemon is available in fresh start (i.e. being a first partner pokemon)
#     nv: Value is 1 if the Pokemon had new variants recently added
#     fx: If the Pokemon is form exclusive
#             Value is 1 for Mega, G-Max, item form changes, or temporary form changes
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

print("Filter writing complete\n\n========== ALL DONE ==========\n")