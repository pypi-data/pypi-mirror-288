from enum import Enum
class Modes(Enum):
    ASK=1
    ASSOCIATION=2
    PROMPT=3

class Levels(Enum):
    SUBJECTIVE=0
    OBJECTIVE=1

class Tones(Enum):
    CALM=1
    LOVELY=2
    LIVELY=3
    SERIOUS=4
    HAPPY=5
    SAD=6
    HIGH_SPRITE=7