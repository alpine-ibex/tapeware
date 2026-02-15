# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import typer
from termcolor import colored, cprint
from typing import Annotated

from tapeware.turing_machine import DeltaFunction, create_initial_config, run_animated
from tapeware.version import __version__


app = typer.Typer(help="Tapeware - Turing machine simulator.")


@app.callback()
def main(
    ctx: typer.Context,
    delay: Annotated[float, typer.Option(help="Delay between steps in seconds")] = 0.08,
    no_delay: Annotated[bool, typer.Option(help="Disable delay between steps")] = False,
    no_wait: Annotated[bool, typer.Option(help="Disable waiting for user input between tests")] = False,
    version: Annotated[bool, typer.Option("--version", help="Show version and exit")] = False,
) -> None:
    """Tapeware - Turing machine simulator."""
    if version:
        typer.echo(f"tapeware version {__version__}")
        raise typer.Exit()

    ctx.obj = {
        "delay": delay,
        "no_delay": no_delay,
        "no_wait": no_wait,
    }


@app.command()
def end_ab(
    ctx: typer.Context,
    input_str: Annotated[str | None, typer.Argument(metavar="input", help="Input string to process")] = None,
) -> None:
    """Run the simple TM that accepts strings ending with 'ab'."""
    from tapeware.examples.end_ab import delta, test_cases

    if input_str is not None:
        run(ctx, delta, ((input_str, None),))
    else:
        run(ctx, delta, test_cases)


@app.command()
def anbn(
    ctx: typer.Context,
    input_str: Annotated[str | None, typer.Argument(metavar="input", help="Input string to process")] = None,
) -> None:
    """Run the aⁿbⁿ Turing machine demo."""
    from tapeware.examples.anbn import delta, test_cases

    if input_str is not None:
        run(ctx, delta, ((input_str, None),))
    else:
        run(ctx, delta, test_cases)


@app.command()
def anbncn(
    ctx: typer.Context,
    input_str: Annotated[str | None, typer.Argument(metavar="input", help="Input string to process")] = None,
) -> None:
    """Run the aⁿbⁿcⁿ Turing machine demo."""
    from tapeware.examples.anbncn import delta, test_cases

    if input_str is not None:
        run(ctx, delta, ((input_str, None),))
    else:
        run(ctx, delta, test_cases)


@app.command()
def anbncn_alt(
    ctx: typer.Context,
    input_str: Annotated[str | None, typer.Argument(metavar="input", help="Input string to process")] = None,
) -> None:
    """Run the alternative aⁿbⁿcⁿ Turing machine demo."""
    from tapeware.examples.anbncn_alt import delta, test_cases

    if input_str is not None:
        run(ctx, delta, ((input_str, None),))
    else:
        run(ctx, delta, test_cases)


@app.command()
def equal_01(
    ctx: typer.Context,
    input_str: Annotated[str | None, typer.Argument(metavar="input", help="Input string to process")] = None,
) -> None:
    """Run the equal 0s and 1s Turing machine demo."""
    from tapeware.examples.equal_01 import delta, test_cases

    if input_str is not None:
        run(ctx, delta, ((input_str, None),))
    else:
        run(ctx, delta, test_cases)


def run(
    ctx: typer.Context,
    delta: DeltaFunction,
    inputs: tuple[tuple[str, bool | None], ...],
) -> None:
    print("=" * 80)
    cprint(delta.__doc__, "cyan", attrs=["bold"])
    print("=" * 80)
    print()

    for i, (input_str, expected) in enumerate(inputs):
        print(f"Input: {colored(repr(input_str), 'yellow', attrs=['bold'])}", end="")
        if expected is not None:
            print(f" - Expected: {colored('ACCEPT' if expected else 'REJECT', 'cyan')}", end="",)
        print()

        config = create_initial_config(input_str, delta)
        run_animated(config, delay=ctx.obj["delay"] if not ctx.obj["no_delay"] else 0)

        is_not_last = i < len(inputs) - 1
        if not ctx.obj["no_wait"] and is_not_last:
            input("Press Enter for next test...")
        print()


# Create CLI alias for backward compatibility
cli = app

if __name__ == "__main__":
    app()
