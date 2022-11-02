from enum import IntEnum


class Color(IntEnum):
    NONE = 0
    DARK = 1
    LIGHT = 2

    def next(self):
        match self:
            case self.NONE:
                return Color.NONE
            case self.DARK:
                return Color.LIGHT
            case self.LIGHT:
                return Color.DARK
