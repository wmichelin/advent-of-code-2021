import collections
import dataclasses
import typing


def input_iter():
    with open('./input.txt') as f:
        for line in f.readlines():
            yield tuple([int(c) for c in line if c != '\n'])


@dataclasses.dataclass
class Count:
    num_zeros: int = 0
    num_ones: int = 0


def binary_tuple_to_int(_in: typing.Tuple[int, ... ]) -> int:
    return int("".join([str(_i) for _i in _in]), base=2)


@dataclasses.dataclass
class FreqCounterByIdx:
    counts_by_position: typing.Dict[int, Count] = dataclasses.field(
        default_factory=lambda: collections.defaultdict(lambda: Count()),
    )

    def record_value(self, value, position):
        assert value in (0, 1), 'unexpected value provided'
        if value == 0:
            self.counts_by_position[position].num_zeros += 1
        else:
            self.counts_by_position[position].num_ones += 1

    def get_gamma_rate(self) -> int:
        value = [None for _ in self.counts_by_position.keys()]
        for position, counts in self.counts_by_position.items():
            value[position] = 0 if counts.num_zeros > counts.num_ones else 1
        return binary_tuple_to_int(tuple(value))

    def get_epsilon_rate(self) -> int:
        value = [None for _ in self.counts_by_position.keys()]
        for position, counts in self.counts_by_position.items():
            value[position] = 0 if counts.num_zeros < counts.num_ones else 1
        return binary_tuple_to_int(tuple(value))

    def get_most_common_by_position(self, position):
        return 1 if self.counts_by_position[position].num_ones >= self.counts_by_position[position].num_zeros else 0

    def get_least_common_by_position(self, position):
        return 1 if self.counts_by_position[position].num_ones < self.counts_by_position[position].num_zeros else 0


def part_one():
    counter = FreqCounterByIdx()
    for l in input_iter():
        for idx, value in enumerate(l):
            counter.record_value(value, idx)
    return counter.get_gamma_rate() * counter.get_epsilon_rate()


def _compute_most_pass(cohort: typing.List[typing.Tuple[int, ...]], position: int) -> typing.List[typing.Tuple[int, ...]]:
    counter = FreqCounterByIdx()

    for l in cohort:
        for idx, value in enumerate(l):
            counter.record_value(value, idx)

    to_return = []
    for l in cohort:
        if l[position] == counter.get_most_common_by_position(position):
            to_return.append(l)
    return to_return


def _compute_least_pass(cohort: typing.List[typing.Tuple[int, ...]], position: int) -> typing.List[typing.Tuple[int, ...]]:
    counter = FreqCounterByIdx()

    for l in cohort:
        for idx, value in enumerate(l):
            counter.record_value(value, idx)

    to_return = []
    for l in cohort:
        if l[position] == counter.get_least_common_by_position(position):
            to_return.append(l)
    return to_return


def part_two():
    counter = FreqCounterByIdx()
    # hydrate frequency counter
    _iter = list(input_iter())
    for l in _iter:
        for idx, value in enumerate(l):
            counter.record_value(value, idx)

    total_passes = len(_iter[0])
    most_iter = _iter
    for i in range(0, total_passes):
        most_iter = _compute_most_pass(most_iter, i)
        if len(most_iter) == 1:
            break
    assert len(most_iter) == 1
    most_ = binary_tuple_to_int(most_iter[0])

    least_iter = _iter
    for i in range(0, total_passes):
        least_iter = _compute_least_pass(least_iter, i)
        if len(least_iter) == 1:
            break

    assert len(least_iter) == 1
    least_ = binary_tuple_to_int(least_iter[0])

    return most_ * least_


print(f"part 1: {part_one()}")
print(f"part 2: {part_two()}")



