import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit import DB

from abc import ABCMeta

_app = __revit__.Application  # noqa


class RevitVersion(object):
    _rvt_version = _app.VersionNumber
    _as_integer = int(_rvt_version)

    @classmethod
    def as_integer(cls):
        return cls._as_integer


class AbstractUnitType(object):
    """
    Abstract unit types across Revit versions.
    The type of physical quantity to be measured, for example length or force.

    since 2014: `DB.UnitType`\n
    since 2021: `DB.SpecTypeId`
    """
    pass


class AbstractUnitsOfMeasurement(object):
    """
    Abstract units of measurement across Revit versions.

    since 2014: `DB.DisplayUnitType`\n
    since 2021: `DB.UnitTypeId`
    """


class _CrossVersionRevitObject(object):

    __metaclass__ = ABCMeta

    _rvt_ver_num = RevitVersion.as_integer()


class _Definition(_CrossVersionRevitObject):
    def __init__(self, definition):
        # type: (DB.Definition) -> None
        self._definition = definition

    def get_unit_type(self):
        # type: () -> AbstractUnitType | DB.UnitType | DB.SpecTypeId
        if self._rvt_ver_num < 2021:
            return self._definition.UnitType

        if self._rvt_ver_num < 2022:
            return self._definition.GetSpecTypeId()

        return self._definition.GetDataType()


class _Parameter(_CrossVersionRevitObject):
    def __init__(self, parameter):
        # type: (DB.Parameter) -> None
        self._parameter = parameter

    def get_units_of_measure(self):
        # type: () -> AbstractUnitsOfMeasurement
        if self._rvt_ver_num < 2021:
            return self._parameter.DisplayUnitType
        return self._parameter.GetUnitTypeId()


class _FormatOptions(_CrossVersionRevitObject):
    def __init__(self, format_opts):
        # type: (DB.FormatOptions) -> None
        self._format_opts = format_opts

    def get_units_of_measure(self):
        # type: (DB.FormatOptions) -> AbstractUnitsOfMeasurement
        if RevitVersion.as_integer() < 2021:
            return self._format_opts.DisplayUnits
        return self._format_opts.GetUnitTypeId()


class _UnitUtils(_CrossVersionRevitObject):
    def __init__(self):
        self._unit_utils = DB.UnitUtils

    def is_unit_of_measure(self, unit_of_measure):
        # type: (AbstractUnitsOfMeasurement) -> bool
        if self._rvt_ver_num < 2021:
            return self._unit_utils.IsValidDisplayUnit()
        return self._unit_utils.IsUnit(unit_of_measure)

    def is_valid_unit_of_measure(self, unit_type, unit_of_measure):
        # type: (AbstractUnitType, AbstractUnitsOfMeasurement) -> bool
        if self._rvt_ver_num < 2021:
            return self._unit_utils.IsValidDisplayUnit(
                unit_type, unit_of_measure
            )
        return self._unit_utils.IsValidUnit(unit_type, unit_of_measure)


def definition(definition):
    # type: (DB.Definition) -> _Definition
    return _Definition(definition)


def format_options(format_opts):
    # type: (DB.FormatOptions) -> _FormatOptions
    return _FormatOptions(format_opts)


def parameter(parameter):
    # type: (DB.Parameter) -> _Parameter
    return _Parameter(parameter)


unit_utils = _UnitUtils()
