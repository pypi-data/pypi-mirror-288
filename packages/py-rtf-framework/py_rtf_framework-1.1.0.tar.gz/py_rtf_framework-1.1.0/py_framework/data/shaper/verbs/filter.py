#
# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project.
#
"""Filter verb implementation."""

import logging
from collections.abc import Callable
from functools import partial
from typing import Any, cast
from uuid import uuid4

import pandas as pd

from py_framework.data.shaper.errors import UnsupportedComparisonOperatorError

from .callbacks import VerbCallbacks
from .decorators import ParallelizationMode, parallel_verb
from .types import (
    BooleanComparisonOperator,
    BooleanLogicalOperator,
    ComparisonStrategy,
    FilterArgs,
    NumericComparisonOperator,
    StringComparisonOperator,
    Table,
)

log = logging.getLogger(__name__)


@parallel_verb(
    name="filter",
    treats_input_tables_as_immutable=True,
    parallelization_mode=ParallelizationMode.CHUNK,
)
async def filter_verb(
    chunk: Table,
    callbacks: VerbCallbacks,  # noqa: ARG001 - use ds verb name
    column: str,
    value: Any,
    strategy: ComparisonStrategy = ComparisonStrategy.Value,
    operator: StringComparisonOperator = StringComparisonOperator.Equals,
    **_kwargs: Any,
) -> Table:
    """Filter verb implementation."""
    input_table = cast(pd.DataFrame, chunk)

    filter_index = filter(
        input_table,
        FilterArgs(
            column,
            value=value,
            strategy=ComparisonStrategy(strategy),
            operator=get_comparison_operator(operator),
        ),
    )
    sub_idx = filter_index == True  # noqa: E712
    idx = filter_index[sub_idx].index  # type: ignore
    result = input_table[chunk.index.isin(idx)].reset_index(drop=True)
    return cast(Table, result)


def filter(df: pd.DataFrame, args: FilterArgs) -> pd.DataFrame | pd.Series:  # noqa A001 - use ds verb name
    """Filter a DataFrame based on the input criteria."""
    filters: list[str] = []
    filtered_df: pd.DataFrame = df.copy()

    filter_name = str(uuid4())
    filters.append(filter_name)
    if args.strategy == ComparisonStrategy.Column:
        filtered_df[filter_name] = _operator_map[args.operator](
            df=df, column=args.column, target=df[args.value]
        )
        if args.operator not in _empty_comparisons:
            __correct_unknown_value(filtered_df, [args.column, args.value], filter_name)
    else:
        filtered_df[filter_name] = _operator_map[args.operator](
            df=df, column=args.column, target=args.value
        )

    filtered_df["dwc_filter_result"] = boolean_function_map[BooleanLogicalOperator.OR](
        filtered_df[filters], ""
    )

    __correct_unknown_value(filtered_df, filters, "dwc_filter_result")

    return filtered_df["dwc_filter_result"]


boolean_function_map = {
    BooleanLogicalOperator.OR: lambda df, columns: df[columns].any(axis="columns")
    if columns != ""
    else df.any(axis="columns"),
    BooleanLogicalOperator.AND: lambda df, columns: df[columns].all(axis="columns")
    if columns != ""
    else df.all(axis="columns"),
    BooleanLogicalOperator.NOR: lambda df, columns: ~df[columns].any(axis="columns")
    if columns != ""
    else ~df.any(axis="columns"),
    BooleanLogicalOperator.NAND: lambda df, columns: ~df[columns].all(axis="columns")
    if columns != ""
    else ~df.all(axis="columns"),
    BooleanLogicalOperator.XNOR: lambda df, columns: df[columns]
    .sum(axis="columns")
    .apply(lambda x: (x % 2) == 0 or x == 0)
    if columns != ""
    else df.sum(axis="columns").apply(lambda x: (x % 2) == 0 or x == 0),
    BooleanLogicalOperator.XOR: lambda df, columns: df[columns]
    .sum(axis="columns")
    .apply(lambda x: (x % 2) != 0 and x != 0)
    if columns != ""
    else df.sum(axis="columns").apply(lambda x: (x % 2) != 0 and x != 0),
}


def __correct_unknown_value(df: pd.DataFrame, columns: list[str], target: str) -> None:
    na_index = df[df[columns].isna().any(axis=1)].index
    df.loc[na_index, target] = None


def __equals(
    df: pd.DataFrame,
    column: str,
    target: pd.Series | str | float | bool,
    **_kwargs: dict,
) -> pd.Series:
    return df[column] == target


def __not_equals(
    df: pd.DataFrame,
    column: str,
    target: pd.Series | str | float | bool,
    **_kwargs: dict,
) -> pd.Series:
    return ~df[column] == target


def __is_null(
    df: pd.DataFrame, column: str, **_kwargs: dict
) -> pd.DataFrame | pd.Series:
    return df[column].isna()


def __is_not_null(
    df: pd.DataFrame, column: str, **_kwargs: dict
) -> pd.DataFrame | pd.Series:
    return df[column].notna()


def __contains(
    df: pd.DataFrame,
    column: str,
    target: pd.Series | str | float | bool,
    **_kwargs: dict,
) -> pd.DataFrame | pd.Series:
    return df[column].str.contains(str(target), regex=False)


def __startswith(
    df: pd.DataFrame,
    column: str,
    target: pd.Series | str | float | bool,
    **_kwargs: dict,
) -> pd.DataFrame | pd.Series:
    return df[column].str.startswith(str(target))


def __endswith(
    df: pd.DataFrame,
    column: str,
    target: pd.Series | str | float | bool,
    **_kwargs: dict,
) -> pd.Series:
    return df[column].str.endswith(str(target))


def __regex(
    df: pd.DataFrame,
    column: str,
    target: pd.Series | str | float | bool,
    **_kwargs: dict,
) -> pd.Series:
    return df[column].str.contains(str(target), regex=True)


def __gt(
    df: pd.DataFrame,
    column: str,
    target: pd.Series | str | float | bool,
    **_kwargs: dict,
) -> pd.Series:
    return df[column] > target


def __gte(
    df: pd.DataFrame,
    column: str,
    target: pd.Series | str | float | bool,
    **_kwargs: dict,
) -> pd.Series:
    return df[column] >= target


def __lt(
    df: pd.DataFrame,
    column: str,
    target: pd.Series | str | float | bool,
    **_kwargs: dict,
) -> pd.Series:
    return df[column] < target


def __lte(
    df: pd.DataFrame,
    column: str,
    target: pd.Series | str | float | bool,
    **_kwargs: dict,
) -> pd.Series:
    return df[column] <= target


_empty_comparisons = {
    StringComparisonOperator.IsEmpty,
    StringComparisonOperator.IsNotEmpty,
    NumericComparisonOperator.IsEmpty,
    NumericComparisonOperator.IsNotEmpty,
    BooleanComparisonOperator.IsEmpty,
    BooleanComparisonOperator.IsNotEmpty,
}


_operator_map: dict[
    StringComparisonOperator | NumericComparisonOperator | BooleanComparisonOperator,
    Callable,
] = {
    StringComparisonOperator.Contains: __contains,
    StringComparisonOperator.StartsWith: __startswith,
    StringComparisonOperator.EndsWith: __endswith,
    StringComparisonOperator.Equals: __equals,
    StringComparisonOperator.NotEqual: __not_equals,
    StringComparisonOperator.IsEmpty: __is_null,
    StringComparisonOperator.IsNotEmpty: __is_not_null,
    StringComparisonOperator.RegularExpression: __regex,
    NumericComparisonOperator.Equals: __equals,
    NumericComparisonOperator.IsEmpty: __is_null,
    NumericComparisonOperator.IsNotEmpty: __is_not_null,
    NumericComparisonOperator.GreaterThan: __gt,
    NumericComparisonOperator.GreaterThanOrEqual: __gte,
    NumericComparisonOperator.LessThan: __lt,
    NumericComparisonOperator.LessThanOrEqual: __lte,
    BooleanComparisonOperator.Equals: __equals,
    BooleanComparisonOperator.NotEqual: __not_equals,
    BooleanComparisonOperator.IsEmpty: __is_null,
    BooleanComparisonOperator.IsNotEmpty: __is_not_null,
    BooleanComparisonOperator.IsTrue: partial(__equals, target=True),
    BooleanComparisonOperator.IsFalse: partial(__equals, target=False),
}


def get_comparison_operator(
    operator: str,
) -> StringComparisonOperator | NumericComparisonOperator | BooleanComparisonOperator:
    """Get a comparison operator based on the input string."""
    try:
        return StringComparisonOperator(operator)
    except Exception:
        log.info("%s is not a string comparison operator", operator)
    try:
        return NumericComparisonOperator(operator)
    except Exception:
        log.info("%s is not a numeric comparison operator", operator)
    try:
        return BooleanComparisonOperator(operator)
    except Exception:
        log.info("%s is not a boolean comparison operator", operator)
    raise UnsupportedComparisonOperatorError(operator)
