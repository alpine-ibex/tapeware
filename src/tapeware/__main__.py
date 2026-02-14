# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import click
from termcolor import colored, cprint

from tapeware.turing_machine import DeltaFunction, create_initial_config, run_animated


@click.group()
@click.version_option()
@click.pass_context
@click.option("--delay", default=0.08, help="Delay between steps in seconds (default: 0.08)")
@click.option("--no-delay", is_flag=True, help="Disable delay between steps")
@click.option("--no-wait", is_flag=True, help="Disable waiting for user input between tests")
def cli(ctx: click.Context, delay: float = 0.08, no_delay: bool = False, no_wait: bool = False) -> None:
    """Tapeware - Turing machine simulator."""
    ctx.obj = {"delay": delay, "no_delay": no_delay, "no_wait": no_wait}


@cli.command()
@click.argument("input_str", metavar="input", default=None)
@click.pass_context
def end_ab(ctx: click.Context, input_str: str | None = None) -> None:
    """Run the simple TM that accepts strings ending with 'ab'."""
    from tapeware.examples.end_ab import delta, test_cases

    if input_str is not None:
        run(ctx, delta, ((input_str, None),))
    else:
        run(ctx, delta, test_cases)


@cli.command()
@click.argument("input_str", metavar="input", default=None)
@click.pass_context
def anbn(ctx: click.Context, input_str: str | None = None) -> None:
    """Run the aⁿbⁿ Turing machine demo."""
    from tapeware.examples.anbn import delta, test_cases

    if input_str is not None:
        run(ctx, delta, ((input_str, None),))
    else:
        run(ctx, delta, test_cases)


@cli.command()
@click.argument("input_str", metavar="input", default=None)
@click.pass_context
def anbncn(ctx: click.Context, input_str: str | None = None) -> None:
    """Run the aⁿbⁿcⁿ Turing machine demo."""
    from tapeware.examples.anbncn import delta, test_cases

    if input_str is not None:
        run(ctx, delta, ((input_str, None),))
    else:
        run(ctx, delta, test_cases)


@cli.command()
@click.argument("input_str", metavar="input", default=None)
@click.pass_context
def anbncn_alt(ctx: click.Context, input_str: str | None = None) -> None:
    """Run the alternative aⁿbⁿcⁿ Turing machine demo."""
    from tapeware.examples.anbncn_alt import delta, test_cases

    if input_str is not None:
        run(ctx, delta, ((input_str, None),))
    else:
        run(ctx, delta, test_cases)


@cli.command()
@click.argument("input_str", metavar="input", default=None)
@click.pass_context
def equal_01(ctx: click.Context, input_str: str | None = None) -> None:
    """Run the equal 0s and 1s Turing machine demo."""
    from tapeware.examples.equal_01 import delta, test_cases

    if input_str is not None:
        run(ctx, delta, ((input_str, None),))
    else:
        run(ctx, delta, test_cases)


def run(ctx: click.Context, delta: DeltaFunction, inputs: tuple[tuple[str, bool | None], ...]) -> None:
    print("=" * 80)
    cprint(delta.__doc__, "cyan", attrs=["bold"])
    print("=" * 80)
    print()

    for i, (input_str, expected) in enumerate(inputs):
        print(f"Input: {colored(repr(input_str), 'yellow', attrs=['bold'])}", end="")
        if expected is not None:
            print(
                f" - Expected: {colored('ACCEPT' if expected else 'REJECT', 'cyan')}",
                end="",
            )
        print()

        config = create_initial_config(input_str, delta)
        run_animated(config, delay=ctx.obj["delay"] if not ctx.obj["no_delay"] else 0)

        is_not_last = i < len(inputs) - 1
        if not ctx.obj["no_wait"] and is_not_last:
            input("Press Enter for next test...")
        print()


if __name__ == "__main__":
    cli()
