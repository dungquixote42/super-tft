import numpy as np
from yaml import safe_load_all

from abilities import ABILITIES
from Champion import Champion

LVL_3_XP = 2
LVL_4_XP = 6
LVL_5_XP = 10
LVL_6_XP = 20
LVL_7_XP = 36
LVL_8_XP = 48
LVL_9_XP = 72
LVL_10_XP = 84  # maximum


class Player:
    def __init__(self, lvl_lut):
        self.lvl_lut = lvl_lut

        # default
        self.hp = 100
        self.gold = 0
        self.lvl = 1
        self.xp = 0
        self.unit_cap = 1

    def buy_xp(self):
        if (self.gold < 4) or (self.xp >= LVL_10_XP):
            return
        self.gold -= 4
        self.xp += 4
        self.lvl = self.lvl_lut[self.xp]

    def process_end_of_round(self):
        if self.xp >= LVL_10_XP:
            return
        self.xp += 2
        self.lvl = self.lvl_lut[self.xp]


class Store:
    def __init__(self):
        pass


class World:
    def __init__(self):
        roster = {}
        with open("champion_data.yaml", "r") as file:
            champion_data = safe_load_all(file)
            for _, cdat in enumerate(champion_data):
                ability = ABILITIES[cdat["ability"]]

                # star 0
                champion = Champion(cdat, 0, ability)
                champion.hp_max *= 0.7
                champion.ad *= 0.7
                roster[cdat["name"] + "_0"] = champion

                # star 1
                champion = Champion(cdat, 1, ability)
                roster[cdat["name"] + "_1"] = champion

                # star 2
                champion = Champion(cdat, 2, ability)
                champion.hp_max *= 1.5
                champion.ad *= 1.8
                roster[cdat["name"] + "_2"] = champion

                # star 3
                champion = Champion(cdat, 3, ability)
                champion.hp_max *= 2.25
                champion.ad *= 3.24
                roster[cdat["name"] + "_3"] = champion

                # star 4
                champion = Champion(cdat, 4, ability)
                champion.hp_max *= 3.375
                champion.ad *= 5.832
                roster[cdat["name"] + "_4"] = champion

        # level lookup table, xp as index
        lvl_lut = np.ones(LVL_10_XP + 1, dtype=np.uint8)
        lvl_lut[:] += 1
        lvl_lut[LVL_3_XP:] += 1
        lvl_lut[LVL_4_XP:] += 1
        lvl_lut[LVL_5_XP:] += 1
        lvl_lut[LVL_6_XP:] += 1
        lvl_lut[LVL_7_XP:] += 1
        lvl_lut[LVL_8_XP:] += 1
        lvl_lut[LVL_9_XP:] += 1
        lvl_lut[LVL_10_XP] += 1

        self.player = Player(np.copy(lvl_lut))  # me
        self.player1 = Player(np.copy(lvl_lut))
        self.player2 = Player(np.copy(lvl_lut))
        self.player3 = Player(np.copy(lvl_lut))
        self.player4 = Player(np.copy(lvl_lut))
        self.player5 = Player(np.copy(lvl_lut))
        self.player6 = Player(np.copy(lvl_lut))
        self.player7 = Player(np.copy(lvl_lut))


if __name__ == "__main__":
    world = World()
    # print(world.player.lvl_lut)

    # print(roster["alistar_1"].ability())

    print("goodbye")
