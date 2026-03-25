# ===== This script parses all the ability/move attributes from the game =====
# =====  fidToProc, typeColors, fidThreshold, upgradeCosts, gameVersion  =====
# =====            It writes all that data to filter_data.js             ===== 
# This is ONLY for numeric data; all localized text is written from updateLangs.py
# This script also composites the layers of the biome images

pathLoc = "game_files/locales/en" # File path to the official localization files
pathData = "game_files/src/data"  # File path for game data

def format_for_disp(arg): # Remove spaces, and convert _ and - to spaces, then capitalize
    return arg.replace(' ','').replace('_',' ').replace('-',' ').title()   
def format_for_attr(arg): # Remove spaces
    return arg.replace(' ','').lower() 

import re, json
from datetime import date
# Open and read the files *******************************
with open("local_files/my_json/filterToFID.json", "r") as f:
    filterToFID = json.load(f)
with open("local_files/my_json/fidThreshold.json", "r") as fp:
    fidThreshold = json.load(fp)
orderedData = [[] for _ in filterToFID][fidThreshold[0]:fidThreshold[2]]
         
print('\n=========== Reading abilities ===========\n')
with open(f'{pathData}/abilities/init-abilities.ts', "r", encoding="utf-8") as f:
    abilityData = f.read()
abilityData = re.findall(r'Ability\[\]\)\.push\(\n(.*?)  \);\n}', abilityData, re.DOTALL)[0]
abilityData = re.sub(r'\/\* Unused.*?End Unused \*\/', '', abilityData, flags=re.DOTALL)
abilityData = re.sub(r' +new ', 'new ', abilityData)
abilityData = abilityData.split('\n')
ability2D = []
for index,line in enumerate(abilityData):
    if line[:3] == 'new':
        abilityName = format_for_attr(format_for_disp(re.findall(r'AbilityId\.(.*?),', line)[0]))

        if f'ability{abilityName}' not in filterToFID:
            if abilityName != 'none':
                input(f'***** ${abilityName} does not exist')
            continue

        # print('Found ability:',abilityName)
        abilityFID = filterToFID[f'ability{abilityName}']
        procList = []
        tagList = []
        if abilityName in ['magicguard', 'comatose', 'shieldsdown', 'fullmetalbody', 'shadowshield', 'prismarmor']:
            tagList.append(50) # Abilities that "Can't be ignored"

        ability2D.append([abilityFID, abilityName, procList, tagList]) # [fid[0], name[1], procs[2], tags[3]]
        
    # All the procs and tags are shared between abilities and moves
    # Tags should be in sequential order as they will be displayed on my site
    # They are not processed in sequential order here, due to string matching
    # My internally used tags start at 200 (for contact, reflectable, etc.)
    elif f'ability{abilityName}' in filterToFID:
        if 'StatMultiplierAbAttr' in line:
            # stat = format_for_attr(re.findall(r'Stat\.(.*?),', line)[0])
            for i in range(5): # Search for a number in the next 5 lines
                if re.findall(r'Stat\.(.*?),', abilityData[index+i]):
                    stat = format_for_attr(re.findall(r'Stat\.(.*?),', abilityData[index+i])[0])
                    break # Once it finds the stat, break
            else:
                input(f'***** Could not find stat to boost for {abilityName} in {line}')
            # amount = re.findall(r'Stat\.\w\w\w\w?\w?,\s?(.*?)[,|)]', line)[0]
            for i in range(5): # Search for a number in the next 5 lines
                if '4 / 3' in abilityData[index+i]:
                    amount = 1.33
                    break
                if re.findall(r'(\d\.?\d?\d?)[,\)]', abilityData[index+i]):
                    amount = re.findall(r'(\d\.?\d?\d?)[,\)]', abilityData[index+i])[0]
                    break # Once it finds the stat, break
            else:
                input(f'***** Could not find stat multiplier for {abilityName} in {line}')
            if abilityName == 'quickfeet':
                amount = 1.5
            index = -1
            for thisStat in ['atk','def','spatk','spdef','spd','acc','eva']:
                index += 1
                if stat == thisStat:
                    entry = [-2,index,amount]
                    if abilityName in ['flowergift','victorystar']:
                        entry[1] += 7
                    if entry not in procList:
                        procList.append(entry)
                    # print('Found ability stat boost:',abilityName,stat,amount)
        elif 'playerFaints' in line:
            procList.append([-3,26,10]) # supremeoverlord
        elif 'MovePowerBoostAbAttr' in line:
            for i in range(10): # Search for a number in the next 5 lines
                if re.findall(r'(\d\.?\d?\d?)', abilityData[index+i]):
                    amount = re.findall(r'(\d\.?\d?\d?)', abilityData[index+i])[-1] # Use the last value on that line
                    if float(amount) < 60:
                        break # Once it finds the multiplier value, break
            else:
                input(f'***** Could not find power multiplier of {abilityName} in {line}')
            procList.append([-2,26,amount])
            # print('Found ability power boost:',abilityName,amount)
        elif 'LowHpMoveTypePowerBoostAbAttr' in line:
            procList.append([-2,26,1.5])
            # print('Found low hp type boost:',abilityName,1.5)
        elif 'UserFieldMoveTypePowerBoostAbAttr' in line: # Steely Spirit
            procList.append([-2,26,1.5])
        elif 'FieldMoveTypePowerBoostAbAttr' in line: # Aura Break, Fairy/Dark Aura
            if abilityName == 'aurabreak':
                amount = '0.75'
            else:
                amount = '1.33'
            if [-2,26,amount] not in procList:
                procList.append([-2,26,amount])
            # print('Found field type boost:',abilityName,amount)
        elif 'MoveTypePowerBoostAbAttr' in line: # Transistor, Rocky Payload, etc.
            if re.findall(r'(\d\.?\d?\d?)', line):
                amount = re.findall(r'(\d\.?\d?\d?)', line)[-1]
            else:
                amount = '1.5'
            if [-2,26,amount] not in procList:
                procList.append([-2,26,amount])
                # print('Found ability type power boost:',abilityName,amount)
        elif 'AllyMoveCategoryPowerBoostAbAttr' in line:
            amount = re.findall(r'(\d\.?\d?\d?)', line)[-1]
            if [-2,26,amount] not in procList:
                procList.append([-2,26,amount])
                # print('Found ally power boost:',abilityName,amount)
        elif 'ReceivedMoveDamageMultiplierAbAttr' in line or 'ReceivedTypeDamageMultiplierAbAttr' in line:
            for i in range(5): # Search for a number in the next 5 lines
                if re.findall(r'  (\d\.?\d?\d?),', abilityData[index+i]):
                    amount = re.findall(r'  (\d\.?\d?\d?),', abilityData[index+i])[-1]
                    break # Once it finds the stat, break
                if re.findall(r', (\d\.?\d?\d?)\)', abilityData[index+i]):
                    amount = re.findall(r', (\d\.?\d?\d?)\)', abilityData[index+i])[-1]
                    break # Once it finds the stat, break
            else:
                input(f'***** Could not damage multiplier for {abilityName} in {line}')
            # if re.findall(r'(\d\.?\d?\d?)', line):
            #     amount = re.findall(r'(\d\.?\d?\d?)', line)[-1]
            if [-2,26,amount] not in procList and abilityName != 'punkrock':
                procList.append([-2,26,amount])
                # print('Found damage taken mod:',abilityName,amount)
        elif 'FieldMultiplyStatAbAttr' in line:
            stat = format_for_attr(re.findall(r'Stat\.(.*?),', line)[0])
            amount = re.findall(r'Stat\.\w\w\w\w?\w?,\s?(.*?)[,|)]', line)[0]
            index = -1
            for thisStat in ['atk','def','spatk','spdef','spd','acc','eva']:
                index += 1
                if stat == thisStat:
                    procList.append([-2,index+7,amount])
                    # print('Found field stat boost:',abilityName,stat,amount)
        elif 'PostSummonStatStageChangeAbAttr' in line:
            stat = format_for_attr(re.findall(r'\[Stat\.(.*?)\]', line)[0])
            amount = re.findall(r'\],\s?(.*?)[,|)]', line)[0]
            self = (re.findall(r'\d, true', line))
            index = -1
            for thisStat in ['atk','def','spatk','spdef','spd','acc','eva']:
                index += 1
                if stat == thisStat:
                    procList.append([-1,index+(not self)*7,amount])
                    # print('Found summon stat boost:',abilityName,stat,amount)
        elif 'PostStatStageChangeStatStageChangeAbAttr' in line:
            stat = format_for_attr(re.findall(r'\[Stat\.(.*?)\]', line)[0])
            amount = re.findall(r'\],\s?(.*?)[,|)]', line)[0]
            self = (re.findall(r'\d, true', line))
            index = -1
            for thisStat in ['atk','def','spatk','spdef','spd','acc','eva']:
                index += 1
                if stat == thisStat:
                    procList.append([-1,index+(not self)*7,amount])
                    # print('Found defiant-like:',abilityName,stat,amount)
        elif 'ApplyStatusEffectAbAttr' in line:
            if 'StatusEffect.POISON' in line:
                procList.append([30,14,0])
            elif 'StatusEffect.TOXIC' in line:
                procList.append([30,15,0])
            elif 'StatusEffect.SLEEP' in line:
                procList.append([30,16,0])
            elif 'StatusEffect.FREEZE' in line:
                procList.append([30,17,0])
            elif 'StatusEffect.PARALYSIS' in line:
                procList.append([30,18,0])
            elif 'StatusEffect.BURN' in line:
                procList.append([30,19,0])
            else:
                print('No status found',line)
            # print('Found status proc ability:',abilityName)
        # elif 'MoveTypeChangeAbAttr' in line and abilityName != 'liquidvoice':
        #     procList.append([-2,26,1.2])
            # print('Found aerilate-like:',abilityName,1.2)
        elif 'StabBoostAbAttr' in line:
            procList.append([-2,26,1.33])
            # print('Found stab boost:',abilityName,1.33)
        elif 'PostAttackApplyBattlerTagAbAttr' in line:
            procList.append([10,21,0])
            # print('Found stench:',abilityName)
        elif 'SpeedBoostAbAttr' in line:
            procList.append([-1,4,1])
            # print('Found speed boost:',abilityName,1)
        elif 'EffectSporeAbAttr' in line:
            procList.append([30,23,0])
        elif 'MultCritAbAttr' in line: # Sniper
            procList.append([-2,26,1.5])
        elif '.unimplemented()' in line:
            tagList.append(62)
            # print('Found unimplemented ability',abilityName)
        elif '.partial()' in line:
            tagList.append(61)
            # print('Found partial ability',abilityName)
        elif '.unsuppressable()' in line:
            tagList.append(48)
        elif '.unreplaceable()' in line:
            tagList.append(49)
        elif '.ignorable()' in line and 50 in tagList:
            input(f'Mismatch for ignorability in {abilityName}')
        elif 'MoveAbilityBypassAbAttr' in line: # Ignores abilities (Mold Breaker, etc.)
            tagList.append(37)         # "Can't be ignored" is 50, done in the previous section
        elif 'DoubleBattleChanceAbAttr' in line: # Lure abilities
            tagList.append(59)
        elif 'sheerForceHitDisableAbCondition' in line: # Abilities prevented by sheer force
            tagList.append(3)
        # elif 'ultipl' in line or 'oost' in line or 'pow' in line:
        #     # Check for keywords in the ability line like 'Multiply', 'Boost', or 'Power'
        #     # Print those lines to make sure I'm not missing anything important
        #     print(abilityName, line)

# Read all the move attributes from the game data
print('\n=========== Reading moves ===========\n')
with open(f'{pathData}/moves/move.ts', "r", encoding="utf-8", errors="replace") as f:
    moveData = f.read()
moveData = re.findall(r'Move\[\]\)\.push\(\n(.*?)  \);\n\}\n', moveData, re.DOTALL)[0]
moveData = re.sub(r'\/\* Unused.*?End Unused \*\/', '', moveData, flags=re.DOTALL)
moveData = re.sub(r'LapseBattlerTagAttr,.*?true\)', '', moveData, flags=re.DOTALL)
moveData = re.sub(r' +new ', 'new ', moveData) # Remove leading spaces
moveData = moveData.split('\n')
move2D = []
for line in moveData:
    if line[:3] == 'new':
        moveName = format_for_attr(format_for_disp(re.findall(r'MoveId\.(.*?),', line)[0]))

        # There are moves that exist in the game code but are not obtainable by any pokemon
        if f'move{moveName}' not in filterToFID:
            print(moveName, 'does not exist')
            continue

        # Parse the attributes from move.ts
        attrRaw = re.findall(r'Type\.(.*?)\)',line)[0].split(',')
        attrRaw = [ format_for_attr(arg) for arg in attrRaw ]
        if re.findall(r'StatusMove\(Move', line) != []:
            # Status moves in move.ts: [type, accuracy, pp, chance, priority, gen]
            [type, accuracy, pp, chance, priority, gen] = attrRaw
            category = 2 # Status moves are category 2
            power = -1
        else:
            # Attacking moves in move.ts: [type, category, power, accuracy, pp, chance, priority, gen]
            [type, category, power, accuracy, pp, chance, priority, gen] = attrRaw
            category = category.split('movecategory.')[1]
            if category == 'physical':  category = 0
            elif category == 'special': category = 1
            elif category not in [0,1]: input(f'Move category parsing error: {line}')

        moveFID = filterToFID[f'move{moveName}']
        type = filterToFID[f'type{format_for_attr(type)}']
        procList = [] # Procs and tags are mostly assembled in the next section
        tagList = []
        # "chance" is written to the procList after parsing the move data
        chance = int(format_for_attr(chance))  
        # -1 is for detrimental guaranteed effects, while 100 is for beneficial guaranteed effects
        if chance > 0: # Sheer Force needs a "chance" >= 1 (only beneficial moves, and some abilities)
            tagList.append(3)
        if 'SelfStatusMove' in line: # Status moves that target self
            tagList.append(202) # These will not be considered reflectable moves

        # fid[0], name[1], procs[2], tags[3], type[4], cat[5], pow[6], acc[7], pp[8], prio[9]
        move2D.append([moveFID, moveName, procList, tagList, type, category, power, accuracy, pp, priority])

    # General order of move descriptors: priority, targets, procs, all other tags
    # All the procs and tags are shared between abilities and moves
    # Tags should be in sequential order as they will be displayed on the searchdex
    # They are not processed in sequential order here, due to string matching
    # My internally used tags start at 200 (for contact, reflectable, etc.)
    elif f'move{moveName}' in filterToFID:
        if '.attr(HighCritAttr)' in line:
            tagList.append(4)
        elif 'CritOnlyAttr' in line: # auto crit
            tagList.append(5)
        elif 'CRIT_BOOST' in line and 'target' not in line: # focus energy, not dragon cheer
            tagList.append(6)
        elif '.makesContact(false)' in line: # those contact values are overrides
            tagList.append(200)              # if it doesn't exist, look at move category
        elif '.makesContact(true)' in line:
            tagList.append(201)
        elif '.makesContact()' in line:
            tagList.append(201)
        elif '.powderMove()' in line: # Move archetypes for synergies/immunities
            tagList.append(23)
        elif '.reflectable()' in line:
            tagList.append(203)
        elif '.slicingMove()' in line:
            tagList.append(28)
        elif '.punchingMove()' in line:
            tagList.append(29)
        elif '.danceMove()' in line:
            tagList.append(26)
        elif '.ballBombMove()' in line:
            tagList.append(33)
        elif '.pulseMove()' in line:
            tagList.append(30)
        elif '.bitingMove()' in line:
            tagList.append(31)
        elif '.triageMove()' in line:
            tagList.append(25)
        elif '.soundBased()' in line:
            tagList.append(35)
            tagList.append(36)
        elif '.windMove()' in line:
            tagList.append(27)
        elif 'failIfDampCondition' in line:
            tagList.append(34)
        elif '.ignoresProtect()' in line:
            tagList.append(38)
        elif '.ignoresSubstitute()' in line:
            tagList.append(36)
        elif 'hidesTarget()' in line: # roar
            tagList.append(40)
        elif 'MoveTarget.RANDOM_NEAR_ENEMY' in line: # outrage
            tagList.append(0)
        elif 'MoveTarget.ALL_NEAR_ENEMIES' in line: # eruption
            tagList.append(1)
        elif 'MoveTarget.ALL_NEAR_OTHERS' in line: # earthquake
            tagList.append(2)
        elif 'MoveTarget.USER_SIDE' in line or 'MoveTarget.USER_AND_ALLIES' in line:
            tagList.append(202) # Internal tag to ignore these for reflectable
        elif 'ProtectAttr' in line or 'MoveTarget.BOTH_SIDES' in line or 'MoveTarget.NEAR_ALLY' in line:
            tagList.append(202) # Internal tag to ignore these for reflectable
        elif 'MultiHitAttr' in line:
            if 'MultiHitType.TWO' in line:
                tagList.append(41)
            elif 'MultiHitType.THREE' in line:
                tagList.append(42)
            elif 'MultiHitType.TEN' in line:
                tagList.append(43)
            else:
                tagList.append(44) # Standard two to five multihit
        elif '.attr(FlinchAttr)' in line:
            procList.append([chance,21,0])
        elif 'ConfuseAttr' in line:
            procList.append([chance,20,0])
        elif 'GrowthStatStageChangeAttr' in line: # Growth
            procList.append([-1,0,1])
            procList.append([-1,2,1])
        elif '(HealStatusEffectAttr,' in line: # cleansing status effects
            if 'HealStatusEffectAttr, true, [' in line:
                tagList.append(19)
            elif 'getNonVolatile' in line:
                tagList.append(19)
            elif 'StatusEffect.SLEEP' in line:
                tagList.append(20)
            elif 'StatusEffect.FREEZE' in line:
                tagList.append(21)
            elif 'StatusEffect.PARALYSIS' in line:
                input('Unknown tag found: Para Heal')
            elif 'StatusEffect.BURN' in line:
                tagList.append(22)
        elif 'MultiStatusEffectAttr' in line: # dire claw and tri attack
            if 'SLEEP' in line:
                procList.append([chance,23,0]) # dire claw
            else:
                procList.append([chance,24,0]) # tri attack
        elif '(StatusEffectAttr,' in line: # applying status effects
            if 'StatusEffect.POISON' in line:
                procList.append([chance,14,0])
            if 'StatusEffect.TOXIC' in line:
                procList.append([chance,15,0])
            if 'StatusEffect.SLEEP' in line:
                procList.append([chance,16,0])
            if 'StatusEffect.FREEZE' in line:
                procList.append([chance,17,0])
            if 'StatusEffect.PARALYSIS' in line:
                procList.append([chance,18,0])
            if 'StatusEffect.BURN' in line:
                procList.append([chance,19,0])
        elif '(StatStageChangeAttr,' in line:
            stats = re.findall(r'\[(.*?)\]', line)[0].split(',')
            stats = [re.sub('stat.','',format_for_attr(stat)) for stat in stats]
            amount = re.findall(r'\], (.*?)[,|)]', line)[0]
            isSelf = (', true' in line)
            index = -1
            if len(stats) == 5:
                procList.append([chance,22,1]) # ancient power, silver wind, ominous wind, no retreat
            elif moveName == 'terablast':
                procList.append([chance,25,-1]) # tera blast
            else:
                if 'effectChanceOverride' in line:
                    effChance = 50
                else:
                    effChance = chance
                for stat in ['atk','def','spatk','spdef','spd','acc','eva']:
                    index += 1
                    if stat in stats:
                        procList.append([effChance,index+(not isSelf)*7,amount])
        elif 'recklessMove' in line: # reckless and recoil moves
            tagList.append(32)
        elif 'RecoilAttr, true, 0.5' in line or 'HalfSacrificialAttr' in line:
            tagList.append(10)
        elif 'CurseAttr' in line:
            tagList.append(9)
        # elif 'RecoilAttr, true, 0.25' in line: # struggle
        #     tagList.append()
        elif 'RecoilAttr, false, 0.33' in line:
            tagList.append(12)
        elif 'RecoilAttr, false, 0.5' in line:
            tagList.append(11)
        elif 'RecoilAttr' in line:
            tagList.append(13)
        elif 'FrenzyAttr' in line: # outrage
            tagList.append(45)
        elif 'HitHealAttr, 1' in line:
            tagList.append(15)
        elif 'HitHealAttr, 0.75' in line:
            tagList.append(16)
        elif 'HitHealAttr, null, Stat.ATK' in line:
            tagList.append(18)
        elif 'HitHealAttr' in line:
            tagList.append(17)
        elif 'OneHitKOAttr' in line:
            tagList.append(56)
            tagList.append(57)
        elif 'TrapAttr' in line:
            if 'RemoveArenaTrapAttr' in line:
                tagList.append(46) # rapid spin
            else:
                tagList.append(47) # binding moves
        elif 'DoublePowerChanceAttr' in line: # fickle beam
            tagList.append(14)
        elif 'BypassRedirectAttr' in line:
            tagList.append(51)
        elif 'ThunderAccuracyAttr' in line:
            tagList.append(53)
        elif 'StormAccuracyAttr' in line:
            tagList.append(53)
        elif '(failOnBossCondition)' in line:
            tagList.append(58)
        elif '.unimplemented()' in line:
            tagList.append(62)
        elif '.partial()' in line:
            tagList.append(61)
        elif 'ForceSwitchOutAttr, true' in line or 'ChillyReceptionAttr' in line: # u turn
            tagList.append(39)
        elif '.ignoresAbilities()' in line: # moongeist beam
            tagList.append(37)
        elif 'LeechSeedAttr' in line: # leech seed
            tagList.append(24)
        elif 'TrappedTag' in line: # no retreat
            tagList.append(54)
        elif 'TRAPPED' in line: # mean look
            tagList.append(55)
        elif 'JawLockAttr' in line: # jaw lock
            tagList.append(54)
            tagList.append(55)
        elif 'OCTOLOCK' in line: # octolock
            tagList.append(55)
            procList.append([chance,8,-1])
            procList.append([chance,10,-1])
        elif 'CutHpStatStageBoostAttr' in line: # belly / clang / fillet
            stats = re.findall(r'\[(.*?)\]', line)[0].split(',')
            stats = [re.sub('stat.','',format_for_attr(stat)) for stat in stats]
            amount = re.findall(r'\], (.*?),', line)[0]
            index = -1
            if len(stats) == 5:
                procList.append([chance,22,1]) # ancient power, silver/ominous, no retreat, clang
            elif amount != '12':
                for stat in ['atk','def','spatk','spdef','spd','acc','eva']:
                    index += 1
                    if stat in stats:
                        procList.append([-1,index,amount])
            if len(stats) == 1: # belly
                tagList.append(7)
                tagList.append(9)
            elif len(stats) == 3: # fillet
                tagList.append(9)
            elif len(stats) == 5: # clang
                tagList.append(8)
            else:
                input('Unknown boosting move',line)
        # Unused tags below this line ================================
        # else: # If nothing has been detected yet, show the game code
        #     for phrase in ['ProtectAttr','failIfLastCondition','crashDamageFunc','HealAttr','UpperHandCondition','Pledge','doublePowerChanceMessageFunc','TeraStarstormTypeAttr','TeraMoveCategoryAttr']:
        #         if phrase in line:
        #             continue
        #     if format_for_attr(line)[:2] == '//' or format_for_attr(line) in ['',');','})','}),','}','}else{','return1;','.attr(','return(',')?2:1','//todo']:
        #         continue
        #     else:
        #         print('\n',moveName,'\n',line)

# The data in ability2D/move2D is just ordered how the moves/abilities appear in the game code
# This next step reorders them according to the fid list (which is alphabetical in english)
# orderedData does not includes types => it starts at fidThreshold[0]
for line in ability2D:
    if f'ability{line[1]}' in filterToFID:
        orderedData[line[0]-fidThreshold[0]] = line # Replace ability rows with assembled ability row
for line in move2D:
    if f'move{line[1]}' in filterToFID:
        orderedData[line[0]-fidThreshold[0]] = line # Replace move rows with assembled move row

print('\n==============================\n')
print('Checking for errors...\n')
multiProcs = []
for fidLine in orderedData:
    if len(fidLine) > 4: # For moves
        # The game tracks which moves are reflectable, but almost every offensive status is reflectable
        # However, i think it's ugly to show something that obvious
        # I'd rather show CAN'T be reflected, to be in line with other tag wording
        if 203 in fidLine[3] and fidLine[5] != 2:
            input(f'***** Reflectable attack: fidLine[1]')
        if 203 not in fidLine[3] and fidLine[5] == 2 and 202 not in fidLine[3]:
            # If it is a status move, not marked as reflectable, and not targeting self
            if 25 not in fidLine[3] and 6 not in fidLine[3]: # If not a healing move, and not belly drum
                isBoosting = 0
                for procLine in fidLine[2]:
                    if procLine[1] < 7 or procLine[1] == 22:
                        isBoosting = 1 # Move is a self stat boost (or omni boost)
                if not isBoosting:
                    # print('Non-reflectable status',fidLine)
                    fidLine[3].append(52) # I only show this for offensive status moves
    for procLine in fidLine[2]: # Check for improper procs
        if procLine[0] == 0 or ( procLine[1] < 14 and procLine[2] == 0 ):
            print('***** Empty proc found:',fidLine[1],procLine)
    if sum([1 for line in fidLine[2] if line[0] > 1]) > 1: # Check for moves with multiple procs (e.g. Fire Fang)
        multiProcs.append(fidLine)
if len(multiProcs) != 4:
    print('There should be 4 attacks with multiple procs')
    for line in multiProcs:
        print('Multiple procs found in',line[1])

# Read the upgrade cost data
with open(f'{pathData}/balance/starters.ts', "r", encoding="utf-8", errors="replace") as f:
    costDataRaw = f.read()
costData = re.findall(r'StarterCandyCosts\[\] = \[\n(.*?)\];\n', costDataRaw, re.DOTALL)[0]
costData = costData.split('\n')[:-1]
passiveData = [re.findall(r'passive: (.*?),', line)[0] for line in costData]
costParsed = [[
    re.findall(r'\[(.*?)\]', line)[0].split(', '), # costReduction
    re.findall(r'\[(.*?)\]', line)[1].split(', '), # eggCosts
    re.findall(r'\[(.*?)\]', line)[2].split(', '), # eggCostReductionThresholds
] for line in costData]
costParsed = [[[int(arg) for arg in line] for line in cost] for cost in costParsed]
friendData = re.findall(r'getStarterValueFriendshipCap(.*?)}\n}', costDataRaw, re.DOTALL)[0]
friendData = re.findall(r'return (.*?);', friendData, re.DOTALL)
friendData.append(friendData[-1])
friendData[-2] = friendData[-3]

# Patch note creating **********************************************************************************
print('\n==============================\n')
input('Review patch changes?')
print("Reviewing patch changes...")
attNames = ['fid','name','procs list','tags list','type','category','power','accuracy','pp','priority']
# Write all the trimmed data to a json file
with open("local_files/proc_data.json", "w") as f:
    json.dump(orderedData, f, indent=4)
# Load the previous trimmed data > You need to manually rename the old one to _prev
with open("local_files/proc_data_prev.json", "r") as fp:
    orderedDataPrev = json.load(fp)
for line in orderedData:
    if line: # Only consider ability/move
        for oldLine in orderedDataPrev: # Need to search for name, as FID may be shuffled
            if oldLine and oldLine[1] == line[1]: # Match the ability/move name
                for i in range(2,len(line)):
                    if line[i] != oldLine[i]:
                        print('Changes in',attNames[i],'for',line[1])
                        print('    from',oldLine[i],'to',line[i])
                break
        else:
            print('Could not find old entry for',line[1])
print('\n==============================\n')
input('Continue to writing website database?')
print('Writing...')

# Load the numeric data from the main script
lines = []
with open("game_files/package.json", "r") as fp:
    packageInfo = json.load(fp)
    lines.append(f'const gameVersion = "{packageInfo["version"]}";') # Game version
todayDate = date.today().strftime("%Y-%m-%d")
lines.append(f'const latestDate = "{todayDate}";')
lines.append('const typeColors = [') # Type colors
typeColors = ["#ADBD21","#735A4A","#7B63E7","#FFC631","#EF70EF","#A55239","#F75231","#9CADF7","#6363B5","#7BCE52","#AE7A3B","#5ACEE7","#ADA594","#9141CB","#EF4179","#BDA55A","#81A6BE","#399CFF"]
for color in typeColors:
    lines.append(f"'{color}',")
lines.append('];\nconst fidThreshold = [') # fid category thresholds
for threshold in fidThreshold:
    lines.append(f"{threshold},")
lines.append('];\nconst upgradeCosts = [') # upgrade costs
for index,costLine in enumerate(costParsed):
    lines.append(f"[{passiveData[index]},{costLine[0]},{costLine[1]},{costLine[2]},{friendData[index]}],".replace(', ',','))

tagToFID = [ # List of ability/move FIDs that match specific tag filters
    [ str(line[0]) for line in orderedData if 59 in line[3] ], # Lure ability
    [ str(line[0]) for line in orderedData if 37 in line[3] and line[0] < fidThreshold[1]], # Ignores abilities
    [ str(line[0]) for line in orderedData if 48 in line[3] ], # Can't be suppressed
    [ str(line[0]) for line in orderedData if 49 in line[3] ], # Can't be replaced
    [ str(line[0]) for line in orderedData if 50 in line[3] ], # Can't be ignored
    # Possibly add move tags later: Switches out target, Spread moves, Healing, Setup, Priority
]
tagToAbility = {
    'electric':['lightningrod','motordrive','voltabsorb'],
    'fire':['flashfire','wellbakedbody'],
    'ground':['levitate','eartheater'],
    'water':['dryskin','stormdrain','waterabsorb'],
    'rain':['drizzle','primordialsea','dryskin','hydration','raindish','swiftswim'],
    'rainCreate':['drizzle','primordialsea'],
    'sand':['sandstream','sandforce','sandrush','sandveil'],
    'sandCreate':['sandstream','sandspit'],
    'snow':['snowwarning','icebody','iceface','slushrush','snowcloak'],
    'sun':['drought','desolateland','orichalcumpulse','chlorophyll','flowergift','harvest','leafguard','protosynthesis','solarpower'],
    'sunCreate':['drought','desolateland','orichalcumpulse'],
}
for synLine in tagToAbility.values():
    tagToFID.append([str(filterToFID[f'ability{abName}']) for abName in synLine])
# Write fid associated with each tag to filter_data.js
lines.append('];\nconst tagToFID = {')
for index, relatedFID in enumerate(tagToFID):
    lines.append(f'{fidThreshold[11]+index}: [{",".join(relatedFID)}],')

# Format of orderedData: 
#   Abilities: [fid[0], name[1], procs[2], tags[3]]
#   Moves: [fid, name, [procs[chance,stat,mag]], [tags], type, cat, pow, acc, pp, prio]
#            0     1      2                        3      4    5    6    7    8    9

# Final structure of fidToProc[fid]:
# ==================================
# Abilities: [ [procs], [tags] ]
#   procs = [[chance,stat,magnitude], [...]]
#       chance is the chance of effect activating (flame body, etc.)
#           > 0  : displays as value%
#           = -1 : does not display chance indicator
#           = -2 : changes magnitude display to ×magnitude (e.g. swift swim is [-2,4,2])
#           = -3 : changes magnitude display to +magnitude% (e.g. supreme overlord is [-3,26,10])
#       stat is which stat, status, etc.
#           0  to  6 : atk/def/spa/spd/spe/acc/eva (for self)
#           7  to 13 : atk/def/spa/spd/spe/acc/eva (for enemy)
#           14 to 20 : pois/tox/sleep/freeze/para/burn/confuse
#           21 to 26 : flinch/omni/direclaw/triattack/terablast/damage
#       magnitude is how much the stat is altered by
#           > 0 : displays as +value
#           < 0 : displays as -value
#           = 0 : does not display magnitude (used for status conditions, etc.)
# Moves: [ [procs[chance,stat,mag]], [tags], type, cat(phys/spec/stat), pow, acc, pp, prio]
#             0                        1       2    3                    4    5    6    7

# ======================= Write numeric filter data to filter_data.js =======================
# This is just numbers. Localized strings are written from updateLangs.py
lines.append('};\nconst fidToProc = [') # Ability/move descriptions
for fidLine in orderedData:

    text = "["

    # Write procs =======
    text = f'{text}['
    for procLine in fidLine[2]:
        text = f'{text}[{procLine[0]},{procLine[1]},{procLine[2]}],'
    text = f'{text}],'

    # Write tags =======
    text = f'{text}['
    if len(fidLine) > 4: # For moves
        # Contact move tag is written to my data is true
        # In the game data, it is only described for special contact moves, or physical moves that aren't contact
        if 201 in fidLine[3] or (fidLine[5] == 0 and (200 not in fidLine[3])):
            text = f'{text}60,'
    for tag in fidLine[3]: # All other tags, for moves and abilities
        if tag < 200: # Don't add internal tags (contact, etc.)
            text = f'{text}{tag},'
    text = f'{text}],'

    # Write properties =======
    if len(fidLine) > 4: # For moves
        for i in range(4,10):
            text = f'{text}{fidLine[i]},'

    text = f'{text}],'
    text = re.sub(',]',']',text) # Remove unnecessary commas
    lines.append(text)

lines.append('];')

with open("website/filter_data.js", "w") as file:
    file.writelines(f"{line}\n" for line in lines)

print("Done writing numeric filter data")

# ======================= Composite all the biome images =======================
print('\n==============================\n')
print('Creating biome images...')

biome_src = "game_files/assets/images/arenas"
biome_dest = "website/ui/biomes"
with open("local_files/my_json/allFilters.json", "r") as file:
    allFilters = json.load(file)
biomeNames = [filter[1].lower().replace(' ','_') for filter in allFilters if filter[0] == 'Biome']
thisFID = fidThreshold[8]-1

import os
from PIL import Image
# Delete previous biome images
for filename in os.listdir(biome_dest):
    file_path = os.path.join(biome_dest, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)

for thisBiome in biomeNames:

    background_filename = f"{thisBiome}_bg.png"
    thisFID += 1
    output_filename = f"{thisFID}.png"

    bg_path = os.path.join(biome_src, background_filename) # Load background image
    background = Image.open(bg_path).convert("RGBA")
    overlay_filenames = [ # Get overlay image paths
        f for f in os.listdir(biome_src) if f.startswith(f"{thisBiome}_b") and f.endswith(".png") and f != background_filename
    ]
    overlay_filenames.sort() # Sort for consistent layering

    # Paste each overlay image on top of the background
    for filename in overlay_filenames:
        # Open the image
        overlay_path = os.path.join(biome_src, filename)
        overlay = Image.open(overlay_path).convert("RGBA")
        bg_pos = [0, 0] # Where to paste the overlay image on the background

        # If json data exists, crop the image
        if os.path.isfile(f'{biome_src}/{filename[:-4]}.json'):
            with open(f'{biome_src}/{filename[:-4]}.json', "r") as f:
                json_data = json.load(f)
            frame_data = json_data['textures'][0]['frames'][0]
            bg_pos = [frame_data["spriteSourceSize"]["x"], frame_data["spriteSourceSize"]["y"]]
            crop_box = [val for val in frame_data["frame"].values()] # Get x, y, w, h
            crop_box[2] += crop_box[0] # Add w to x
            crop_box[3] += crop_box[1] # Add h to y
            overlay = overlay.crop(crop_box)

        # Overlay the image on the bg
        background.paste(overlay, bg_pos, overlay)

    background = background.crop((150, 20, 282, 110)) # Crop to a nice size for the SearchDex
    background.save(os.path.join(biome_dest, output_filename))
    print(f"Composite biome image saved as: {output_filename}")
print('Done processing all biome images')

print('\n=========== ALL DONE ===========\n')