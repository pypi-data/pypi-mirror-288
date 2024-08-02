from __future__ import annotations

from typing import cast, overload

from .._identification import ColumnIdentifier, HasIdentifier
from .._measure.calculated_measure import AggregatedMeasure
from .._measure.column_measure import ColumnMeasure
from .._measure.level_measure import LevelMeasure
from .._measure.udaf_measure import UdafMeasure
from .._measure_convertible import VariableMeasureConvertible
from .._measure_description import MeasureDescription
from ..scope._scope import Scope
from ._utils import (
    VariableColumnConvertibleOrLevel,
    is_non_constant_column_convertible_or_level,
)


@overload
def agg(
    operand: VariableColumnConvertibleOrLevel,
    /,
    *,
    plugin_key: str,
) -> MeasureDescription: ...


@overload
def agg(
    operand: VariableMeasureConvertible,
    /,
    *,
    plugin_key: str,
    scope: Scope,
) -> MeasureDescription: ...


def agg(
    operand: VariableColumnConvertibleOrLevel | VariableMeasureConvertible,
    /,
    *,
    plugin_key: str,
    scope: Scope | None = None,
) -> MeasureDescription:
    if is_non_constant_column_convertible_or_level(operand):
        if scope:
            raise ValueError(
                "The passed operand has an intrinsic scope, no other scope can be specified.",
            )

        if isinstance(operand, HasIdentifier):
            identifier = operand._identifier

            return (
                ColumnMeasure(
                    _column_identifier=identifier,
                    _plugin_key=plugin_key,
                )
                if isinstance(identifier, ColumnIdentifier)
                else AggregatedMeasure(
                    _underlying_measure=LevelMeasure(
                        # Pyright is able to check that `identifier` is of type `LevelIdentifier` but mypy cannot.
                        identifier,  # type: ignore[arg-type]
                    ),
                    _plugin_key=plugin_key,
                    _on_levels=[
                        # Pyright is able to check that `identifier` is of type `LevelIdentifier` but mypy cannot.
                        identifier,  # type: ignore[list-item]
                    ],
                )
            )

        return UdafMeasure(_plugin_key=plugin_key, _operation=operand)

    operand = cast(VariableMeasureConvertible, operand)

    if not scope:
        raise ValueError("The passed operand requires a scope to be specified.")

    return scope._create_measure_description(operand, plugin_key=plugin_key)
