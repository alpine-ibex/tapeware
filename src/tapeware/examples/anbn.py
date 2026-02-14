# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


def delta(state: str, symbol: str) -> tuple[str, str, str] | None:
    """
    Delta function for recognising context-free language aⁿbⁿ

    Strategy:
    - q₀: Find first unmarked 'a', mark it as 'A', go to q₁
    - q₁: Find first unmarked 'b', mark it as 'B', go to q₂
    - q₂: Go back to left until we find 'A', go to q₀
    - q₃: Check if all symbols are marked, if so accept, else continue
    - qₐ: Accept state
    - qᵣ: Reject state
    """

    # State q₀: Initial state, look for first 'a'
    if state == "q₀":
        if symbol == "a":
            return ("q₁", "A", "R")  # Mark 'a' and look for 'b'
        else:
            return ("q₃", symbol, "R")  # No 'a' found, check if done

    # State q₁: Marked 'a', looking for 'b'
    elif state == "q₁":
        if symbol in ["a", "B"]:
            return ("q₁", symbol, "R")  # Skip unmarked 'a' and marked 'b'
        elif symbol == "b":
            return ("q₂", "B", "L")  # Mark 'b' and look for 'a'
        else:
            return None  # No 'b' found, reject

    # State q₂: Go back to left until we find 'A'
    elif state == "q₂":
        if symbol in ["a", "B"]:
            return ("q₂", symbol, "L")  # Keep going left
        if symbol == "A":
            return ("q₀", "A", "R")  # Found marked 'a', go back to q₀
        else:
            return None  # No 'A' found, reject

    # State q₃: Check if all symbols are marked
    elif state == "q₃":
        if symbol == "B":
            return ("q₃", "B", "R")  # Skip marked 'b'
        elif symbol == "□":
            return ("qₐ", "□", "R")  # All marked, accept
        else:
            return None  # Found unmarked symbol, reject

    # Accept state
    elif state == "qₐ":
        return ("qₐ", symbol, "R")

    # Reject state
    elif state == "qᵣ":
        return ("qᵣ", symbol, "R")

    return None


test_cases = (
    ("", True),  # n=0
    ("ab", True),  # n=1
    ("aabb", True),  # n=2
    ("aaabbb", True),  # n=3
    ("aab", False),  # unequal
    ("aabbb", False),  # unequal
    ("aaabb", False),  # unequal
)
