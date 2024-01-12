import dataclasses
from util import *
import aoc

submit = aoc.for_day(24)


@click.group()
def cli():
    pass


@dataclass
class ArmyGroup:
    size: int
    hp: int
    attack_damage: int
    attack_type: str
    initiative: int

    weak_to: tuple
    immune_to: tuple

    team: str = None

    def effective_power(self):
        return self.size * self.attack_damage

    def damage_for(self, enemy):
        if not enemy:
            return 0
        elif self.attack_type in enemy.immune_to:
            return 0
        elif self.attack_type in enemy.weak_to:
            return 2 * self.effective_power()
        else:
            return self.effective_power()

    def __hash__(self):
        return self.initiative


def process_line(line):
    if not line:
        return

    if ":" in line:
        return line.lower().split()[0].rstrip(":")

    res = parse(
        "{:d} units each with {:d} hit points {} an attack that does {:d} {} damage at initiative {:d}",
        line,
    )

    args = res[0:2] + res[3:]
    args += process_weak_immune(res[2])

    return ArmyGroup(*args)


def process_weak_immune(s):
    r = {}
    s = s.split("with")[0].replace(" ", "").replace("(", "").replace(")", "")
    if not s:
        return tuple(), tuple()

    parts = s.split(";")
    for part in parts:
        k, v = part.split("to")
        r[k] = v.split(",")
    return tuple(r.get("weak", [])), tuple(r.get("immune", []))


def collect(lines):
    out = []
    for team, *groups in split_before(lines, lambda l: isinstance(l, str)):
        for group in groups:
            group.team = team
            out.append(group)
    return out


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    groups = collect([process_line(l) for l in read_file(input)])
    return submit.part(1, sum(g.size for g in run_game(groups)))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    groups = collect([process_line(l) for l in read_file(input)])

    for p in count():
        max_boost = 2 ** p
        winner = first(run_game(groups, immune_boost=max_boost)).team
        if winner == "immune":
            break

    binary_search = BinarySearch(max_boost)
    while boost := binary_search.next():
        try:
            winner = first(run_game(groups, immune_boost=boost)).team
        except ValueError:
            winner = "?"

        if winner == "immune":
            binary_search.too_high()
        else:
            binary_search.too_low()

    min_boost = binary_search.mid()
    return submit.part(2, sum(g.size for g in run_game(groups, immune_boost=min_boost)))


def run_game(in_combat, immune_boost=0):
    in_combat = deepcopy(in_combat)
    if immune_boost:
        for group in in_combat:
            if group.team == "immune":
                group.attack_damage += immune_boost

    seen = set()
    while len(Counter(g.team for g in in_combat)) > 1:
        # targeting
        targets = {}
        for group in sorted(
            in_combat,
            key=lambda x: (x.effective_power(), x.initiative),
            reverse=True,
        ):
            enemies = [g for g in in_combat if g.team != group.team]
            worst_enemy = max(
                [e for e in enemies if e not in targets.values()],
                key=lambda enemy: (
                    group.damage_for(enemy),
                    enemy.effective_power(),
                    enemy.initiative,
                ),
                default=None,
            )
            if group.damage_for(worst_enemy) > 0:
                targets[group] = worst_enemy

        # attacking
        for group in sorted(
            in_combat,
            key=lambda x: x.initiative,
            reverse=True,
        ):
            if group.size == 0:
                continue
            if target := targets.get(group):
                target.size = max(
                    0, target.size - group.damage_for(target) // target.hp
                )

        state = tuple(sorted((g.initiative, g.size) for g in in_combat))
        if state in seen:
            raise ValueError("stalemate")
        seen.add(state)

        in_combat = [g for g in in_combat if g.size != 0]
    return in_combat


class BinarySearch:
    def __init__(self, hi):
        self.lo = 0
        self.hi = hi

    def mid(self):
        return (self.hi + self.lo) // 2

    def next(self):
        if self.hi <= self.lo:
            return None
        return self.mid()

    def too_high(self):
        self.hi = self.mid()

    def too_low(self):
        self.lo = self.mid() + 1


if __name__ == "__main__":
    cli()
