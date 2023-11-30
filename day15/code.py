import os

from util import *
import aoc

submit = aoc.for_day(15)


@click.group()
def cli():
    pass


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    g = Grid.from_string(input.read())
    units = get_units(g)
    rounds = count(1)

    for round in rounds:
        for u in units:
            live_units = [u for u in units if u.alive]
            if game_over(live_units):
                return submit.part(1, (round - 1) * sum(u.hp for u in units if u.alive))

            if u.alive:
                take_turn(u, g, live_units)

        units = [u for u in units if u.alive]
        units.sort(key=point_order)


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]
    pprint(locals())
    return submit.part(2, None)


@dataclass
class Unit:
    p: tuple
    v: str
    ap: int
    hp: int
    alive: bool


def point_order(x):
    if hasattr(x, "p"):
        return x.p[1], x.p[0]
    else:
        return x[1], x[0]


def get_units(g):
    out = []
    for p, v in zip(g.walk_coords(), g.walk()):
        if v in "EG":
            out.append(Unit(p, v, ap=3, hp=200, alive=True))
    return out


def take_turn(u, g, units):
    targets = [enemy for enemy in units if enemy.v != u.v]

    spots_in_range = list(set(flatten([g.neighbors(*t.p) for t in targets])))
    spots_in_range.sort(key=point_order)

    already_in_range = u.p in spots_in_range

    open_in_range = [p for p in spots_in_range if g.get(*p) == "."]

    if not open_in_range and not already_in_range:
        return

    if not already_in_range:
        move(u, open_in_range, g)

    killed = attack(u, g, units)


def move(u, open_in_range, g):
    path = shortest_path_to_any(u.p, open_in_range, g)
    if path:
        x, y = u.p
        g.set(x, y, ".")

        u.p = path[0]

        x, y = u.p
        g.set(x, y, u.v)


def shortest_path_to_any(start, goals, g):
    q = [start]
    seen = set()
    backlinks = {}
    while q:
        p = q.pop(0)

        seen.add(p)
        if p in goals:
            curr_path = get_path(p, backlinks)
            return curr_path[1:]

        for dx, dy in [(0, -1), (-1, 0), (1, 0), (0, 1)]:
            np = p[0] + dx, p[1] + dy
            if g.get(*np) == "." and np not in seen:
                backlinks[np] = p
                q.append(np)

    return None


def get_path(p, backlinks):
    out = [p]
    while p in backlinks:
        p = backlinks[p]
        out.append(p)
    return out[::-1]


def attack(u, g, units):
    in_range = [e for e in units if u.v != e.v and manhattan(u.p, e.p) == 1]
    in_range.sort(key=point_order)
    if in_range:
        weakest = min(in_range, key=lambda x: x.hp)

        weakest.hp -= u.ap
        if weakest.hp <= 0:
            weakest.alive = False
            x, y = weakest.p
            g.set(x, y, ".")

            return weakest


def game_over(units):
    return len(set(u.v for u in units)) == 1


if __name__ == "__main__":
    cli()
