# Creates all the localized string files
import re, os, json, importlib
pathLocales = './game_files/locales' # File path to the official localization files
pathOverrides = "local_files/lang_overrides"
allLangs = ['en','fr','ko','ja','zh-Hans','es-ES','it']

langsToDo = ['']
# Specify a subset of languages to process
# Leave blank to process all languages

ignoreOverrides = [''] 
# Put a language in here to ignore the .py override file
# Can put 'all' to ignore for every language
# This lets you see what the script can auto-translate

warnLongNames = 0 
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
#   Add language to the langs loop
#   Manually translate the phrases in manualTran
#   If the main loop gives an error, the in-game translation is incomplete
#   Only continue if there are no errors
#   Check length of types/abilities/moves/species
#   Check length and meaning of headers/etc
#   Put in overrides for those if necessary
#   Auto translate the help menu, but use exact translate for words that appear in headers/etc
#   Provide overrides for headers/etc. to make sure spacing is good, and check for other bugs

subs = { # Replacement strings to make text fit
    'en': [
        ["Nidoran F","Female Nidoran"],
        ["Nidoran M","Male Nidoran"],
        ["50 Zygarde","50% Zygarde"],
        ["50 PC Zygarde","Power Construct 50% Zygarde"],
        ["10 Zygarde","10% Zygarde"],
        ["10 PC Zygarde","Power Construct 10% Zygarde"],
        ["10 Complete Zygarde","Complete 10% Zygarde"],
        ["Lowkey Toxtricity","Low Key Toxtricity"],
        ["???","The End"],
    ],
    'fr': [
        ['Osmose Équine','Osmose'],
        ['Masque de la ',''],
        ['Masque du ',''],
        ['Masque ',''],
        ['Rassemblement Forme','Rassemblement'],
        ['Mode Transe ','Transe '],
    ]
}

# All the manual translations =====================
manualTran = {
    'en': {
        'exclusive': 'Exclusive',
        'shinyVariants': 'Shiny Variants',
        'new': 'New',
        'tag': 'Tag',
        'lureAbility': 'Lure Ability',
        'ignoresAbilities': 'Ignores Abilities',
        'targetSwitchesOut': 'Target Switches Out',
        'spreadMoves': 'Spread Moves',
        'waterImmunity': 'Water Immunity',
        'electricImmunity': 'Electric Immunity',
        'sunAbility': 'Sun Ability',
        'rainAbility': 'Rain Ability',
        'sandAbility': 'Sand Ability',
        'snowAbility': 'Snow Ability',
    },
    'fr': {
        'exclusive': 'Exclusif',
        'shinyVariants': 'Variantes Chromatique',
        'new': 'Nouvelle',
        'tag': 'Attribut',
        'lureAbility': 'Talent d’Appât',
        'ignoresAbilities': 'Ignore les Talents',
        'targetSwitchesOut': 'Force le Changement',
        'spreadMoves': 'Attaques de Zone'
    },
    'ko': {
        'exclusive': '한정',
        'shinyVariants': '색 다른 이로치',
        'new': '새로운',
        'tag': '속성',
        'lureAbility': '유인 특성',
        'ignoresAbilities': '특성 무시',
        'targetSwitchesOut': '상대 교체',
        'spreadMoves': '범위 기술'
    },
    'ja': {
        'exclusive': '限定',
        'shinyVariants': '色違い',
        'new': '新しい',
        'tag': '属性',
        'lureAbility': 'おびき寄せ特性',
        'ignoresAbilities': '特性無視',
        'targetSwitchesOut': '強制交代',
        'spreadMoves': '範囲技'
    },
    'zh-Hans': {
        'exclusive': '限定',
        'shinyVariants': '变种闪光',
        'new': '新的',
        'tag': '属性',
        'lureAbility': '诱导特性',
        'ignoresAbilities': '无视特性',
        'targetSwitchesOut': '迫使对手替换',
        'spreadMoves': '范围招式'
    },
    'es-ES': {
        'exclusive': 'Exclusivo',
        'shinyVariants': 'Variantes Shiny',
        'new': 'Nuevo',
        'tag': 'Atributo',
        'lureAbility': 'Habilidad de Colonia',
        'ignoresAbilities': 'Ignora Habilidades',
        'targetSwitchesOut': 'Cambia al Objetivo',
        'spreadMoves': 'Movimientos de Área'
    },
    'it': {
        'exclusive': 'Esclusivo',
        'shinyVariants': 'Varianti Cromatiche',
        'new': 'Nuovo',
        'tag': 'Attributo',
        'lureAbility': 'Abilità Esca',
        'ignoresAbilities': 'Ignora Abilità',
        'targetSwitchesOut': 'Forza il Cambio',
        'spreadMoves': 'Mosse ad Area'
    }
}

# Functions for formatting the text
def format_for_camel(arg): # Key format for official jsons
    arg = arg.title().replace(' ','')
    return f'{arg[0].lower()}{arg[1:]}'  
def is_numeric(value): # Function to determine if a value is numeric
    return re.match(r'^-?\d+(\.\d+)?$', str(value)) is not None
def shortenText(text):
    if lang in subs:
        for line in subs[lang]:
            text = str(text).replace(line[0],line[1])
    return text

# Load all the manual overrides from the lang_overrides folder, these are applied at the end
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

    tall = {}
    fileNames = [file for file in os.listdir(path) if file.lower().endswith('.json')]
    for fileName in fileNames:
        with open(f'{path}/{fileName}', "r", encoding="utf-8") as file:
            keyName = fileName.split('.')[0]
            tall[keyName] = json.load(file)

    # Translate everything from allFilters =========================
    print('\nTranslating filter names...')
    with open("local_files/my_json/allFilters.json", "r") as file:
        allFilters = json.load(file) # These have to be reloaded for every lang, because they are overwritten in english
    locFilters = ['' for line in allFilters]
    # Translate types
    for index,filter in enumerate(allFilters):
        if filter[0] == 'Type':
            text = tall['pokemon-info']['type'][filter[1].lower()]
            text = shortenText(text)
            locFilters[index] = text
            if len(text) > 8 and warnLongNames:
                print('Long type found:',text)
    # Translate abilities
    for index,filter in enumerate(allFilters):
        if filter[0] == 'Ability':
            key = format_for_camel(filter[1])
            if 'embody' in key: # Add variants of embody aspect, with stat names
                if 'Teal' in key:
                    text = f"{tall['ability'][key]['name']} {tall['pokemon-info']['stat']['spd'].replace(' ','&nbsp')}"
                elif 'Wellspring' in key:
                    text = f"{tall['ability'][key]['name']} {tall['pokemon-info']['stat']['spdef'].replace(' ','&nbsp')}"
                elif 'Hearthflame' in key:
                    text = f"{tall['ability'][key]['name']} {tall['pokemon-info']['stat']['atk'].replace(' ','&nbsp')}"
                elif 'Cornerstone' in key:
                    text = f"{tall['ability'][key]['name']} {tall['pokemon-info']['stat']['def'].replace(' ','&nbsp')}"
                else:
                    input('Could not find mask')
            elif key == 'asOneGlastrier': # Add horse names to "As One"
                text = f"{tall['ability'][key]['name']} {tall['pokemon']['glastrier']}"
            elif key == 'asOneSpectrier':
                text = f"{tall['ability'][key]['name']} {tall['pokemon']['spectrier']}"
            else:
                text = tall['ability'][key]['name']
            text = shortenText(text)
            locFilters[index] = text
            # print('Translated',filter[1],'to',text)
            if len(text) > 15 and warnLongNames:
                print('Long ability found:',text)
    # Translate moves
    for index,filter in enumerate(allFilters):
        if filter[0] == 'Move':
            text = tall['move'][format_for_camel(filter[1])]['name']
            text = shortenText(text)
            locFilters[index] = text
            # print('Translated',filter[1],'to',text)
            if len(text) > 15 and warnLongNames:
                print('Long move found:',text)
    # Copy numeric values
    for index,filter in enumerate(allFilters):
        # if is_numeric(filter[1]):
        if filter[0] == 'Gen' or filter[0] == 'Cost':
            # print('Copied',filter[1])
            locFilters[index] = filter[1]
    # Translate female
    for index,filter in enumerate(allFilters):
        if filter[0] == 'Gender':
            text = tall['pokemon-form']['espurrFemale']
            # print('Translated',filter[1],'to',text)
            locFilters[index] = text
    # Translate modes
    for index,filter in enumerate(allFilters):
        if filter[0] == 'Mode':
            text = filter[1]
            if 'Flip' in filter[1]:
                if 'name' in tall['challenges']['flipStat']:
                    text = tall['challenges']['flipStat']['name']
            if 'Fresh' in filter[1]:
                if 'name' in tall['challenges']['freshStart']:
                    text = tall['challenges']['freshStart']['name']
            if 'Starter' in filter[1]:
                if 'starter' in tall['filter-bar']:
                    text = tall['filter-bar']['starter']
            locFilters[index] = text
    # Translate egg tiers
    for index,filter in enumerate(allFilters):
        if filter[0] == 'Egg Tier':
            text = ''
            if filter[1] == 'Common':
                text = 'defaultTier'
            if filter[1] == 'Rare':
                text = 'greatTier'
            if filter[1] == 'Epic':
                text = 'ultraTier'
            if filter[1] == 'Legendary':
                text = 'masterTier'
            if text:
                text = tall['egg'][text]
                # print('Translated',filter[1],'to',text)
                locFilters[index] = text
    # Translate manaphy egg tier
    for index,filter in enumerate(allFilters):
        if filter[0] == 'Egg Tier' and filter[1] == 'Manaphy':
            text = tall['pokemon']['manaphy']
            # print('Translated',filter[1],'to',text)
            locFilters[index] = text
    # Translate exclusive egg tier
    for index,filter in enumerate(allFilters):
        if filter[0] == 'Egg Tier' and filter[1] == 'Exclusive':
            locFilters[index] = manualTran[lang]['exclusive']
    # Translate new variants filter
    for index,filter in enumerate(allFilters):
        if filter[0] == 'Shiny Variants':
            if filter[1] == 'New':
                locFilters[index] = manualTran[lang]['new']
            if filter[1] == 'All':
                locFilters[index] = tall['menu']['yes']
            if filter[1] == 'None':
                locFilters[index] = tall['menu']['no']
    # Translate biome names
    for index,filter in enumerate(allFilters):
        if filter[0] == 'Biome':
            text = tall['biomes'][format_for_camel(filter[1])]
            if lang == 'en': # Get official names of biome, even in english
                filter[1] = text
            locFilters[index] = shortenText(text)
    # Translate tag names
    for index,filter in enumerate(allFilters):
        if filter[0] == 'Tag':
            for key in ['lureAbility','ignoresAbilities','targetSwitchesOut','spreadMoves']:
                if manualTran['en'][key] in filter[1]:
                    text = manualTran[lang][key]
                    # if '(Ability)' in filter[1]: text += f"({re.sub(r' *: *','',tall['filter-text']['ability1Field'])})"
                    # if '(Move)' in filter[1]: text += f"({re.sub(r' *: *','',tall['filter-text']['move1Field'])})"
                    locFilters[index] = text
    # Translate names of family filters
    for index,filter in enumerate(allFilters):
        if filter[0] == 'Related To':
            text = format_for_camel(filter[1])
            if text in tall['pokemon']:
                justLocForm = ''
                justLocSpec = tall['pokemon'][text]
            else:
                print('Could not find base species',text)
                input()
            # Put the name in correct format
            nameFormat = '{{pokemonName}}'
            if 'Alola' in filter[1]:
                nameFormat = tall['pokemon-form']['appendForm']['alola']
            if 'Galar' in filter[1]:
                nameFormat = tall['pokemon-form']['appendForm']['galar']
            if 'Hisui' in filter[1]:
                nameFormat = tall['pokemon-form']['appendForm']['hisui']
            if 'Paldea' in filter[1]:
                nameFormat = tall['pokemon-form']['appendForm']['paldea']
            nameFormat = re.sub('{{pokemonName}}',justLocSpec,nameFormat)
            nameFormat = re.sub("'",'',nameFormat) # Remove single quotes
            # nameFormat = re.sub(":",' ',nameFormat)
            # print('Translated',specLine[0],'to',nameFormat)
            locFilters[index] = nameFormat
            if len(nameFormat) > 20 and warnLongNames:
                print('Long name found:',nameFormat)
            if not nameFormat or '{' in nameFormat:
                input('Blank pokemon entry')
    for i in range(len(locFilters)):
        locFilters[i] = re.sub('-',' ',str(locFilters[i]))
    if lang == 'en': # Many of the english filters are custom from updateDatabase.py
        locFilters = [shortenText(line[1]) for line in allFilters] # Only some are modified in this file (like biome)
    missingAmount = sum([1 for line in locFilters if not line])
    print('Done translating filter names')     
    if missingAmount: input(f'***** Missing {missingAmount} filter names')
    
    # Translate speciesNames =========================
    print('\nTranslating species names...')
    with open("local_files/my_json/allSpecies.json", "r") as file:
        allSpecies = json.load(file)
    maxSpecLength = 0
    for specLine in allSpecies:
        maxSpecLength = max(maxSpecLength, len(specLine[0]))
    # print('Longest species name in default list is',longest)
    locSpecies = ['' for line in allSpecies]
    maxLenSpec = 0
    for index,specLine in enumerate(allSpecies): # specLine is [full name, form name, species name]
        
        if specLine[2] == 'Koraidon' or specLine[2] == 'Miraidon':
            specLine[1] = '' # Remove form key of those pokemon

        # Translate just the base species name
        text = format_for_camel(specLine[2])
        if text in tall['pokemon']:
            justLocForm = ''
            justLocSpec = tall['pokemon'][text]
        else:
            print('Could not find base species',text)
            input()

        # Translate the form name
        if specLine[1]: # If it is a form
            effSpec = specLine[2]
            # The game only lists form keys for the first stage of evolution
            # If a form pokemon evolves, it needs to be manually linked here
            if effSpec == 'Wormadam': effSpec = 'Burmy'
            if effSpec == 'Cherrim': effSpec = 'Cherubi'
            if effSpec == 'Gastrodon': effSpec = 'Shellos'
            if effSpec == 'Darmanitan': effSpec = 'Darumaka'
            if effSpec == 'Sawsbuck': effSpec = 'Deerling'
            if effSpec == 'Frogadier': effSpec = 'Froakie'
            if effSpec == 'Greninja': effSpec = 'Froakie'
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
            if specLine[1] == '10 Complete': specLine[1] = 'Complete'
            text = format_for_camel(f'{effSpec} {specLine[1]}')
            if text in tall['pokemon-form']: # For regular forms
                justLocForm = tall['pokemon-form'][text]
                # print('Translated',specLine[0],'to',justLocForm,justLocSpec)
            elif format_for_camel(specLine[1]) in tall['pokemon-form']['battleForm']: # For mega/giga/etc
                justLocForm = tall['pokemon-form']['battleForm'][format_for_camel(specLine[1])]
            elif effSpec == 'Arceus' or effSpec == 'Silvally':
                justLocForm = tall['pokemon-info']['type'][specLine[1].lower()]
            else:
                print('Could not find',text)
                input()

        # Put the name in correct format (for regionals or forms)
        nameFormat = '{{pokemonName}}'
        if 'Alola' in specLine[2]:
            nameFormat = tall['pokemon-form']['appendForm']['alola']
        if 'Galar' in specLine[2]:
            nameFormat = tall['pokemon-form']['appendForm']['galar']
        if 'Hisui' in specLine[2]:
            nameFormat = tall['pokemon-form']['appendForm']['hisui']
        if 'Paldea' in specLine[2]:
            nameFormat = tall['pokemon-form']['appendForm']['paldea']
        if tall['pokemon-form']['appendForm']['generic'] != '{{pokemonName}} ({{formName}})':
            input('Odd format detected') # This is never used, but it's just to check the format
        if specLine[1]: # If it is a form
            if lang == 'fr':
                nameFormat = f'{nameFormat} {justLocForm}' # French has form name after
                if 'Méga' in justLocForm:
                    nameFormat = f'Méga-{nameFormat.replace(" Méga","")}'
            else:
                nameFormat = f'{justLocForm} {nameFormat}' # Other langs have form name first

        # Insert the species name, and remove most punctuation
        nameFormat = re.sub('{{pokemonName}}',justLocSpec,nameFormat)
        nameFormat = re.sub("'",'',nameFormat) # Keep ’
        # nameFormat = re.sub(":",' ',nameFormat)
        # print('Translated',specLine[0],'to',nameFormat)
        if lang == 'en': # Use my custom english names, using form keys, not actual form names
            nameFormat = specLine[0] # They don't have punctuation because I just use the keys from the code
            # To-do: Farfetch'd, Sirfetch'd, Ho-oh, Porygon-Z, Porygon2, Type: Null, Mr. Mime, Mime Jr., Mr. Rime
        nameFormat = shortenText(nameFormat)
        locSpecies[index] = nameFormat
        maxLenSpec = max(maxLenSpec, len(nameFormat))
        if len(nameFormat) > maxSpecLength and warnLongNames:
            print('Name longer than',maxSpecLength,'found:',nameFormat)
        if not nameFormat or '{' in nameFormat:
            input('Error with pokemon entry',nameFormat,specLine)
    missingAmount = sum([1 for line in locSpecies if not line])
    print('Done translating species names')
    if missingAmount: input('***** Missing',missingAmount,'species names')

    # Translate the descriptions of abilities/moves =========================
    print('\nTranslating filter descriptions...')
    locDesc = ['' for line in allFilters if (line[0] == 'Move' or line[0] == 'Ability')]
    with open("local_files/my_json/fidThresholds.json", "r") as fp:
        fidThresholds = json.load(fp)
    # Translate abilities
    for index,filter in enumerate(allFilters):
        if filter[0] == 'Ability':
            key = format_for_camel(filter[1])
            if 'description' in tall['ability'][key]:
                text = tall['ability'][key]['description'].replace('\n','')
            else:
                text = ''
                print('No description for',filter[1],'in',lang)
            locDesc[index-fidThresholds[0]] = text
    # Translate moves
    for index,filter in enumerate(allFilters):
        if filter[0] == 'Move':
            if 'effect' in tall['move'][format_for_camel(filter[1])]:
                text = tall['move'][format_for_camel(filter[1])]['effect'].replace('\n','')
            else:
                text = ''
                print('** No description for',filter[1],'in',lang)
            locDesc[index-fidThresholds[0]] = text
    missingAmount = sum([1 for line in locDesc if not line])
    print('Done translating ability/move descriptions')
    if missingAmount: print('** Missing',missingAmount,'ability/move descriptions')

    # Translate the header names and other ui elements =========================
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
    # locUI['altText'][18] = 'Evo'
    locUI['altText'][19] = tall['filter-bar']['egg']

    locUI['catToName'] = ['' for line in overrides['en']['catToName']]
    locUI['catToName'][0] = tall['filter-bar']['typeFilter']
    locUI['catToName'][1] = re.sub(r'\s*:\s*','',tall['filter-text']['ability1Field'])
    locUI['catToName'][2] = re.sub(r'\s*:\s*','',tall['filter-text']['move1Field'])
    locUI['catToName'][3] = tall['filter-bar']['genFilter']
    locUI['catToName'][4] = tall['filter-bar']['sortByCost']
    locUI['catToName'][5] = re.sub(r'\s*:\s*','',tall['pokedex-ui-handler']['cycleGender'])
    locUI['catToName'][6] = re.sub('[&nbsp\s]','',tall['run-history']['mode'])
    locUI['catToName'][7] = tall['filter-bar']['egg']
    locUI['catToName'][8] = manualTran[lang]['shinyVariants']
    locUI['catToName'][9] = tall['filter-bar']['biomeFilter']
    locUI['catToName'][10] = tall['pokedex-ui-handler']['evolutions']
    locUI['catToName'][11] = manualTran[lang]['tag']

    locUI['infoText'] = ['' for line in overrides['en']['infoText']]
    locUI['infoText'][0] = tall['pokemon-summary']['friendship']
    locUI['infoText'][1] = tall['filter-bar']['passive']
    locUI['infoText'][2] = tall['filter-bar']['costReduction']
    locUI['infoText'][3] = tall['pokedex-ui-handler']['sameSpeciesEgg']
    locUI['infoText'][4] = tall['filter-bar']['hiddenAbility']
    locUI['infoText'][5] = f"{tall['filter-bar']['egg']} {manualTran[lang]['exclusive']}"
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
    locUI['tagToDesc'][59] = tall['modifier-type']['ModifierType']['LURE']['name']

    locUI['biomeLongText'] = ['' for line in overrides['en']['biomeLongText']]
    locUI['warningText'] = ['' for line in overrides['en']['warningText']]
    locUI['helpMenuText'] = overrides['en']['helpMenuText']

    print('Done translating ui elements')
    missingAmount = sum([1 for line in locUI['headerNames']+locUI['altText']+locUI['catToName']+locUI['biomeText']+locUI['infoText'] if not line])
    if missingAmount: print('Could not auto translate',missingAmount,'ui elements')

    # Apply manual overrides from the lang_overrides folder =========================
    # These go directly onto the searchdex
    if lang not in ignoreOverrides and 'all' not in ignoreOverrides:
        for overrideName in overrides['en'].keys():
            if overrideName in overrides[lang]:
                locUI[overrideName] = overrides[lang][overrideName]
            elif overrideName in ['procToDesc','tagToDesc','biomeLongText','warningText']:
                locUI[overrideName] = overrides['en'][overrideName] # Fallback to english names
            else:
                print('***** Missing override object',overrideName,'in',lang)
    # Do a final check for missing UI elements
    missingAmount = sum([1 for line in locUI['headerNames']+locUI['altText']+locUI['catToName']+locUI['biomeText']+locUI['infoText'] if not line])
    if missingAmount: print('***** Missing',missingAmount,'ui elements')

    # Write all the translated text to lang/{lang}.js =========================
    # headerNames, altText, catToName, fidToDesc, speciesNames, fidToName
    print("\nWriting to website language files...")
    # Assemble the lines of data
    lines = []
    lines.append('// Do not edit these files directly\n')
    lines.append('// They are changed automatically by the update script\n')
    lines.append('// Changes must be made through the updater repository\n')
    for overrideName in overrides['en'].keys():
        if overrideName != 'helpMenuText':
            lines.append(f'{overrideName} = [') # Add each UI category
            for line in locUI[overrideName]:
                if overrideName in ['biomeLongText','warningText']:
                    if "'" in line: 
                        print('** Single quote found in',line)
                        line = line.replace("'","’")
                    lines.append(f"\n'{line}',")
                elif overrideName in ['procToDesc','tagToDesc']:
                    lines.append(f'\n"{line}",')
                else:
                    lines.append(f"'{line}',")
            lines[-1] = lines[-1][:-1] # Remove comma
            lines.append('];\n')

    lines.append('fidToDesc = [') # filter descriptions
    for line in locDesc:
        if "'" in line: 
            print('** Single quote found in',line)
            line = line.replace("'","’")
        lines.append(f"\n'{line}',")
    lines[-1] = lines[-1][:-1]
    lines.append('\n];\n')

    lines.append('speciesNames = [') # species display names
    for line in locSpecies:
        lines.append(f"\n'{line}',")
    lines[-1] = lines[-1][:-1]
    lines.append('\n];\n')

    lines.append('fidToName = [') # localized filter names
    for filter in locFilters:
        lines.append(f"\n'{filter}',")
        if "'" in str(filter):
            input('Single quote found in',filter)
    lines[-1] = lines[-1][:-1]
    lines.append('\n];\n')

    lines.append('helpMenuText = `') # help text
    # This must be done last because it references other strings
    lines.append(locUI['helpMenuText'])
    lines.append('`;')

    with open(f"website/lang/{lang}.js", "w", encoding="utf-8") as file:
        file.writelines(lines)
    print("Filter writing complete")

print("\n********** ALL LANGUAGES DONE **********\n")