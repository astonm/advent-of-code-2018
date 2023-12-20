from util import *
from device import *
import aoc

submit = aoc.for_day(16)


@click.group()
def cli():
    pass


def process_line(line):
    return line.split("\n")


def process_samples(samples):
    reg = inst = exp = None
    for line in samples:
        if not line.strip():
            continue
        elif m := parse("Before: {}", line):
            assert reg is None
            reg = json.loads(m[0])
        elif m := parse("After: {}", line):
            assert exp is None
            exp = json.loads(m[0])

            yield inst, reg, exp
            reg = inst = exp = None
        else:
            assert inst is None
            inst = line


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    samples, _ = [process_line(l) for l in read_file(input, delim="\n\n\n\n")]

    matches = []
    for inst, reg, exp in process_samples(samples):
        matches.append(get_matching_opcodes(inst, reg, exp))

    return submit.part(1, sum(1 for m in matches if len(m) >= 3))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    samples, program = [process_line(l) for l in read_file(input, delim="\n\n\n\n")]

    matches = {}
    for inst, reg, exp in process_samples(samples):
        opcode = int(inst.split()[0])
        if opcode not in matches:
            matches[opcode] = set(OPS)
        matching = get_matching_opcodes(inst, reg, exp)
        matches[opcode] &= set(matching)

    op_map = {}
    while len(op_map) < len(OPS):
        opcodes = sorted(matches.items(), key=lambda m: len(m[1]))
        op, options = opcodes[0]
        assert len(options) == 1

        assignment = first(options)
        op_map[op] = assignment
        del matches[op]

        for options in matches.values():
            options -= {assignment}

    reg = [0, 0, 0, 0]
    for inst in program:
        op_code, a, b, c = [int(x) for x in inst.split()]
        op = op_map[op_code]
        reg = apply_op(op, a, b, c, reg)

    return submit.part(2, reg[0])


def get_matching_opcodes(inst, reg, exp):
    out = []
    opcode, a, b, c = [int(x) for x in inst.split()]

    for op in OPS:
        if exp == apply_op(op, a, b, c, reg):
            out.append(op)

    return out


if __name__ == "__main__":
    cli()
