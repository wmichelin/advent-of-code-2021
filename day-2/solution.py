from dataclasses import dataclass


@dataclass
class Position:
    part: str = "1"
    horizontal: int = 0
    vertical: int = 0
    aim: int = 0

    def __setattr__(self, key, value):
        before = self.__getattribute__(key)
        super().__setattr__(key, value)
        if self.part != "1" and key == "horizontal":
            self.vertical += self.aim * (value - before)



POS_TO_MODIFIER_MAP = {
    "forward": ("horizontal", 1),
    "down": ("vertical", 1),
    "up": ("vertical", -1),
}

POS_TO_MODIFIER_MAP_W_AIM = {
    "forward": ("horizontal", 1),
    "down": ("aim", 1),
    "up": ("aim", -1),
}


def input_iter():
    with open('./input.txt') as f:
        for line in f.readlines():
            _dir, mag = line.split(" ")
            yield _dir, int(mag)


def part_1():
    pos = Position()

    for direction, magnitude in input_iter():
        attr_name, modifier = POS_TO_MODIFIER_MAP[direction]
        setattr(
            pos,
            attr_name,
            getattr(pos, attr_name) + (magnitude * modifier)
        )

    return pos.vertical * pos.horizontal


def part_2():
    pos = Position(part="2")
    for direction, magnitude in input_iter():
        attr_name, modifier = POS_TO_MODIFIER_MAP_W_AIM[direction]
        setattr(
            pos,
            attr_name,
            getattr(pos, attr_name) + (magnitude * modifier)
        )
    return pos.horizontal * pos.vertical


print(f"part 1: {part_1()}")
print(f"part 2: {part_2()}")



