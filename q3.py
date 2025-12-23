import inspect
import re
from dataclasses import dataclass
from pathlib import Path

import typer

PAT = re.compile(
    r"(?P<id>\d+): faces=\[(?P<faces>(?:-?\d+,)*-?\d+)] seed=(?P<seed>\d+)"
)


@dataclass
class Die:
    id: int
    faces: list[int]
    seed: int


@dataclass
class DieState:
    pulse: int
    face: int = 0
    roll_number: int = 1

    def h(self) -> tuple[int, int, int]:
        return self.pulse, self.face, self.roll_number

    @property
    def spin(self) -> int:
        return self.roll_number * self.pulse

    def next(self, seed: int, num_faces: int) -> int:
        spin = self.spin
        self.pulse += spin
        self.pulse %= seed
        self.pulse += 1 + self.roll_number + seed
        self.roll_number += 1
        self.face += spin
        self.face %= num_faces
        return self.face


class DieRoll:
    def __init__(self, die: Die):
        self.die = die
        self.state = DieState(die.seed)

    def h(self) -> tuple[int, int, int]:
        return self.state.h()

    def roll(self) -> int:
        face = self.state.next(self.die.seed, len(self.die.faces))
        return self.die.faces[face]


def parse_input(inputs: str) -> list[DieRoll]:
    out: list[DieRoll] = []
    for line in inputs.splitlines():
        if match := re.match(PAT, line):
            md = match.groupdict()
            faces = list(map(int, md["faces"].split(",")))
            die = Die(int(md["id"]), faces, int(md["seed"]))
            out.append(DieRoll(die))
        else:
            raise ValueError(f"Invalid line: {line}")
    return out


def parse_input2(inputs: str) -> tuple[list[DieRoll], list[int]]:
    head, tail = inputs.strip().split("\n\n")
    track = [int(d) for d in tail]
    return parse_input(head), track


def parse_input3(inputs: str) -> tuple[list[DieRoll], list[list[int]]]:
    head, tail = inputs.strip().split("\n\n")
    grid = [[int(i) for i in row] for row in tail.splitlines()]
    return parse_input(head), grid


def solve1(dice: list[DieRoll], min_points: int = 10_000) -> int:
    num_rolls = 0
    total_points = 0
    while total_points < min_points:
        num_rolls += 1
        for die in dice:
            points = die.roll()
            total_points += points
    return num_rolls


def solve2(inputs: tuple[list[DieRoll], list[int]]) -> tuple[int, ...]:
    dice, track = inputs
    n = len(track)
    positions = [0] * len(dice)
    turn = 0
    order = []
    done = set()
    while len(done) < len(dice):
        turn += 1
        for i, die in enumerate(dice):
            if i in done:
                continue
            pos = positions[i]
            if pos >= n:
                done.add(i)
                order.append(i + 1)
                continue
            face = die.roll()
            if face == track[pos]:
                positions[i] += 1
    return tuple(order)


def visit(grid: list[list[int]], die: DieRoll) -> set[tuple[int, int]]:
    m, n = len(grid), len(grid[0])
    queue = []
    roll = die.roll()
    seen = set()
    seen_state = set()
    for r, row in enumerate(grid):
        for c, num in enumerate(row):
            if num == roll:
                queue.append((0, r, c))
                seen_state.add((r, c, die.h()))
                seen.add((r, c))
    rolls = [(roll, die.h())]
    while queue:
        s, r, c = queue.pop()
        if s >= len(rolls):
            rolls.append((die.roll(), die.h()))
        face, state = rolls[s]
        if face == grid[r][c]:
            seen.add((r, c))
            for nr, nc in [(r, c), (r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
                if 0 <= nr < m and 0 <= nc < n and (nr, nc, state) not in seen_state:
                    seen_state.add((nr, nc, state))
                    queue.append((s + 1, nr, nc))
    return seen


def solve3(inputs: tuple[list[DieRoll], list[list[int]]]) -> int:
    dice, grid = inputs
    seen = set()
    for die in dice:
        seen |= visit(grid, die)
    return len(seen)


def test1():
    file = Path(__file__).stem
    name = inspect.stack()[0].function
    test_input = Path(f"data/{file}/{name}").read_text()
    parsed = parse_input(test_input)
    actual = solve1(parsed)
    expected = 844
    assert actual == expected, f"{actual=} {expected=}"


def test2():
    file = Path(__file__).stem
    name = inspect.stack()[0].function
    test_input = Path(f"data/{file}/{name}").read_text()
    parsed = parse_input2(test_input)
    actual = solve2(parsed)
    expected = 1, 3, 4, 2
    assert actual == expected, f"{actual=} {expected=}"


def test3():
    file = Path(__file__).stem
    name = inspect.stack()[0].function
    test_input = Path(f"data/{file}/{name}").read_text()
    parsed = parse_input3(test_input)
    actual = solve3(parsed)
    expected = 33
    assert actual == expected, f"{actual=} {expected=}"


def test31():
    file = Path(__file__).stem
    name = inspect.stack()[0].function
    test_input = Path(f"data/{file}/{name}").read_text()
    parsed = parse_input3(test_input)
    actual = solve3(parsed)
    expected = 1125
    assert actual == expected, f"{actual=} {expected=}"


def main(part: int):
    file = Path(__file__).stem
    inputs = Path(f"data/{file}/input{part}").read_text()
    parser = globals()[f"parse_input{part}"]
    parsed = parser(inputs)
    solver = globals()[f"solve{part}"]
    actual = solver(parsed)
    print(actual)


if __name__ == "__main__":
    typer.run(main)
