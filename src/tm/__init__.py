from .__main__ import cli
from .turing_machine import (
    DeltaFunction,
    TMConfiguration,
    create_initial_config,
    step,
    run_until_halt,
    run_with_history,
    display_config,
    run_animated
)


# Export public API
__all__ = [
    'DeltaFunction',
    'TMConfiguration',
    'create_initial_config',
    'step',
    'run_until_halt',
    'run_with_history',
    'display_config',
    'run_animated'
]
