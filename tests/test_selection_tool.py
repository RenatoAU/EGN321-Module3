import pytest

from src.selection_tool import select_coefficient


def test_exact_lookup():
    pytest.skip("Use a known exact-row reference case.")


def test_interpolated_lookup():
    pytest.skip("Use a known interpolation reference case.")


def test_lower_boundary_accepted():
    pytest.skip("Prove the table minimum is accepted.")


def test_upper_boundary_accepted():
    pytest.skip("Prove the table maximum is accepted.")


def test_below_range_refused():
    with pytest.raises(ValueError):
        pytest.skip("Implement below-range refusal.")


def test_above_range_refused():
    with pytest.raises(ValueError):
        pytest.skip("Implement above-range refusal.")


def test_unknown_family_refused():
    with pytest.raises(ValueError):
        pytest.skip("Implement unknown-family refusal.")
