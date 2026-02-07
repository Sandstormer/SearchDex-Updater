headerNames = ['Dex','Image','Species','Types','Abilities','Egg Moves','Cost', # [0-6]
               'BST','HP','Atk','Def','SpA','SpD','Spe'] # [7-13]
altText = ['Moves','Main Only','Hidden Only','Passive Only','Search','Pow','Acc','PP', # [0-7]
           'Add to filters','Memory','Shiny','Egg Move','Rare Egg Move', # [8-12]
           'Common','Great','Ultra','TM','Lv.','Evo','Egg'] # [13-19]
catToName = ['Type','Ability','Move','Gen','Cost','Egg Tier','Mode', # [0-6]
             'Evolution','Form','Biome','Related To','Shiny Variants','Tag'] # [7-12]
infoText = ['Friendship per Candy','Passive','Cost Reduction','Species Egg','Hidden Ability', # [0-4]
            'Egg Exclusive','Baby Exclusive','Paradox Pokemon','Form Change','Biomes','Filters', # [5-10]
            'Reduced after ## eggs','via Level','via Egg','via TM'] # [11-14]
biomeText = ['Common','Uncommon','Rare','Super Rare','Ultra Rare', # [0-4]
             'Boss','Com.','Unc.','Rare','SR','UR','Dawn','Day','Dusk','Night'] # [5-10][11-14]
biomeLongText = [
    '<b>This form is only available via <span style="color:rgb(140, 130, 240);">Form Change</span>.</b> Other forms can be encountered in the biomes shown.',
    '<b>This Pokemon is <span style="color:rgb(143, 214, 154);">Egg Exclusive</span>.</b><br>It does not appear in any biomes, and can only be obtained from eggs.',
    '<b>This is a <span style="color:rgb(216, 143, 205);">Baby Pokemon</span>.</b><br>It does not appear in any biomes, but can be unlocked by encountering its evolution.',
    '<b>This <span style="color:rgb(239, 131, 131);">Paradox Pokemon</span> is <span style="color:rgb(143, 214, 154);">Egg Exclusive</span>.</b><br>It can only be obtained from eggs, but can afterward be caught in Classic mode.',
    'This Pokemon can only be caught after obtaining <b><span style="color:rgb(239, 131, 131);">All Other Pokemon</span></b>.<br>It does not appear in standard eggs.',
    '<b>This form is unobtainable.</b>',
]
phrases = { # Phrases to be used in the auto-translating of filters (do not translate the left side of each line)
    'exclusive': 'Exclusive',
    'new': 'New',
    'tag': 'Tag', # A tag/attribute/property of a move
    'theEnd': 'The End', # The final biome/zone
    'fullyEvolved': 'Fully Evolved',
    'formBase': 'Base', # Referring to the base form of a pokemon (not mega, giga, etc.)
    'formMega': 'Mega', # Shorthand for Mega evolution
    'formNewMega': 'New Mega', # Shorthand for newly introduced Mega evolutions
    'formGiga': 'Giga', # Shorthand for Gmax/Gigantamax
    'formTransformed': 'Transformed', # Shorthand for other pokemon forms
    'lureAbility': 'Lure Ability',
    'ignoresAbilities': 'Ignores Abilities',
    'electricImmunity': 'Electric Immunity',
    'fireImmunity': 'Fire Immunity',
    'waterImmunity': 'Water Immunity',
    'rainAbility': 'Rain Ability',
    'sandAbility': 'Sand Ability',
    'snowAbility': 'Snow Ability',
    'sunAbility': 'Sun Ability',
    'targetSwitchesOut': 'Target Switches Out',
    'spreadMoves': 'Spread Moves',
}
substitutions = [ # Text shortenings to make it fit in the UI
    ["Nidoran F","Female Nidoran"],
    ["Nidoran M","Male Nidoran"],
    ["50 Zygarde","50% Zygarde"],
    ["50 PC Zygarde","Power Construct 50% Zygarde"],
    ["10 Zygarde","10% Zygarde"],
    ["10 PC Zygarde","Power Construct 10% Zygarde"],
    ["Lowkey Toxtricity","Low Key Toxtricity"],
]
warningText = [
    'Restricted to Pokemon that have shiny variants.',
    'Abilities are restricted to only Main Abilities.',
    'Abilities are restricted to only Hidden Abilities.',
    'Abilities are restricted to only Passive Abilities.',
    '<b>There are no Pokemon that match the filters and the search term.</b><br>Adding another filter may change the results.',
    '<b>Click on a suggestion to filter it.</b><br>Filter preview is only for Species/Types/Abilities.',
    '<b>There are no Pokemon that match the filters and the search term.</b><br>Try a different combination.',
    '<b>There are no Pokemon that match the filters.</b><br>Remove filters, or change the connections to "OR".',
    '<b>There are no Pokemon or filters that match the search term.</b><br>Please check your spelling and try again.',
    'Click to see the instructions.',
]
procToDesc = ["User Atk","User Def","User SpAtk","User SpDef","User Speed","User Accuracy","User Evasion", # [0-6]
    "Atk","Def","SpAtk","SpDef","Speed","Accuracy","Evasion", # [7-13]
    "Applies Poison","Applies Toxic","Applies Sleep","Applies Freeze","Applies Paralysis","Applies Burn","Applies Confuse", # [14-20]
    "Flinch","User Atk/Def/SpA/SpD/Spe","Poison/Para/Sleep","Burn/Para/Freeze","Stellar User Atk/SpAtk","Damage","Priority"] # [21-27]
tagToDesc = [
    "Targets: Random Enemy",
    "Targets: All Enemies",
    "Targets: Entire Field",
    "Affected by Sheer Force",
    "High Critical Ratio",
    "Guaranteed Critical Hit",
    "User Critical Rate +2",
    "User Atk maxed",
    "Costs 33% of HP",
    "Costs 50% of HP",
    "Recoil 50% of HP",
    "Recoil 50% of damage",
    "Recoil 33% of damage",
    "Recoil 25% of damage",
    "30% deal double damage",
    "Heals 100% damage dealt",
    "Heals 75% damage dealt",
    "Heals 50% damage dealt",
    "Heals based on target's Atk",
    "Heals Status Effects",
    "Heals Sleep",
    "Heals Freeze",
    "Heals Burn",
    "No effect on Grass/Overcoat",
    "No seeding on Grass Types",
    "Triggers Triage ability",
    "Triggers Dancer ability",
    "Triggers Wind Rider ability",
    "Boosted by Sharpness",
    "Boosted by Iron Fist",
    "Boosted by Mega Launcher",
    "Boosted by Strong Jaw",
    "Boosted by Reckless",
    "No effect on Bulletproof",
    "Prevented by Damp ability",
    "Sound based move",
    "Ignores Substitute",
    "Ignores Abilities",
    "Ignores Protect",
    "User switches out",
    "Target switches out",
    "Hits 2 times",
    "Hits 3 times",
    "Hits 10 times",
    "Hits 2 to 5 times",
    "Repeats for 2-3 turns",
    "Removes hazards",
    "Traps and damages target",
    "Can't be suppressed",
    "Can't be replaced",
    "Can't be ignored",
    "Can't be redirected",
    "Can't be reflected",
    "Always hits in Rain",
    "User can't switch out",
    "Target can't switch out",
    "One Hit KO move",
    "Modified against Bosses",
    "No effect on Bosses",
    "Lure ability",
    "Makes Contact",
    "Partially Implemented",
    "Not Implemented",
]
helpMenuText = [ # Do not translate anything that is inside <> or {}
'This is a <span style="color:rgb(140, 130, 240);">fast and powerful search</span> for PokeRogue',
'Use the <span style="color:rgb(140, 130, 240);">Search Bar</span> to add filters:',
'Combine multiple filters to get what you want',
'Click between locked filters to use the "OR" condition',
'Click the <span style="color:rgb(140, 130, 240);">Headers</span> to sort results:',
'Click the <b>${headerNames[1]}</b> column to see shiny variants',
'Click the <b>${headerNames[4]}</b> column to restrict to one slot:',
'Main Abilities', '${infoText[4]}', '${infoText[1]}',
'<b>${headerNames[5]}</b> are shown as <b>${fidToName[fidThreshold[4]]}</b> and <span style="color:rgb(240, 230, 140); font-weight: bold;">${fidToName[fidThreshold[4]+1]}</span>',
'Click the header to switch to <b>${infoText[9]}</b> instead',
'That column will also show <b>filtered ${altText[0]}/${infoText[9]}</b>',
'<b>${catToName[4]}</b> column shows rarity color of <b>${catToName[5]}</b>:',
'Click on an entry to see details for:',
'Click a <b>${headerNames[2]}</b> to see their full moveset.',
'Color of <b>${altText[5]}</b> shows <span style="color:${col.or}; font-weight: bold;">Physical</span> or <span style="color:${col.bl}; font-weight: bold;">Special</span> damage',
'Color of <b>${altText[6]}</b> shows <span style="color:${col.re}; font-weight: bold;">Multi-Target</span> moves',
'This site was created by Sandstorm, with a lot of hard work. I do not store any cookies or collect any personal data. Images and game data are from the PokeRogue GitHub. All asset rights are retained by their original creators.',
'Game Version', 'Date', 'Persistent Filters',
]