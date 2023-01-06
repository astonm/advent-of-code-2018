from util import *
import aoc

submit = aoc.for_day(9)


@click.group()
def cli():
    pass


def process_line(line):
    return parse("{:d} players; last marble is worth {:d} points", line)


def high_score(n_players, n_marbles):
    circle = CircularDoublyLinkedList()
    current = circle.append(0)

    scores = defaultdict(int)

    for marble in range(1, n_marbles + 1):
        player = (marble - 1) % n_players
        if marble % 23 > 0:
            current = circle.insert_after(current.next, Node(marble))
        else:
            back_marble = current.prev.prev.prev.prev.prev.prev.prev  # lol
            current = back_marble.next
            circle.remove_elem(back_marble)

            scores[player] += marble
            scores[player] += back_marble.data

    return max(scores.values())


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    for n_players, n_marbles in data:
        submit.part(1, high_score(n_players, n_marbles))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]
    for n_players, n_marbles in data:
        submit.part(2, high_score(n_players, n_marbles * 100))


if __name__ == "__main__":
    cli()
