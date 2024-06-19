from item_OLD import *
from copy import deepcopy
from warnings import warn


class Background:
    def __init__(self, name):
        self.name = name
        self.description = ''
        self.skills = []
        self.starting_gear = ['setattr(self, "caps", 850)']

    def choose_starting_gear(self, race):
        race_exists = False
        for i in range(1, len(self.starting_gear)):
            if race.title() in self.starting_gear[i][0]:
                self.starting_gear = self.starting_gear[i][1:]
                race_exists = True
                break
        if not race_exists:
            warn('Invalid race: race does not exist')


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
    (Armor('Cloth'), 1, ['Lead-lined (rank 1)']),  # format is (class_instance, qty, [mods_if_any])
    (BladedWeapon('Knife'), 1),
    (Handgun('Bolt-Action Pipe Pistol'), 1),
    (Ammo('9mm'), 15),
    (Bag('Backpack'), 1),
    (Gear('Chain'), 1),
    (Food('CRAM'), 3),
    (Healing('RadAway (Diluted)'), 1),
    (Healing('Rad-X'), 1),
    (Healing('Healing Powder'), 1),
    (Drink('Dirty Water'), 3),
    (Drink('Purified Water'), 1),
]
# cultist.starting_gear.append(human_cultist_gear)

ghoul_or_mutant_cultist_gear = deepcopy(human_cultist_gear)
ghoul_or_mutant_cultist_gear[0] = ('Ghoul', 'Super Mutant')
ghoul_or_mutant_cultist_gear[2] = (Armor('Leather'), 1)
ghoul_or_mutant_cultist_gear[9] = (Healing('Stimpak'), 1)
ghoul_or_mutant_cultist_gear[10] = (Healing('Stimpak (Diluted)'), 1)
ghoul_or_mutant_cultist_gear[12] = (Drink('Dirty Water'), 4)
del ghoul_or_mutant_cultist_gear[13]
del ghoul_or_mutant_cultist_gear[11]

synth_or_robot_cultist_gear = deepcopy(human_cultist_gear)
synth_or_robot_cultist_gear[0] = ('Gen-2 Synth', 'Robot')
synth_or_robot_cultist_gear[2] = (Armor('Leather'), 1)
synth_or_robot_cultist_gear[8] = (Healing('Quick Fix-it 1.0'), 2)
synth_or_robot_cultist_gear[9] = (Overclock('Overclock Hardware'), 1)
synth_or_robot_cultist_gear[10] = (Overclock('Cache Clearer'), 1)
del synth_or_robot_cultist_gear[11:]
print(synth_or_robot_cultist_gear)


cultist.starting_gear.extend([human_cultist_gear, ghoul_or_mutant_cultist_gear, synth_or_robot_cultist_gear])
