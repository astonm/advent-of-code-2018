from util import *
import aoc

submit = aoc.for_day(18)


@click.group()
def cli():
    pass


def run_step(grid, step):
    next_grid = grid.copy()
    for p, c in zip(grid.walk_coords(), grid.walk()):
        neighbors = [
            grid.get(x[0], x[1]) for x in grid.neighbors(p[0], p[1], diags=True)
        ]
        if c == "." and neighbors.count("|") >= 3:
            next_grid.set(p[0], p[1], "|")
        if c == "|" and neighbors.count("#") >= 3:
            next_grid.set(p[0], p[1], "#")
        if c == "#":
            if "|" not in neighbors or "#" not in neighbors:
                next_grid.set(p[0], p[1], ".")

    return next_grid


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    grid = Grid.from_string(input.read())
    grid = reduce(run_step, range(10), grid)
    grid.print()

    resources = list(grid.walk())
    return submit.part(1, resources.count("|") * resources.count("#"))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    grid = Grid.from_string(input.read())
    minutes = 1_000_000_000

    seen = {}
    loop_len = None
    for n in count(1):
        grid = run_step(grid, n)
        s = "\n".join("".join(l) for l in grid.lines)
        if s in seen:
            loop_len = n - seen[s]
            break
        seen[s] = n

    target_ind = minutes % loop_len
    for s, ind in seen.items():
        if ind % loop_len == target_ind:
            grid = Grid.from_string(s)

    resources = list(grid.walk())
    return submit.part(2, resources.count("|") * resources.count("#"))


if __name__ == "__main__":
    cli()
