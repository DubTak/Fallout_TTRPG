class Item:
    def __init__(self, name):
        self.name = name
        self.id =0
        self.load = 0
        self.base_cost = 0
        self.type = None
        self.properties = None
        self.description = None

    def __repr__(self):
        return f'{self.name}'


class Armor(Item):
    def __init__(self, name):
        super().__init__(name)
        self.type = "Armor"
        self.ac = 10
        self.dt = 0
        self.slots = 0
        self.str_req = 0
        self.decay = 0
        self.is_equipped = False

    def __repr__(self):
        return f'{self.name} {self.type}'


class Weapon(Item):
    def __init__(self, name):
        # , name, id=0, type=None, subtype=None, load=0, base_cost=0, ap_cost=0, damage_dice='', damage_type='',
        #             damage_dice2=None, damage_type2=None, slots=0, str_req=0
        super().__init__(name)
        self.subtype = None
        self.main_attribute = None
        self.ap_cost = 0
        self.damage_dice = ''
        self.damage_type = ''
        self.damage_dice2 = None
        self.damage_type2 = None
        self.slots = 0
        self.str_req = 0
        self.crit = {'Target Num': 20, 'Multiplier': None, 'Bonus_Damage': None, 'Effect': None}
        self.range = 0
        self.decay = 0
        self.is_equipped = False


class MeleeWeapon(Weapon):
    def __init__(self, name):
        super().__init__(name)
        self.type = 'Melee Weapon'
        self.main_attribute = 'Strength'
        self.slots = 1

    def __repr__(self):
        return f'{self.name} ({self.subtype})'


class BladedWeapon(MeleeWeapon):
    def __init__(self, name):
        super().__init__(name)
        self.subtype = 'Bladed Weapon'


class BluntWeapon(MeleeWeapon):
    def __init__(self, name):
        super().__init__(name)
        self.subtype = 'Blunt Weapon'


class MechanicalWeapon(MeleeWeapon):
    def __init__(self, name):
        super().__init__(name)
        self.subtype = 'Mechanical Weapon'


class UnarmedWeapon(MeleeWeapon):
    def __init__(self, name):
        super().__init__(name)
        self.subtype = 'Unarmed'
        self.main_attribute = ['Strength', 'Agility']


class RangedWeapon(Weapon):
    def __init__(self, name):
        super().__init__(name)
        self.type = 'Ranged Weapon'
        self.main_attribute = 'Agility'
        self.ammo = {'Type': None, 'Mag Size': None, 'Current Mag': None, 'Times Reloaded': None}

class Handgun(RangedWeapon):
    def __init__(self, name):
        super().__init__(name)
        self.subtype = 'Handgun'


class SubmachineGun(RangedWeapon):
    def __init__(self, name):
        super().__init__(name)
        self.subtype = 'Submachine Gun'


class Rifle(RangedWeapon):
    def __init__(self, name):
        super().__init__(name)
        self.subtype = 'Rifle'


class Shotgun(RangedWeapon):
    def __init__(self, name):
        super().__init__(name)
        self.subtype = 'Shotgun'


class BigGun(RangedWeapon):
    def __init__(self, name):
        super().__init__(name)
        self.subtype = 'Big Gun'


class EnergyWeapon(RangedWeapon):
    def __init__(self, name):
        super().__init__(name)
        self.subtype = 'Energy Weapon'
        self.main_attribute = 'Perception'


class Gear(Item):
    def __init__(self, name):
        super().__init__(name)
        self.type = 'Gear'