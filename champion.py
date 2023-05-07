MODIFIABLE_STATS = ["ad"]

class Champion:
    def __init__(self, name, stats):
        self.name = name
        stats = stats[name]
        self.buy = stats["buy"]
        self.sell = stats["sell"]
        self.traits = stats["traits"]

        self.hp = stats["hp"]
        self.mp = stats["mp"]
        self.range = stats["range"]
        self.att_speed = stats["att_speed"]
        self.armor = stats["armor"]
        self.mr = stats["mr"]

        self.active = None
        if "active" in stats:
            self.active = stats["active"]

        self.passive = None
        if "passive" in stats:
            self.passive = stats["passive"]

        mod_stats = {}
        mods = {}
        for s in MODIFIABLE_STATS:
            mod_stats[s] = stats[s]
            mods[s] = 0.0
        self.mod_stats = mod_stats
        self.mods = mods

        self.star = None

    def use_active(self):
        active = self.active
        if active is not None:
            if self.mp >= active["mp_cost"]:
                if 0 in active["target"]:
                    self.mods[active["buff"]] += active["ratio"][self.star]

    def modify(self):
        for stat in self.mods:
            self.mod_stats[stat] *= self.mods[stat]
