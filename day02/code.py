from util import *
import aoc

submit = aoc.for_day(2)


@click.group()
def cli():
    pass


def process_line(line):
    return Counter(line)


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]

    twos = 0
    threes = 0

    for box in data:
        if 2 in box.values():
            twos += 1
        if 3 in box.values():
            threes += 1
    return submit.part(1, twos * threes)


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = read_file(input)
    for x, y in product(data, repeat=2):
        mismatches = [i for i in range(len(x)) if x[i] != y[i]]
        if len(mismatches) == 1:
            return submit.part(2, "".join([x[: mismatches[0]], x[mismatches[0] + 1 :]]))


if __name__ == "__main__":
    cli()
