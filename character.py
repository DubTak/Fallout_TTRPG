class Attribute:
    def __init__(self, name, abbreviation, score):
        self.name = name
        self.abbreviation = abbreviation
        self.score = score
        self.modifier = 5 - self.score

    def __repr__(self):
        return str(
            {'name': self.name, 'abbreviation': self.abbreviation, 'score': self.score, 'modifier': self.modifier}
        )

    def calc_modifier(self):
        self.modifier = self.score - 5

class Skill:
    def __init__(self, name, attribute, ranks=0, total_bonus=0):
        self.name = name
        self.attribute = attribute
        self.ranks = ranks
        self.total_bonus = total_bonus

    def __repr__(self):
        return str(
            {'name': self.name, 'attribute': self.attribute, 'ranks': self.ranks, 'total_bonus': self.total_bonus}
        )


class Character:
    def __init__(self):
        # General Info
        self.new_character = True
        self.player = None
        self.name = None
        self.race = None
        self.background = None
        self.level = 1
        self.xp = 0
        self.karma_caps = 1
        self.luck_10_karma = False

        # Inventory and Equipped items
        self.inventory = {}
        self.caps = 0
        self.ac = 10
        self.dt = 0
        self.equipped_weapon = None
        self.equipped_armor = None
        self.worn_items = []


        # Attributes
        self.S = Attribute('Strength', 'S', 5)
        self.P = Attribute('Perception', 'P', 5)
        self.E = Attribute('Endurance', 'E', 5)
        self.C = Attribute('Charisma', 'C', 5)
        self.I = Attribute('Intelligence', 'I', 5)
        self.A = Attribute('Agility', 'A', 5)
        self.L = Attribute('Luck', 'L', 5)
        self.unspent_perks = 3
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
        self.skills_per_level_bonus = 0
        self.skills_per_level_misc_bonus = 0
        self.unspent_skills = 0
        self.skills = [
            self.barter, self.breach, self.crafting, self.energy_weapons,
            self.explosives, self.guns, self.intimidation, self.medicine,
            self.melee_weapons, self.science, self.sneak, self.speech, self.unarmed,
        ]

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

        self.refresh()

    def calc_luck_bonus(self):
        if self.L.modifier < 0:
            self.luck_bonus = -1
        elif self.L.modifier > 0:
            self.luck_bonus = self.L.modifier // 2
        else:
            self.luck_bonus = 0

    def calc_total_penalty(self):
        self.total_penalty = (
            0 - self.hunger - self.thirst - self.exhaustion - self.fatigue - self.rad_level
        )

    def calc_skill_total(self, skill):
        if isinstance(skill.attribute, list):
            skill.total_bonus = [
                skill.attribute[0].modifier + skill.ranks + self.luck_bonus + self.total_penalty,
                skill.attribute[1].modifier + skill.ranks + self.luck_bonus + self.total_penalty,
            ]
        else:
            skill.total_bonus = skill.attribute.modifier + skill.ranks + self.luck_bonus + self.total_penalty

    def refresh(self):
        self.calc_total_penalty()
        for attribute in self.attributes:
            attribute.calc_modifier()
        self.calc_luck_bonus()
        for skill in self.skills:
            self.calc_skill_total(skill)
        if self.I.modifier > 0:
            self.skills_per_level_bonus = 1 + self.skills_per_level_misc_bonus
        elif self.I.modifier < 0:
            self.skills_per_level_bonus = -1 + self.skills_per_level_misc_bonus
        else:
            self.skills_per_level_bonus = 0 + self.skills_per_level_misc_bonus

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

    def adjust_attribute(self, attribute, change):
        attribute.score += change
        if self.L.score >= 10 and not self.luck_10_karma:
            self.karma_caps += 1
            self.luck_10_karma = True
        elif self.L.score < 10 and self.luck_10_karma:
            self.karma_caps -= 1
            self.luck_10_karma = False
        self.refresh()

    def adjust_skill(self, skill, change):
        if change > 0 and change > self.unspent_skills:
            return
        skill.ranks += change
        self.refresh()




# bob = Character()
# bob.unspent_perks = 20
# bob.adjust_attribute(bob.L, 5)
# print(f'current luck: {bob.L.score}  current karma caps: {bob.karma_caps}')
# bob.adjust_attribute(bob.L, -1)
# print(f'current luck: {bob.L.score}  current karma caps: {bob.karma_caps}')
# bob.adjust_attribute(bob.L, 1)
# print(f'current luck: {bob.L.score}  current karma caps: {bob.karma_caps}')

