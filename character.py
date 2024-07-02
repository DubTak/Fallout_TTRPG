from race import (
    # Race,
    human, human_var1, human_var2, human_var1_and_var2,
    ghoul, ghoul_var1,
    synth, synth_var1,
    robot, handy,  # protectron, robobrain
    buzz_saw, clippers, robo_drill, gripper, robo_torch
    # add robots and super mutants once implemented
)  # make a main.py and move this over to it
from background import cultist
import random
from copy import deepcopy
from warnings import warn


class Attribute:
    def __init__(self, name, abbreviation, score):
        self.name = name
        self.abbreviation = abbreviation
        self.score = score
        self.modifier = 5 - self.score
        self.max = 10

    def __repr__(self):
        return f'self.name'

    def calc_modifier(self):
        self.modifier = self.score - 5


class Skill:
    def __init__(self, name, attribute):
        self.name = name
        self.attribute = attribute
        self.ranks = 0
        self.total_bonus = 0

    def __repr__(self):
        return f'{self.name}'


class Character:
    def __init__(self):
        # General Info
        self.new_character = True
        self.player = None
        self.name = None
        self.race = None
        self.size = ''
        self.age = 0
        self.background = None
        self.level = 1
        self.xp = 0
        self.karma_caps = 1
        self.luck_10_karma = False

        # Resistances, Vulnerabilities, and Immunities
        self.resistances = set()
        self.vulnerabilities = set()
        self.immunities = set()
        self.condition_immunities = set()

        # Inventory
        self.inventory = {}  # format is item_name: [item_class_instance, quantity]
        self.caps = 0
        self.ac = 10
        self.dt = 0
        self.equipped_armor = None
        self.equipped_weapons = {}
        self.equipped_misc = {}
        self.bag_bonus_load = 0


        # Attributes
        self.strength = Attribute('Strength', 'STR', 5)
        self.perception = Attribute('Perception', 'PER', 5)
        self.endurance = Attribute('Endurance', 'END', 5)
        self.charisma = Attribute('Charisma', 'CHA', 5)
        self.intelligence = Attribute('Intelligence', 'INT', 5)
        self.agility = Attribute('Agility', 'AGI', 5)
        self.luck = Attribute('Luck', 'LCK', 5)
        self.unspent_attributes = 3
        self.attributes = [self.strength, self.perception, self.endurance, self.charisma, self.intelligence, self.agility, self.luck]

        # Skills
        self.barter = Skill('Barter', self.charisma)
        self.breach = Skill('Breach', [self.perception, self.intelligence])
        self.crafting = Skill('Crafting', self.intelligence)
        self.energy_weapons = Skill('Energy Weapons', self.perception)
        self.explosives = Skill('Explosives', self.perception)
        self.guns = Skill('Guns', self.agility)
        self.intimidation = Skill('Intimidation', [self.strength, self.charisma])
        self.medicine = Skill('Medicine', [self.perception, self.intelligence])
        self.melee_weapons = Skill('Melee Weapons', self.strength)
        self.science = Skill('Science', self.intelligence)
        self.sneak = Skill('Sneak', self.agility)
        self.speech = Skill('Speech', self.charisma)
        self.unarmed = Skill('Unarmed', [self.strength, self.agility])
        self.skills_per_levelup = 0
        self.skills_per_levelup_misc_bonus = 0
        self.unspent_skills = 0
        self.skills = [
            self.barter, self.breach, self.crafting, self.energy_weapons,
            self.explosives, self.guns, self.intimidation, self.medicine,
            self.melee_weapons, self.science, self.sneak, self.speech, self.unarmed,
        ]

        # Perks and Traits
        self.unspent_perks = 1
        self.perks = []
        self.traits = []

        # Derived Stats
        self.luck_bonus = 0
        self.sp_max = self.agility.modifier + 10
        self.sp_current = self.sp_max
        self.sp_misc_bonus = 0
        self.hp_max = self.endurance.modifier + 10
        self.hp_current = self.hp_max
        self.hp_misc_bonus = 0
        self.ap_max = self.agility.modifier + 10
        self.ap_limit = 15
        self.ap_current = self.ap_max
        self.healing_rate = (self.level + self.endurance.modifier) // 2
        self.carry_load = self.strength.score * 10
        self.passive_sense = self.perception.modifier + 12
        self.party_nerve = 0  # derived elsewhere
        self.group_sneak = 0  # derived elsewhere
        self.death_save_mod = max([self.endurance.modifier, self.luck.modifier]) + self.party_nerve
        self.death_saves = {'Success': 0, 'Failure': 0}
        self.targeted_attack_rerolls = max([self.luck.modifier, 0])
        self.targeted_attack_rerolls_current = self.targeted_attack_rerolls
        # chem limit is minimum 1, maximum 4
        self.chem_limit = min([4, max([1, (self.endurance.modifier // 2) + 2])])

        # Penalties and Radiation DC
        self.total_penalty = 0
        self.hunger = 0
        self.thirst = 0
        self.exhaustion = 0
        self.fatigue = 0
        self.rad_level = 0
        self.radiation_dc = 12 - self.endurance.modifier
        self.irradiated_food = 0
        self.rad_damage = 0

        self.recalculate()

    def calc_luck_bonus(self):
        if self.luck.modifier < 0:
            self.luck_bonus = -1
        elif self.luck.modifier >= 0:
            self.luck_bonus = self.luck.modifier // 2

    def calc_total_penalty(self):
        self.total_penalty = 0 - self.exhaustion - self.fatigue
        if self.hunger is not None:
            self.total_penalty -= self.hunger
        if self.thirst is not None:
            self.total_penalty -= self.thirst
        if self.rad_level is not None:
            self.total_penalty -= self.rad_level

    def calc_skill_total(self, skill):
        if isinstance(skill.attribute, list):
            skill.total_bonus = [
                skill.attribute[0].modifier + skill.ranks + self.luck_bonus + self.total_penalty,
                skill.attribute[1].modifier + skill.ranks + self.luck_bonus + self.total_penalty,
            ]
        else:
            skill.total_bonus = skill.attribute.modifier + skill.ranks + self.luck_bonus + self.total_penalty

    def recalculate(self):
        self.calc_total_penalty()
        for attribute in self.attributes:
            attribute.calc_modifier()

        self.calc_luck_bonus()

        for skill in self.skills:
            self.calc_skill_total(skill)

        if self.intelligence.modifier > 0:
            self.skills_per_levelup = 5 + self.skills_per_levelup_misc_bonus
        elif self.intelligence.modifier < 0:
            self.skills_per_levelup = 3 + self.skills_per_levelup_misc_bonus
        else:
            self.skills_per_levelup = 4 + self.skills_per_levelup_misc_bonus

        self.sp_max = self.agility.modifier + 10 + (5 + self.agility.modifier) * ((self.level - 1) // 2)
        self.hp_max = (self.endurance.modifier + 10 + (5 + self.endurance.modifier) *
                       ((self.level - 1) // 2)) - self.rad_damage
        # Max AP is USUALLY 15, and this check is to make sure we're at or under Max
        self.ap_max = min([self.agility.modifier + 10, self.ap_limit])
        self.healing_rate = (self.level + self.endurance.modifier) // 2
        self.carry_load = (self.strength.score * 10) + self.bag_bonus_load
        self.passive_sense = self.perception.modifier + 12
        self.death_save_mod = max([self.endurance.modifier, self.luck.modifier]) + self.party_nerve
        self.targeted_attack_rerolls = max([self.luck.modifier, 0])
        if self.radiation_dc is not None:
            self.radiation_dc = 12 - self.endurance.modifier
        self.chem_limit = min([4, max([1, (self.endurance.modifier // 2) + 2])])

        if self.equipped_armor is not None:
            self.ac = min([self.equipped_armor.ac - (self.equipped_armor.decay // 2), 10])
            self.dt = min([self.equipped_armor.dt - (self.equipped_armor.decay // 2), 0])
        else:
            self.ac, self.dt = 10, 0
        for weapon in self.equipped_weapons:
            for skill in self.skills:
                if self.equipped_weapons[weapon][0].type in skill.name:
                    if isinstance(skill.total_bonus, list):
                        self.equipped_weapons[weapon][1] = max(skill.total_bonus)
                    else:
                        self.equipped_weapons[weapon][1] = skill.total_bonus

    def adjust_attribute(self, attribute, change):
        attribute.score += change
        if self.luck.score >= 10 and not self.luck_10_karma:
            self.karma_caps += 1
            self.luck_10_karma = True
        elif self.luck.score < 10 and self.luck_10_karma:
            self.karma_caps -= 1
            self.luck_10_karma = False
        self.recalculate()

    def adjust_skill(self, skill, change):
        skill.ranks += change
        self.recalculate()

    def apply_race(self, race):
        self.race = race

        for k, v in race.traits.items():
            if k == 'Age':  # need to figure out where to put the age desc
                continue
            if k == 'Size':  # need to make a toggle to choose which size from the list
                self.size = v
            else:
                if v[0] != 'UNIMPLEMENTED':
                    exec(v[0])

        if race.extra_traits != {}:
            key_list = [key for key in race.extra_traits.keys()]
            choice = random.choice(key_list)  # VERY TEMPORARY FIX: IMPLEMENT CHOOSING ASAP
            exec(race.extra_traits[choice])

        self.recalculate()
        # figure out a way to remove race

    def add_to_inventory(self, item, qty):
        if item.name in self.inventory:
            if item == self.inventory[item.name]:
                self.inventory[item.name][1] += qty
            else:
                item_suffix = 1
                name_available = False
                while not name_available:
                    if item.name.endswith(f'({item_suffix})'):
                        item_suffix += 1
                    else:
                        self.inventory[f'{item.name}({item_suffix})'] = [item, qty]
                        name_available = True
        else:
            self.inventory[item.name] = [item, qty]

    def equip_item(self, item):
        if 'Armor' in item.type:
            if self.equipped_armor is not None:
                self.equipped_armor.load *= 2  # equipped armor has half load (reversing that before return to inv)
                self.add_to_inventory(self.equipped_armor, 1)
            self.equipped_armor = item
            self.equipped_armor.load /= 2  # equipped armor has half load
        elif 'Weapon' in item.type:
            for skill in self.skills:
                if item.type in skill.name:  # using this syntax because some of the skill names are pluralized
                    to_hit = skill.total_bonus
                    self.equipped_weapons[item.name] = [item, to_hit]
        else:
            if item.subtype is not None and 'Bag' in item.subtype:
                self.bag_bonus_load += item.load_bonus
            self.equipped_misc[item.name] = [item]

        self.recalculate()

    def apply_upgrade_to_item(self, item_name, upgrade):
        if item_name in self.inventory:
            if self.inventory[item_name][1] > 1:
                self.inventory[item_name][1] -= 1
                new_item = deepcopy(self.inventory[item_name][0])
# I'm trying to pop out one instance of the item, add ' (upgraded)' if it doesn't have it, apply upgrades
    # AKA [properties], add upgraded item to inv, and delete the old entry if qty == 0

    def apply_trait(self, trait, wild_wasteland=None):
        if not trait.check_requirements(self):
            warn('Trait requirements not met')
        else:
            if wild_wasteland is not None:  # might wanna retool this so we don't have the ww check in 2 places
                trait.wild_wasteland = wild_wasteland
            trait.apply_wild_wasteland()
            exec(trait.effect)
            self.traits.append(trait)
            self.recalculate()

    def apply_perk(self, perk):
        if not perk.check_requirements(self):
            warn('Perk requirements not met')
        else:
            exec(perk.effect)
            self.perks.append(perk)

    def apply_background(self, background, wild_trait=False):
        self.background = deepcopy(background)

        for bg_skill in self.background.skills:
            for skill in self.skills:
                if bg_skill == skill.name:
                    skill.ranks += 2

        if wild_trait:
            self.apply_trait(self.background.trait, wild_wasteland=True)
        else:
            self.apply_trait(self.background.trait)

        self.background.choose_starting_gear(self.race.name)
        for item in self.background.starting_gear:
            if isinstance(item, str):
                exec(item)
            else:
                self.add_to_inventory(item[0], item[1])
                if len(item) == 3:
                    item_properties = item[2]
                    if item_properties[0] == 'UPGRADES':
                        item_properties = item_properties[1:]
                        for property in item_properties:
                            item[0].slots_current -= 1
                            self.inventory[item[0].name][0].properties.append(property)
                    else:
                        self.inventory[item[0].name][0].properties.extend(item_properties)
