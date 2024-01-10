from util import *
import aoc

submit = aoc.for_day(22)


@click.group()
def cli():
    pass


def process_line(line):
    parts = line.split(": ")
    return parts[0], list(map(int, parts[1].split(",")))


def process_input(input):
    data = dict(process_line(l) for l in read_file(input))
    depth = data["depth"][0]
    start = (0, 0)
    target = tuple(data["target"])

    return start, target, cave_type_getter((start, target), depth)


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    start, target, get_cave_type = process_input(input)

    x_range = range(start[0], target[0] + 1)
    y_range = range(start[1], target[1] + 1)
    return submit.part(1, sum(get_cave_type(p) for p in product(x_range, y_range)))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    start, target, get_cave_type = process_input(input)
    h = lambda p: manhattan(p, target)

    can_equip = {
        CaveType.ROCKY: {"climbing gear", "torch"},
        CaveType.WET: {"climbing gear", "neither"},
        CaveType.NARROW: {"torch", "neither"},
    }

    min_cost = defaultdict(lambda: inf)
    min_cost[(start, "torch")] = 0

    q = PriorityQueue()
    q.put((h(start), start, "torch", 0))

    while not q.empty():
        _, p, equipped, cost = q.get()
        if (p, equipped) == (target, "torch"):
            return submit.part(2, cost)

        for d in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            next_p = p[0] + d[0], p[1] + d[1]
            try:
                next_cave_type = get_cave_type(next_p)
            except ValueError:
                continue

            if equipped in can_equip[next_cave_type]:
                next_cost = cost + 1
                if next_cost < min_cost[(next_p, equipped)]:
                    min_cost[(next_p, equipped)] = next_cost
                    q.put((h(next_p) + next_cost, next_p, equipped, next_cost))

        next_equip = first(can_equip[get_cave_type(p)] - {equipped})
        next_cost = cost + 7
        if next_cost < min_cost[(p, next_equip)]:
            min_cost[(p, next_equip)] = next_cost
            q.put((h(next_p) + next_cost, p, next_equip, next_cost))


class CaveType(IntEnum):
    SOLID = -1
    ROCKY = 0
    WET = 1
    NARROW = 2


def cave_type_getter(endpoints, depth):
    EROSION_LEVEL = {}

    def get_erosion_level(p):
        if p[0] < 0 or p[1] < 0:
            raise ValueError("solid rock")

        if p not in EROSION_LEVEL:
            if p in endpoints:
                geo_index = 0
            elif p[1] == 0:
                geo_index = p[0] * 16807
            elif p[0] == 0:
                geo_index = p[1] * 48271
            else:
                left = get_erosion_level((p[0] - 1, p[1]))
                up = get_erosion_level((p[0], p[1] - 1))
                geo_index = up * left

            EROSION_LEVEL[p] = (geo_index + depth) % 20183
        return EROSION_LEVEL[p]

    def get_cave_type(p):
        return CaveType(get_erosion_level(p) % 3)

    return get_cave_type


if __name__ == "__main__":
    cli()
