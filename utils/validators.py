"""
Deterministic input and state validators.
"""
from typing import List, Tuple, Dict, Any
import re

def sanitize_string(text: str, max_length: int = 120) -> str:
    """Sanitize player input to prevent injection or abnormal character lengths."""
    if not text:
        return ""
    clean = re.sub(r'[^\w\s\-\.,\'?!]', '', str(text)).strip()
    return clean[:max_length]

def validate_location_transition(current: str, target: str, available_locations: List[str]) -> Tuple[bool, str]:
    """Validates whether a proposed location movement is physically permissible."""
    if target not in available_locations:
        return False, f"Location '{target}' has not yet been discovered or charted."
    if current == target:
        return True, "Player remained in the current area."
    return True, f"Navigated successfully to {target}."

def validate_stat_bounds(val: int, min_val: int = 0, max_val: int = 100) -> int:
    """Clamps a numeric stat within valid fantasy world boundaries."""
    return max(min_val, min(max_val, int(val)))

def validate_preference_bounds(val: float) -> float:
    """Clamps an adaptive preference between 0.0 and 1.0."""
    return max(0.0, min(1.0, round(float(val), 2)))
