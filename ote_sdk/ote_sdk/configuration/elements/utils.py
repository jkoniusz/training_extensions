# INTEL CONFIDENTIAL
#
# Copyright (C) 2021 Intel Corporation
#
# This software and the related documents are Intel copyrighted materials, and
# your use of them is governed by the express license under which they were provided to
# you ("License"). Unless the License provides otherwise, you may not use, modify, copy,
# publish, distribute, disclose or transmit this software or the related documents
# without Intel's prior written permission.
#
# This software and the related documents are provided as is,
# with no express or implied warranties, other than those that are expressly stated
# in the License.


"""
This module contains utility functions to use with the attr package, concerning for instance parameter validation
or serialization. They are used within the ote_config_helper or the configuration elements.
"""

from enum import Enum
from typing import Callable, List, Optional, Type, TypeVar, Union

from attr import Attribute

from ote_sdk.configuration.elements.configurable_enum import ConfigurableEnum
from ote_sdk.configuration.elements.parameter_group import ParameterGroup
from ote_sdk.entities.id import ID

NumericTypeVar = TypeVar("NumericTypeVar", int, float)
SelectableTypeVar = TypeVar("SelectableTypeVar", float, str)
ConfigurableEnumTypeVar = TypeVar("ConfigurableEnumTypeVar", bound=ConfigurableEnum)


def attr_enum_to_str_serializer(
    instance: object,  # pylint: disable=unused-argument
    attribute: Attribute,  # pylint: disable=unused-argument
    value: Union[Enum, str],
) -> str:
    """
    This function converts Enums to their string representation. It is used when converting between yaml and python
    object representation of the configuration. The function signature matches what is expected by the
    `attr.asdict` value_serializer argument.
    """
    if isinstance(value, Enum):
        return str(value)
    return value


def _convert_enum_selectable_value(
    value: Union[str, ConfigurableEnumTypeVar],
    enum_class: Type[ConfigurableEnumTypeVar],
) -> ConfigurableEnumTypeVar:
    """
    Helper function that converts the input value to an instance of the correct ConfigurableEnum

    :param value: input value to convert
    :param enum_class: Type of the Enum to convert to
    """
    if isinstance(value, str):
        try:
            enum_value = enum_class(value)
        except ValueError as ex:
            raise ValueError(
                f"The value {value} is an invalid option for {enum_class.__name__}. Valid options are:"
                f" {enum_class.get_values()}"
            ) from ex
        return enum_value
    return value


def construct_attr_enum_selectable_converter(
    default_value: ConfigurableEnumTypeVar,
) -> Callable[[Union[str, ConfigurableEnumTypeVar]], ConfigurableEnumTypeVar]:
    """
    This function converts an input value to the correct instance of the ConfigurableEnum. It is used when
    initializing a selectable parameter

    :param default_value: Default value for the selectable
    """
    enum_class = type(default_value)

    def attr_convert_enum_selectable_value(
        value: Union[str, ConfigurableEnumTypeVar]
    ) -> ConfigurableEnumTypeVar:
        """
        Function that converts an input value to an instance of the appropriate ConfigurableEnum. Can be used as a
        `converter` for attrs.Attributes of type ConfigurableEnum

        :param value: Value to convert to ConfigurableEnum instance
        """
        return _convert_enum_selectable_value(value, enum_class=enum_class)

    return attr_convert_enum_selectable_value


def construct_attr_enum_selectable_onsetattr(
    default_value: ConfigurableEnumTypeVar,
) -> Callable[
    [ParameterGroup, Attribute, Union[str, ConfigurableEnumTypeVar]],
    ConfigurableEnumTypeVar,
]:
    """
    This function converts an input value to the correct instance of the ConfigurableEnum. It is used when
    setting a value for a selectable parameter.

    :param default_value: Default value for the enum_selectable
    """
    enum_class = type(default_value)

    def attr_convert_enum_selectable_value(
        instance: ParameterGroup,  # pylint: disable=unused-argument
        attribute: Attribute,  # pylint: disable=unused-argument
        value: Union[str, ConfigurableEnumTypeVar],
    ) -> ConfigurableEnumTypeVar:
        """
        Function that converts an input value to an instance of the appropriate ConfigurableEnum. Can be used with
        the `on_setattr` hook of the attrs package
        """
        return _convert_enum_selectable_value(value, enum_class=enum_class)

    return attr_convert_enum_selectable_value


def construct_attr_value_validator(
    min_value: NumericTypeVar, max_value: NumericTypeVar
) -> Callable[[ParameterGroup, Attribute, NumericTypeVar], None]:
    """
    Constructs a validator function that is used in the attribute validation of numeric configurable parameters
    """

    def attr_validate_value(
        instance: ParameterGroup, attribute: Attribute, value: NumericTypeVar
    ):  # pylint: disable=unused-argument
        """
        This function is used to validate values for numeric ConfigurableParameters
        """
        if not min_value <= value <= max_value:
            raise ValueError(
                f"Invalid value set for {attribute.name}: {value} is out of bounds."
            )

    return attr_validate_value


def construct_attr_selectable_validator(
    options: List[SelectableTypeVar],
) -> Callable[[ParameterGroup, Attribute, SelectableTypeVar], None]:
    """
    Constructs a validator function that is used in the attribute validation of selectable configurable parameters
    """

    def attr_validate_selectable(
        instance: ParameterGroup, attribute: Attribute, value: SelectableTypeVar
    ):  # pylint: disable=unused-argument
        """
        This function is used to validate values for selectable ConfigurableParameters
        """
        if value not in options:
            raise ValueError(
                f"Invalid value set for {attribute.name}: {value} is not a valid option for this "
                f"parameter."
            )

    return attr_validate_selectable


def convert_string_to_id(id_string: Optional[Union[str, ID]]) -> ID:
    """
    This function converts an input string representing an ID into an OTE SDK ID object.
    Inputs that are already in the form of an ID are left untouched.

    :param id_string: string, ID or None object that should be converted to an ID
    :return: the input as an instance of ID
    """
    if id_string is None:
        output_id = ID()
    elif isinstance(id_string, str):
        output_id = ID(id_string)
    else:
        output_id = id_string
    return output_id