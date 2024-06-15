from copy import deepcopy
from item import Gear, BladedWeapon, MechanicalWeapon, RangedWeapon

class Race:
    def __init__(self, name, type, variant1=False, variant2=False, variant3=False):
        self.name = name
        self.type = type
        self.traits = {'Age': '', 'Size': []}
        self.extra_traits = {}
        self.variant1 = variant1
        self.variant2 = variant2
        self.variant3 = variant3
        self.extra_description = None

    def __repr__(self):
        if self.type == 'Robot':
            return f'{self.name} {self.type}'
        return f'{self.name}'


# Human
human = Race('Human', 'Human')
human.traits['Age'] = ("Humans reach adulthood in their late teens and live less than a century. "
                       "Though, those who live this long are far and few between in the wasteland.")
human.traits['Size'] = [
    ['Medium', 'Small'],
    "Humans vary widely in height and build. Your size is Medium or Small.",
]

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
ghoul.traits['Size'] = [
    ['Medium', 'Small'],
    "Ghouls vary widely in height and build. Your size is Medium or Small.",
]
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

# Trait shared by synths and robots
inorganic_body_exec = '''
self.immunities.update(["poison", "radiation"])
self.condition_immunities.add("suffocating")
self.rad_level, self.irradiated_food, self.hunger, self.thirst, self.radiation_dc = None, None, None, None, None
'''
inorganic_body_desc = ("You are immune to radiation and poison. You gain no effects from Chems, Drinks or Food. "
                       "Additionally you have no need to breathe, sleep, eat, or drink.")
synth_and_robot_rest = """
- You do not require sleep.
- 1 hour of rest restores your stamina points to full.
- 2 hours of rest restores a number of hit points equal to half your INT or PER score + your level 
  and removes one level of exhaustion.
"""

# Gen-2 Synth
synth = Race('Gen-2 Synth', 'Synth')
synth.traits['Age'] = ("Gen-2 Synths can live hundreds of years before their inorganic materials begin to "
                       "corrode and their programming deteriorates. However, a Synth who keeps consistent "
                       "repairs is nigh immortal.")
synth.traits['Size'] = [
    ['Medium', 'Small'],
    "Gen-2 Synths vary widely in height and build. Your size is Medium or Small.",
]
synth.traits['Inorganic Body'] = [
    inorganic_body_exec,
    inorganic_body_desc,
    # 'UNIMPLEMENTED'  # I need to add food/drink/etc effects and then add ability to reduce those effects
]
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
robot = Race('Robot', 'Robot')
robot.traits['Age'] = ("Robots can live hundreds of years before their inorganic materials begin to corrode and "
                       "their programming deteriorates. However, a Robot who keeps consistent repairs "
                       "is nigh immortal.")
robot.traits['Size'] = [
    'Medium',
    "While there are many types of Robots, most were built to maintain a similar size to humans. "
    "Handy’s are about 2 and a half feet to 3 and a half feet in height but hover 2 to 3 feet off the ground. "
    "Protectrons rarely were built taller than 5 feet. And Robobrains typically sit around 5 and a half feet. "
    "Regardless, your size is medium.",
]
robot.traits['Inorganic Body'] = [
    inorganic_body_exec,
    inorganic_body_desc,
    # 'UNIMPLEMENTED'  # I need to add food/drink/etc effects and then add ability to reduce those effects
]
robot.traits['Severed Limbs'] = [
    'UNIMPLEMENTED',  # there is very little chance of automating this, so we'll just have the text desc somewhere
    "Luckily for most robots, reattaching limbs is commonplace when they break or fall off. "
    "If any of your limbs are severed, you do not go into shock and they can be reattached with 3 steel "
    "and 1 circuitry junk item. When you or a creature reattaches a limb, it takes a number of minutes equal "
    "to 10 - their or your crafting skill bonus. If the amount of time is reduced to 0, "
    "it takes 6 AP to reattach the limb instead.",
]
robot.traits['Armor and Weapons'] = [
    'UNIMPLEMENTED',  # ditto from Severed Limbs, unless I can flag 'no power armor'?
    "You can use armor and weapons just as any other race would. If your robot sub-type grants you a weapon, "
    "you can upgrade and modify this weapon just like any other weapon. However, you cannot use power armor.",
]

handy = deepcopy(robot)
handy.name = 'Handy'
handy.variant1 = True
handy.traits['Limbs and Targeted Attacks'] = [
    'UNIMPLEMENTED', # need to implement limb damage, and even then this will be mostly desc
    "Handys have a less human shape to them than other robots, floating off the ground with three appendages "
    "and three eyes attached to a large round core. You have three arms, three eyes, and can have up to three "
    "hands if you choose to have three Grippers in the Incredible Multi-Talented Appliance section below. "
    "You do not have a head, groin, or legs that can be targeted by targeted attacks or severed. "
    "Instead; targeted attacks to your eyes cost 2 less AP and creatures can target your jet engine. "
    "The jet engine functions exactly the same as a targeted attack to the legs, except the attack costs 2 more AP. "
    "If your jet engine is severed, you fall prone and cannot move until it is reattached.",
]
handy.traits['Fuel'] = [
    'UNIMPLEMENTED',  # this feels like another desc only trait
    "You require fuel to continue to operate. Every week, 7 days, or 168 hours; you can spend 6 AP to fill "
    "your tank with a gallon of fuel or six oil junk items which are consumed upon use. "
    "If you fail to consume a gallon of fuel after the week, you must succeed a DC 12 Endurance check for each "
    "hour past 168. For each successful check, the DC increases by 2. On a fail, you become unconscious until "
    "another creature fills your tank with fuel. Alternatively, you can load a fusion core into your chassis. "
    "If you do, you can operate for 30 days without requiring fuel."
]
handy.traits['Jet Engine'] = [
    'UNIMPLEMENTED',  # are robots gonna be mostly desc only? maybe...
    "You hover a few feet off the ground while active and moving. You don't trigger any floor based traps or "
    "activated effects. However, if you are knocked prone, become stunned, or fall unconscious; "
    "you fall to the ground."
]
handy.traits['Incredible Multi-Talented Appliance!'] = [
    'UNIMPLEMENTED',  # need to implement a choosing function for the multi-talents
    "Handy’s are built with three special tools that are attached and built into three of their arms. "
    "These tools and weapons can be modified like any other weapon, only require one hand to use, "
    "and do not cost AP to equip or stow. Additionally, they cannot be detached from you unless the arm that "
    "the tool or weapon is attached to is severed. "
    "Choose one tool or weapon from the following list that is attached to your arm."
]

buzz_saw = BladedWeapon('Buzz Saw')
buzz_saw.description = "A mechanical saw housed in a metal frame used to cut wood, food, bodies, or debris."
buzz_saw.ap_cost = 5
buzz_saw.damage_dice = '1d8'
buzz_saw.damage_type = 'slashing'
buzz_saw.crit.update({'Multiplier': 2, 'Effect': 'applies bleeding'})
buzz_saw.properties = ['Cleave', 'Durable']
handy.extra_traits['Buzz Saw'] = 'self.add_to_inventory("Buzz Saw (attached)", buzz_saw)'

clippers = BladedWeapon('Clippers')
clippers.description = "A large, sharp set of clippers for wiring, gardening, or opening boxes."
clippers.ap_cost = 3
clippers.damage_dice = '1d4'
clippers.damage_type = 'piercing'
clippers.crit.update({'Target Num': 19, 'Bonus_Damage': '1d4'})
clippers.properties = ['Dismember', 'Durable']
handy.extra_traits['Clippers'] = 'self.add_to_inventory("Clippers (attached)", clippers)'

robo_drill = MechanicalWeapon('Drill')
robo_drill.description = "This drill has interchanging bits used for screws, nuts, bolts, and pilot holes"
robo_drill.ap_cost = 6
robo_drill.damage_dice = '1d8'
robo_drill.damage_type = 'slashing'
robo_drill.crit.update({'Bonus_Damage': '2d8'})
robo_drill.properties = ['Durable', 'Mangle']
handy.extra_traits['Drill'] = 'self.add_to_inventory("Drill (attached)", robo_drill)'

gripper = Gear('Gripper')
gripper.description = ("The Gripper is two finger-like appendages that can grab, twist, operate, use weapons, "
                       "and hold items. Operating at similar efficiency to a human hand. "
                       "If you do not have at least two of these tools, you effectively only have one hand. (This"
                       "affects some weapons which have the two handed, unwieldy, or kickback special properties.")
handy.extra_traits['Gripper'] = 'self.add_to_inventory("Gripper (attached)", gripper)'

robo_torch = RangedWeapon('Mr. Handy Torch')
robo_torch.description = ("This kitchen tool emits a flame with an adjustable nozzle for cooking, flambéing, "
                          "taking care of pesky bug nests, or lighting candles.")
robo_torch.ap_cost = 5
robo_torch.damage_dice = '1d10'
robo_torch.damage_type = 'fire'
robo_torch.range = '10 ft. line'
robo_torch.properties = ['Area of Effect', 'Durable', 'Incendiary']
robo_torch.ammo.update({'Type': 'fuel', 'Mag Size': 5, 'Current Mag': 5})
handy.extra_traits['Mr. Handy Torch'] = 'self.add_to_inventory("Mr. Handy Torch (attached)", robo_torch)'


# Super Mutants
