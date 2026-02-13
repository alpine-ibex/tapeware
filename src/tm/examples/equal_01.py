"""
Simple example: Create a custom Turing machine that accepts strings with equal 0s and 1s.
"""

def delta_equal_01(state: str, symbol: str) -> tuple[str, str, str] | None:
    """
    Recognizes strings with equal number of 0s and 1s.
    
    Strategy:
    - Mark one '0' with 'X', mark one '1' with 'Y'
    - Repeat until all matched or mismatch
    """
    
    # Initial state: find first unmarked symbol
    if state == "q₀":
        if symbol == "0":
            return ("q₁", "X", "R")  # Mark '0', look for '1'
        elif symbol == "1":
            return ("q₂", "Y", "R")  # Mark '1', look for '0'
        elif symbol == "X":
            return ("q₀", "X", "R")  # Skip marked '0'
        elif symbol == "Y":
            return ("q₀", "Y", "R")  # Skip marked '1'
        elif symbol == "□":
            return ("qₐ", "□", "R")  # All matched, accept
    
    # Marked '0', looking for '1'
    elif state == "q₁":
        if symbol == "0":
            return ("q₁", "0", "R")
        elif symbol == "1":
            return ("q₃", "Y", "L")  # Found '1', mark it, go back
        elif symbol == "X":
            return ("q₁", "X", "R")
        elif symbol == "Y":
            return ("q₁", "Y", "R")
        elif symbol == "□":
            return None  # No '1' to match, reject
    
    # Marked '1', looking for '0'
    elif state == "q₂":
        if symbol == "1":
            return ("q₂", "1", "R")
        elif symbol == "0":
            return ("q₃", "X", "L")  # Found '0', mark it, go back
        elif symbol == "X":
            return ("q₂", "X", "R")
        elif symbol == "Y":
            return ("q₂", "Y", "R")
        elif symbol == "□":
            return None  # No '0' to match, reject
    
    # Go back to start
    elif state == "q₃":
        if symbol in ["0", "1", "X", "Y"]:
            return ("q₃", symbol, "L")
        elif symbol == "□":
            return ("q₀", "□", "R")
    
    # Accept state
    elif state == "qₐ":
        return ("qₐ", symbol, "R")
    
    return None
