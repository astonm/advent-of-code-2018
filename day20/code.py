from util import *
import aoc

submit = aoc.for_day(20)


@click.group()
def cli():
    pass


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    parsed = parse_regex(tokenize(input.read()))
    doors = regex_to_doors(parsed, (0, 0))
    graph = edges_to_graph(doors)

    return submit.part(1, max(point_distances(graph)))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    parsed = parse_regex(tokenize(input.read()))
    doors = regex_to_doors(parsed, (0, 0))
    graph = edges_to_graph(doors)

    return submit.part(2, sum(1 for d in point_distances(graph) if d >= 1000))


class TokenStream:
    def __init__(self, stream):
        self.stream = stream

    def peek(self):
        return self.stream[0]

    def consume(self, expect=None):
        out = self.stream.pop(0)
        if expect is not None:
            assert out == expect, f"{out=}, {expect=}"
        return out


def tokenize(s):
    return TokenStream([x for x in re.split(r"(\W)", s) if x])


def parse_regex(tokens):
    tokens.consume("^")
    out = parse_sequence(tokens)
    tokens.consume("$")

    return out


class Sequence(list):
    pass


def parse_sequence(tokens):
    out = Sequence()

    while True:
        v = tokens.peek()

        if v.startswith(tuple("NSEW")):
            out.append(tokens.consume())
        elif v.startswith("("):
            out.append(parse_option(tokens))
        else:
            break

    return out


class Option(list):
    pass


def parse_option(tokens):
    out = Option()

    tokens.consume("(")

    while True:
        out.append(parse_sequence(tokens))
        if tokens.peek() == "|":
            tokens.consume("|")
        else:
            break

    tokens.consume(")")

    return out


DIRS = {"N": (0, -1), "S": (0, +1), "E": (+1, 0), "W": (-1, 0)}


def regex_to_doors(parsed, start):
    doors = set()

    if isinstance(parsed, Sequence):
        p = start
        for item in parsed:
            if isinstance(item, Option):
                for door in regex_to_doors(item, p):
                    doors.add(door)
            else:
                assert isinstance(item, str)
                for dir in item:
                    d = DIRS[dir]
                    next_p = p[0] + d[0], p[1] + d[1]
                    doors.add((p, next_p))
                    p = next_p

    if isinstance(parsed, Option):
        for item in parsed:
            for door in regex_to_doors(item, start):
                doors.add(door)

    return doors


def edges_to_graph(doors):
    out = defaultdict(list)
    for a, b in doors:
        out[a].append(b)
        out[b].append(a)
    return out


def point_distances(graph):
    start = (0, 0)
    q = [(0, start)]
    seen = set()

    out = {}

    while q:
        dist, p = q.pop(0)
        out[p] = dist

        for next_p in graph[p]:
            if next_p not in seen:
                seen.add(next_p)
                q.append((dist + 1, next_p))

    return out.values()


if __name__ == "__main__":
    cli()
