import random
import re
from collections import Counter

class Dice:
    def __init__(self, sides):
        self.sides = sides

    def __repr__(self):
        return f'd{self.sides}'

    def roll(self, num_dice=1, sides=None, modifier=0, **kwargs):
        if sides is None:
            sides = self.sides
        advantage = False
        disadvantage = False
        reroll = None
        success_on = None
        explode_on = None

        # protecting against 0 dice rolled
        if num_dice == 0:
            return 0
        # I don't want to raise an exception for invalid num_dice lest it stop the program, so it'll just return None
        if num_dice < 0 or not isinstance(num_dice, int):
            return None

        for key, value in kwargs.items():
            if key == 'advantage' and value == True:
                advantage = True
            if key == 'disadvantage' and value == True:
                disadvantage = True
            if key == 'reroll':
                reroll = value
            if key == 'success_on':
                success_on = value
                modifier = 0  # success-on-x rolls are incompatible with post-roll modifiers
            if key == 'explode_on':
                explode_on = value

        # the roll in dice notation, based mostly on Roll20's Dice Reference
        roll_str = f'{num_dice}d{sides}'
        if advantage and not disadvantage:
            roll_str = f'{num_dice + 1}d{sides}kh1'
        if disadvantage and not advantage:
            roll_str = f'{num_dice + 1}d{sides}kl1'
        if reroll is not None:
            if isinstance(reroll, int):
                roll_str += f'r{reroll}'
            elif isinstance(reroll, (tuple, list)) and len(reroll) == 2:
                if reroll[1] == 'le':
                    roll_str += f'r>{reroll[0]}'
                elif reroll[1] == 'ge':
                    roll_str += f'r<{reroll[0]}'
        if explode_on is not None:
            if success_on is None:
                if explode_on == sides:
                    roll_str += '!'
                else:
                    roll_str += f'!>{explode_on}'
            else:
                if explode_on == sides:
                    roll_str = f'{{{num_dice}d{sides}!}}'
                else:
                    roll_str = f'{{{num_dice}d{sides}!>{explode_on}}}'
        if success_on is not None:
            roll_str += f'>{success_on}'
        if modifier > 0:
            roll_str += f' + {modifier}'
        if modifier < 0:
            roll_str += f' - {abs(modifier)}'

        raw_roll = [random.randint(1, sides) for _ in range(num_dice)]
        res = sum(raw_roll) + modifier

        if advantage and not disadvantage:
            raw_roll2 = [random.randint(1, sides) for _ in range(num_dice)]
            total = 0
            for i in range(num_dice):
                raw_roll[i] = (raw_roll[i], raw_roll2[i])
                total += max(raw_roll[i])
            res = total + modifier
        if disadvantage and not advantage:
            raw_roll2 = [random.randint(1, sides) for _ in range(num_dice)]
            total = 0
            for i in range(num_dice):
                raw_roll[i] = (raw_roll[i], raw_roll2[i])
                total += min(raw_roll[i])
            res = total + modifier

        if reroll is not None:
            if isinstance(reroll, int):
                for value in raw_roll:
                    if value == reroll:
                        idx = raw_roll.index(value)
                        raw_roll[idx] = (random.randint(1, sides), value)
                        res += raw_roll[idx][0] - raw_roll[idx][1]
            elif isinstance(reroll, (tuple, list)) and len(reroll) == 2:
                if reroll[1] == 'le':
                    for value in raw_roll:
                        if value <= reroll[0]:
                            idx = raw_roll.index(value)
                            raw_roll[idx] = (random.randint(1, sides), value)
                            res += raw_roll[idx][0] - raw_roll[idx][1]
                elif reroll[1] == 'ge':
                    for value in raw_roll:
                        if value >= reroll[0]:
                            idx = raw_roll.index(value)
                            raw_roll[idx] = (random.randint(1, sides), value)
                            res += raw_roll[idx][0] - raw_roll[idx][1]

        if explode_on is not None:
            count = Counter(raw_roll)[explode_on]
            final_idx = len(raw_roll) - 1
            while count > 0:
                for explode in raw_roll:
                    if explode >= explode_on:
                        # protection against overfilling list with infinite explodes & making runtime absurd
                        if len(raw_roll) == 100000:
                            break
                        raw_roll.append(random.randint(1, sides))
                        count += Counter(raw_roll[final_idx:])[explode_on]
                        final_idx += 1
                    count -= 1


        if success_on is not None:
            full_count = Counter(raw_roll)
            num_success = full_count[success_on]
            if success_on != sides:
                for i in range(success_on, sides + 1):
                    num_success += full_count[i]
            res = num_success

        return tuple([res, raw_roll, roll_str])

d20 = Dice(20)
print(d20)
print(d20.roll(modifier=-1, advantage=True))
print(d20.roll(num_dice=4, sides=6, modifier=5, reroll=(2, 'le')))
print(d20.roll(num_dice=10, sides=10, success_on=8, explode_on=10))
