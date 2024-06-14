class Item:
    def __init__(self, name='', id=0, load=0, base_cost=0):
        self.name = name
        self.id = id
        self.load = load
        self.base_cost = base_cost
        self.type = None
        self.properties = None

    def __repr__(self):
        return f'{self.name}'


class Armor(Item):
    def __init__(self):
        # , name, id=0, load=0, base_cost=0, ac=10, dt=0, slots=0, str_req=0
        super().__init__()
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
    def __init__(self):
        # , name, id=0, type=None, subtype=None, load=0, base_cost=0, ap_cost=0, damage_dice='', damage_type='',
        #             damage_dice2=None, damage_type2=None, slots=0, str_req=0
        super().__init__()
        self.subtype = None
        self.main_attribute = None
        self.ap_cost = 0
        self.damage_dice = ''
        self.damage_type = ''
        self.damage_dice2 = None
        self.damage_type2 = None
        self.slots = 0
        self.str_req = 0
        self.crit = {'Target Num': None, 'Multiplier': None, 'Bonus_Damage': None, 'Effect': None}
        self.range = 0
        self.decay = 0
        self.is_equipped = False


class MeleeWeapon(Weapon):
    def __init__(self):
        super().__init__()
        self.type = 'Melee Weapon'
        self.main_attribute = 'Strength'
        self.slots = 1

    def __repr__(self):
        return f'{self.name} ({self.subtype})'


class BladedWeapon(MeleeWeapon):
    def __init__(self):
        super().__init__()
        self.subtype = 'Bladed Weapon'


class BluntWeapon(MeleeWeapon):
    def __init__(self):
        super().__init__()
        self.subtype = 'Blunt Weapon'


class MechanicalWeapon(MeleeWeapon):
    def __init__(self):
        super().__init__()
        self.subtype = 'Mechanical Weapon'


class UnarmedWeapon(MeleeWeapon):
    def __init__(self):
        super().__init__()
        self.subtype = 'Unarmed'
        self.main_attribute = ['Strength', 'Agility']


class Ranged_Weapon(Weapon):
    def __init__(self):
        super().__init__()
        self.type = 'Ranged Weapon'
        self.main_attribute = 'Agility'
        self.ammo = {'Type': None, 'Mag Size': None, 'Current Mag': None, 'Times Reloaded': 0}

    def __repr__(self):
        if self.subtype is None:
            return f'{self.name} ({self.type})'
        else:
            return f'{self.name} ({self.subtype})'