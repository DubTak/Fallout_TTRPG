import pandas as pd
import re


# WEAPONS
def extract_crit_info(crit):
    # 'Critical Hit' column is in format '<target_num>, <bonus_dice/multiplier>. <effect>'
    # bonus_dice, multiplier, and effect are all optional. bonus_dice and multiplier cannot coexist.
    target_num, bonus_dice, multiplier, effect = None, None, None, None
    match = re.findall(r'(\d+)[\., ]+(\d?[dx]\d+)?[\., ]*(.*)[\.,]?', crit)
    match = match[0]  # re.findall() returns [(x, y, z)] and I'd prefer (x, y, z), so this grabs the inner tuple
    target_num = int(match[0])
    if 'd' in match[1]:
        bonus_dice = str(match[1])
    elif 'x' in match[1]:
        multiplier = int(match[1][1])
    # a few of the bonus_dice are '+x' and this ends up in the effect match, so I'm putting it in the right place
    # it also (thankfully) never coexists with effect text, so no string slicing required
    # and yes, I tried getting RegEx to find it, but I only have so much time in the day and this fix worked, so...
    if '+' in match[2]:
        bonus_dice = str(match[2]).replace('.', '')  # removing pesky periods
    elif match[2] != '':
        effect = str(match[2]).replace('.', '')  # removing pesky periods
    return target_num, multiplier, bonus_dice, effect


def properties_to_list(properties):
    properties_list = []
    for property in properties.rstrip('.').split(', '):
        properties_list.append(property)
    return properties_list


def extract_range(range, thrown=False):
    range_short, range_long = None, None
    if thrown:
        match = re.findall(r'Thrown \(x(\d+)/x(\d+)\)', str(range))
        if len(match) != 0:  # wasn't a problem above because all entries started the same way.
            match = match[0]
            range_short = int(match[0])
            range_long = int(match[1])
    else:
        match = re.findall(r'x(\d+)/x(\d+)', str(range))
        if len(match) != 0:
            match = match[0]
            range_short = int(match[0])
            range_long = int(match[1])
    return range_short, range_long


WEAPONS = pd.read_csv('csv/weapons.csv')

WEAPONS[['Crit Target Num', 'Crit Bonus Dice', 'Crit Multiplier', 'Crit Effect']] = None
# populating the new crit columns with their appropriate values (keeping the None entries for exist checks later)
for i in range(len(WEAPONS)):
    crit_tuple = extract_crit_info(WEAPONS.loc[i, 'Critical Hit'])
    WEAPONS.loc[i, 'Crit Target Num'] = crit_tuple[0]
    WEAPONS.loc[i, 'Crit Bonus Dice'] = crit_tuple[1]
    WEAPONS.loc[i, 'Crit Multiplier'] = crit_tuple[2]
    WEAPONS.loc[i, 'Crit Effect'] = crit_tuple[3]

WEAPONS[['Range Short', 'Range Long']] = None
# populating the new range columns as above
for i in range(len(WEAPONS)):
    range_tuple = extract_range(WEAPONS.loc[i, 'Range'])
    if range_tuple[1] is not None:
        WEAPONS.loc[i, 'Range Short'] = range_tuple[0]
        WEAPONS.loc[i, 'Range Long'] = range_tuple[1]
    else:
        WEAPONS.loc[i, 'Range Short'] = WEAPONS.loc[i, 'Range']
for i in range(len(WEAPONS)):
    if 'Thrown' in WEAPONS.loc[i, 'Properties']:
        range_tuple = extract_range(WEAPONS.loc[i, 'Properties'], thrown=True)
        WEAPONS.loc[i, 'Range Short'] = range_tuple[0]
        WEAPONS.loc[i, 'Range Long'] = range_tuple[1]

WEAPONS['Properties'] = WEAPONS['Properties'].apply(properties_to_list)


# ARMOR
ARMOR = pd.read_csv('csv/armor.csv')



