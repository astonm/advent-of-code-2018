from util import *
import aoc

submit = aoc.for_day(12)


@click.group()
def cli():
    pass


def process_line(line):
    p = parse("initial state: {}", line)
    if p:
        return {i: c for (i, c) in enumerate(p[0])}
    else:
        rules = {}
        for line in line.split("\n"):
            rule, res = parse("{} => {}", line)
            rules[rule] = res
        return rules


def p(state):
    for i in range(min(state) - 1, max(state) + 2):
        print(state.get(i, "."), end="", sep="")
    print()


def run_plants(state, rules):
    while 1:
        next_state = {}
        start, end = min(state) - 2, max(state) + 2
        for i in range(start, end + 1):
            s = "".join(state.get(i + d, ".") for d in [-2, -1, 0, 1, 2])
            if rules.get(s) == "#":
                next_state[i] = "#"
        state = next_state
        yield state


def score(state):
    return sum(x for x in state if state[x] == "#")


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    state, rules = [process_line(l) for l in read_file(input, delim="\n\n")]
    state = last(take(20, run_plants(state, rules)))
    return submit.part(1, score(state))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    state, rules = [process_line(l) for l in read_file(input, delim="\n\n")]

    runs = take(3000, run_plants(state, rules))
    counts = [score(state) for state in runs]
    diffs = deltas(counts)
    repeating_diff = Counter(diffs).most_common(1)[0][0]

    start = first(i for (i, d) in enumerate(diffs) if d == repeating_diff)
    end = 50e9

    extrapolated = int((end - 1 - start) * repeating_diff + counts[start])
    return submit.part(2, extrapolated)


if __name__ == "__main__":
    cli()
