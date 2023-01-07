from util import *
import aoc

submit = aoc.for_day(10)


@click.group()
def cli():
    pass


def process_line(line):
    r = parse("position=<{:d}, {:d}> velocity=<{:d}, {:d}>", line)
    return Vector(r[:2]), Vector(r[2:])


def is_pic(pts):
    LINE_LEN = 7
    pos = [p for (p, v) in pts]
    by_column = defaultdict(set)
    for p, _ in pts:
        by_column[p[0]].add(p[1])

    for ys in by_column.values():
        if deltas(sorted(ys))[:LINE_LEN] == [1] * LINE_LEN:
            return True
    return False


def is_small(pts):
    xs = [p[0] for (p, v) in pts]
    if max(xs) - min(xs) < 100:
        return True


def draw_pic(pts):
    g = GridN(default=".")
    for p, _ in pts:
        g.set(tuple(p), "#")
    g.print(axis_order=[1, 0])


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    for i in count(start=1):
        for p, v in data:
            p += v

        if is_pic(data):
            draw_pic(data)
            break

    return submit.part(1, None)


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]
    for i in count(start=1):
        for p, v in data:
            p += v

        if is_pic(data):
            return submit.part(2, i)


if __name__ == "__main__":
    cli()
