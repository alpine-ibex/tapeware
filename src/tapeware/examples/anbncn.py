# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

def delta_anbncn(state: str, symbol: str) -> tuple[str, str, str] | None:
    """
    Delta function for recognising aⁿbⁿcⁿ
    
    Strategy:
    - q₀: Find first unmarked 'a', mark it as 'X', go to q₁
    - q₁: Find first unmarked 'b', mark it as 'Y', go to q₂
    - q₂: Find first unmarked 'c', mark it as 'Z', go to q₃
    - q₃: Go back to beginning
    - q₄: Check if all marked, if so accept, else continue
    - qₐ: Accept state
    - qᵣ: Reject state
    """
    
    # State q₀: Initial state, look for first 'a'
    if state == "q₀":
        if symbol == "a":
            return ("q₁", "X", "R")  # Mark 'a' and look for 'b'
        elif symbol == "X":
            return ("q₀", "X", "R")  # Skip already marked 'a'
        elif symbol == "Y":
            return ("q₄", "Y", "R")  # No more 'a', check if done
        elif symbol == "□":
            return ("qₐ", "□", "R")  # Empty input, accept
        else:
            return None  # Reject
    
    # State q₁: Marked 'a', looking for 'b'
    elif state == "q₁":
        if symbol == "a":
            return ("q₁", "a", "R")  # Skip unmarked 'a'
        elif symbol == "X":
            return ("q₁", "X", "R")  # Skip marked 'a'
        elif symbol == "b":
            return ("q₂", "Y", "R")  # Mark 'b' and look for 'c'
        elif symbol == "Y":
            return ("q₁", "Y", "R")  # Skip marked 'b'
        else:
            return None  # No 'b' found, reject
    
    # State q₂: Marked 'b', looking for 'c'
    elif state == "q₂":
        if symbol == "b":
            return ("q₂", "b", "R")  # Skip unmarked 'b'
        elif symbol == "Y":
            return ("q₂", "Y", "R")  # Skip marked 'b'
        elif symbol == "c":
            return ("q₃", "Z", "L")  # Mark 'c' and go back
        elif symbol == "Z":
            return ("q₂", "Z", "R")  # Skip marked 'c'
        else:
            return None  # No 'c' found, reject
    
    # State q₃: Go back to beginning
    elif state == "q₃":
        if symbol in ["a", "b", "c", "X", "Y", "Z"]:
            return ("q₃", symbol, "L")  # Keep going left
        elif symbol == "□":
            return ("q₀", "□", "R")  # Reached beginning, start new cycle
    
    # State q₄: Check if all symbols are marked
    elif state == "q₄":
        if symbol == "Y":
            return ("q₄", "Y", "R")  # Skip marked 'b'
        elif symbol == "Z":
            return ("q₄", "Z", "R")  # Skip marked 'c'
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