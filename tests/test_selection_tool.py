import pytest

from src.selection_tool import select_coefficient


def test_exact_lookup_vx100():
    """A listed VX-100 row should return the table value unchanged."""
    result = select_coefficient("VX-100", 40)

    assert result["coefficient"] == pytest.approx(0.93)
    assert result["method"] == "exact"
    assert result["lower_point"] == (40, 0.93)
    assert result["upper_point"] == (40, 0.93)


def test_exact_lookup_vx200():
    """A second family proves that family selection occurs before lookup."""
    result = select_coefficient("VX-200", 90)

    assert result["coefficient"] == pytest.approx(1.54)
    assert result["method"] == "exact"


def test_interpolated_lookup_vx100_reference_case():
    """The workbook states that VX-100 at 50 C should produce 0.96."""
    result = select_coefficient("VX-100", 50)

    assert result["coefficient"] == pytest.approx(0.96)
    assert result["method"] == "interpolation"
    assert result["lower_point"] == (40, 0.93)
    assert result["upper_point"] == (60, 0.99)


def test_interpolated_lookup_vx200_reference_case():
    """The workbook states that VX-200 at 65 C should produce 1.36."""
    result = select_coefficient("VX-200", 65)

    assert result["coefficient"] == pytest.approx(1.36)
    assert result["method"] == "interpolation"
    assert result["lower_point"] == (50, 1.27)
    assert result["upper_point"] == (70, 1.39)


def test_interpolated_lookup_vx300_reference_case():
    """The third workbook reference case checks another table and interval."""
    result = select_coefficient("VX-300", 62.5)

    assert result["coefficient"] == pytest.approx(1.63)
    assert result["method"] == "interpolation"


def test_lower_boundary_accepted():
    """The minimum supported temperature is valid and is not extrapolation."""
    result = select_coefficient("VX-100", 20)

    assert result["coefficient"] == pytest.approx(0.88)
    assert result["method"] == "exact"
    assert result["supported_range"] == (20, 100)


def test_upper_boundary_accepted():
    """The maximum supported temperature is also a valid exact row."""
    result = select_coefficient("VX-300", 125)

    assert result["coefficient"] == pytest.approx(2.12)
    assert result["method"] == "exact"
    assert result["supported_range"] == (25, 125)


def test_below_range_refused():
    """A request below the table must not produce an extrapolated number."""
    with pytest.raises(ValueError, match="supported minimum 20"):
        select_coefficient("VX-100", 5)


def test_above_range_refused():
    """A request above the table must not produce an extrapolated number."""
    with pytest.raises(ValueError, match="supported maximum 90"):
        select_coefficient("VX-200", 95)


def test_unknown_family_refused():
    """The program must not silently substitute a supported valve family."""
    with pytest.raises(ValueError, match="Unsupported valve_family: VX-999"):
        select_coefficient("VX-999", 50)


def test_structured_result_contains_explanation_fields():
    """The returned dictionary should explain the evidence behind the result."""
    result = select_coefficient("VX-200", 65)

    assert result == {
        "valve_family": "VX-200",
        "temperature_c": 65,
        "coefficient": pytest.approx(1.36),
        "method": "interpolation",
        "lower_point": (50, 1.27),
        "upper_point": (70, 1.39),
        "supported_range": (10, 90),
    }

