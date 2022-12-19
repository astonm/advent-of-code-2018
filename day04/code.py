from util import *
import aoc

submit = aoc.for_day(4)


@click.group()
def cli():
    pass


def process_line(line):
    return parse("[1518-{mon:d}-{date:d} {h:d}:{m:d}] {desc}", line)


def get_guard_summary(input):
    data = [process_line(l) for l in sorted(read_file(input))]
    guards = defaultdict(Counter)
    curr = None
    sleep = None
    for line in data:
        if m := parse("Guard #{:d} begins shift", line["desc"]):
            curr = m[0]
            sleep = None
        if line["desc"] == "falls asleep":
            sleep = line["m"]
        if line["desc"] == "wakes up":
            assert sleep is not None, line
            for m in range(sleep, line["m"]):
                guards[curr][m] += 1
    return guards


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    guards = get_guard_summary(input)
    guard_hours = sorted((sum(c.values()), g) for (g, c) in guards.items())
    worst_guard = guard_hours[-1][1]
    return submit.part(1, worst_guard * guards[worst_guard].most_common()[0][0])


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    guards = get_guard_summary(input)
    guard_hours = sorted((max(c.values()), g) for (g, c) in guards.items())
    worst_guard = guard_hours[-1][1]
    return submit.part(2, worst_guard * guards[worst_guard].most_common()[0][0])


if __name__ == "__main__":
    cli()
