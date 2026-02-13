import click
from termcolor import colored

from tm.turing_machine import (
    DeltaFunction,
    create_initial_config,
    run_animated,
    display_config
)


@click.group()
def cli() -> None:
    """Run Turing machine demos and tests."""

@cli.command()
@click.argument("input_str", metavar="input", default=None)
def end_ab(input_str: str | None = None) -> None:
    """Run the simple TM that accepts strings ending with 'ab'."""
    from tm.examples.end_ab import delta_end_ab

    print("=" * 80)
    print(colored("Turing Machine: Simple TM (strings ending with 'ab')", "cyan", attrs=["bold"]))
    print("=" * 80)
    print()

    if input_str is not None:
        run(input_str, delta_end_ab)
        return

    test_cases = [
        ("ab", True),
        ("aab", True),
        ("bab", True),
        ("aaab", True),
        ("abab", True),
        ("ba", False),
        ("", False),
    ]

    for input_str, expected in test_cases:
        run(input_str, delta_end_ab, expected)
        
        input("Press Enter for next test...")
        print()

@cli.command()
@click.argument("input_str", metavar="input", default=None)
def anbncn(input_str: str | None = None) -> None:
    """Run the aⁿbⁿcⁿ Turing machine demo."""
    from tm.examples.anbncn import delta_anbncn

    print("=" * 80)
    print(colored("Turing Machine: aⁿbⁿcⁿ", "cyan", attrs=["bold"]))
    print("=" * 80)
    print()

    if input_str is not None:
        run(input_str, delta_anbncn)
        return
        
    # Otherwise run all test cases for aⁿbⁿcⁿ
    test_cases = [
        ("", True),           # n=0
        ("abc", True),        # n=1
        ("aabbcc", True),     # n=2
        ("aaabbbccc", True),  # n=3
        ("aabbbc", False),    # unequal
        ("aaabbc", False),    # unequal
        ("abbc", False),      # unequal
        ("aabcc", False),     # unequal
    ]

    for input_str, expected in test_cases:
        run(input_str, delta_anbncn, expected)
        
        input("Press Enter for next test...")
        print()


@cli.command()
@click.argument("input_str", metavar="input", default=None)
def equal_01(input_str: str | None = None) -> None:
    """Run the equal 0s and 1s Turing machine demo."""
    from tm.examples.equal_01 import delta_equal_01
    
    print("=" * 80)
    print(colored("Turing Machine: Equal 0s and 1s", "cyan", attrs=["bold"]))
    print("=" * 80)
    print()

    if input_str is not None:
        run(input_str, delta_equal_01)
        return

    test_cases = [
        ("", True),          # n=0
        ("01", True),        # n=1
        ("0011", True),      # 2 0s, 2 1s
        ("1100", True),      # 2 1s, 2 0s
        ("001011", True),    # 3 0s, 3 1s
        ("010101", True),    # 3 0s, 3 1s
        ("0", False),        # 1 0, 0 1s
        ("000111", True),    # 3 0s, 3 1s
        ("00011", False),    # 3 0s, 2 1s
    ]

    for input_str, expected in test_cases:
        run(input_str, delta_equal_01, expected)
        
        input("Press Enter for next test...")
        print()

def run(input_str: str, delta: DeltaFunction, expected: bool | None = None) -> None:
    print(f"Input: {colored(repr(input_str), "yellow", attrs=["bold"])}", end="")
    if expected is not None:
        print(f" - Expected: {colored("ACCEPT" if expected else "REJECT", "cyan")}", end="")
    print()
    
    config = create_initial_config(input_str, delta)
    final_config = run_animated(config, delay=0.08)


if __name__ == "__main__":
    cli()