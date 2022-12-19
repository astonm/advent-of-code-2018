from util import *
import aoc

submit = aoc.for_day(6)


@click.group()
def cli():
    pass


def process_line(line):
    return tuple(map(int, line.split(", ")))


def n3_voronoi(pts):
    mins = [min(x[i] for x in pts) - 1 for i in range(2)]
    maxs = [max(x[i] for x in pts) + 1 for i in range(2)]

    voronoi = {}
    for x in range(mins[0], maxs[0] + 1):
        for y in range(mins[1], maxs[1] + 1):
            best = (None, 10000)
            for ind, pt in enumerate(pts):
                d = abs(pt[0] - x) + abs(pt[1] - y)
                if (x, y) == (5, 5):
                    print(ind, d)
                if d < best[1]:
                    best = (ind, d)
                elif d == best[1]:
                    if best[0] != ind:
                        best = (None, d)
            voronoi[(x, y)] = best

    infinite = {
        voronoi[p][0]
        for p in voronoi
        if p[0] in (mins[0], maxs[0]) or p[1] in (mins[1], maxs[1])
    }
    return Counter(voronoi[p][0] for p in voronoi if voronoi[p][0] not in infinite)


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    counts = n3_voronoi(data)
    return submit.part(1, counts.most_common()[0][1])


def circle_size(pts, dist_sum):
    size = 0

    mins = [min(x[i] for x in pts) - 1 for i in range(2)]
    maxs = [max(x[i] for x in pts) + 1 for i in range(2)]
    for x in range(mins[0], maxs[0] + 1):
        for y in range(mins[1], maxs[1] + 1):
            s = 0
            for pt in pts:
                s += abs(pt[0] - x) + abs(pt[1] - y)
            if s < dist_sum:
                size += 1
    return size


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]
    dist_sum = 32 if "ex" in input.name else 10000
    return submit.part(2, circle_size(data, dist_sum))


if __name__ == "__main__":
    cli()
