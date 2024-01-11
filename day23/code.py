from util import *
import aoc

submit = aoc.for_day(23)


@click.group()
def cli():
    pass


@dataclass
class Nanobot:
    pos: Vector
    r: int


def process_line(line):
    x, y, z, r = parse("pos=<{:d},{:d},{:d}>, r={:d}", line)
    return Nanobot(Vector([x, y, z]), r)


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    strongest = max(data, key=lambda n: n.r)

    def in_range(other):
        dist = sum(abs(d) for d in (strongest.pos - other.pos))
        if dist <= strongest.r:
            return True

    return submit.part(1, sum(1 for n in data if in_range(n)))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]

    def intersect(a, b):
        dist = sum(abs(d) for d in (a.pos - b.pos))
        return a.r + b.r >= dist

    intersection_graph = defaultdict(set)
    for i, a in enumerate(data):
        for j, b in enumerate(data):
            if i != j and intersect(a, b):
                intersection_graph[i].add(j)

    max_clique = set()
    for clique in bron_kerbosch(intersection_graph):
        if len(clique) > len(max_clique):
            max_clique = clique

        if len(clique) > len(data) // 2:  # majority clique
            break
    clique_bots = [data[i] for i in max_clique]

    # mathematically, bot ranges look like
    # |x - pos[0]| + |y - pos[1]| + |z - pos[2]| <= r
    # assuming (x,y,z) is closer to (0,0,0) than any in-range points, it's
    # (pos[0] - x) + (pos[1] - y) + (pos[2] - z) <= r
    # thus
    # pos[0] + pos[1] + pos[2] - r <= x + y + z
    # luckily, we're actually looking for x + y + z as our answer!
    # the lhs to use is that of the total intersected octahedron
    # so we take the one furtherest from (0,0,0)
    return submit.part(2, max(sum(bot.pos) - bot.r for bot in clique_bots))


def bron_kerbosch(neighbors):
    def bron_kerbosch_inner(r, p, x):
        if not p and not x:
            yield r

        for v in list(p):
            next_r = r | {v}
            next_p = p & neighbors[v]
            next_x = x & neighbors[v]
            yield from bron_kerbosch_inner(next_r, next_p, next_x)
            p = p - {v}
            x = x | {v}

    return bron_kerbosch_inner(set(), set(neighbors), set())


def intersect_ranges(r1, r2):
    if r1 is None:
        return r2
    if r2 is None:
        return r1

    assert r1[0] < r1[1], r1
    assert r2[0] < r2[1], r2

    return (max(r1[0], r2[0]), min(r1[1], r2[1]))


if __name__ == "__main__":
    cli()
