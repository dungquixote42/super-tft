def gilded_endurance(self, allies, enemies, bench):
    pass

def gilded_endurance_passive(self, allies, enemies, bench):
    pass

def holoblade(self, allies, enemies, bench):
    pass


ABILITIES = {}
locals_copy = dict(locals())
for key, value in locals_copy.items():
    if callable(value) and (value.__module__ == __name__):
        ABILITIES[key] = value

if __name__ == "__main__":
    print(ABILITIES)
    print(locals_copy)
    print("goodbye")
