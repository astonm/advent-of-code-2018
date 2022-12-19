from util import *
import aoc

submit = aoc.for_day(3)


@click.group()
def cli():
    pass


def process_line(line):
    return parse("#{n:d} @ {x:d},{y:d}: {w:d}x{h:d}", line)


def get_fabric(claims):
    fabric = defaultdict(set)
    for claim in claims:
        for dx in range(claim["w"]):
            for dy in range(claim["h"]):
                fabric[(claim["x"] + dx, claim["y"] + dy)].add(claim["n"])
    return fabric


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    fabric = get_fabric(data)
    return submit.part(1, sum(1 for i, c in fabric.items() if len(c) > 1))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]
    fabric = get_fabric(data)
    uncontested_claims = set(claim["n"] for claim in data)

    for c in fabric.values():
        if len(c) > 1:
            uncontested_claims -= c
    return submit.part(2, first(uncontested_claims))


if __name__ == "__main__":
    cli()
