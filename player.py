from copy import deepcopy


class Player:
    def __init__(self):
        self.hp = 100
        self.gold = 0
        self.champions = []

    def __add__(self, champion):
        if champion.star == None:
            champion.star = 1
        self.champions.append(champion)
        for star in range(1, 3):
            i_list = []
            for i in range(0, len(self.champions)):
                c = self.champions[i]
                if c.name == champion.name and c.star == star:
                    i_list.append(i)
            if len(i_list) > 2:
                self - i_list.pop(-1)
                self - i_list.pop(-1)
                self - i_list.pop(-1)
                new_champion = deepcopy(champion)
                new_champion.star = star + 1
                self.champions.append(new_champion)

    def __sub__(self, i):
        self.champions.pop(i)

    def print_champions(self):
        for c in self.champions:
            print(c.name, end="")
            print(c.star, end=" ")
        print("")
