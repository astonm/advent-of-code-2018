from util import *
import aoc

submit = aoc.for_day(5)


@click.group()
def cli():
    pass


def process_line(line):
    return line


def react(l):
    def sub(m):
        if m.group(1).lower() == m.group(2).lower():
            return ""
        return m.group(0)

    while 1:
        next_l = l
        next_l = re.sub("([A-Z])([a-z])", sub, next_l)
        next_l = re.sub("([a-z])([A-Z])", sub, next_l)
        if next_l == l:
            return next_l
        else:
            l = next_l


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    for line in data:
        while 1:
            next_line = react(line)
            if next_line == line:
                break
            else:
                line = next_line
    return submit.part(1, len(line))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]
    for line in data:
        types = set(line.lower())
        best = len(line)
        for c in types:
            filtered_line = line.replace(c, "").replace(c.upper(), "")
            reacted = react(filtered_line)
            best = min(best, len(reacted))
        return submit.part(2, best)


if __name__ == "__main__":
    cli()
