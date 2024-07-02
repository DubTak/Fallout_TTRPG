from item import WEAPONS, ARMOR  # , AMMO, CONSUMABLES, GEAR


class Item:
    def __init__(self, name):
        self.name = name
        self.id = 0
        self.load = 0
        self.base_cost = 0
        self.type = None
        self.subtype = None
        self.properties = []
        self.description = None

    # I should probably make this the __str__() and make __repr__() more descriptive, but that's a tomorrow problem
    def __repr__(self):
        return f'{self.__class__.__name__}(\'{self.name}\')'

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Armor(Item):
    def __init__(self, name):
        super().__init__(name)
        self.type = 'Armor'
        if ARMOR['Name'].isin([self.name]).any():
            entry = ARMOR[ARMOR.Name == self.name]
            self.ac = entry['AC'].values[0]
            self.dt = entry['DT'].values[0]
            self.slots_max = entry['Slots'].values[0]
            self.str_req = entry['STR Req'].values[0]
        else:
            self.ac = 10
            self.dt = 0
            self.slots_max = 0
            self.str_req = 0

        self.slots_current = self.slots_max
        self.decay = 0
        self.is_equipped = False


class Weapon(Item):
    def __init__(self, name):
        # , name, id=0, type=None, subtype=None, load=0, base_cost=0, ap_cost=0, damage_dice='', damage_type='',
        #             damage_dice2=None, damage_type2=None, slots=0, str_req=0
        super().__init__(name)
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


class Bag(Gear):
    def __init__(self, name):
        super().__init__(name)
        self.subtype = 'Bag'
        self.load_bonus = 0


class Ammo(Item):
    def __init__(self, name, special=False):
        super().__init__(name)
        if special:
            pass  # I, obviously, need to make the AMMO DataFrame for this to work
            # entry = AMMO.loc[AMMO['name'] == name]
            # self.name = name + ' ' + entry['Sub Type]'
        self.type = 'Ammo'


class Consumable(Item):
    def __init__(self, name):
        super().__init__(name)
        self.type = 'Consumable'


class Healing(Consumable):
    def __init__(self, name):
        super().__init__(name)
        self.subtype = 'Healing'


class Food(Consumable):
    def __init__(self, name):
        super().__init__(name)
        self.subtype = 'Food'


class Drink(Consumable):
    def __init__(self, name):
        super().__init__(name)
        self.subtype = 'Drink'


class Chem(Consumable):
    def __init__(self, name):
        super().__init__(name)
        self.subtype = 'Chem'


class Overclock(Consumable):
    def __init__(self, name):
        super().__init__(name)
        self.subtype = 'Overclock Program'
