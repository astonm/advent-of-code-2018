from device import *
from util import *
import aoc

submit = aoc.for_day(21)


@click.group()
def cli():
    pass


def process_line(line):
    return line


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    program = load_program(input)

    # by inspection of debug output plus algorithm in translated.txt
    # when ip=28, reg[5] = 6778585 initially
    answer = 6778585
    run_program(program, regs=[answer, 0, 0, 0, 0, 0], debug=True)
    return submit.part(1, answer)


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    seen = []
    seen_again = []
    for reg5 in implemented_program():
        if reg5 in seen:
            break
        seen.append(reg5)

    return submit.part(2, seen[-1])


def implemented_program():
    reg5 = 0
    reg2 = reg5 | 65536
    reg5 = 10362650

    while True:
        reg4 = reg2 & 255
        reg5 += reg4
        reg5 &= 16777215
        reg5 *= 65899
        reg5 &= 16777215

        if reg2 < 256:
            yield reg5  # the value tested against reg[0]
            reg2 = reg5 | 65536
            reg5 = 10362650
            continue
        else:
            reg2 = reg2 // 256


if __name__ == "__main__":
    cli()
