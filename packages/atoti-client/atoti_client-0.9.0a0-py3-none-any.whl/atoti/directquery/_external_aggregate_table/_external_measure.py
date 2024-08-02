from collections.abc import Sequence
from dataclasses import dataclass
from typing import final

from ..._identification import ColumnIdentifier, ExternalColumnIdentifier


@final
@dataclass(frozen=True, kw_only=True)
class ExternalMeasure:
    """Links the aggregated columns to their result."""

    aggregation_key: str
    granular_columns: Sequence[ColumnIdentifier]
    aggregate_columns: Sequence[ExternalColumnIdentifier]
