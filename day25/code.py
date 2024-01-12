from util import *
import aoc

submit = aoc.for_day(25)


@click.group()
def cli():
    pass


def process_line(line):
    return tuple([int(x) for x in line.split(",")])


def nearby(p1, p2):
    return sum(abs(x - y) for x, y in zip(p1, p2)) <= 3


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]

    neighbors = defaultdict(list)
    for p1 in data:
        for p2 in data:
            if p1 != p2 and nearby(p1, p2):
                neighbors[p1].append(p2)

    constellations = []
    unconstellated = set(data)
    while unconstellated:
        start = first(unconstellated)
        constellation = find_connected(start, neighbors)
        constellations.append(constellation)
        unconstellated -= constellation

    return submit.part(1, len(constellations))


def find_connected(s, neighbors):
    constellation = set()

    q = [s]
    while q:
        star = q.pop(0)
        constellation.add(star)

        for other in neighbors[star]:
            if other not in constellation:
                q.append(other)
    return constellation


if __name__ == "__main__":
    cli()
