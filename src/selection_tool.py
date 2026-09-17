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

from numbers import Real

from src.interpolation import linear_interpolate
from src.lookup_tables import LOOKUP_TABLES


def select_coefficient(valve_family, temperature_c):
    """Select a coefficient for a valve family and operating temperature.

    Exact table temperatures return their listed coefficient. A temperature
    between two rows uses linear interpolation. The function raises
    ``ValueError`` for an unknown family or a temperature outside the selected
    family's supported range because extrapolation is not allowed.

    Returns:
        dict: The input, coefficient, calculation method, evidence points,
        and supported temperature range.
    """
    # The valve family is the first lookup criterion.
    if valve_family not in LOOKUP_TABLES:
        raise ValueError(f"Unsupported valve_family: {valve_family}")

    # Reject values that cannot represent an engineering temperature.
    if isinstance(temperature_c, bool) or not isinstance(temperature_c, Real):
        raise TypeError("temperature_c must be a real number")

    table = LOOKUP_TABLES[valve_family]
    minimum_temp = table[0][0]
    maximum_temp = table[-1][0]
    supported_range = (minimum_temp, maximum_temp)

    # Refuse extrapolation before looking for exact or surrounding rows.
    if temperature_c < minimum_temp:
        raise ValueError(
            f"temperature_c {temperature_c} is below "
            f"the supported minimum {minimum_temp}"
        )

    if temperature_c > maximum_temp:
        raise ValueError(
            f"temperature_c {temperature_c} exceeds "
            f"the supported maximum {maximum_temp}"
        )

    # An exact table row is direct evidence, so no interpolation is needed.
    for point in table:
        table_temperature, coefficient = point
        if temperature_c == table_temperature:
            return {
                "valve_family": valve_family,
                "temperature_c": temperature_c,
                "coefficient": coefficient,
                "method": "exact",
                "lower_point": point,
                "upper_point": point,
                "supported_range": supported_range,
            }

    # Compare each neighboring pair until the requested temperature is found.
    for lower_point, upper_point in zip(table, table[1:]):
        lower_temp, lower_coefficient = lower_point
        upper_temp, upper_coefficient = upper_point

        if lower_temp < temperature_c < upper_temp:
            coefficient = linear_interpolate(
                x=temperature_c,
                x1=lower_temp,
                y1=lower_coefficient,
                x2=upper_temp,
                y2=upper_coefficient,
            )

            return {
                "valve_family": valve_family,
                "temperature_c": temperature_c,
                "coefficient": coefficient,
                "method": "interpolation",
                "lower_point": lower_point,
                "upper_point": upper_point,
                "supported_range": supported_range,
            }

    # Reaching this point means the source table is empty, unsorted, or has a gap.
    raise RuntimeError("No surrounding table rows were found for the request")

