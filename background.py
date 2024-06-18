from item_OLD import *
from copy import deepcopy


class Background:
    def __init__(self, name):
        self.name = name
        self.description = ''
        self.skills = []
        self.starting_gear = ['setattr(self, "caps", 850)']

# Custom Background
custom = Background('Custom Background')
custom.description = ("If you’d like to instead craft your own background within the post-apocalypse, "
                      "choose this option for your background instead of the ones listed below.")
custom.skills.extend([2, 2, 2])
custom.starting_gear.append('UNIMPLEMENTED')  # need to implement choice of starting equipment


# Cultist
cultist = Background('Cultist')
cultist.description = ("Whether you were born into this life or these people brought hope to you when you hit "
                       "rock bottom. You are in service to a group of followers who zealously recruit all they "
                       "can find into their doctrine. This new world, born of fire, is a gift. Only now that "
                       "this world has been cleansed can the truth be seen. You now wander the wastes looking"
                       "for signs and awaiting orders from the great beyond.")
human_cultist_gear = [
    'Human',
    'setattr(self, "caps", 50)',
    ('Cloth', Armor('Cloth'), 1, 'rank 1 lead lined'),  # format is (name, class_instance, qty, mods_if_any)
    ('Knife', BladedWeapon('Knife'), 1),
    ('Bolt-Action Pistol', Handgun('Bolt-Action Pistol'), 1),
    ('9mm', Ammo('9mm'), 15),
    ('Backpack', Bag('Backpack'), 1),
    ('Chain', Gear('Chain'), 1),
    ('CRAM', Food('Cram'), 3),
    ('RadAway (Diluted)', Healing('RadAway (Diluted)'), 1),
    ('Rad-X', Healing('Rad-X'), 1),
    ('Healing Powder', Healing('Healing Powder'), 1),
    ('Dirty Water', Drink('Dirty Water'), 3),
    ('Purified Water', Drink('Purified Water'), 1),
]
ghoul_or_mutant_gear = deepcopy(human_cultist_gear)
ghoul_or_mutant_gear[0] = ['Ghoul', 'Super Mutant']
ghoul_or_mutant_gear[2] = ('Leather', Armor('Leather'), 1)
ghoul_or_mutant_gear[9] = ('Stimpak', Healing('Stimpak'), 1)
ghoul_or_mutant_gear[10] = ('Stimpak (Diluted)', Healing('Stimpak (Diluted)'), 1)
ghoul_or_mutant_gear[12] = ('Dirty Water', Drink('Dirty Water'), 4)
del ghoul_or_mutant_gear[13]
del ghoul_or_mutant_gear[11]
for i in ghoul_or_mutant_gear:
    print(i)

cultist.starting_gear.extend(human_cultist_gear)