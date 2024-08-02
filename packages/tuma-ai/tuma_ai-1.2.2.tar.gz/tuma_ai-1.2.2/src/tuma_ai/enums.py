from enum import IntEnum


class Modes(IntEnum):
    ASK=1
    ASSOCIATION=2
    PROMPT=3

class Levels(IntEnum):
    SUBJECTIVE=0
    OBJECTIVE=1

class Tones(IntEnum):
    CALM=1
    LOVELY=2
    LIVELY=3
    SERIOUS=4
    HAPPY=5
    SAD=6
    HIGH_SPRITE=7
class Roles(IntEnum):
    ASSISTANT=1
    EN_TEACHER=2
    MATH_TEACHER=3
    SCIENTIST=4
    FRIEND=5
    ROBOT=6
    PROGRAMMING_TEACHER=7