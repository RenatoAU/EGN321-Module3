import pytest

from src.interpolation import linear_interpolate


def test_midpoint_interpolation():
    """A point halfway between x1 and x2 should be halfway between y1 and y2."""
    result = linear_interpolate(
        x=25,
        x1=20,
        y1=100,
        x2=30,
        y2=140,
    )

    assert result == pytest.approx(120)


def test_non_midpoint_interpolation():
    """A point one quarter across the x-range should move one quarter in y."""
    result = linear_interpolate(
        x=12.5,
        x1=10,
        y1=4,
        x2=20,
        y2=8,
    )

    assert result == pytest.approx(5)


def test_repeated_x_values_are_rejected():
    """Equal x-values would cause division by zero and are invalid evidence."""
    with pytest.raises(ValueError, match="x1 and x2 must be different"):
        linear_interpolate(x=10, x1=5, y1=1, x2=5, y2=2)
