from typing import TypeGuard

from ._constant import Constant, ConstantValue, is_constant_value
from ._identification import ColumnIdentifier, HasIdentifier
from ._operation import (
    ComparisonOperator,
    Condition,
    ConditionBound,
    Operation,
    OperationBound,
)

ColumnOperation = Operation[ColumnIdentifier]

# `isin` and combined conditions are not supported in UDAFs for now.
ColumnCondition = Condition[
    ColumnIdentifier,
    ComparisonOperator,
    ColumnIdentifier | ColumnOperation | Constant | None,
    None,
]


VariableColumnConvertible = (
    ColumnCondition | ColumnOperation | HasIdentifier[ColumnIdentifier]
)
ColumnConvertible = ConstantValue | VariableColumnConvertible


def _is_column_base_operation(value: ConditionBound | OperationBound, /) -> bool:
    return value._identifier_types == frozenset([ColumnIdentifier])


def is_column_condition(value: object, /) -> TypeGuard[ColumnCondition]:
    return isinstance(value, Condition) and _is_column_base_operation(value)


def is_column_operation(value: object, /) -> TypeGuard[ColumnOperation]:
    return isinstance(value, Operation) and _is_column_base_operation(value)


def is_column_condition_or_operation(
    value: object,
    /,
) -> TypeGuard[ColumnCondition | ColumnOperation]:
    return (
        is_column_condition(value)
        if isinstance(value, Condition)
        else is_column_operation(value)
    )


def is_non_constant_column_convertible(
    value: object,
    /,
) -> TypeGuard[VariableColumnConvertible]:
    return (
        isinstance(value._identifier, ColumnIdentifier)
        if isinstance(value, HasIdentifier)
        else is_column_condition_or_operation(value)
    )


def is_column_convertible(value: object, /) -> TypeGuard[ColumnConvertible]:
    return (
        is_non_constant_column_convertible(value)
        if isinstance(value, Condition | HasIdentifier | Operation)
        else is_constant_value(value)
    )
