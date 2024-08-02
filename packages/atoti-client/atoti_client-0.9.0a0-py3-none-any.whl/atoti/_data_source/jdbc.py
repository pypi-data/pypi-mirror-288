from __future__ import annotations

from collections.abc import Mapping, Set as AbstractSet
from typing import Final, final

from typing_extensions import override

from .._constant import Constant
from .._data_type import DataType
from .._identification import TableIdentifier
from .data_source import DataSource, InferTypes, LoadDataIntoTable


def _create_source_params(
    *,
    driver: str,
    sql: str,
    url: str,
) -> dict[str, object]:
    return {
        "driverClass": driver,
        "query": sql,
        "url": url,
    }


@final
class JdbcDataSource(DataSource):
    def __init__(
        self,
        *,
        infer_types: InferTypes,
        load_data_into_table: LoadDataIntoTable,
    ) -> None:
        super().__init__(load_data_into_table=load_data_into_table)

        self._infer_types: Final = infer_types

    @property
    @override
    def key(self) -> str:
        return "JDBC"

    def load_sql_into_table(
        self,
        identifier: TableIdentifier,
        sql: str,
        /,
        *,
        driver: str,
        scenario_name: str | None,
        url: str,
    ) -> None:
        source_params = _create_source_params(
            driver=driver,
            sql=sql,
            url=url,
        )
        self.load_data_into_table(
            identifier,
            source_params,
            scenario_name=scenario_name,
        )

    def infer_sql_types(
        self,
        sql: str,
        /,
        *,
        keys: AbstractSet[str],
        default_values: Mapping[str, Constant | None],
        url: str,
        driver: str,
    ) -> dict[str, DataType]:
        source_params = _create_source_params(
            driver=driver,
            sql=sql,
            url=url,
        )
        return self._infer_types(
            self.key,
            source_params,
            keys=keys,
            default_values=default_values,
        )
