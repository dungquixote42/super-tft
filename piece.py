from champion import Champion


class Piece(Champion):
    def __init__(self, name, champions):
        super().__init__(champions[name])
        self.name = name
        self.star = None
        self.modifiers = None

    def use_active(self):
        active = self.active
        if active is not None:
            if self.mp >= active["mp_cost"]:
                if 0 in active["target"]:
                    self.modifiers[active["buff"]] += active["ratio"][self.star]

    def modify(self):
        for stat in self.modifiers:
            self.volatile[stat] *= self.modifiers[stat]
