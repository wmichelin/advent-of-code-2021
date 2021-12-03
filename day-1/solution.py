import typing


def input_iter():
    with open('./input.txt') as f:
        for line in f.readlines():
            yield int(line)


def part_1():
    last: typing.Optional[int] = None
    increase_count = 0
    for num in input_iter():
        if last and last < num:
            increase_count += 1
        last = num

    return increase_count


def is_increasing(window_a, window_b):
    return sum(window_a) < sum(window_b)


def part_2():
    window_size = 3

    window_a = []
    window_b = []
    input_i = input_iter()
    for i in range(window_size + 1):
        val = next(input_i)
        if i < window_size:
            window_a.append(val)
        if i > 0:
            window_b.append(val)

    last = window_b[-1]

    increasing_count = 1 if is_increasing(window_a, window_b) else 0
    for val in input_i:
        assert len(window_a) == 3 and len(window_b) == 3, 'expected window sizes to maintain consistent'
        window_a.pop(0)
        window_a.append(last)

        window_b.pop(0)
        window_b.append(val)

        last = val
        if is_increasing(window_a, window_b):
            increasing_count += 1

    return increasing_count


print(f"part 1: {part_1()}")
print(f"part 2: {part_2()}")
