from util import *
import aoc

submit = aoc.for_day(1)


@click.group()
def cli():
    pass


def process_line(line):
    return int(line)


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    submit.part(1, sum(data))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]
    vals = running_sum(cycle(data))

    seen = set()
    for x in vals:
        if x in seen:
            return submit.part(2, x)
        seen.add(x)


if __name__ == "__main__":
    cli()
