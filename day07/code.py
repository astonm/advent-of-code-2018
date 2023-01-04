from util import *
import aoc

submit = aoc.for_day(7)


@click.group()
def cli():
    pass


def process_line(line):
    return parse("Step {} must be finished before step {} can begin.", line)


def make_graph(data):
    graph = defaultdict(list)
    for pre, post in data:
        graph[pre].append(post)
        graph[post] = graph[post]  # ensure an entry for every item
    return graph


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    graph = make_graph(data)

    out = []
    while graph:
        available = graph.keys() - set(p for posts in graph.values() for p in posts)
        choice = first(sorted(available))
        graph.pop(choice)
        out.append(choice)

    return submit.part(1, "".join(out))


@dataclass(order=True)
class Worker:
    id: int
    available_at: int = 0
    steps: list = field(default_factory=list)


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]
    graph = make_graph(data)
    num_workers = 2 if "ex" in input.name else 5
    time_offset = -64 if "ex" in input.name else -4

    workers = [Worker(i + 1) for i in range(num_workers)]
    working_on = set()
    for t in count():
        if not graph:
            break

        available_workers = [w for w in workers if w.available_at <= t]
        if not available_workers:
            continue

        for worker in available_workers:
            if worker.steps:
                last_step = worker.steps[-1]
                if last_step in working_on:
                    del graph[last_step]
                    working_on.remove(last_step)

        remaining_steps = set(p for posts in graph.values() for p in posts)
        unblocked_steps = graph.keys() - remaining_steps
        available_steps = sorted(x for x in unblocked_steps if x not in working_on)

        for worker, step in zip(available_workers, available_steps):
            step_time = ord(step) + time_offset
            worker.available_at = t + step_time
            worker.steps.append(step)
            working_on.add(step)

    return submit.part(2, max(w.available_at for w in workers))


if __name__ == "__main__":
    cli()
