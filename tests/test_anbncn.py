import pytest

from tapeware.turing_machine import create_initial_config, run_until_halt
from tapeware.examples.anbncn import delta, test_cases

@pytest.mark.parametrize("input_str,expected", test_cases)
def test_anbncn(input_str: str, expected: bool) -> None:

    config = create_initial_config(input_str, delta)
    config = run_until_halt(config)
    assert config.is_accepted() == expected
