class Character:
    name: str
    character_class: str
    level: int
    xp: int

    defense: float
    dexterity: float
    hp: float
    strength: float
    wisdom: float

    def __init__(self, name: str, character_class: str, level: int, xp: int, dexterity: float, defense: float, hp: float, strength: float, wisdom: float):
        self.name = name
        self.level = level
        self.xp = xp
        self.character_class = character_class
        self.strength = strength
        self.dexterity = dexterity
        self.defense = defense
        self.hp = hp
        self.wisdom = wisdom

    def add_to_attribute(self, points: float, attribute: float):
        if hasattr(self, attribute):
            setattr(self, attribute, getattr(self, attribute) + points)
        
    def get_defense(self):
        return self.defense
        
    def get_dexterity(self):
        return self.dexterity

    def get_name(self):
        return self.name
        
    def get_hp(self):
        return self.hp
        
    def get_class(self):
        return self.character_class
        
    def get_level(self):
        return self.level
        
    def get_strength(self):
        return self.strength
        
    def get_wisdom(self):
        return self.wisdom
        
    def get_xp(self):
        return self.xp