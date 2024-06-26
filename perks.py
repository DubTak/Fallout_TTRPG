class Perk:
    def __init__(self, name):
        self.name = name
        self.effect = ''
        self.description = ''
        self.requirements = []

    def __str__(self):
        return self.name

    def check_requirements(self, character):
        for attribute in character.attributes:
            if self.requirements[0] == attribute.abbreviation:
                if attribute.score >= self.requirements[1]:
                    return True
        if self.requirements[0] == character.race.type:
            return True
        elif isinstance(character.race.type, list) and self.requirements[0] in character.race.type:
            return True
        return False


class Trait(Perk):
    def __init__(self, name, wild_wasteland=False):
        super().__init__(name)
        self.effect = []
        self.description = []
        self.wild_wasteland = wild_wasteland

    def apply_wild_wasteland(self):
        if self.wild_wasteland:
            self.effect = self.effect[1]
            self.description = self.description[1]
        else:
            self.effect = self.effect[0]
            self.description = self.description[0]


