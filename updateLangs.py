# ===== This script assembles all translated text for the SearchDex =====
# =====    headerNames, altText, catToName, infoText, biomeText     =====
# =====     biomeLongText, warningText, procTodesc, tagToDesc       =====
# =====     fidToDesc, speciesNames, fidToName, helpMenuText        =====
# Most filters (abilities/moves/pokemon) are auto-translated from the game files
# Some filters (tags, etc.) must have manual translations
# Initially, some UI elements are auto-translated from similar in-game phrases
# However, all UI elements must have overrides in local_files/lang_overrides/{lang}.py
# All data is written to {lang}.js in "/website/lang/"

pathLocales = './game_files/locales' # File path to the official localization files
pathOverrides = "local_files/lang_overrides"
allLangs = ['en','fr','ko','ja','zh-Hans','es-ES','it']

langsToDo = []
# Specify a subset of languages to process
# Leave blank to process all languages

ignoreOverrides = [''] 
# Put a language in here to ignore the .py override file
# Can put 'all' to ignore for every language
# This lets you see what the script can auto-translate

warnNameLength = 0 
# Set to 1 to warn of names that may be too long for the UI
# Set to 0 to ignore this check

# - en - English
# - de - German
# - es-ES - Spanish (Spain)
# - fr - French
# - it - Italian
# - ja - Japanese
# - ko - Korean
# - pt-BR - Portuguese (Brazil)
# - zh-Hans - Chinese (Simplified)
# - zh-Hant - Chinese (Traditional)

# How to do a translation:
#   Add language to allLangs
#   Manually translate the phrases in manualTran
#   If the main loop gives an error, the in-game translation is incomplete
#   Only continue if there are no errors
#   Check length of types/abilities/moves/species
#   Check length and meaning of headers/etc
#   Put custom UI translations into the python override file
#   Use consistent translations for words that appear elsewhere (headers/tags/etc.)
#   Make sure spacing is good, shorten UI phrases if needed

import re, os, json, importlib
# Functions for formatting the text
def format_for_camel(arg): # Key format for official jsons
    arg = arg.title().replace(' ','')
    if arg == '': return ''
    return f'{arg[0].lower()}{arg[1:]}'
def shortenText(text):
    if 'substitutions' in overrides[lang]:
        for line in overrides[lang]['substitutions']:
            text = str(text).replace(line[0],line[1])
    if '♀' in text: text = f"{tall['pokemon-form']['espurrFemale']} {text.replace('♀','')}"
    if '♂' in text: text = f"{tall['pokemon-form']['espurrMale']} {text.replace('♂','')}"
    return text

# Load all the manual overrides from the lang_overrides folder, these are applied at the end
#region Load Overrides
langs = allLangs
if langsToDo != [''] and langsToDo != []:
    langs = langsToDo
overrides = {}
for lang in allLangs:
    spec = importlib.util.spec_from_file_location(f"{lang}_over", f'local_files/lang_overrides/{lang}.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    # Convert module to dictionary, filtering out built-in stuff
    overrides[lang] = { k: v for k, v in vars(mod).items() if not k.startswith("__") }

for lang in langs: # =========================================== Main loop for each language
    print(f"\n============= Beginning {lang} =============")
    path = f'{pathLocales}/{lang}'

    # Load all the official translations for the current language
    #region Load Official
    tall = {} # t(ranslations) all
    fileNames = [file for file in os.listdir(path) if file.lower().endswith('.json')]
    for fileName in fileNames:
        with open(f'{path}/{fileName}', "r", encoding="utf-8") as file:
            keyName = fileName.split('.')[0]
            tall[keyName] = json.load(file)

    # Translate everything from allFilters =========================
    #region Translate Filters
    # Structure of allFilters is like [ ['Category', 'Filter Name'], [ ], ...]
    print('\nTranslating filter names...')
    with open("local_files/my_json/allFilters.json", "r") as file:
        allFilters = json.load(file) # These have to be reloaded for every lang, because they are overwritten in english
    locFilters = ['' for line in allFilters]
    for index,line in enumerate(allFilters):
        text = ''
        # Translate types
        if line[0] == 'Type':
            text = tall['pokemon-info']['type'][line[1].lower()]
            text = shortenText(text)
            if len(text) > 8 and warnNameLength:
                print('Long type found:',text)
        # Translate abilities
        if line[0] == 'Ability':
            key = format_for_camel(line[1])
            text = tall['ability'][key]['name']
            if 'embody' in key: # Add variants of embody aspect, with stat names
                if 'Teal' in key:
                    text = f"{text} {tall['pokemon-info']['stat']['spd'].replace(' ','&nbsp')}"
                elif 'Wellspring' in key:
                    text = f"{text} {tall['pokemon-info']['stat']['spdef'].replace(' ','&nbsp')}"
                elif 'Hearthflame' in key:
                    text = f"{text} {tall['pokemon-info']['stat']['atk'].replace(' ','&nbsp')}"
                elif 'Cornerstone' in key:
                    text = f"{text} {tall['pokemon-info']['stat']['def'].replace(' ','&nbsp')}"
                else:
                    input(f'***** Error: Could not find ogerpon mask {key}')
            elif key == 'asOneGlastrier': # Add horse names to "As One"
                text = f"{text} {tall['pokemon']['glastrier']}"
            elif key == 'asOneSpectrier':
                text = f"{text} {tall['pokemon']['spectrier']}"
            text = shortenText(text)
            if len(text) > 15 and warnNameLength:
                print('Long ability found:',text)
        # Translate moves
        if line[0] == 'Move':
            text = tall['move'][format_for_camel(line[1])]['name']
            text = shortenText(text)
            if len(text) > 15 and warnNameLength:
                print('Long move found:',text)
        # Copy numeric values
        if line[0] == 'Gen' or line[0] == 'Cost':
            text = line[1]
        # Translate egg tiers
        if line[0] == 'Egg Tier':
            text = ''
            if line[1] == 'Common':     text = 'defaultTier'
            if line[1] == 'Rare':       text = 'greatTier'
            if line[1] == 'Epic':       text = 'ultraTier'
            if line[1] == 'Legendary':  text = 'masterTier'
            if text:                    text = tall['egg'][text] # standard egg tiers
            if line[1] == 'Manaphy':    text = tall['pokemon']['manaphy'] # manaphy egg tier
            if line[1] == 'Exclusive':  text = overrides[lang]['phrases']['exclusive'] # exclusive egg tier
        # Translate modes
        if line[0] == 'Mode':
            if 'Flip' in line[1] and 'name' in tall['challenges']['flipStat']:
                text = tall['challenges']['flipStat']['name']
            if 'Fresh' in line[1] and 'name' in tall['challenges']['freshStart']:
                text = tall['challenges']['freshStart']['name']
            if 'Starter' in line[1] and 'starter' in tall['filter-bar']:
                text = tall['filter-bar']['starter']
        # Translate evolution filters
        if line[0] == 'Evolution':
            if line[1] == 'Starter':       text = tall['filter-bar']['starter']
            if line[1] == 'Fully Evolved': text = overrides[lang]['phrases']['fullyEvolved']
        # Translate form filters
        if line[0] == 'Form':
            if format_for_camel(f'form {line[1]}') in overrides[lang]['phrases']:
                text = overrides[lang]['phrases'][format_for_camel(f'form {line[1]}')]
            if line[1] == 'Female':
                text = tall['pokemon-form']['espurrFemale']
        # Translate new variants filter
        if line[0] == 'Shiny Variants':
            if line[1] == 'New':  text = overrides[lang]['phrases']['new']
            if line[1] == 'All':  text = tall['menu']['yes']
            if line[1] == 'None': text = tall['menu']['no']
        # Translate biome names
        if line[0] == 'Biome':
            text = tall['biomes'][format_for_camel(line[1])]
            if text == "???":
                text = overrides[lang]['phrases']['theEnd']
        # Translate tag names
        if line[0] == 'Tag': # line[1] for tags is the tagID, not the name
            text = overrides[lang]['tagToDesc'][line[1]]
        # Translate names of family filters
        if line[0] == 'Related To':
            # Translate special filters like "Related To: New Mega"
            if format_for_camel(f'form {line[1]}') in overrides[lang]['phrases']:
                locFilters[index] = overrides[lang]['phrases'][format_for_camel(f'form {line[1]}')]
                continue
            # Translate standard "Related To" filters
            # Look up the correct name format, depending on the region
            nameFormat = '{{pokemonName}}'
            regions = ['Alola','Galar','Hisui','Paldea','Bloodmoon','Eternal']
            for region in regions:
                if region in line[1]:
                    nameFormat = tall['pokemon-form']['appendForm'][region.lower()]
            justLocSpec = tall['pokemon'][format_for_camel(line[1])] # Look up species name
            if line[1] == 'Battle Bond Greninja':
                justLocSpec = f"{tall['pokemon-form']['battleBondGreninja']} {justLocSpec}"
            thisName = nameFormat.replace('{{pokemonName}}',justLocSpec) # Fill in the actual species name
            thisName = thisName.replace("'",'’') # Replace single quotes with unicode
            text = shortenText(thisName)
            if len(text) > 20 and warnNameLength:
                print('Long name found:',text)
            if not text or '{' in text:
                input(f'***** Error: Pokemon name failure\n{text}')
        locFilters[index] = shortenText(text)
        if lang == 'en' and line[0] in ["Mode","Shiny Variants"]:
            locFilters[index] = line[1] # Use original english filters names from updateDatabase.py
        # print(f'Translated "{line[0]}:{line[1]}" to: "{locFilters[index]}"')
    print('Done translating filter names')
    
    # Check for the shortest and longest translations of types/abilities/moves
    with open("local_files/my_json/fidThreshold.json", "r") as fp:
        fidThreshold = json.load(fp)
    if warnNameLength:
        catNames = ['TYPE','ABILITY','MOVE']
        for i in [0,1,2]:
            filterStart = fidThreshold[i-1]
            if (i==0): filterStart = 0
            maxLengthCat = max(locFilters[filterStart:fidThreshold[i]], key=len)
            print('Longest translated',catNames[i],'is',maxLengthCat,'(',len(maxLengthCat),'char )')
            minLengthCat = min(locFilters[filterStart:fidThreshold[i]], key=len)
            print('Shortest translated',catNames[i],'is',minLengthCat,'(',len(minLengthCat),'char )')
        for line in locFilters[:fidThreshold[2]]:
            collisionCount = sum(1 for inLine in locFilters if line.lower() in inLine.lower())
            if collisionCount > 20:
                print('High collisions in',line,'[',collisionCount,'hits ]')
    # Report any missing filter translations (these are mandatory)
    missingAmount = sum([1 for line in locFilters if not line])
    if missingAmount: input(f'***** Error: Missing {missingAmount} filter names')

    # Translate speciesNames =========================
    #region Translate Pokemon
    print('\nTranslating species names...')
    with open("local_files/my_json/allSpecies.json", "r") as file:
        allSpecies = json.load(file)
    maxLengthSpeciesEng = max(len(specLine[0]) for specLine in allSpecies)
    if lang == 'en' and warnNameLength:
        print('Longest species name in english list is',maxLengthSpeciesEng)
    locSpecies = ['' for line in allSpecies]
    maxLengthSpecies = 0
    for index,specLine in enumerate(allSpecies): # specLine is [full name, form name, species name]
        
        if specLine[2] == 'Koraidon' or specLine[2] == 'Miraidon' or 'Hero Of Many Battles' in specLine[0]:
            specLine[0:2] = [specLine[2],''] # Remove form key of those pokemon

        # Translate just the base species name [2]
        text = format_for_camel(specLine[2])
        if text in tall['pokemon']:
            justLocSpec = tall['pokemon'][text]
            justLocForm = ''
        else:
            input(f'***** Error: Could not find base species {text}')

        # Translate the form name [1]
        if specLine[1]: # If it is a form
            # The game only lists form keys for the first stage of evolution
            # If a form pokemon evolves, it needs to be manually linked here
            effSpec = specLine[2]
            if effSpec == 'Wormadam': effSpec = 'Burmy'
            if effSpec == 'Cherrim': effSpec = 'Cherubi'
            if effSpec == 'Gastrodon': effSpec = 'Shellos'
            if effSpec == 'Darmanitan': effSpec = 'Darumaka'
            if effSpec == 'Sawsbuck': effSpec = 'Deerling'
            if effSpec == 'Spewpa': effSpec = 'Scatterbug'
            if effSpec == 'Vivillon': effSpec = 'Scatterbug'
            if effSpec == 'Floette': effSpec = 'Flabebe'
            if effSpec == 'Florges': effSpec = 'Flabebe'
            if effSpec == 'Meowstic': effSpec = 'Espurr'
            if effSpec == 'Aegislash': effSpec = 'Honedge'
            if effSpec == 'Gourgeist': effSpec = 'Pumpkaboo'
            if effSpec == 'Lycanroc': effSpec = 'Rockruff'
            if effSpec == 'Toxtricity': effSpec = 'Toxel'
            if effSpec == 'Polteageist': effSpec = 'Sinistea'
            if effSpec == 'Alcremie': effSpec = 'Milcery'
            if effSpec == 'Urshifu': effSpec = 'Kubfu'
            if effSpec == 'Basculegion': effSpec = 'Basculin'
            if effSpec == 'Oinkologne': effSpec = 'Lechonk'
            if effSpec == 'Maushold': effSpec = 'Tandemaus'
            if effSpec == 'Palafin': effSpec = 'Finizen'
            if effSpec == 'Dudunsparce': effSpec = 'Dunsparce'
            if effSpec == 'Sinistcha': effSpec = 'Poltchageist'
            if effSpec == 'Galar Darmanitan': effSpec = 'Galar Darumaka'
            if specLine[2] == 'Battle Bond Greninja' and specLine[1] == 'Battle Bond': specLine[1] = ''
            if format_for_camel(specLine[1]) in tall['pokemon-form']['battleForm']: # For mega/giga/etc
                justLocForm = tall['pokemon-form']['battleForm'][format_for_camel(specLine[1])]
            elif effSpec == 'Arceus' or effSpec == 'Silvally':
                justLocForm = tall['pokemon-info']['type'][specLine[1].lower()]
            else:
                specLine[1] = specLine[1].replace('Mega ','') # Remove 'Mega' from form names
                text = format_for_camel(f"{effSpec} {specLine[1]}")
                if text in tall['pokemon-form']: # For regular forms
                    justLocForm = tall['pokemon-form'][text]
                else:
                    input(f'***** Error: Could not find form name for {specLine[0]}')

        # Put the name in correct format (for regionals or forms)
        nameFormat = '{{pokemonName}}'
        regions = ['Alola','Galar','Hisui','Paldea','Bloodmoon','Eternal']
        for region in regions:
            if region in specLine[2]:
                nameFormat = tall['pokemon-form']['appendForm'][region.lower()]
        if tall['pokemon-form']['appendForm']['generic'] != '{{pokemonName}} ({{formName}})':
            input('***** Error: Odd format detected') # This is never used, but it's just to check the format
        if justLocForm: # If it is a form, add the form name to the format
            if lang == 'fr':
                nameFormat = f'{nameFormat} {justLocForm}' # French has form name after
                if 'Méga' in justLocForm:
                    nameFormat = f'Méga-{nameFormat.replace(" Méga","")}'
            else:
                nameFormat = f'{justLocForm} {nameFormat}' # Other langs have form name first

        # Insert the species name, and remove most punctuation
        thisName = nameFormat.replace('{{pokemonName}}',justLocSpec) # Fill in the species name
        thisName = thisName.replace("'",'’') # Replace single quotes with unicode
        # print('Translated',specLine[0],'to',locName)
        if lang == 'en': # My original english names don't have punctuation because I just use the keys from the code
            if all(char not in thisName for char in ["’",":",".","-","♂","♀"]):
                thisName = specLine[0] # Use custom names if there isn't supposed to be punctuation
        thisName = shortenText(thisName)
        locSpecies[index] = thisName
        maxLengthSpecies = max(maxLengthSpecies, len(thisName))
        if len(thisName) > maxLengthSpeciesEng and warnNameLength:
            print('Name longer than',maxLengthSpeciesEng,'found:',thisName)
        if not thisName or '{' in thisName:
            input(f'***** Error: Pokemon name failure\n{thisName}\n{specLine}')
    print('Done translating species names')

    if warnNameLength:
        maxLengthCat = max(locSpecies, key=len)
        print('Longest translated species is',maxLengthCat,'(',len(maxLengthCat),'char )')
        minLengthSpecies = min(locSpecies, key=len)
        print('Shortest translated species is',minLengthCat,'(',len(minLengthCat),'char )')
        for index,line in enumerate(locFilters[fidThreshold[0]:fidThreshold[2]]+locSpecies):
            for index2,line2 in enumerate(locFilters[fidThreshold[0]:fidThreshold[2]]+locSpecies):
                if line == line2 and index != index2:
                    print('***** Same name of pokemon/ability/move in',line)
    missingAmount = sum([1 for line in locSpecies if not line])
    if missingAmount: input(f'***** Missing {missingAmount} species names')

    # Translate the descriptions of abilities/moves =========================
    #region Translate Descriptions
    print('\nTranslating filter descriptions...')
    locDesc = ['' for line in allFilters if (line[0] == 'Move' or line[0] == 'Ability')]
    bonusDesc = { # Add reminder text to things that generate weather/terrain
        'sandstorm': ['sandStream','sandSpit'],
        'sunnyDay': ['drought','orichalcumPulse'],
        'rainDance': ['drizzle'],
        'snowscape': ['snowWarning','chillyReception'],
        'electricTerrain': ['electricSurge','hadronEngine'],
        'grassyTerrain': ['grassySurge','seedSower'],
        'mistyTerrain': ['mistySurge'],
        'psychicTerrain': ['psychicSurge'],
    }
    for index,line in enumerate(allFilters):
        if line[0] == 'Ability' or line[0] == 'Move':
            key = format_for_camel(line[1])
            text = ''
            if key in tall['ability'] and 'description' in tall['ability'][key]:
                text = tall['ability'][key]['description'] # Translate abilities
            if key in tall['move'] and 'effect' in tall['move'][key]:
                text = tall['move'][key]['effect'] # Translate moves
            if not text: print('** No description for',line[1],'in',lang)
            for reminder, moveList in bonusDesc.items():
                for move in moveList:
                    if move == key:
                        text += f'<br><br><span style="color:rgb(145, 145, 145);">{tall["move"][reminder]["effect"]}</span>'
            text = text.replace('\n','')
            locDesc[index-fidThreshold[0]] = text
    print('Done translating ability/move descriptions')
    missingAmount = sum([1 for line in locDesc if not line])
    if missingAmount: print('** Missing',missingAmount,'ability/move descriptions')

    # Translate the header names and other ui elements =========================
    #region Translate UI Elements
    print('\nTranslating ui elements...')
    locUI = {} # Translated UI elements go into a dictionary, similar to overrides['en']
    if lang == 'en': 
        print('Index of tags:')       
        for index,desc in enumerate(overrides['en']['tagToDesc']):
            print(index, desc)
    
    locUI['headerNames'] = ['' for line in overrides['en']['headerNames']]
    locUI['headerNames'][0] = tall['filter-bar']['sortByNumber']
    locUI['headerNames'][1] = re.sub(r'\s*:\s*','',tall['pokedex-ui-handler']['cycleShiny'])
    locUI['headerNames'][2] = tall['filter-bar']['sortByName']
    locUI['headerNames'][3] = tall['filter-bar']['typeFilter']
    locUI['headerNames'][4] = tall['pokedex-ui-handler']['menuAbilities']
    locUI['headerNames'][5] = tall['pokedex-ui-handler']['eggMoves']
    locUI['headerNames'][6] = tall['filter-bar']['sortByCost']
    locUI['headerNames'][7] = tall['pokedex-ui-handler']['baseTotal']
    locUI['headerNames'][8] = tall['pokemon-info']['stat']['hpShortened']
    locUI['headerNames'][9] = tall['pokemon-info']['stat']['atkShortened']
    locUI['headerNames'][10] = tall['pokemon-info']['stat']['defShortened']
    locUI['headerNames'][11] = tall['pokemon-info']['stat']['spatkShortened']
    locUI['headerNames'][12] = tall['pokemon-info']['stat']['spdefShortened']
    locUI['headerNames'][13] = tall['pokemon-info']['stat']['spdShortened']

    locUI['altText'] = ['' for line in overrides['en']['altText']]
    locUI['altText'][0] = tall['pokemon-info-container']['moveset']
    locUI['altText'][1] = tall['pokemon-form']['pikachu']
    locUI['altText'][2] = re.sub(r'\s*:\s*','',tall['pokedex-ui-handler']['hidden'])
    locUI['altText'][3] = tall['filter-bar']['passive']
    locUI['altText'][4] = tall['pokedex-ui-handler']['scanLabelName']
    locUI['altText'][5] = tall['fight-ui-handler']['power']
    locUI['altText'][6] = tall['fight-ui-handler']['accuracy']
    locUI['altText'][7] = tall['fight-ui-handler']['pp']
    locUI['altText'][8] = re.sub(r'\s*:\s*','',tall['pokedex-ui-handler']['goFilters'])
    locUI['altText'][9] = tall['modifier-type']['ModifierType']['MEMORY_MUSHROOM']['name']
    locUI['altText'][10] = tall['pokedex-ui-handler']['evolutions']
    locUI['altText'][11] = tall['pokedex-ui-handler']['eggMoves']
    locUI['altText'][12] = f"{re.sub(r' *: *','',tall['pokedex-ui-handler']['rare'])} {locUI['altText'][11]}" # Rare egg move kinda funky
    locUI['altText'][13] = re.sub(r'\s*:\s*','',tall['pokedex-ui-handler']['common'])
    locUI['altText'][14] = re.sub(r'\s*:\s*','',tall['pokedex-ui-handler']['great'])
    locUI['altText'][15] = re.sub(r'\s*:\s*','',tall['pokedex-ui-handler']['ultra'])
    locUI['altText'][16] = tall['pokedex-ui-handler']['menuTmMoves']
    locUI['altText'][17] = tall['pokemon-summary']['lv']
    # locUI['altText'][18] = 'Evo' # (a 3-char version of 'Evolution')
    locUI['altText'][19] = tall['filter-bar']['egg']

    locUI['catToName'] = ['' for line in overrides['en']['catToName']]
    locUI['catToName'][0] = tall['filter-bar']['typeFilter']
    locUI['catToName'][1] = re.sub(r'\s*:\s*','',tall['filter-text']['ability1Field'])
    locUI['catToName'][2] = re.sub(r'\s*:\s*','',tall['filter-text']['move1Field'])
    locUI['catToName'][3] = tall['filter-bar']['genFilter']
    locUI['catToName'][4] = tall['filter-bar']['sortByCost']
    locUI['catToName'][5] = tall['filter-bar']['egg']
    locUI['catToName'][6] = re.sub('[&nbsp\s]','',tall['run-history']['mode'])
    locUI['catToName'][7] = tall['pokedex-ui-handler']['evolutions']
    locUI['catToName'][8] = re.sub(r'\s*:\s*','',tall['pokedex-ui-handler']['cycleForm'])
    locUI['catToName'][9] = tall['filter-bar']['biomeFilter']
    locUI['catToName'][10] = tall['pokedex-ui-handler']['evolutions'] # "Related To" filters
    locUI['catToName'][11] = f"{re.sub(r' *: *','',tall['pokedex-ui-handler']['cycleShiny'])} {re.sub(r' *: *','',tall['pokedex-ui-handler']['cycleVariant'])}"
    # locUI['catToName'][12] = overrides[lang]['phrases']['tag']

    locUI['infoText'] = ['' for line in overrides['en']['infoText']]
    locUI['infoText'][0] = tall['pokemon-summary']['friendship']
    locUI['infoText'][1] = tall['filter-bar']['passive']
    locUI['infoText'][2] = tall['filter-bar']['costReduction']
    locUI['infoText'][3] = tall['pokedex-ui-handler']['sameSpeciesEgg']
    locUI['infoText'][4] = tall['filter-bar']['hiddenAbility']
    # locUI['infoText'][5] = f"{tall['filter-bar']['egg']} {overrides[lang]['phrases']['exclusive']}"
    # locUI['infoText'][6] = 'Baby Exclusive'
    # locUI['infoText'][7] = 'Paradox Pokemon'
    # locUI['infoText'][8] = 'Form Change'
    locUI['infoText'][9] = tall['pokedex-ui-handler']['menuBiomes']
    # locUI['infoText'][10] = '(Chosen) Filters'

    locUI['biomeText'] = ['' for line in overrides['en']['biomeText']]
    locUI['biomeText'][0] = tall['biomes']['common']
    locUI['biomeText'][1] = tall['biomes']['uncommon']
    locUI['biomeText'][2] = tall['biomes']['rare']
    locUI['biomeText'][3] = tall['biomes']['superRare']
    locUI['biomeText'][4] = tall['biomes']['ultraRare']
    locUI['biomeText'][5] = tall['biomes']['boss']
    locUI['biomeText'][6] = tall['biomes']['common']
    locUI['biomeText'][7] = tall['biomes']['uncommon']
    locUI['biomeText'][8] = tall['biomes']['rare']
    locUI['biomeText'][9] = tall['biomes']['superRare']
    locUI['biomeText'][10] = tall['biomes']['ultraRare']
    locUI['biomeText'][11] = tall['biomes']['dawn']
    locUI['biomeText'][12] = tall['biomes']['day']
    locUI['biomeText'][13] = tall['biomes']['dusk']
    locUI['biomeText'][14] = tall['biomes']['night']

    locUI['procToDesc'] = ['' for line in overrides['en']['procToDesc']]
    #   0-6 = self atk/def/spa/spd/spe/acc/eva
    #  7-13 = opp  atk/def/spa/spd/spe/acc/eva
    # 14-20 = pois/tox/sleep/freeze/para/burn/confuse
    # 21-27 = flinch/omni/dire/triatt/terablast/damage/prio
    locUI['procToDesc'][0] = tall['pokemon-info']['stat']['atk']
    locUI['procToDesc'][1] = tall['pokemon-info']['stat']['def']
    locUI['procToDesc'][2] = tall['pokemon-info']['stat']['spatk']
    locUI['procToDesc'][3] = tall['pokemon-info']['stat']['spdef']
    locUI['procToDesc'][4] = tall['pokemon-info']['stat']['spd']
    locUI['procToDesc'][5] = tall['pokemon-info']['stat']['acc']
    locUI['procToDesc'][6] = tall['pokemon-info']['stat']['eva']
    locUI['procToDesc'][7] = tall['pokemon-info']['stat']['atk']
    locUI['procToDesc'][8] = tall['pokemon-info']['stat']['def']
    locUI['procToDesc'][9] = tall['pokemon-info']['stat']['spatk']
    locUI['procToDesc'][10] = tall['pokemon-info']['stat']['spdef']
    locUI['procToDesc'][11] = tall['pokemon-info']['stat']['spd']
    locUI['procToDesc'][12] = tall['pokemon-info']['stat']['acc']
    locUI['procToDesc'][13] = tall['pokemon-info']['stat']['eva']
    locUI['procToDesc'][14] = tall['status-effect']['poison']['name']
    locUI['procToDesc'][15] = tall['status-effect']['toxic']['name']
    locUI['procToDesc'][16] = tall['status-effect']['sleep']['name']
    locUI['procToDesc'][17] = tall['status-effect']['freeze']['name']
    locUI['procToDesc'][18] = tall['status-effect']['paralysis']['name']
    locUI['procToDesc'][19] = tall['status-effect']['burn']['name']
    locUI['procToDesc'][20] = tall['battler-tags']['confusedDesc']
    locUI['procToDesc'][21] = tall['battler-tags']['flinchedDesc']
    locUI['procToDesc'][22] = f"{tall['pokemon-info']['stat']['atkShortened']}/{tall['pokemon-info']['stat']['defShortened']}/{tall['pokemon-info']['stat']['spatkShortened']}/{tall['pokemon-info']['stat']['spdefShortened']}/{tall['pokemon-info']['stat']['spdShortened']}"
    locUI['procToDesc'][23] = f"{tall['status-effect']['poison']['name']}/{tall['status-effect']['paralysis']['name']}/{tall['status-effect']['sleep']['name']}"
    locUI['procToDesc'][24] = f"{tall['status-effect']['burn']['name']}/{tall['status-effect']['paralysis']['name']}/{tall['status-effect']['freeze']['name']}"
    locUI['procToDesc'][25] = tall['pokemon-info']['type']['stellar']
    locUI['procToDesc'][26] = tall['settings']['damageNumbers']
    locUI['procToDesc'][27] = tall['modifier-type']['ModifierType']['QUICK_CLAW']['description']

    locUI['tagToDesc'] = ['' for line in overrides['en']['tagToDesc']]
    locUI['tagToDesc'][4]  = tall['ability']['sheerForce']['name']
    locUI['tagToDesc'][23] = f"{tall['pokemon-info']['type']['grass']}/{tall['ability']['overcoat']['name']}"
    locUI['tagToDesc'][24] = tall['pokemon-info']['type']['grass']
    locUI['tagToDesc'][25] = tall['ability']['triage']['name']
    locUI['tagToDesc'][26] = tall['ability']['dancer']['name']
    locUI['tagToDesc'][27] = tall['ability']['windRider']['name']
    locUI['tagToDesc'][28] = tall['ability']['sharpness']['name']
    locUI['tagToDesc'][29] = tall['ability']['ironFist']['name']
    locUI['tagToDesc'][30] = tall['ability']['megaLauncher']['name']
    locUI['tagToDesc'][31] = tall['ability']['strongJaw']['name']
    locUI['tagToDesc'][32] = tall['ability']['reckless']['name']
    locUI['tagToDesc'][33] = tall['ability']['bulletproof']['name']
    locUI['tagToDesc'][34] = tall['ability']['damp']['name']
    locUI['tagToDesc'][36] = tall['move']['substitute']['name']
    locUI['tagToDesc'][38] = tall['move']['protect']['name']
    locUI['tagToDesc'][60] = tall['ability']['intimidate']['name']
    locUI['tagToDesc'][71] = tall['modifier-type']['ModifierType']['LURE']['name']

    locUI['biomeLongText'] = ['' for line in overrides['en']['biomeLongText']]
    locUI['warningText'] = ['' for line in overrides['en']['warningText']]
    locUI['helpMenuText'] = ['' for line in overrides['en']['helpMenuText']]

    print('Done translating ui elements')
    allCatToCheck = ['headerNames','altText','catToName','biomeText','infoText']
    if lang in ignoreOverrides or 'all' in ignoreOverrides:
        for catToCheck in allCatToCheck:
            missingAmount = sum([1 for line in locUI[catToCheck] if not line])
            if missingAmount: print('Could not auto translate',missingAmount,'ui elements in',catToCheck)

    # Apply manual overrides from the lang_overrides folder =========================
    #region Apply Overrides
    # These go directly onto the SearchDex
    if lang not in ignoreOverrides and 'all' not in ignoreOverrides:
        for overrideName in overrides['en'].keys():
            if overrideName in overrides[lang]:
                locUI[overrideName] = overrides[lang][overrideName]
            elif overrideName in ['procToDesc','tagToDesc','biomeLongText','warningText','helpMenuText']:
                locUI[overrideName] = overrides['en'][overrideName] # Fallback to english names
            else:
                print('***** Missing override object',overrideName,'in',lang)
    # Do a final check for missing UI elements
    missingAmount = 0
    for catToCheck in allCatToCheck:
        missingAmount += len(overrides['en'][catToCheck]) - sum([1 for line in locUI[catToCheck] if line])
    if missingAmount: print('\n***** Missing',missingAmount,'ui elements')
    
    #region Write Data
    # Write all the translated text to lang/{lang}.js =========================
    # headerNames, altText, catToName, infoText, biomeText, biomeLongText,
    # warningText, procTodesc, tagToDesc, fidToDesc, speciesNames, fidToName, helpMenuText
    print("\nWriting to website language files...")
    jsText = []
    # Show a warning to not edit the javascript files directly
    # Changes must be done through the python override files
    jsText.append('// Do not edit these files directly\n')
    jsText.append('// They are changed automatically by the update script\n')
    jsText.append('// Changes must be made through the updater repository')

    def addLines(varName, varContent): # Write a variable and its content to the javascript file
        jsText.append(f'\n{varName} = [')
        newLine = "\n" if len(varContent) > 20 or len(varContent[0]) > 20 else "" # Use new lines for long content
        for content in varContent:
            content = content.replace("'","’") # Replace single quotes with unicode
            quotes = "`" if "{" in content else "'" # Use javascript template string if needed
            jsText.append(f"{newLine}{quotes}{content}{quotes},")
        jsText[-1] = jsText[-1][:-1] # Remove final comma
        jsText.append(f'{newLine}];')
    
    # Add all the manually translated things from the override file
    for categoryName in overrides['en'].keys():
        if categoryName not in ['helpMenuText','phrases','substitutions']:
            addLines(categoryName, locUI[categoryName]) # Add each UI category

    # Add all the auto-translated things from the game files
    addLines('fidToDesc', locDesc)       # filter descriptions
    addLines('speciesNames', locSpecies) # species display names
    addLines('fidToName', locFilters)    # localized filter names
    
    # helpMenuText must be done last because it references other strings
    addLines('helpMenuText', locUI['helpMenuText']) # help menu text

    with open(f"website/lang/{lang}.js", "w", encoding="utf-8") as file:
        file.writelines(jsText)
    print(f"Finished writing language file: {lang}.js")

print("\n=========== ALL LANGUAGES DONE ===========\n")