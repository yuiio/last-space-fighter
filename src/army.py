from vector import Vector as v2

from constants import WIDTH, HEIGHT
from enemies import En1, En2, En3, Boss, XRotator, Sider, Pendulum, TowerGun, BigBoss

# positions

L = WIDTH * 2 / 10  # Left
C = WIDTH / 2  # Center (width)
R = WIDTH * 8 / 10  # Right
T = HEIGHT * 1 / 6  # Top
M = HEIGHT / 2  # Middle (height)
B = HEIGHT * 5 / 6  # Bottom


troops = (
    (  # 0 : Green on left
        {"enemy": En1, "pos": v2(L, 0), "delay": 1.5},
        {"enemy": En1, "pos": v2(L, 0), "delay": 0.55},
        {"enemy": En1, "pos": v2(L, 0), "delay": 0.55},
        {"enemy": En1, "pos": v2(L, 0), "delay": 0.55},
    ),
    (  # 1 : Green on right
        {"enemy": En1, "pos": v2(R, 0), "delay": 0.55},
        {"enemy": En1, "pos": v2(R, 0), "delay": 0.55},
        {"enemy": En1, "pos": v2(R, 0), "delay": 0.55},
        {"enemy": En1, "pos": v2(R, 0), "delay": 0.55},
    ),
    (  # 2: Green on center
        {"enemy": En1, "pos": v2(C, 0), "delay": 0.55},
        {"enemy": En1, "pos": v2(C, 0), "delay": 0.55},
        {"enemy": En1, "pos": v2(C, 0), "delay": 0.55},
        {"enemy": En1, "pos": v2(C, 0), "delay": 0.55},
    ),
    (  # 3:  Purple stairs on right
        {"enemy": En3, "pos": v2(C, 0), "delay": 1},
        {"enemy": En3, "pos": v2(C, 0), "delay": 1},
        {"enemy": En3, "pos": v2(C, 0), "delay": 1},
        {"enemy": En3, "pos": v2(C, 0), "delay": 1},
    ),
    (  # 4 : Purple stairs on center
        {"enemy": En3, "pos": v2(L, 0), "delay": 1},
        {"enemy": En3, "pos": v2(L, 0), "delay": 1},
        {"enemy": En3, "pos": v2(L, 0), "delay": 1},
        {"enemy": En3, "pos": v2(L, 0), "delay": 1},
    ),
    (  # 5 : Blue worms left
        {"enemy": En2, "pos": v2(L, 0), "delay": 0.5},
        {"enemy": En2, "pos": v2(L, 0), "delay": 0.1},
        {"enemy": En2, "pos": v2(L, 0), "delay": 0.1},
        {"enemy": En2, "pos": v2(L, 0), "delay": 0.1},
        {"enemy": En2, "pos": v2(L, 0), "delay": 0.1},
        {"enemy": En2, "pos": v2(L, 0), "delay": 0.1},
        {"enemy": En2, "pos": v2(L, 0), "delay": 0.1},
    ),
    (  # 6 : Blue worm right
        {"enemy": En2, "pos": v2(R, 0), "dir": -1, "delay": 0.5},
        {"enemy": En2, "pos": v2(R, 0), "dir": -1, "delay": 0.1},
        {"enemy": En2, "pos": v2(R, 0), "dir": -1, "delay": 0.1},
        {"enemy": En2, "pos": v2(R, 0), "dir": -1, "delay": 0.1},
        {"enemy": En2, "pos": v2(R, 0), "dir": -1, "delay": 0.1},
        {"enemy": En2, "pos": v2(R, 0), "dir": -1, "delay": 0.1},
        {"enemy": En2, "pos": v2(R, 0), "dir": -1, "delay": 0.1},
    ),
    ({"enemy": En2, "pos": v2(R, 0), "dir": -1, "delay": 4},),
    ({"enemy": Boss, "pos": v2(C, 0), "delay": 1},),
    # LEVEL 2
    (
        # 9 : Xrotators | top side to middle side
        {"enemy": XRotator, "pos": v2(L, 0), "destination": v2(R, M), "delay": 0.5},
        {"enemy": XRotator, "pos": v2(R, 0), "destination": v2(L, M), "delay": 0},
    ),
    (
        # 10 : Xrotators | top center to bottom side
        {"enemy": XRotator, "pos": v2(C, 0), "destination": v2(R, B), "delay": 0.5},
        {"enemy": XRotator, "pos": v2(C, 0), "destination": v2(L, B), "delay": 0},
    ),
    (
        # 11 : Xrotators | middle side to top side
        {"enemy": XRotator, "pos": v2(0, M), "destination": v2(R, T), "delay": 0.5},
        {"enemy": XRotator, "pos": v2(WIDTH, M), "destination": v2(L, T), "delay": 0},
    ),
    # 12 : Sider left to right
    ({"enemy": Sider, "dir": 1, "delay": 0},),
    # 13 : Sider right to left
    ({"enemy": Sider, "dir": -1, "delay": 0},),
    # 14 : pendulum
    ({"enemy": Pendulum, "pos": v2(C, 0), "delay": 2},),
    # 15 : BigBoss
    ({"enemy": BigBoss, "pos": v2(C, 0), "delay": 0},),
)

waves = (
    # Level 1
    (5, 6, 0, 1, 2, 0, 5, 6),
    (0, 1, 5, 6, 2, 2, 3, 4, 3, 4, 5, 6),
    (0, 1, 2, 0, 1, 5, 6, 5, 6),
    (8,),  # boss
    (7,),  # break
    # Level 2
    (9,),
    (9, 5, 10, 6, 11),
    (14, 0, 1),
    (13,),
    (12, 7, 5, 6),
    (9, 10, 2, 11),
    (9, 10, 5, 6, 13),
    (14, 1, 3, 14, 14),
    (12, 5, 6, 2, 5, 6, 13),
    (7,),
    (15,),
)
# 0 : Green on left
# 1 : Green on right
# 2 : Green on center
# 3 : Purple stairs on right
# 4 : Purple stairs on center
# 5 : Blue worms left
# 6 : Blue worm right
# 7 : blue break
# 8 : boss 1
# 9 : Xrotators | top side to middle side
# 10 : Xrotators | top center to bottom side
# 11 : Xrotators | middle side to top side
# 12 : Sider left to rightx
# 13 : Sider right to left
# 14 : pendulum
# 15 : BigBoss
_waves = (  # Tests
    # Level 2
    (6,),
    # (8,),  # Boss
    (15,),  # Big boss
    # (7,),  # break
    # (0,),
    # (0, 1, 2),
    # (9,5,10,6,11),
    # (14, 0, 1,),
    # (12, 7, 5, 6,),
    # (9, 10, 2, 11),
    # (9, 10, 5, 6, 13),
    # (14, 1, 3, 14, 14),
    # (12, 5, 6, 2, 5, 6, 13),
    # (12, 2, 2),
    # (11, 4, 9, 4),
    # (7,),
    # # (5, 6, 5, 6),
    # (0, 1, 2, 1),
    # (3, 4),
)


class Army:
    def __init__(self):
        self.soldiers_factory = SoldierFactory()
        self.start_war()

    def start_war(self):
        self.soldiers = []
        self.end_war = False
        self.wave = 0

    @property
    def delay(self):
        if len(self.soldiers):
            return self.soldiers[0]["delay"]
        return None

    def get_troop(self):
        if self.wave == len(waves):
            self.end_war = True
        else:
            for troop_number in waves[self.wave]:
                self.soldiers.extend(list(troops[troop_number]))
            self.wave += 1

    def get_soldier(self):
        if len(self.soldiers):
            next_soldier = self.soldiers[0]
            self.soldiers.remove(next_soldier)
            return self.soldiers_factory.create(next_soldier)
        else:
            return None


# Soldiers creation


class SoldierFactory:
    def create(self, datas):
        _type = datas["enemy"]
        creator = get_creator(_type)
        return creator(datas)


def get_creator(_type):
    if _type is None:
        return none_creator
    name = _type.__name__
    if name in ["En1", "En3", "Boss", "Pendulum", "BigBoss"]:
        return base_creator
    elif name == "En2":
        return worm_creator
    elif name == "Sider":
        return sider_creator
    elif name in ["XRotator"]:
        return rot_creator
    else:
        raise ValueError(name)


def none_creator(datas):
    return None


def base_creator(datas):
    return datas["enemy"](datas["pos"])


def worm_creator(
    datas,
):
    direc = datas.get("dir", 1)
    return datas["enemy"](datas["pos"], direc=direc)


def sider_creator(datas):
    direc = datas.get("dir", 1)
    return datas["enemy"](direc=direc)


def rot_creator(datas):
    return datas["enemy"](datas["pos"], datas["destination"])
