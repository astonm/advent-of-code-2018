from util import *
import aoc

submit = aoc.for_day(17)


@click.group()
def cli():
    pass


def process_line(line):
    var, c0, _, v0, v1 = parse("{}={:d}, {}={:d}..{:d}", line)
    return [(c0, v) if var == "x" else (v, c0) for v in range(v0, v1 + 1)]


def get_grid(points):
    grid = GridN(default=".")
    for p in points:
        grid.set(p, "#")

    y_range = range(
        min(p[1] for p in points),
        max(p[1] for p in points) + 1,
    )

    return grid, y_range


pause = input


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    points = list(flatten([process_line(l) for l in read_file(input)]))
    g, y_range = get_grid(points)
    run_simulation(g)

    return submit.part(1, sum(1 for p, v in g.walk() if v in "~|" and p[1] in y_range))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    points = list(flatten([process_line(l) for l in read_file(input)]))
    g, y_range = get_grid(points)
    run_simulation(g)

    g.print(axis_order=(1, 0))
    return submit.part(2, sum(1 for p, v in g.walk() if v == "~" and p[1] in y_range))


def run_simulation(grid):
    sources = [(500, 0)]
    runs = 1
    while sources:
        source = sources.pop(0)
        spillovers = flow(grid, source)
        sources.extend(spillovers)
        sources = list(set(sources))


def flow(grid, source):
    spillovers = []
    max_y = max(grid.bounds()[1])

    # flow down
    p = source
    while p[1] <= max_y:
        if grid.get(p) == "#":
            p = p[0], p[1] - 1
            break
        grid.set(p, "|")
        p = p[0], p[1] + 1

    if p[1] > max_y:
        return []

    # fill left to right and then upward
    spilled = False
    while not spilled:
        added_on_row = []
        for dir in (1, -1):
            for dist in count():
                np = p[0] + dir * dist, p[1]
                if grid.get(np) == "#":
                    break

                below = np[0], np[1] + 1
                if grid.get(below) in "~#":
                    grid.set(np, "~")
                    added_on_row.append(np)
                else:
                    spilled = True
                    spillovers.append(np)
                    break
        if spilled:
            for a in added_on_row:
                grid.set(a, "|")

        p = p[0], p[1] - 1

    return spillovers


if __name__ == "__main__":
    cli()
