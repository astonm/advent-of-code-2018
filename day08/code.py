from util import *
import aoc

submit = aoc.for_day(8)


@click.group()
def cli():
    pass


def process_line(line):
    return list(map(int, line.split()))


@dataclass
class Node:
    children: list
    metadata: list


def parse(data):
    n_child, n_meta, *rest = data

    children = []
    for _ in range(n_child):
        child, rest = parse(rest)
        children.append(child)

    metadata, rest = rest[:n_meta], rest[n_meta:]
    assert len(metadata) == n_meta

    return Node(children=children, metadata=metadata), rest


def all_metadata(tree):
    for child in tree.children:
        yield from all_metadata(child)
    for md in tree.metadata:
        yield md


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)][0]
    tree, rest = parse(data)
    assert not rest
    return submit.part(1, sum(all_metadata(tree)))


def node_value(node):
    if node is None:
        return 0

    if not node.children:
        return sum(node.metadata)
    else:
        return sum(node_value(lget(node.children, i - 1, None)) for i in node.metadata)


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)][0]
    tree, _ = parse(data)
    return submit.part(2, node_value(tree))


if __name__ == "__main__":
    cli()
