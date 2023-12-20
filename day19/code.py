from util import *
from device import *
import aoc

submit = aoc.for_day(19)


@click.group()
def cli():
    pass


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    program = load_program(input)
    regs = run_program(program, [0, 0, 0, 0, 0, 0])
    return submit.part(1, regs[0])


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    program = load_program(input)
    # regs = run_program(program, [1, 0, 0, 0, 0, 0])

    # naive run loops for a long time between ip=3...ip=11 (skipping ip=7)
    # state at top of loop looks something like [0, 0, 10551354, 3, 1, 1571926], ip=3
    # seems to be waiting for reg[4]*reg[5] to equal reg[2], so start one below

    # regs = run_program(program, [0, 0, 10551354, 3, 1, 10551353], ip=3)

    # that goes a different way but eventually just increments reg[4] by 1, resets reg[5] to 1, and jumps back to ip=3
    # can try to trigger with reg[4] = 2 by setting reg[5] = 10551354/2-1 and also reg[0] = old reg[4]

    # regs = run_program(program, [1, 0, 10551354, 3, 2, 5275676], ip=3)

    # see translated.txt for rough decompilation
    # reg[0] is incremented by reg[4] every time reg[4]*reg[5] == reg[2]
    # we reset reg[5] and increment reg[4] if reg[5] > reg[2]
    # we exit if reg[4] > reg[2]

    # so... reg[0] will be the sum of all the numbers that evenly divide 10551354
    return submit.part(2, implemented_program(10551354))


def implemented_program(reg2):
    reg0 = 0
    for reg4 in range(1, reg2 + 1):
        if reg2 % reg4 == 0:
            reg0 += reg4
    return reg0


if __name__ == "__main__":
    cli()
