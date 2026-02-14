# Tapeware

*Tapeware - keeps your tape fresh and your states sealed tight.*

A general-purpose, visual Turing machine simulator with support for custom delta functions, arbitrary states, and any alphabet.

**Built with Functional Programming principles** - immutable data structures, pure functions, and composable operations.

## Features

- **Functional Programming Style**: Immutable configurations, pure functions, referential transparency
- **General-purpose framework**: Define any Turing machine with custom delta functions
- **Flexible state system**: Support for any number of states with custom names
- **Arbitrary alphabets**: Work with any symbols (letters, digits, special characters)
- **Rich visualisation**: Color-coded tape display with animated execution
- **Built-in examples**: Includes sample implementations for aⁿbⁿcⁿ and more
- **Time Travel**: Full execution history with ability to replay any configuration

## Quick Start

### Running the built-in example (aⁿbⁿcⁿ):

```bash
# Test a specific input
uv run tapeware anbncn aaabbbccc

# Run all test cases
uv run tapeware anbncn
```

Alternatively, run it directly from github:

```bash
# Test a specific input
uvx --from git+https://github.com/alpine-ibex/tapeware tapeware anbncn aaabbbccc

# Run all test cases
uvx --from git+https://github.com/alpine-ibex/tapeware tapeware anbncn
```

### Creating a custom Turing machine:

```python
from tapeware import create_initial_config, run_animated

def my_delta(state: str, symbol: str) -> tuple[str, str, str] | None:
    """
    Your transition function.
    Returns: (new_state, write_symbol, direction) or None to reject
    Direction: "L" (left) or "R" (right)
    """
    if state == "q₀":
        if symbol == "a":
            return ("q₁", "X", "R")
        # ... more transitions
    # ... more states
    return None

# Create initial configuration
config = create_initial_config(
    "your_input", 
    my_delta,
    initial_state="q₀",
    accept_states={"qₐ"},
    reject_states={"qᵣ"}
)

# Run with animation
final = run_animated(config, delay=0.15)
```

## Functional Programming API

The simulator is built with **functional programming principles** using immutable data structures and pure functions:

```python
from tapeware import create_initial_config, step, run_with_history

# Create immutable configuration
config = create_initial_config("test", my_delta)

# Pure functions - returns new config without mutation
config1 = step(config)
config2 = step(config1)

# Original unchanged!
assert config.state == "q₀"

# Get complete execution history
history = run_with_history(config)
states = [cfg.state for cfg in history]
print(f"State sequence: {' → '.join(states)}")
```

**Benefits:**
- Immutability: No hidden state changes
- Pure functions: Predictable, testable, composable
- History: Full execution replay capability
- Parallelisable: Safe for concurrent execution

## Color Scheme

The tape display uses colors to make execution easy to follow:

- 🟨 **Yellow background**: Current head position
- 🟦 **Blue background**: Lowercase letters (input symbols)
- 🟩 **Light green background**: Uppercase letters (marked symbols)
- 🟪 **Magenta background**: Digits (0-9)
- ⬜ **Grey background**: Blank cells and other symbols

State colors:
- 🔵 **Cyan**: Processing states
- 🟢 **Green**: Accept states
- 🔴 **Red**: Reject states

## Built-in Examples

### aⁿbⁿcⁿ (Context-Sensitive Language)

Recognises strings with equal numbers of a's, b's, and c's in order.

**Algorithm**: Mark one 'a' (→X), one 'b' (→Y), one 'c' (→Z), repeat until all marked.

```bash
uv run tapeware anbncn "aaabbbccc"
```

**Test cases**:
- Accept: `""`, `"abc"`, `"aabbcc"`, `"aaabbbccc"`
- Reject: `"aabbc"`, `"aabbbc"`, `"abbc"`

### Strings ending with "ab"

```bash
uv run tapeware end-ab
```

Simple example showing how to create custom delta functions.

## API Reference

### Core Functions

```python
# Create initial configuration
create_initial_config(
    input_string: str,
    delta_function: DeltaFunction,
    initial_state: str = "q₀",
    accept_states: set[str] | None = None,  # Default: {"qₐ"}
    reject_states: set[str] | None = None,  # Default: {"qᵣ"}
    blank_symbol: str = "□"
) -> TMConfiguration

# Execute one step (pure function)
step(config: TMConfiguration) -> TMConfiguration

# Run to completion
run_until_halt(
    config: TMConfiguration, 
    max_steps: int | None = None
) -> TMConfiguration

# Get full execution history
run_with_history(
    config: TMConfiguration, 
    max_steps: int | None = None
) -> list[TMConfiguration]

# Display and animation (side effects)
display_config(config: TMConfiguration) -> None
run_animated(
    config: TMConfiguration, 
    delay: float = 0.2, 
    max_steps: int | None = None
) -> TMConfiguration
```

**Example**:
```python
from tapeware import create_initial_config, run_animated

config = create_initial_config("abc", my_delta)
final = run_animated(config, delay=0.15)
```

### Delta Function Type

```python
DeltaFunction = Callable[[str, str], tuple[str, str, str] | None]
```

**Signature**: `delta(state: str, symbol: str) -> tuple[new_state, write_symbol, direction] | None`

- **state**: Current state name
- **symbol**: Current symbol under the tape head
- **Returns**: `(new_state, write_symbol, direction)` or `None` to reject
  - **new_state**: Name of the next state
  - **write_symbol**: Symbol to write at current position
  - **direction**: `"L"` (left) or `"R"` (right)

**Example**:
```python
def my_delta(state: str, symbol: str) -> tuple[str, str, str] | None:
    if state == "q₀" and symbol == "a":
        return ("q₁", "X", "R")
    # ... more transitions
    return None  # Reject if no transition defined
```

## Code Structure

```
/
├── src/tapeware/
│   ├── examples/         # Example turing machines
│   │   ├── __init__.py
│   │   ├── anbncn.py     # Recognise strings aⁿbⁿcⁿ
│   │   ├── end_ab.py     # Recognise strings ending with 'ab'
│   │   └── equal_01.py  # Recognise strings with equal number of 0s and 1s.
│   ├── __init__.py
│   ├── __main__.py       # Entry point for `uv run tapeware`
│   └── turing_machine.py # Turing machine implementation
├── pyproject.toml        # Project configuration
└── README.md             # This file
```

## Dependencies

- `click` - For a nice cli
- `termcolor` - For colored terminal output

## Theory

This simulator demonstrates the full computational power of Turing machines:

- **Universality**: Can simulate any Turing machine by providing appropriate delta function
- **Context-sensitive languages**: Can recognise languages like aⁿbⁿcⁿ (Type 1 in Chomsky hierarchy)
- **Beyond context-free**: More powerful than pushdown automata
- **Church-Turing thesis**: Can compute any computable function

**Example: aⁿbⁿcⁿ**
- Context-sensitive (cannot be recognised by pushdown automaton)
- Requires marking strategy to track equal counts

## Implementation Notes

- Tape extends automatically in both directions as needed
- Multiple blank symbols can be used (configurable)
- Custom states and alphabets fully supported
- Animation speed adjustable via `delay` parameter
- Each step displays state and complete tape contents

## Author

Ruben Bär (polar@bear.sh)
