from util import *
import aoc

submit = aoc.for_day(14)


@click.group()
def cli():
    pass


def process_line(line):
    return int(line)


def draw(board, curr):
    parts = []
    for i, n in enumerate(board):
        if curr[0] == i:
            parts.append("({})".format(n))
        elif curr[1] == i:
            parts.append("[{}]".format(n))
        else:
            parts.append(" {} ".format(n))
    print("".join(parts))


def subseq(haystack, needle):
    for offset in range(0, len(haystack) - len(needle)):
        if haystack[offset : offset + len(needle)] == needle:
            return offset
    return -1


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]

    for n_recipes in data:
        board = [3, 7]
        curr = [0, 1]

        while len(board) < n_recipes + 10:
            s = sum(board[curr[i]] for i in [0, 1])
            digs = map(int, str(s))
            board.extend(digs)
            curr = [(curr[i] + board[curr[i]] + 1) % len(board) for i in [0, 1]]
        submit.part(1, "".join(map(str, board[n_recipes : n_recipes + 10])))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [list(map(int, l)) for l in read_file(input)]

    for target in data:
        board = [3, 7]
        curr = [0, 1]

        while True:
            s = sum(board[curr[i]] for i in [0, 1])
            digs = map(int, str(s))
            board.extend(digs)
            curr = [(curr[i] + board[curr[i]] + 1) % len(board) for i in [0, 1]]

            found = subseq(board[-20:], target)
            if found > -1:
                submit.part(2, found + len(board[:-20]))
                break


if __name__ == "__main__":
    cli()
