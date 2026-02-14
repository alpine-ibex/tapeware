# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

def delta_end_ab(state: str, symbol: str) -> tuple[str, str, str] | None:
    """Simple TM that accepts strings ending with 'ab'."""
    
    if state == "q₀":
        if symbol == "a":
            return ("q₁", "a", "R")
        elif symbol == "b":
            return ("q₀", "b", "R")
        elif symbol == "□":
            return ("qᵣ", "□", "R")  # Empty or doesn't end with 'ab'
    
    elif state == "q₁":
        if symbol == "a":
            return ("q₁", "a", "R")  # Stay in q1 (last was 'a')
        elif symbol == "b":
            return ("q₂", "b", "R")  # Saw 'ab', move to q2
        elif symbol == "□":
            return ("qᵣ", "□", "R")  # Ends with 'a', reject
    
    elif state == "q₂":
        if symbol == "a":
            return ("q₁", "a", "R")  # New 'a', back to q1
        elif symbol == "b":
            return ("q₀", "b", "R")  # Another 'b', back to q0
        elif symbol == "□":
            return ("qₐ", "□", "R")  # Ended with 'ab', accept!
    
    elif state == "qₐ":
        return ("qₐ", symbol, "R")
    
    elif state == "qᵣ":
        return ("qᵣ", symbol, "R")
    
    return None

test_cases = (
    ("ab", True),
    ("aab", True),
    ("bab", True),
    ("aaab", True),
    ("abab", True),
    ("ba", False),
    ("", False),
)