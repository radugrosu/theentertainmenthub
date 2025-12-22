from collections import deque
import inspect
import itertools
from pathlib import Path
from typing import Literal, TypeAlias
import typer


Balloon: TypeAlias = Literal["R", "G", "B"]


def parse_input(inputs: str) -> list[Balloon]:
    out: list[Balloon] = []
    valid = ("R", "G", "B")
    for ch in inputs.strip():
        if ch in valid:
            out.append(ch)
        else:
            raise ValueError(f"Invalid character: {ch}")
    return out


def solve1(balloons: list[Balloon]) -> int:  # pyright: ignore[reportReturnType]
    balloons = balloons[::-1]
    for i, arrow in enumerate(itertools.cycle("RGB"), 1):
        if not balloons:
            return i - 1
        b = balloons.pop()
        while b == arrow:
            if not balloons:
                return i
            b = balloons.pop()


def solve2(balloons: list[Balloon], reps: int = 100) -> int:  # pyright: ignore[reportReturnType]
    balloons = balloons * reps
    for i, arrow in enumerate(itertools.cycle("RGB"), 1):
        if not balloons:
            return i - 1
        if (n := len(balloons)) % 2 == 0:
            mid = n // 2
            if arrow == balloons[0]:
                balloons = balloons[1:mid] + balloons[mid + 1 :]
            else:
                balloons = balloons[1:]
        else:
            balloons = balloons[1:]


ENC = {"R": 0, "G": 1, "B": 2}


def solve3(balloons: list[str], reps: int = 100000) -> int:  # pyright: ignore[reportReturnType]
    base = [ENC[ch] for ch in balloons]
    n = len(base)
    N = n * reps

    L = deque()
    R = deque()
    left_len = (N + 1) // 2
    for i in range(N):
        x = base[i % n]
        if i < left_len:
            L.append(x)
        else:
            R.append(x)

    for shots, arrow in enumerate(itertools.cycle((0, 1, 2))):
        if not L:
            return shots
        total_before = len(L) + len(R)
        first = L.popleft()
        if total_before % 2 == 0 and first == arrow:
            R.popleft()
        if len(L) < len(R):
            L.append(R.popleft())
        elif len(L) > len(R) + 1:
            R.appendleft(L.pop())


def test1():
    file = Path(__file__).stem
    name = inspect.stack()[0].function
    test_input = Path(f"data/{file}/{name}").read_text()
    parsed = parse_input(test_input)
    actual = solve1(parsed)
    expected = 7
    assert actual == expected, f"{actual=} {expected=}"


def test2():
    file = Path(__file__).stem
    name = inspect.stack()[0].function
    test_input = Path(f"data/{file}/{name}").read_text()
    parsed = parse_input(test_input)
    actual = solve2(parsed, 5)
    expected = 14
    assert actual == expected, f"{actual=} {expected=}"


def test21():
    file = Path(__file__).stem
    name = inspect.stack()[0].function
    test_input = Path(f"data/{file}/{name}").read_text()
    parsed = parse_input(test_input)
    for repeat, expected in zip([10, 50, 100], [304, 1464, 2955]):
        actual = solve3(parsed, repeat)
        assert actual == expected, f"{actual=} {expected=}"


def test3():
    test_input = Path("data/q2/test2").read_text()
    parsed = parse_input(test_input)
    actual = solve3(parsed, 5)
    expected = 14
    assert actual == expected, f"{actual=} {expected=}"


def main(part: int):
    file = Path(__file__).stem
    inputs = Path(f"data/{file}/input{part}").read_text()
    parsed = parse_input(inputs)
    solver = globals()[f"solve{part}"]
    actual = solver(parsed)
    print(actual)


if __name__ == "__main__":
    typer.run(main)
