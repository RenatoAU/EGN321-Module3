"""
Linear interpolation helpers.
"""


def linear_interpolate(x, x1, y1, x2, y2):
    """Return the y-value at x between the two known points.

    The two known points are ``(x1, y1)`` and ``(x2, y2)``. Range checking is
    intentionally handled by ``select_coefficient`` because this helper only
    performs the interpolation calculation.
    """
    if x1 == x2:
        raise ValueError("x1 and x2 must be different for interpolation")

    # Find how far x is between x1 and x2, then apply that same fraction to y.
    fraction_between_points = (x - x1) / (x2 - x1)
    return y1 + fraction_between_points * (y2 - y1)
