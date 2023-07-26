# RevitCrossVerForPython
Revit API cross-version compatibility utils for Python.

## Description
Library for python-like environment (e.g. IronPython) with utilities that help to bypass changes in some methods across different versions of Revit API.

With this library you won't have to check every time ```if app.VersionNumber then ... elif then... ``` I did that for you ^_^

Just started, so it only has a few methods at the moment. Hopefully more methods coming soon.

## Example of usage
```python
import revit_crossver as rcv

pipe_length_param = pipe.get_Parameter(DB.BuiltInParameter.CURVE_ELEM_LENGTH)

# getting type of unit for input parameter definition (e.g. Length)
unit_type = rcv.definition(pipe_length_param.Definition).get_unit_type()
# in Revit < 2021 returns DB.UnitType
# starting Revit 2021 returns DB.SpecTypeId


# getting units of measure for input parameter (e.g. mm)
uom = rcv.parameter(pipe_length_param).get_units_of_measure()
# in Revit < 2021 returns DB.DisplayUnitType
# starting Revit 2021 returns DB.UnitTypeId


# checking if units of measure are valid for selected unit type:
rcv.unit_utils.is_valid_unit_of_measure(unit_type, uom)
>>> True
```

## Compatibility
Initially made for [pyRevit](https://github.com/eirannejad/pyRevit) using `IronPython 2.7` engine, but should also work in [RPS](https://github.com/architecture-building-systems/revitpythonshell) with `IronPython 3.4` or other similar frameworks (slight modifications may be required).

Supposed to work in Revit versions 2018-2024.

**I don't have all Revit versions installed, so can not actually test all of them. Assumed methods are taken from [Revit API chm files](https://github.com/ADN-DevTech/revit-api-chms/).**

## Other Notes
 - Methods naming will try to follow naming in Revit API as much as possible. I hope this helps to make my code more self-explanatory.
 - Some methods indicate abstract types of Data Transfer Objects as input or output. They intended to express the common abstract meaning of objects that became different type in Revit API. For example:
    ```python
    class AbstractUnitOfMeasure:
        """
        Abstract units of measure across Revit versions, e.g. millimeters for Length.

        since 2014: uses DB.DisplayUnitType Enumeration
        since 2021: uses DB.ForgeTypeId class as DB.UnitTypeId object
        """
    ```
    But those methods still consume and return Revit API objects.
 - Utilities in this library supposed to help with replaceable methods only. They are not supposed to expand existing methods or implement methods that do not have analog in Revit API releases between 2018 and 2024.
 - Methods marked by Revit API as `Obsolete` should not be implemented. Even if they still work, replacement methods must be used instead... at least I'll try to do so.
 - Have I heard about the Strategy pattern? Yes, I have :-)
