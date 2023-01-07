from util import *
import aoc

submit = aoc.for_day(11)


@click.group()
def cli():
    pass


def process_line(line):
    return int(line)


def get_windows(size=3):
    starts = [Vector(list(x)) for x in product(range(1, 300 + 2 - size), repeat=2)]
    offsets = [Vector(list(d)) for d in product(range(size), repeat=2)]
    for start in starts:
        out = []
        for offset in offsets:
            out.append(start + offset)
        yield out


@lru_cache(maxsize=None)
def fuel_cell_value(x, y, serial_num):
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial_num
    power_level *= rack_id
    hundreds_digit = (power_level % 1000) // 100
    return hundreds_digit - 5


def coord(t):
    return ",".join(str(x) for x in t)


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]

    for serial_num in data:
        best_score = -1
        best_value = None

        for window in get_windows():
            score = sum(fuel_cell_value(x, y, serial_num) for (x, y) in window)
            if score > best_score:
                best_score = score
                best_value = window[0]

        submit.part(1, coord(best_value))


def get_running_sums(serial_num):
    size = 300
    col_sum = defaultdict(int)
    row_sum = defaultdict(int)
    out = {}
    for y in range(size + 1):
        for x in range(size + 1):
            if x == 0 or y == 0:
                out[(x, y)] = 0
                continue

            val = fuel_cell_value(x, y, serial_num)

            total = val
            total += col_sum[x]
            total += row_sum[y]
            if x > 0 and y > 0:
                total += out[(x - 1, y - 1)]

            out[(x, y)] = total
            col_sum[x] += val
            row_sum[y] += val

    return out


def get_window_sum(rs, x, y, size):
    outer_include = rs[(x + size - 1, y + size - 1)]
    left_exclude = rs[(x - 1, y + size - 1)]
    top_exclude = rs[(x + size - 1, y - 1)]
    inner_include = rs[(x - 1, y - 1)]

    return outer_include - left_exclude - top_exclude + inner_include


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]
    for serial_num in data:
        rs = get_running_sums(serial_num)

        best_score = -1
        best_value = None
        for size in tqdm(range(1, 301)):
            for x, y in product(range(1, 300 + 2 - size), repeat=2):
                score = get_window_sum(rs, x, y, size)
                if score > best_score:
                    best_score = score
                    best_value = x, y, size

        submit.part(2, coord(best_value))


if __name__ == "__main__":
    cli()
