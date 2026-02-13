from typing import Callable
from dataclasses import dataclass, replace
import time
from termcolor import colored

# Type alias for a delta function
DeltaFunction = Callable[[str, str], tuple[str, str, str] | None]


@dataclass(frozen=True)
class TMConfiguration:
    """
    Immutable Turing Machine configuration.
    
    Represents the complete state of a TM at a single point in time.
    All fields are immutable to support functional programming style.
    """
    tape: tuple[str, ...]
    head: int
    state: str
    steps: int
    blank: str
    delta: DeltaFunction
    accept_states: frozenset[str]
    reject_states: frozenset[str]
    
    def is_halted(self) -> bool:
        """Check if machine has halted (pure function)."""
        return self.state in self.accept_states or self.state in self.reject_states
    
    def is_accepted(self) -> bool:
        """Check if machine is in accept state (pure function)."""
        return self.state in self.accept_states
    
    def current_symbol(self) -> str:
        """Get symbol under head (pure function)."""
        return self.tape[self.head]


def create_initial_config(
    input_string: str,
    delta_function: DeltaFunction,
    initial_state: str = "q₀",
    accept_states: set[str] | None = None,
    reject_states: set[str] | None = None,
    blank_symbol: str = "□"
) -> TMConfiguration:
    """
    Create initial TM configuration from input (pure function).
    
    Returns an immutable configuration ready for execution.
    """
    blank = blank_symbol
    tape = tuple([blank] + list(input_string) + [blank] * 10)
    
    return TMConfiguration(
        tape=tape,
        head=1,
        state=initial_state,
        steps=0,
        blank=blank,
        delta=delta_function,
        accept_states=frozenset(accept_states or {"qₐ"}),
        reject_states=frozenset(reject_states or {"qᵣ"})
    )


def extend_tape_left(tape: tuple[str, ...], blank: str, amount: int = 10) -> tuple[str, ...]:
    """Extend tape to the left (pure function)."""
    return tuple([blank] * amount) + tape


def extend_tape_right(tape: tuple[str, ...], blank: str, amount: int = 10) -> tuple[str, ...]:
    """Extend tape to the right (pure function)."""
    return tape + tuple([blank] * amount)


def write_symbol(tape: tuple[str, ...], position: int, symbol: str) -> tuple[str, ...]:
    """Write symbol to tape at position (pure function, returns new tape)."""
    tape_list = list(tape)
    tape_list[position] = symbol
    return tuple(tape_list)


def step(config: TMConfiguration) -> TMConfiguration:
    """
    Execute one step of the TM (pure function).
    
    Takes a configuration and returns a new configuration after one transition.
    Does not mutate the input configuration.
    """
    # If halted, return same configuration
    if config.is_halted():
        return config
    
    # Get current symbol and apply delta function
    current_symbol = config.current_symbol()
    result = config.delta(config.state, current_symbol)
    
    # If delta returns None, transition to reject state
    if result is None:
        if config.reject_states:
            reject_state = next(iter(config.reject_states))
            return replace(config, state=reject_state)
        return config
    
    new_state, write_symbol_val, direction = result
    
    # Write to tape
    new_tape = write_symbol(config.tape, config.head, write_symbol_val)
    
    # Calculate new head position
    new_head = config.head + (1 if direction == "R" else -1)
    
    # Extend tape if needed
    if new_head >= len(new_tape):
        new_tape = extend_tape_right(new_tape, config.blank)
    elif new_head < 0:
        new_tape = extend_tape_left(new_tape, config.blank)
        new_head = 10
    
    # Return new configuration
    return TMConfiguration(
        tape=new_tape,
        head=new_head,
        state=new_state,
        steps=config.steps + 1,
        blank=config.blank,
        delta=config.delta,
        accept_states=config.accept_states,
        reject_states=config.reject_states
    )


def run_until_halt(config: TMConfiguration, max_steps: int | None = None) -> TMConfiguration:
    """
    Run TM until it halts (functional recursion with tail call optimization via iteration).
    
    Returns the final configuration.
    """
    current = config
    steps = 0
    
    while not current.is_halted():
        if max_steps is not None and steps >= max_steps:
            break
        current = step(current)
        steps += 1
    
    return current


def run_with_history(config: TMConfiguration, max_steps: int | None = None) -> list[TMConfiguration]:
    """
    Run TM and collect all configurations (pure function).
    
    Returns list of configurations at each step, useful for visualization.
    """
    history = [config]
    current = config
    steps = 0
    
    while not current.is_halted():
        if max_steps is not None and steps >= max_steps:
            break
        current = step(current)
        history.append(current)
        steps += 1
    
    return history


def display_config(config: TMConfiguration) -> None:
    """
    Display a configuration (side effect - not pure).
    
    Separated from pure computation logic.
    """
    tape_display = ""
    for i, symbol in enumerate(config.tape):
        if i == config.head:
            # Current head position - highlighted in yellow
            tape_display += colored(f" {symbol} ", "black", "on_light_yellow", attrs=['bold'])
        else:
            # Color scheme: lowercase=blue, uppercase=light green, blank=grey
            if symbol == config.blank:
                tape_display += colored(f" {symbol} ", "white", "on_grey")
            elif symbol.islower() and symbol.isalpha():
                tape_display += colored(f" {symbol} ", "white", "on_blue")
            elif symbol.isupper() and symbol.isalpha():
                tape_display += colored(f" {symbol} ", "black", "on_light_green")
            elif symbol.isdigit():
                tape_display += colored(f" {symbol} ", "white", "on_magenta")
            else:
                tape_display += colored(f" {symbol} ", "white", "on_grey")
    
    print(tape_display, end="")

    # Print step number and state
    if config.is_accepted():
        state_color = "green"
    elif config.is_halted():
        state_color = "red"
    else:
        state_color = "cyan"
    print(f" - Step {config.steps}: State = {colored(config.state, state_color, attrs=['bold'])}")


def run_animated(config: TMConfiguration, delay: float = 0.2, max_steps: int | None = None) -> TMConfiguration:
    """
    Run with animation (side effects for display and timing).
    
    Separates pure computation from I/O.
    """
    display_config(config)
    current = config
    steps = 0
    
    while not current.is_halted():
        if max_steps is not None and steps >= max_steps:
            break
        time.sleep(delay)
        current = step(current)
        display_config(current)
        steps += 1
    
    # Final result
    print()
    if current.is_accepted():
        print(colored("ACCEPTED", "green", attrs=['bold']))
    else:
        print(colored("REJECTED", "red", attrs=['bold']))
    print()
    
    return current