import pandas as pd
import re


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


weapons = pd.read_csv('csv/weapons.csv')
weapons[['Crit Target Num', 'Crit Bonus Dice', 'Crit Multiplier', 'Crit Effect']] = None
# populating the new columns with their appropriate values (keeping the None entries for exist checks later)
for i in range(len(weapons)):
    crit_tuple = extract_crit_info(weapons.loc[i, 'Critical Hit'])
    weapons.loc[i, 'Crit Target Num'] = crit_tuple[0]
    weapons.loc[i, 'Crit Bonus Dice'] = crit_tuple[1]
    weapons.loc[i, 'Crit Multiplier'] = crit_tuple[2]
    weapons.loc[i, 'Crit Effect'] = crit_tuple[3]

weapons[['Crit Target Num', 'Crit Bonus Dice', 'Crit Multiplier', 'Crit Effect']]


