from enum import Enum


class Street(Enum):
    PREFLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3
    FINISHED = 4


class Actions(Enum):
    FOLD = 0
    CALL = 1
    BET = 2
