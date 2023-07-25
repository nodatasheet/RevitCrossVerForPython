# RevitCrossVerForPython
Revit API cross-version compatible library for python-like environment (IronPython, Python.net, etc).

## Description
Utilities that can be used to bypass changes in some methods across different versions of Revit API.

## Example of usage
```python
import revit_crossver as rcv

pipe_length_param = pipe.get_Parameter(DB.BuiltInParameter.CURVE_ELEM_LENGTH)

# getting type of unit for input parameter definition (e.g. Length)
unit_type = rcv.definition(pipe_length_param.Definition).get_unit_type()
# in Revit < 2021 returns DB.UnitType
# from Revit 2021 returns DB.SpecTypeId


# getting units of measure for input parameter (e.g. mm)
uom = rcv.parameter(pipe_length_param).get_units_of_measure()
# in Revit < 2021 returns DB.DisplayUnitType
# from Revit 2021 returns DB.UnitTypeId


# checking if units of measure are valid for selected unit type:
rcv.unit_utils.is_valid_unit_of_measure(unit_type, uom)
>>> True
```

## Compatibility
Initially made for [pyRevit](https://github.com/eirannejad/pyRevit), but can also be used in [RPS](https://github.com/architecture-building-systems/revitpythonshell) or other similar frameworks (with slight modifications).

Supposed to work in Revit versions 2018-2024.

**I don't have all Revit versions installed, so can not actually test all of them. Assumed methods are taken from [Revit API chm files](https://github.com/ADN-DevTech/revit-api-chms/).**
