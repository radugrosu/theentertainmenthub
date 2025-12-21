import inspect
from pathlib import Path
import typer


def parse_input(inputs: str):
    nails, instructions = inputs.strip().split("\n\n")
    return nails.splitlines(), instructions.splitlines()


def roll(slot: int, instruction: str, grid: list[str]) -> int:
    col = 2 * (slot - 1)
    height = 0
    i = 0
    width = len(grid[0])
    while height < len(grid):
        if grid[height][col] == "*":
            side = instruction[i]
            col += 1 if side == "R" else -1
            if col >= width:
                col -= 2
            elif col < 0:
                col += 2
            i += 1
        height += 1
    assert col % 2 == 0
    final_slot = col // 2 + 1
    return max(2 * final_slot - slot, 0)


def solve1(grid: list[str], instructions: list[str]) -> int:
    total = 0
    for slot, instruction in enumerate(instructions, 1):
        coins_won = roll(slot, instruction, grid)
        total += coins_won
    return total


def compute_max_payout(grid: list[str], instruction: str) -> int:
    max_payout = 0
    for slot in range(1, len(grid[0]) // 2 + 2):
        coins_won = roll(slot, instruction, grid)
        max_payout = max(max_payout, coins_won)
    return max_payout


def solve2(grid: list[str], instructions: list[str]) -> int:
    total = 0
    for instruction in instructions:
        total += compute_max_payout(grid, instruction)
    return total


def solve3(grid: list[str], instructions: list[str]) -> tuple[int, int]:
    num_slots = (len(grid[0]) + 1) // 2
    payouts = [[0] * num_slots for _ in range(len(instructions))]
    for i, instruction in enumerate(instructions):
        for slot in range(num_slots):
            payouts[i][slot] = roll(slot + 1, instruction, grid)
    dp = {0: 0}
    for row in payouts:
        ndp = {}
        for mask, val in dp.items():
            for s in range(num_slots):
                bit = 1 << s
                if mask & bit:
                    continue
                nmask = mask | bit
                cand = val + row[s]
                prev = ndp.get(nmask)
                if prev is None or cand > prev:
                    ndp[nmask] = cand
        dp = ndp
    max_payout = max(dp.values())

    dp = {0: 0}
    for row in payouts:
        ndp = {}
        for mask, val in dp.items():
            for s in range(num_slots):
                bit = 1 << s
                if mask & bit:
                    continue
                nmask = mask | bit
                cand = val + row[s]
                prev = ndp.get(nmask)
                if prev is None or cand < prev:
                    ndp[nmask] = cand
        dp = ndp
    min_payout = min(dp.values())
    return min_payout, max_payout


def test1():
    file = Path(__file__).stem
    name = inspect.stack()[0].function
    test_input = Path(f"data/{file}/{name}").read_text()
    parsed = parse_input(test_input)
    actual = solve1(*parsed)
    expected = 26
    assert actual == expected, f"{actual=} {expected=}"


def test2():
    file = Path(__file__).stem
    name = inspect.stack()[0].function
    test_input = Path(f"data/{file}/{name}").read_text()
    parsed = parse_input(test_input)
    actual = solve2(*parsed)
    expected = 115
    assert actual == expected, f"{actual=} {expected=}"


def test3():
    file = Path(__file__).stem
    name = inspect.stack()[0].function
    test_input = Path(f"data/{file}/{name}").read_text()
    parsed = parse_input(test_input)
    actual = solve3(*parsed)
    expected = 13, 43
    assert actual == expected, f"{actual=} {expected=}"


def main(part: int):
    inputs = Path(f"data/q1/input{part}").read_text()
    parsed = parse_input(inputs)
    solver = globals()[f"solve{part}"]
    actual = solver(*parsed)
    print(actual)


if __name__ == "__main__":
    typer.run(main)
