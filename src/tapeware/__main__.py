# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import click
from termcolor import colored, cprint

from tapeware.turing_machine import DeltaFunction, create_initial_config, run_animated


@click.group()
def cli() -> None:
    """Tapeware - Turing machine simulator."""


@cli.command()
@click.argument("input_str", metavar="input", default=None)
def end_ab(input_str: str | None = None) -> None:
    """Run the simple TM that accepts strings ending with 'ab'."""
    from tapeware.examples.end_ab import delta
    from tapeware.examples.end_ab import test_cases

    if input_str is not None:
        run(delta, ((input_str, None),))
    else:
        run(delta, test_cases)


@cli.command()
@click.argument("input_str", metavar="input", default=None)
def anbn(input_str: str | None = None) -> None:
    """Run the aⁿbⁿ Turing machine demo."""
    from tapeware.examples.anbn import delta
    from tapeware.examples.anbn import test_cases

    if input_str is not None:
        run(delta, ((input_str, None),))
    else:
        run(delta, test_cases)


@cli.command()
@click.argument("input_str", metavar="input", default=None)
def anbncn(input_str: str | None = None) -> None:
    """Run the aⁿbⁿcⁿ Turing machine demo."""
    from tapeware.examples.anbncn import delta
    from tapeware.examples.anbncn import test_cases

    if input_str is not None:
        run(delta, ((input_str, None),))
    else:
        run(delta, test_cases)


@cli.command()
@click.argument("input_str", metavar="input", default=None)
def equal_01(input_str: str | None = None) -> None:
    """Run the equal 0s and 1s Turing machine demo."""
    from tapeware.examples.equal_01 import delta
    from tapeware.examples.equal_01 import test_cases

    if input_str is not None:
        run(delta, ((input_str, None),))
    else:
        run(delta, test_cases)


def run(delta: DeltaFunction, inputs: tuple[tuple[str, bool | None], ...]) -> None:
    print("=" * 80)
    cprint(delta.__doc__, "cyan", attrs=["bold"])
    print("=" * 80)
    print()

    for input_str, expected in inputs:
        print(f"Input: {colored(repr(input_str), 'yellow', attrs=['bold'])}", end="")
        if expected is not None:
            print(
                f" - Expected: {colored('ACCEPT' if expected else 'REJECT', 'cyan')}",
                end="",
            )
        print()

        config = create_initial_config(input_str, delta)
        run_animated(config, delay=0.08)

        input("Press Enter for next test...")
        print()


if __name__ == "__main__":
    cli()
