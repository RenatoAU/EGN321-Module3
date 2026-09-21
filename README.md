# Module 3 Lookup Tool

## Purpose

This Python tool selects an engineering coefficient using two inputs:

1. The valve family.
2. The operating temperature in degrees Celsius.

If the temperature exactly matches a row in the selected table, the tool returns the listed coefficient. If the temperature is between two rows, it calculates the coefficient using linear interpolation. The tool refuses temperatures outside the supported range.

## Source Data

The engineering data comes from the `Engineering Tables` worksheet in the course-provided `VALVE_SELECTION_rev3.xlsx` workbook. The same values are also available in `data/valve_lookup_table.csv`.

The data is represented as readable Python lists inside the `LOOKUP_TABLES` dictionary in `src/lookup_tables.py`. This keeps the engineering data separate from the selection and interpolation logic.

## Supported Valve Families

| Family | Minimum Temperature | Maximum Temperature |
| ------ | ------------------: | ------------------: |
| VX-100 |                20°C |               100°C |
| VX-200 |                10°C |                90°C |
| VX-300 |                25°C |               125°C |

The minimum and maximum temperatures are valid exact table rows.

## Lookup Behavior

The `select_coefficient()` function follows these steps:

1. It checks whether the requested valve family exists.
2. It selects the table for that valve family.
3. It determines the minimum and maximum supported temperatures.
4. It refuses the request if the temperature is outside that range.
5. It checks whether the temperature exactly matches a table row.
6. If there is no exact match, it finds the nearest lower and upper rows.
7. It uses those two rows to calculate the coefficient with linear interpolation.

### Exact Lookup

If the requested temperature exactly matches a table row, the listed coefficient is returned without interpolation.

For example, `VX-100` at `40°C` returns `0.93`.

### Surrounding-Row Search

For a temperature that is inside the supported range but does not exactly match a row, the program searches consecutive table points until it finds:

* The closest lower temperature.
* The closest upper temperature.

For example, `VX-200` at `65°C` uses the points `(50, 1.27)` and `(70, 1.39)`.

### Interpolation

After finding the surrounding rows, the program passes those points to the `linear_interpolate()` function.

For `VX-200` at `65°C`, the interpolated coefficient is approximately `1.36`.

### Refusal to Extrapolate

The program does not calculate a coefficient below the minimum or above the maximum supported temperature. It raises `ValueError` instead of returning an unsupported engineering value.

## Interpolation Formula

The tool uses the linear interpolation equation:

```text
y = y1 + ((x - x1) / (x2 - x1)) * (y2 - y1)
```

The variables represent:

* `x`: Requested operating temperature.
* `x1`: Lower known temperature.
* `x2`: Upper known temperature.
* `y1`: Coefficient at the lower temperature.
* `y2`: Coefficient at the upper temperature.
* `y`: Interpolated coefficient.

The interpolation function performs the mathematical calculation. Range validation is handled by `select_coefficient()` before the interpolation function is called.

## Refusal Behavior

### Below the Supported Range

```python
select_coefficient("VX-100", 5)
```

Expected error:

```text
ValueError: temperature_c 5 is below the supported minimum 20
```

### Above the Supported Range

```python
select_coefficient("VX-200", 95)
```

Expected error:

```text
ValueError: temperature_c 95 exceeds the supported maximum 90
```

### Unsupported Valve Family

```python
select_coefficient("VX-999", 50)
```

Expected error:

```text
ValueError: Unsupported valve_family: VX-999
```

## Testing

The automated test suite uses `pytest` and includes:

* Independent midpoint interpolation tests.
* Independent non-midpoint interpolation tests.
* Exact lookup tests for different valve families.
* Interpolation tests based on workbook reference cases.
* A lower-boundary test.
* An upper-boundary test.
* A below-range refusal test.
* An above-range refusal test.
* An unsupported-family refusal test.
* A test that checks the structured result.

The expected coefficients come from the workbook reference cases, the engineering table, or independent hand calculations. The function being tested is not used to generate its own expected answers.

## Running Tests

Open the terminal in the main project folder containing `README.md`, `src`, and `tests`.

Install the required dependency:

```bash
python -m pip install pytest
```

Run the complete test suite:

```bash
python -m pytest -v
```

Run only the interpolation tests:

```bash
python -m pytest tests/test_interpolation.py -v
```

Do not run `test_interpolation.py` directly because it is designed to be executed by `pytest`.

## Assumptions

* All operating temperatures use degrees Celsius.
* The course-provided engineering table is the authoritative data source.
* The temperatures in each valve-family table are arranged from lowest to highest.
* Each valve family has at least two valid table points.
* Exact table values should be returned without interpolation.
* Linear interpolation is valid only between adjacent supported table points.
* Temperatures outside the documented range are unsupported.

## Known Limitations

* The tool supports only `VX-100`, `VX-200`, and `VX-300`.
* The program does not extrapolate outside the engineering table.
* New valve families must be added manually to `LOOKUP_TABLES`.
* The tool does not replace professional engineering review.
* The tool accepts temperatures only as numeric values.

## AI Use

ChatGPT was used to help review the assignment requirements, explain the interpolation process, organize the documentation, and suggest test cases. The table values and expected results were checked against the assigned workbook, CSV data, reference cases, and automated tests. More information is recorded in `AI_LOG.md`.


## AI Use
If AI was used, summarize it here and provide details in AI_LOG.md.
