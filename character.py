from race import (
    # Race,
    human, human_var1, human_var2, human_var1_and_var2,
    ghoul, ghoul_var1,
    synth, synth_var1,
    robot, handy,  # protectron, robobrain
    buzz_saw, clippers, robo_drill, gripper, robo_torch
    # add robots and super mutants once implemented
)  # make a main.py and move this over to it
import random



class Attribute:
    def __init__(self, name, abbreviation, score):
        self.name = name
        self.abbreviation = abbreviation
        self.score = score
        self.modifier = 5 - self.score

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
        self.inventory = {}  # format is item_name: [qty, item_class_instance]
        self.caps = 0
        self.ac = 10
        self.dt = 0


        # Attributes
        self.S = Attribute('Strength', 'STR', 5)
        self.P = Attribute('Perception', 'PER', 5)
        self.E = Attribute('Endurance', 'END', 5)
        self.C = Attribute('Charisma', 'CHA', 5)
        self.I = Attribute('Intelligence', 'INT', 5)
        self.A = Attribute('Agility', 'AGI', 5)
        self.L = Attribute('Luck', 'LCK', 5)
        self.unspent_attributes = 3
        self.attributes = [self.S, self.P, self.E, self.C, self.I, self.A, self.L]

        # Skills
        self.barter = Skill('Barter', self.C)
        self.breach = Skill('Breach', [self.P, self.I])
        self.crafting = Skill('Crafting', self.I)
        self.energy_weapons = Skill('Energy Weapons', self.P)
        self.explosives = Skill('Explosives', self.P)
        self.guns = Skill('Guns', self.A)
        self.intimidation = Skill('Intimidation', [self.S, self.C])
        self.medicine = Skill('Medicine', [self.P, self.I])
        self.melee_weapons = Skill('Melee Weapons', self.S)
        self.science = Skill('Science', self.I)
        self.sneak = Skill('Sneak', self.A)
        self.speech = Skill('Speech', self.C)
        self.unarmed = Skill('Unarmed', [self.S, self.A])
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
        self.sp_max = self.A.modifier + 10
        self.sp_current = self.sp_max
        self.hp_max = self.E.modifier + 10
        self.hp_current = self.hp_max
        self.ap_max = self.A.modifier + 10
        self.ap_limit = 15
        self.ap_current = self.ap_max
        self.healing_rate = (self.level + self.E.modifier) // 2
        self.carry_load = self.S.score * 10
        self.passive_sense = self.P.modifier + 12
        self.party_nerve = 0  # derived elsewhere
        self.group_sneak = 0  # derived elsewhere
        self.death_save_mod = max([self.E.modifier, self.L.modifier]) + self.party_nerve
        self.death_saves = {'Success': 0, 'Failure': 0}
        self.targeted_attack_rerolls = max([self.L.modifier, 0])
        self.targeted_attack_rerolls_current = self.targeted_attack_rerolls

        # Penalties and Radiation DC
        self.total_penalty = 0
        self.hunger = 0
        self.thirst = 0
        self.exhaustion = 0
        self.fatigue = 0
        self.rad_level = 0
        self.radiation_dc = 12 - self.E.modifier
        self.irradiated_food = 0
        self.rad_damage = 0

        self.recalculate()

    def calc_luck_bonus(self):
        if self.L.modifier < 0:
            self.luck_bonus = -1
        elif self.L.modifier >= 0:
            self.luck_bonus = self.L.modifier // 2

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
        if self.I.modifier > 0:
            self.skills_per_levelup = 5 + self.skills_per_levelup_misc_bonus
        elif self.I.modifier < 0:
            self.skills_per_levelup = 3 + self.skills_per_levelup_misc_bonus
        else:
            self.skills_per_levelup = 4 + self.skills_per_levelup_misc_bonus

        self.sp_max = self.A.modifier + 10 + (5 + self.A.modifier) * ((self.level - 1) // 2)
        self.hp_max = (self.E.modifier + 10 + (5 + self.E.modifier) * ((self.level - 1) // 2)) - self.rad_damage
        self.ap_max = self.A.modifier + 10
        if self.ap_max > self.ap_limit:
            self.ap_max = self.ap_limit
        self.healing_rate = (self.level + self.E.modifier) // 2
        self.carry_load = self.S.score * 10
        self.passive_sense = self.P.modifier + 12
        self.death_save_mod = max([self.E.modifier, self.L.modifier]) + self.party_nerve
        self.targeted_attack_rerolls = max([self.L.modifier, 0])
        if self.radiation_dc is not None:
            self.radiation_dc = 12 - self.E.modifier

    def adjust_attribute(self, attribute, change):
        attribute.score += change
        if self.L.score >= 10 and not self.luck_10_karma:
            self.karma_caps += 1
            self.luck_10_karma = True
        elif self.L.score < 10 and self.luck_10_karma:
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

    def add_to_inventory(self, item_name, item, qty):
        if item_name in self.inventory:
            self.inventory[item_name][0] += qty
        else:
            self.inventory[item_name] = [qty, item]
