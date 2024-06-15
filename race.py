from copy import deepcopy

class Race:
    def __init__(self, name, type, variant1=False, variant2=False):
        self.name = name
        self.type = type
        self.traits = {'Age': '', 'Size': []}
        self.variant1 = variant1
        self.variant1_traits = None
        self.variant2 = variant2
        self.variant2_traits = None
        self.extra_description = None

    def __repr__(self):
        return f'{self.name}'


# Human
human = Race('Human', 'Human')
human.traits['Age'] = ("Humans reach adulthood in their late teens and live less than a century. "
                       "Though, those who live this long are far and few between in the wasteland.")
human.traits['Size'] = ['Medium', 'Small']

human_var1 = deepcopy(human)
human_var1.name = 'Human (Variant)'
human_var1.variant1 = True
human_var1.traits['Resourceful'] = [
    'self.karma_caps += 1',
    'You gain one extra Karma Cap (see page 8) that you can use each game.',
]
human_var1.traits['Unexposed'] = [
    'UNIMPLEMENTED',  # I need to make an advantage/disadvantage flag on the character sheet
    'You have disadvantage on all Radiation and Addiction checks.'
]

human_var2 = deepcopy(human)
human_var2.name = 'Gen-3 Synth'
human_var2.variant2 = True
human_var2_desc = ("Oftentimes, Humans in the wasteland are actually synthetic machines that are indistinguishable "
                   "from a regular human created by a secret cabal of scientists called “The Institute”. "
                   "This variant option provides no abilities or statistical change. However it can provide a "
                   "psychological or narrative one. Work with your GM on how this potentiality could affect your "
                   "character. Alternatively, when creating your human character; roll a d20. On a 20, your character "
                   "is secretly a Gen 3 Synth.")
human_var2.extra_description = human_var2_desc

human_var1_and_var2 = deepcopy(human_var1)
human_var1_and_var2.name = 'Gen-3 Synth (Variant)'
human_var2.variant2 = True
human_var1_and_var2.extra_description = human_var2_desc


# Ghoul
ghoul = Race('Ghoul', 'Ghoul')
ghoul.traits['Age'] = ("Ghouls are nearly immortal, their lifespan is unknown. "
                       "Some Ghouls have survived from even before the Great War over 200 years ago.")
ghoul.traits['Size'] = ['Medium', 'Small']
evolution_exec = '''
setattr(self, 'rad_level', None), setattr(self, 'irradiated_food', None)
setattr(self, 'radiation_dc', None), self.immunities.add("radiation") 
'''
ghoul.traits['Evolution'] = [
    evolution_exec,
    "You cannot gain levels of radiation and you are immune to radiation damage. Additionally, you gain no "
    "Irradiated levels from consuming food or water.",
]
ghoul.traits['Resilient Anatomy'] = [
    'self.resistances.add("poison")',
    "You are resistant to poison damage. Any stamina points you would gain from consuming food, drinks, or chems "
    "is halved (rounded down). Any hit points you would gain from stimpaks is halved (rounded down). "
    "You cannot gain hit points from healing powder. Syringes that aren’t ‘loaders’ have no effect on you. "
    "Additionally, whenever you take damage from the bleeding condition, you take half as much.",
    # 'UNIMPLEMENTED',  # I need to add  flag for 1/2 SP or HP gains etc
]

ghoul_var1 = deepcopy(ghoul)
ghoul_var1.name = 'Ghoul (Variant)'
ghoul_var1.variant1 = True
many_roads_walked_exec = """
for i in range(len(self.skills)):
    self.skills[i].ranks += 2
self.unspent_perks += 1
"""
ghoul_var1.traits['Many Roads Walked'] = [
    many_roads_walked_exec,
    "You gain a +2 in all skills and you gain an extra perk at 1st Level.",
]
ghoul_var1.traits['Old Bones'] = [
    'self.resistances.remove("poison"), self.immunities.add("poison")',
    "You are immune to poison damage and you gain the Stitched Together perk.",
     # 'UNIMPLEMENTED',  # I haven't made perks yet
]
ghoul_var1.traits['Half Life'] = [
    '',
    "Your mind slips each day, ghoulification has taken an immense toll on you and you feel yourself slowly "
    "becoming feral. When you reach Level 15, you are fully consumed by ghoulification, your mind is no longer your "
    "own, and your character is controlled by the GM."
]


# Gen-2 Synth
synth = Race('Gen-2 Synth', 'Synth')
synth.traits['Age'] = ("Gen-2 Synths can live hundreds of years before their inorganic materials begin to "
                       "corrode and their programming deteriorates. However, a Synth who keeps consistent "
                       "repairs is nigh immortal.")
synth.traits['Size'] = ['Medium', 'Small']
inorganic_body_exec = """
self.immunities.update(["poison", "radiation"])
self.condition_immunities.add("suffocating")
self.rad_level, self.irradiated_food, self.hunger, self.thirst, self.radiation_dc = None, None, None, None, None
"""
synth.traits['Inorganic Body'] = [
    inorganic_body_exec,
    "You are immune to radiation and poison. You gain no effects from Chems, Drinks or Food. "
    "Additionally you have no need to breathe, sleep, eat, or drink.",
    # 'UNIMPLEMENTED'  # I need to add food/drink/etc effects and then add ability to reduce those effects
]
synth_and_robot_rest = """
- You do not require sleep.
- 1 hour of rest restores your stamina points to full.
- 2 hours of rest restores a number of hit points equal to half your INT or PER score + your level 
  and removes one level of exhaustion.
"""
synth.extra_description = synth_and_robot_rest

synth_var1 = deepcopy(synth)
synth_var1.name = 'Gen-2 Synth (Variant)'
synth_var1.variant1 = True
synth_var1.traits['Brittle Body'] = [
    'self.vulnerabilities.add("electricity")',
    "Whenever a creature makes a targeted attack against you, you gain two limb conditions instead of one. "
    "Additionally you are vulnerable to electricity damage.",
    # UNIMPLEMENTED: I need to somehow implement the extra limb conditions thing? Might just have the text displayed.
]
synth_var1.traits['Software and Hardware Upgrades'] = [
    'UNIMPLEMENTED',  # I need to make perks and also make a tag for perk reqs
    "Whenever you gain a perk, you are considered a Robot for perk requirements."
]
synth_var1.traits['Artificial Intelligence Algorithms'] = [
    'self.skills_per_levelup_misc_bonus += 1',
    "Whenever you gain skill points, you gain 1 more."
]


# Robots



# Super Mutants