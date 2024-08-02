from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping, Set as AbstractSet
from typing import Final, Protocol

from .._constant import Constant
from .._data_type import DataType
from .._identification import TableIdentifier


class LoadDataIntoTable(Protocol):
    def __call__(
        self,
        identifier: TableIdentifier,
        source_key: str,
        source_params: Mapping[str, object],
        /,
        *,
        scenario_name: str | None,
    ) -> None: ...


class InferTypes(Protocol):
    def __call__(
        self,
        source_key: str,
        source_params: Mapping[str, object],
        /,
        *,
        keys: AbstractSet[str],
        default_values: Mapping[str, Constant | None],
    ) -> dict[str, DataType]: ...


class DataSource(ABC):
    def __init__(self, *, load_data_into_table: LoadDataIntoTable) -> None:
        self._load_data_into_table: Final = load_data_into_table

    @property
    @abstractmethod
    def key(self) -> str: ...

    def load_data_into_table(
        self,
        identifier: TableIdentifier,
        source_params: Mapping[str, object],
        /,
        *,
        scenario_name: str | None,
    ) -> None:
        """Load the data into an existing table with a given source.

        Args:
            table_name: The name of the table to feed.
            scenario_name: The name of the scenario to feed.
            source_params: The parameters specific to the source.
        """
        self._load_data_into_table(
            identifier,
            self.key,
            source_params,
            scenario_name=scenario_name,
        )
