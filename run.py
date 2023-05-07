import yaml
from yaml import CLoader as Loader, CDumper as Dumper


from board import Board
from champion import Champion
from player import Player
# from piece import Piece


if __name__ == "__main__":
    file = open("champion_data.yaml", "r")
    champion_data = yaml.load(file, Loader=Loader)
    file.close()

    p0 = Player()
    p1 = Player()

    p0 + Champion("ashe", champion_data)
    p1 + Champion("ashe", champion_data)

    # champion_data1 = {}
    # for name in champions:
    #     roster[name] = Champion(champions[name])
    
    # print(type(roster["ashe"].cost))
    # print(roster)

    # champions = []
    # champions.append(Champion("ashe", champion_data))
    
    for i in range(0, 9):
        p0 + Champion("ashe", champion_data)
        p0.print_champions()