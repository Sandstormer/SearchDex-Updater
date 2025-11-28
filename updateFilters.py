# ===== This script parses all the ability/move attributes from the game =====
# =====      It writes that data to filters_global.js as fidToProc       ===== 
# =====      It also writes typeColors, fidThreshold, upgradeCosts       =====
# This is ONLY for numeric data; all localized text is written from updateLangs.py

pathLoc = './game_files/locales/en'   # File path to the official localization files
pathData = "game_files/src/data" # File path for game data

def format_for_disp(arg): # Remove spaces, and convert _ and - to spaces, then capitalize
    return arg.replace(' ','').replace('_',' ').replace('-',' ').title()   
def format_for_attr(arg): # Remove spaces
    return arg.replace(' ','').lower() 

import re, json
from datetime import date
# Open and read the files *******************************
with open("local_files/my_json/filterToFID.json", "r") as f:
    filterToFID = json.load(f)
with open("local_files/my_json/fidThresholds.json", "r") as fp:
    fidThresholds = json.load(fp)
orderedData = [[] for _ in filterToFID][fidThresholds[0]:fidThresholds[2]]
         
print('\n=========== Reading abilities ===========\n')
with open(f'{pathData}/abilities/ability.ts', "r", encoding="utf-8") as f:
    abilityData = f.read()
abilityData = re.findall(r'Ability\[\]\)\.push\(\n(.*?)  \);\n', abilityData, re.DOTALL)[0]
abilityData = re.sub(r'\/\* Unused.*?End Unused \*\/', '', abilityData, flags=re.DOTALL)
abilityData = re.sub(r' +new ', 'new ', abilityData)
abilityData = abilityData.split('\n')
ability2D = []
for index,line in enumerate(abilityData):
    if line[:3] == 'new':
        abilityName = format_for_attr(format_for_disp(re.findall(r'AbilityId\.(.*?),', line)[0]))
        if f'ability{abilityName}' not in filterToFID:
            if abilityName != 'none':
                input('*****', abilityName, 'does not exist')
            ability2D.append(['xxxxx',abilityName])
        else:
            # print('Found ability:',abilityName)
            abilityFID = filterToFID[f'ability{abilityName}']
            ability2D.append([abilityFID, abilityName, [], []]) # [fid[0], name[1], procs[2], tags[3]]
        if abilityName in ['magicguard', 'comatose', 'shieldsdown', 'fullmetalbody', 'shadowshield', 'prismarmor']:
            ability2D[-1][3].append(50) 
    elif len(ability2D[-1]):
        # All the procs and tags are shared between abilities and moves
        # Tags should be in sequential order as they will be displayed on my site
        # They are not processed in sequential order here, due to string matching
        # My internally used tags start at 200 (for contact, reflectable, etc.)
        if 'StatMultiplierAbAttr' in line:
            stat = format_for_attr(re.findall(r'Stat\.(.*?),', line)[0])
            amount = re.findall(r'Stat\.\w\w\w\w?\w?,\s?(.*?)[,|)]', line)[0]
            if amount == '4 / 3':
                amount = 1.33
            if abilityName == 'quickfeet':
                amount = 1.5
            index = -1
            for thisStat in ['atk','def','spatk','spdef','spd','acc','eva']:
                index += 1
                if stat == thisStat:
                    entry = [-2,index,amount]
                    if abilityName in ['flowergift','victorystar']:
                        entry[1] += 7
                    if entry not in ability2D[-1][2]:
                        ability2D[-1][2].append(entry)
                    # print('Found ability stat boost:',abilityName,stat,amount)
        elif 'playerFaints' in line:
            amount = 10
            ability2D[-1][2].append([-3,26,amount]) # supremeoverlord
        elif 'MovePowerBoostAbAttr' in line:
            for i in range(5): # Search for a number in the next 5 lines
                if re.findall(r'(\d\.?\d?\d?)', abilityData[index+i]):
                    amount = re.findall(r'(\d\.?\d?\d?)', abilityData[index+i])[-1] # Use the last value on that line
                    if float(amount) < 60:
                        break # Once it finds the multiplier value, break
            else:
                print(abilityName,line)
            ability2D[-1][2].append([-2,26,amount])
            # print('Found ability power boost:',abilityName,amount)
        elif 'LowHpMoveTypePowerBoostAbAttr' in line:
            ability2D[-1][2].append([-2,26,1.5])
            # print('Found low hp type boost:',abilityName,1.5)
        elif 'FieldMoveTypePowerBoostAbAttr' in line:
            if abilityName == 'aurabreak':
                amount = '0.75'
            else:
                amount = '1.33'
            if [-2,26,amount] not in ability2D[-1][2]:
                ability2D[-1][2].append([-2,26,amount])
            # print('Found field type boost:',abilityName,amount)
        elif 'MoveTypePowerBoostAbAttr' in line:
            if re.findall(r'(\d\.?\d?\d?)', line):
                amount = re.findall(r'(\d\.?\d?\d?)', line)[-1]
            else:
                amount = '1.5'
            if [-2,26,amount] not in ability2D[-1][2]:
                ability2D[-1][2].append([-2,26,amount])
                # print('Found ability type power boost:',abilityName,amount)
        elif 'AllyMoveCategoryPowerBoostAbAttr' in line:
            amount = re.findall(r'(\d\.?\d?\d?)', line)[-1]
            if [-2,26,amount] not in ability2D[-1][2]:
                ability2D[-1][2].append([-2,26,amount])
                # print('Found ally power boost:',abilityName,amount)
        elif 'ReceivedMoveDamageMultiplierAbAttr' in line or 'ReceivedTypeDamageMultiplierAbAttr' in line:
            if re.findall(r'(\d\.?\d?\d?)', line):
                amount = re.findall(r'(\d\.?\d?\d?)', line)[-1]
            if [-2,26,amount] not in ability2D[-1][2] and abilityName != 'punkrock':
                ability2D[-1][2].append([-2,26,amount])
                # print('Found damage taken mod:',abilityName,amount)
        elif 'FieldMultiplyStatAbAttr' in line:
            stat = format_for_attr(re.findall(r'Stat\.(.*?),', line)[0])
            amount = re.findall(r'Stat\.\w\w\w\w?\w?,\s?(.*?)[,|)]', line)[0]
            index = -1
            for thisStat in ['atk','def','spatk','spdef','spd','acc','eva']:
                index += 1
                if stat == thisStat:
                    ability2D[-1][2].append([-2,index+7,amount])
                    # print('Found field stat boost:',abilityName,stat,amount)
        elif 'PostSummonStatStageChangeAbAttr' in line:
            stat = format_for_attr(re.findall(r'Stat\.(.*?)\s', line)[0])
            amount = re.findall(r'\],\s?(.*?)[,|)]', line)[0]
            self = (re.findall(r'\d, true', line))
            index = -1
            for thisStat in ['atk','def','spatk','spdef','spd','acc','eva']:
                index += 1
                if stat == thisStat:
                    ability2D[-1][2].append([-1,index+(not self)*7,amount])
                    # print('Found summon stat boost:',abilityName,stat,amount)
        elif 'PostStatStageChangeStatStageChangeAbAttr' in line:
            stat = format_for_attr(re.findall(r'Stat\.(.*?)\s', line)[0])
            amount = re.findall(r'\],\s?(.*?)[,|)]', line)[0]
            self = (re.findall(r'\d, true', line))
            index = -1
            for thisStat in ['atk','def','spatk','spdef','spd','acc','eva']:
                index += 1
                if stat == thisStat:
                    ability2D[-1][2].append([-1,index+(not self)*7,amount])
                    # print('Found defiant-like:',abilityName,stat,amount)
        elif 'ApplyStatusEffectAbAttr' in line:
            if 'StatusEffect.POISON' in line:
                ability2D[-1][2].append([30,14,0])
            elif 'StatusEffect.TOXIC' in line:
                ability2D[-1][2].append([30,15,0])
            elif 'StatusEffect.SLEEP' in line:
                ability2D[-1][2].append([30,16,0])
            elif 'StatusEffect.FREEZE' in line:
                ability2D[-1][2].append([30,17,0])
            elif 'StatusEffect.PARALYSIS' in line:
                ability2D[-1][2].append([30,18,0])
            elif 'StatusEffect.BURN' in line:
                ability2D[-1][2].append([30,19,0])
            else:
                print('No status found',line)
            # print('Found status proc ability:',abilityName)
        elif 'MoveTypeChangeAbAttr' in line and abilityName != 'liquidvoice':
            ability2D[-1][2].append([-2,26,1.2])
            # print('Found aerilate-like:',abilityName,1.2)
        elif 'StabBoostAbAttr' in line:
            ability2D[-1][2].append([-2,26,1.33])
            # print('Found stab boost:',abilityName,1.33)
        elif 'PostAttackApplyBattlerTagAbAttr' in line:
            ability2D[-1][2].append([10,21,0])
            # print('Found stench:',abilityName)
        elif 'SpeedBoostAbAttr' in line:
            ability2D[-1][2].append([-1,4,1])
            # print('Found speed boost:',abilityName,1)
        elif 'EffectSporeAbAttr' in line:
            ability2D[-1][2].append([30,23,0])
        elif 'MultCritAbAttr' in line: # Sniper
            ability2D[-1][2].append([-2,26,1.5])
        elif '.unimplemented()' in line:
            ability2D[-1][3].append(62)
            # print('Found unimp ability',abilityName)
        elif '.partial()' in line:
            ability2D[-1][3].append(61)
            # print('Found partial ability',abilityName)
        elif '.unsuppressable()' in line:
            ability2D[-1][3].append(48)
        elif '.unreplaceable()' in line:
            ability2D[-1][3].append(49)
        # Unignorable is 50, done in the previous section
        elif 'MoveAbilityBypassAbAttr' in line: # Ignores abilities (Mold Breaker, etc.)
            ability2D[-1][3].append(37)
        elif 'DoubleBattleChanceAbAttr' in line: # Lure abilities
            ability2D[-1][3].append(59)
        # elif 'ultipl' in line or 'oost' in line or 'pow' in line:
        #     # Check for keywords in the ability line like 'Multiply', 'Boost', or 'Power'
        #     # Print those lines to make sure I'm not missing anything important
        #     print(abilityName, line)

# Read all the move attributes from the game data
print('\n=========== Reading moves ===========\n')
with open(f'{pathData}/moves/move.ts', "r") as f:
    moveData = f.read()
moveData = re.findall(r'Move\[\]\)\.push\(\n(.*?)  \);\n', moveData, re.DOTALL)[0]
moveData = re.sub(r'\/\* Unused.*?End Unused \*\/', '', moveData, flags=re.DOTALL)
moveData = re.sub(r'LapseBattlerTagAttr,.*?true\)', '', moveData, flags=re.DOTALL)
moveData = re.sub(r' +new ', 'new ', moveData)
moveData = moveData.split('\n')
move2D = []
for line in moveData:
    if line[:3] == 'new':
        moveName = format_for_attr(format_for_disp(re.findall(r'MoveId\.(.*?),', line)[0]))
        if f'move{moveName}' not in filterToFID:
            # There are moves that exist in the game code but are not obtainable by any pokemon
            print(moveName, 'does not exist')
            # They have to be added here so that attributes don't error, but I ignore these moves later
            move2D.append(['xxxxx',moveName]) 
        else:
            moveFID = filterToFID[f'move{moveName}']
            move2D.append([moveFID, moveName, [], []]) # [fid[0], name[1], procs[2], tags[3]]

            # Append the fid of move type
            moveType = re.findall(r'Type\.(.*?),', line)[0]
            move2D[-1].append(filterToFID[f'type{format_for_attr(moveType)}']) # [4] type

            # Append the move category (phys/spec/stat)
            if re.findall(r'StatusMove\(Move', line) != []:
                move2D[-1].append(2) # [5] category    
                moveAttr = ['','']
                moveAttr.extend(re.findall(r'Type\.(.*?)\)', line)[0].split(','))
            else:
                moveCat = re.findall(r'MoveCategory\.(.*?),', line)[0]
                moveAttr = re.findall(r'Type\.(.*?)\)', line)[0].split(',')
                if moveCat == 'PHYSICAL':
                    move2D[-1].append(0) 
                elif moveCat == 'SPECIAL':
                    move2D[-1].append(1)
                else:
                    print(line)
                    input()

            # Indicies for line input from move.ts:
            # [category, power, accuracy, pp, chance, priority, gen]
            # (status moves lack cat and power)

            if move2D[-1][5] == 2: # If status move
                move2D[-1].append(-1) # [6] power
            else:
                move2D[-1].append(format_for_attr(moveAttr[2])) # [6] power
            move2D[-1].append(format_for_attr(moveAttr[3])) # [7] accuracy
            move2D[-1].append(format_for_attr(moveAttr[4])) # [8] pp
            move2D[-1].append(format_for_attr(moveAttr[6])) # [9] priority  
            procChance = int(format_for_attr(moveAttr[5]))                     
            if 'SelfStatusMove' in line:                                    
                move2D[-1][3].append(202)
    else:                                                            
        # General order of move descriptors: priority, targets, procs, all other tags
        # All the procs and tags are shared between abilities and moves
        # Tags should be in sequential order as they will be displayed on my site
        # They are not processed in sequential order here, due to string matching
        # My internally used tags start at 200 (for contact, reflectable, etc.)
        if len(move2D[-1]) > 2:
            if '.attr(HighCritAttr)' in line:
                move2D[-1][3].append(3)
            elif 'CritOnlyAttr' in line: # auto crit
                move2D[-1][3].append(4)
            elif 'CRIT_BOOST' in line and 'target' not in line: # focus energy, not dragon cheer
                move2D[-1][3].append(5)
            elif '.makesContact(false)' in line: # these contact values are overrides
                move2D[-1][3].append(200)       # if it doesn't exist, look at move category
            elif '.makesContact(true)' in line:
                move2D[-1][3].append(201)
            elif '.makesContact()' in line:
                move2D[-1][3].append(201)
            elif '.powderMove()' in line: # Move archetypes for synergies/immunities
                move2D[-1][3].append(23)
            elif '.reflectable()' in line:
                move2D[-1][3].append(203)
            elif '.slicingMove()' in line:
                move2D[-1][3].append(28)
            elif '.punchingMove()' in line:
                move2D[-1][3].append(29)
            elif '.danceMove()' in line:
                move2D[-1][3].append(26)
            elif '.ballBombMove()' in line:
                move2D[-1][3].append(33)
            elif '.pulseMove()' in line:
                move2D[-1][3].append(30)
            elif '.bitingMove()' in line:
                move2D[-1][3].append(31)
            elif '.triageMove()' in line:
                move2D[-1][3].append(25)
            elif '.soundBased()' in line:
                move2D[-1][3].append(35)
                move2D[-1][3].append(36)
            elif '.windMove()' in line:
                move2D[-1][3].append(27)
            elif 'failIfDampCondition' in line:
                move2D[-1][3].append(34)
            elif '.ignoresProtect()' in line:
                move2D[-1][3].append(38)
            elif '.ignoresSubstitute()' in line:
                move2D[-1][3].append(36)
            elif 'hidesTarget()' in line: # roar
                move2D[-1][3].append(40)
            elif 'MoveTarget.RANDOM_NEAR_ENEMY' in line: # outrage
                move2D[-1][3].append(0)
            elif 'MoveTarget.ALL_NEAR_ENEMIES' in line: # eruption
                move2D[-1][3].append(1)
            elif 'MoveTarget.ALL_NEAR_OTHERS' in line: # earthquake
                move2D[-1][3].append(2)
            elif 'MoveTarget.USER_SIDE' in line or 'MoveTarget.USER_AND_ALLIES' in line:
                move2D[-1][3].append(202) # Internal tag to ignore these for reflectable
            elif 'ProtectAttr' in line or 'MoveTarget.BOTH_SIDES' in line or 'MoveTarget.NEAR_ALLY' in line:
                move2D[-1][3].append(202) # Internal tag to ignore these for reflectable
            elif 'MultiHitAttr' in line:
                if 'MultiHitType._2' in line:
                    move2D[-1][3].append(41)
                elif 'MultiHitType._3' in line:
                    move2D[-1][3].append(42)
                elif 'MultiHitType._10' in line:
                    move2D[-1][3].append(43)
                else:
                    move2D[-1][3].append(44)
            elif '.attr(FlinchAttr)' in line:
                move2D[-1][2].append([procChance,21,0])
            elif 'ConfuseAttr' in line:
                move2D[-1][2].append([procChance,20,0])
            elif 'GrowthStatStageChangeAttr' in line: # Growth
                move2D[-1][2].append([-1,0,1])
                move2D[-1][2].append([-1,2,1])
            elif '(HealStatusEffectAttr,' in line: # cleansing status effects
                if '[ StatusEffect' in line:
                    move2D[-1][3].append(19)
                elif 'getNonVolatile' in line:
                    move2D[-1][3].append(19)
                elif 'StatusEffect.SLEEP' in line:
                    move2D[-1][3].append(20)
                elif 'StatusEffect.FREEZE' in line:
                    move2D[-1][3].append(21)
                elif 'StatusEffect.PARALYSIS' in line:
                    input('unused')
                    move2D[-1][3].append(203)
                elif 'StatusEffect.BURN' in line:
                    move2D[-1][3].append(22)
            elif 'MultiStatusEffectAttr' in line: # dire claw and tri attack
                if 'SLEEP' in line:
                    move2D[-1][2].append([procChance,23,0]) # dire claw
                else:
                    move2D[-1][2].append([procChance,24,0]) # tri attack
            elif '(StatusEffectAttr,' in line: # applying status effects
                if 'StatusEffect.POISON' in line:
                    move2D[-1][2].append([procChance,14,0])
                if 'StatusEffect.TOXIC' in line:
                    move2D[-1][2].append([procChance,15,0])
                if 'StatusEffect.SLEEP' in line:
                    move2D[-1][2].append([procChance,16,0])
                if 'StatusEffect.FREEZE' in line:
                    move2D[-1][2].append([procChance,17,0])
                if 'StatusEffect.PARALYSIS' in line:
                    move2D[-1][2].append([procChance,18,0])
                if 'StatusEffect.BURN' in line:
                    move2D[-1][2].append([procChance,19,0])
            elif '(StatStageChangeAttr,' in line:
                stats = re.findall(r'\[(.*?)\]', line)[0].split(',')
                stats = [re.sub('stat.','',format_for_attr(stat)) for stat in stats]
                amount = re.findall(r'\], (.*?)[,|)]', line)[0]
                isSelf = (', true' in line)
                index = -1
                if len(stats) == 5:
                    move2D[-1][2].append([procChance,22,1]) # ancient power, silver wind, ominous wind, no retreat
                elif 'PokemonType.STELLAR' in line:
                    move2D[-1][2].append([procChance,25,-1]) # tera blast
                else:
                    if 'effectChanceOverride' in line:
                        effChance = 50
                    else:
                        effChance = procChance
                    for stat in ['atk','def','spatk','spdef','spd','acc','eva']:
                        index += 1
                        if stat in stats:
                            move2D[-1][2].append([effChance,index+(not isSelf)*7,amount])
            elif 'recklessMove' in line: # reckless and recoil moves
                move2D[-1][3].append(32)
            elif 'RecoilAttr, true, 0.5' in line or 'HalfSacrificialAttr' in line:
                move2D[-1][3].append(9)
            elif 'CurseAttr' in line:
                move2D[-1][3].append(8)
            # elif 'RecoilAttr, true, 0.25' in line: # struggle
            #     move2D[-1][3].append()
            elif 'RecoilAttr, false, 0.33' in line:
                move2D[-1][3].append(11)
            elif 'RecoilAttr, false, 0.5' in line:
                move2D[-1][3].append(10)
            elif 'RecoilAttr' in line:
                move2D[-1][3].append(12)
            elif 'FrenzyAttr' in line: # outrage
                move2D[-1][3].append(45)
            elif 'HitHealAttr, 1' in line:
                move2D[-1][3].append(15)
            elif 'HitHealAttr, 0.75' in line:
                move2D[-1][3].append(16)
            elif 'HitHealAttr, null, Stat.ATK' in line:
                move2D[-1][3].append(18)
            elif 'HitHealAttr' in line:
                move2D[-1][3].append(17)
            elif 'OneHitKOAttr' in line:
                move2D[-1][3].append(56)
                move2D[-1][3].append(57)
            elif 'TrapAttr' in line:
                if 'RemoveArenaTrapAttr' in line:
                    move2D[-1][3].append(46) # rapid spin
                else:
                    move2D[-1][3].append(47) # binding moves
            elif 'DoublePowerChanceAttr' in line: # fickle beam
                move2D[-1][3].append(13)
            elif 'BypassRedirectAttr' in line:
                move2D[-1][3].append(51)
            elif 'ThunderAccuracyAttr' in line:
                move2D[-1][3].append(53)
            elif 'StormAccuracyAttr' in line:
                move2D[-1][3].append(53)
            elif '(failOnBossCondition)' in line:
                move2D[-1][3].append(58)
            elif '.unimplemented()' in line:
                move2D[-1][3].append(62)
            elif '.partial()' in line:
                move2D[-1][3].append(61)
            elif 'ForceSwitchOutAttr, true' in line or 'ChillyReceptionAttr' in line: # u turn
                move2D[-1][3].append(39)
            elif '.ignoresAbilities()' in line: # moongeist beam
                move2D[-1][3].append(37)
            elif 'LeechSeedAttr' in line: # leech seed
                move2D[-1][3].append(24)
            # elif 'StealHeldItemChanceAttr' in line: # thief, covet
            #     move2D[-1][3].append()
            elif 'TrappedTag' in line: # no retreat
                move2D[-1][3].append(54)
            elif 'TRAPPED' in line: # mean look
                move2D[-1][3].append(55)
            elif 'JawLockAttr' in line: # jaw lock
                move2D[-1][3].append(54)
                move2D[-1][3].append(55)
            elif 'OCTOLOCK' in line: # octolock
                move2D[-1][3].append(55)
                move2D[-1][2].append([procChance,8,-1])
                move2D[-1][2].append([procChance,10,-1])
            elif 'CutHpStatStageBoostAttr' in line: # belly / clang / fillet
                stats = re.findall(r'\[(.*?)\]', line)[0].split(',')
                stats = [re.sub('stat.','',format_for_attr(stat)) for stat in stats]
                amount = re.findall(r'\], (.*?),', line)[0]
                index = -1
                if len(stats) == 5:
                    move2D[-1][2].append([procChance,22,1]) # ancient power, silver/ominous, no retreat, clang
                elif amount != '12':
                    for stat in ['atk','def','spatk','spdef','spd','acc','eva']:
                        index += 1
                        if stat in stats:
                            move2D[-1][2].append([-1,index,amount])
                if len(stats) == 1: # belly
                    move2D[-1][3].append(6)
                    move2D[-1][3].append(8)
                elif len(stats) == 3: # fillet
                    move2D[-1][3].append(8)
                elif len(stats) == 5: # clang
                    move2D[-1][3].append(7)
                else:
                    input('Unknown boosting move',line)
            # Unused tags below this line ================================
            # elif 'ProtectAttr' in line: # show different protect moves ????
            #     move2D[-1][3].append()
            # elif 'failIfLastCondition' in line:
            #     move2D[-1][3].append()
            elif 'crashDamageFunc' in line:
                e = 'nothing'
            elif 'HealAttr' in line:
                e = 'nothing'
            elif 'UpperHandCondition' in line:
                e = 'nothing'
            elif 'Pledge' in line:
                e = 'nothing'
            elif 'doublePowerChanceMessageFunc' in line:
                e = 'nothing'
            elif 'TeraStarstormTypeAttr' in line:
                e = 'nothing'
            elif 'TeraMoveCategoryAttr' in line:
                e = 'nothing'
            elif format_for_attr(line) in ['',');','})','}),','}','}else{','return1;','.attr(','return(',')?2:1','//todo']:
                e = 'nothing'
            elif format_for_attr(line)[:2] == '//':
                e = 'nothing'
            else:
                e = 'nothing'
                # print('\n',move2D[-1][0],'\n',line)

# The above data is just ordered how the moves/abilities appear in the game code
# This next step reorders them according to the fid list
for line in ability2D:
    if f'ability{line[1]}' in filterToFID:
        orderedData[line[0]-fidThresholds[0]] = line # Replace ability rows with assembled ability row
for line in move2D:
    if f'move{line[1]}' in filterToFID:
        orderedData[line[0]-fidThresholds[0]] = line # Replace move rows with assembled move row

print('\n==============================\n')
print('Checking for errors...\n')
if orderedData[-1][1] != 'eternabeam':
    print('\nLast five moves:')
    print([orderedData[-index][1] for index in range(5,0,-1)])
print('There should be 4 attacks with multiple procs')
for fidLine in orderedData:
    if len(fidLine) > 4: # For moves
        procCount = 0
        for procLine in fidLine[2]:
            if procLine[0] > -1:
                procCount += 1
            if procCount > 1:
                print('Multiple procs found in',fidLine[1])
        if 203 in fidLine[3] and fidLine[5] != 2:
            input('***** Reflectable attack',fidLine[1])
        if 203 not in fidLine[3] and fidLine[5] == 2 and 202 not in fidLine[3]:
            if 25 not in fidLine[3] and 6 not in fidLine[3]:
                isBoosting = 0
                for procLine in fidLine[2]:
                    if procLine[1] < 7 or procLine[1] == 22:
                        isBoosting = 1
                if not isBoosting:
                    # The game tracks which moves are reflectable, but almost every offensive status is reflectable
                    # However, i think it's ugly to show something that obvious
                    # I'd rather show CAN'T be reflected, to be in line with other tag wording
                    # print('Non-reflectable status',fidLine)
                    fidLine[3].append(52)
    elif len(fidLine) == 4: # For abilities
        for procLine in fidLine[2]:
            if procLine[0] == 0 and procLine[2] == 0:
                print('Empty proc',fidLine[1],procLine)

# Read the upgrade cost data
with open(f'{pathData}/balance/starters.ts', "r") as f:
    costDataRaw = f.read()
costData = re.findall(r'starterCandyCosts(.*?)\];\n', costDataRaw, re.DOTALL)[0]
costData = costData.split('\n')[1:-1]
costParsed = [[
    re.findall(r'passive: (.*?),', line)[0],
    re.findall(r'\[ (.*?) \]', line)[0].split(', ')[0],
    re.findall(r'\[ (.*?) \]', line)[0].split(', ')[1],
    re.findall(r'egg: (.*?) }', line)[0],
] for line in costData]
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
typeColors = ["#ADBD21","#735A4A","#7B63E7","#FFC631","#EF70EF","#A55239","#F75231","#9CADF7","#6363B5","#7BCE52","#AE7A3B","#5ACEE7","#ADA594","#9141CB","#EF4179","#BDA55A","#81A6BE","#399CFF"]
lines = []
with open("game_files/package.json", "r") as fp:
    packageInfo = json.load(fp)
    lines.append(f'const gameVersion = "{packageInfo["version"]}";') # Type colors
todayDate = date.today().strftime("%Y-%m-%d")
lines.append(f'const latestDate = "{todayDate}";')
lines.append('const typeColors = [') # Type colors
for color in typeColors:
    lines.append(f"'{color}',")
lines.append('];\nconst fidThreshold = [') # fid category thresholds
for threshold in fidThresholds:
    lines.append(f"{threshold},")
lines.append('];\nconst upgradeCosts = [') # upgrade costs
for index,costLine in enumerate(costParsed):
    lines.append(f"[{costLine[0]},{costLine[1]},{costLine[2]},{costLine[3]},{friendData[index]}],")
 
# Format of orderedData: 
#   Abilities: [fid[0], name[1], procs[2], tags[3]]
#   Moves: [fid, name, [procs[chance,stat,val]], [tags], type, cat, pow, acc, pp, prio]
#            0     1      2                        3      4    5    6    7    8    9

# Final structure of fidToProc[fid]:
# ==================================
# Abilities: [ [procs], [tags] ]
#   procs = [[chance,stat,value], [...]]
#       chance = chance of ability activating (flame body, etc.) > error on chance of 0 ???????????????????????
#           or -1 for no chance indicator
#           or -2 for ×value (default is +)
#           or -3 for +value%
#       stat is which stat, status, etc.
#           0-6 = self atk/def/spa/spd/spe/acc/eva
#           7-13 = opp  atk/def/spa/spd/spe/acc/eva
#           14-20 = pois/tox/sleep/freeze/para/burn/confuse
#           21-26 = flinch/omni/dire/triatt/terablast/damage
#       value is how much (default +value or -value)
#           0 is don't show
# Moves: [ [procs[chance,stat,val]], [tags], type, cat(phys/spec/stat), pow, acc, pp, prio]
#             0                        1       2    3                    4    5    6    7

# ======================= Write numeric filter data to filters_global.js =======================
# This is just numbers. Localized strings are written from updateLangs.py
lines.append('];\nconst fidToProc = [') # Ability/move descriptions
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

with open("website/filters_global.js", "w") as file:
    file.writelines(f"{line}\n" for line in lines)

print("Done writing numeric filter data")

# ======================= Composite all the biome images =======================
print('\n==============================\n')
print('Creating biome images...')

biome_src = "./game_files/assets/images/arenas"
biome_dest = "./website/ui/biomes"
with open("local_files/my_json/allFilters.json", "r") as file:
    allFilters = json.load(file)
with open("local_files/my_json/fidThresholds.json", "r") as fp:
    fidThresholds = json.load(fp)
biomeNames = [filter[1].lower().replace(' ','_') for filter in allFilters if filter[0] == 'Biome']
thisFID = fidThresholds[8]-1

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