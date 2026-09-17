"""
Validated lookup / interpolation tool.

Required behavior:
1. Validate valve family.
2. Identify that family's supported temperature range.
3. Refuse values outside the range.
4. Return exact table value when temperature matches a row.
5. Otherwise locate surrounding rows and interpolate.
6. Return useful details about how the result was produced.
"""

from src.interpolation import linear_interpolate
from src.lookup_tables import LOOKUP_TABLES


def select_coefficient(valve_family, temperature_c):
    # TODO: validate family
    # TODO: get the correct table
    # TODO: determine min/max supported temperature
    # TODO: refuse extrapolation with ValueError
    # TODO: return exact match if available
    # TODO: find lower and upper surrounding rows
    # TODO: interpolate
    # TODO: return a structured result
    raise NotImplementedError("Implement select_coefficient().")
