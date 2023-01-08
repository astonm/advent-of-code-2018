from util import *
import aoc

submit = aoc.for_day(13)


@click.group()
def cli():
    pass


@dataclass
class Cart:
    p: Vector
    v: Vector
    t: object
    visible: bool = True


turns = {
    "/": lambda x, y: (-y, -x),
    "\\": lambda x, y: (y, x),
    "L": lambda x, y: (y, -x),
    "R": lambda x, y: (-y, x),
}


def get_turner():
    turn = cycle("LSR")

    def turner():
        return next(turn)

    return turner


def process_grid(grid):
    carts = []
    for x, y in grid.walk_coords():
        c = grid.get(x, y)
        v = None
        if c in "<>":
            grid.set(x, y, "-")
            v = Vector([1 if c == ">" else -1, 0])
        if c in "^v":
            grid.set(x, y, "|")
            v = Vector([0, 1 if c == "v" else -1])

        if v:
            cart = Cart(p=Vector([x, y]), v=v, t=get_turner())
            carts.append(cart)
    return carts


def draw(grid, carts):
    g = grid.copy()
    d = {
        (1, 0): ">",
        (-1, 0): "<",
        (0, 1): "v",
        (0, -1): "^",
    }

    for c in carts:
        g.set(c.p[0], c.p[1], d[tuple(c.v)])
    g.lines = g.lines[:10]
    g.height = len(g.lines)
    g.print()
    print()


def coord(t):
    return ",".join(str(x) for x in t)


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    grid = Grid.from_string(input.read())
    carts = process_grid(grid)

    for i in count():
        carts.sort(key=lambda cart: (cart.p[1], cart.p[0]))  # order matters!

        for cart in carts:
            cart.p += cart.v

            c = grid.get(*cart.p)
            if c == "+":
                c = cart.t()
            if c in turns:
                cart.v = turns[c](*cart.v)

            spots = Counter(tuple(cart.p) for cart in carts).most_common()
            collision = first(spot for (spot, n) in spots if n > 1)
            if collision:
                print(i)
                return submit.part(1, coord(collision))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    grid = Grid.from_string(input.read())
    carts = process_grid(grid)

    for i in count():
        carts.sort(key=lambda cart: (cart.p[1], cart.p[0]))  # order matters!

        for cart in carts:
            if not cart.visible:
                continue

            cart.p += cart.v
            c = grid.get(*cart.p)
            if c == "+":
                c = cart.t()
            if c in turns:
                cart.v = turns[c](*cart.v)

            spots = Counter(tuple(cart.p) for cart in carts).most_common()
            collisions = set(spot for (spot, n) in spots if n > 1)
            for cart in carts:
                if tuple(cart.p) in collisions:
                    cart.visible = False

        carts = [cart for cart in carts if cart.visible]
        if len(carts) == 1:
            return submit.part(2, coord(carts[0].p))


if __name__ == "__main__":
    cli()
