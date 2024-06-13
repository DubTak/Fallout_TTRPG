import pandas as pd
import random


def dice_roll_xDy_plus_z(x, y, z=0):
    running_total = 0
    rolls_list = []
    for n in range(x):
        rolls_list.append(random.randint(1, y))
        running_total += rolls_list[n]
    return [rolls_list, running_total, z, running_total + z]


print(dice_roll_xDy_plus_z(6, 6))
