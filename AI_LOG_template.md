# AI Usage Log — Module 3 Assignment 3.1

## AI Interaction

* **Tool used:** ChatGPT
* **Date:** September 17, 2026
* **Prompt:** Help me understand the lookup assignment, review the interpolation logic, and suggest appropriate tests and documentation.
* **AI assistance:** ChatGPT explained the interpolation formula, reviewed the assignment requirements, suggested a readable table structure, and produced an initial draft of parts of the code, tests, and documentation.
* **What I retained:** I retained the dictionary-based lookup tables, the interpolation equation, the supported-range validation, and several test ideas.
* **What I reviewed:** I reviewed the variable names, comments, table values, error messages, and expected test results before using them in the project.
* **How the result was verified:** The lookup values were compared with `VALVE_SELECTION_rev3.xlsx` and `valve_lookup_table.csv`. The interpolation results were compared with the workbook reference cases and hand calculations. The behavior was also checked using `pytest`.
* **Tests used as evidence:** The tests cover exact lookup, interpolation, lower and upper boundaries, below-range refusal, above-range refusal, and unsupported valve families.

## Reflection

A linear interpolation formula can calculate values outside the engineering table. For that reason, I checked that `select_coefficient()` validates the supported range before calling the interpolation function. Temperatures outside the table raise `ValueError` instead of returning an extrapolated coefficient.
