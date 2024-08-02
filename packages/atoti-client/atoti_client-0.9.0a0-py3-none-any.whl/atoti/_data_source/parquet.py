from __future__ import annotations

from collections.abc import Mapping, Set as AbstractSet
from typing import Final, final

from typing_extensions import override

from .._constant import Constant
from .._data_type import DataType
from .._identification import TableIdentifier
from .._pydantic import get_type_adapter
from ..client_side_encryption_config import ClientSideEncryptionConfig
from .data_source import DataSource, InferTypes, LoadDataIntoTable


def create_parquet_params(
    globfree_absolute_path: str,
    /,
    *,
    glob_pattern: str | None,
    columns: Mapping[str, str],
    client_side_encryption: ClientSideEncryptionConfig | None,
) -> dict[str, object]:
    return {
        "absolutePath": globfree_absolute_path,
        "globPattern": glob_pattern,
        "columns": columns,
        "clientSideEncryptionConfig": get_type_adapter(
            type(client_side_encryption),
        ).dump_python(client_side_encryption)
        if client_side_encryption is not None
        else None,
    }


@final
class ParquetDataSource(DataSource):
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
        return "PARQUET"

    def infer_parquet_types(
        self,
        globfree_absolute_path: str,
        /,
        *,
        keys: AbstractSet[str],
        glob_pattern: str | None,
        client_side_encryption: ClientSideEncryptionConfig | None,
        columns: Mapping[str, str],
        default_values: Mapping[str, Constant | None],
    ) -> dict[str, DataType]:
        return self._infer_types(
            self.key,
            create_parquet_params(
                globfree_absolute_path,
                glob_pattern=glob_pattern,
                columns=columns,
                client_side_encryption=client_side_encryption,
            ),
            keys=keys,
            default_values=default_values,
        )

    def load_parquet_into_table(
        self,
        identifier: TableIdentifier,
        globfree_absolute_path: str,
        /,
        *,
        columns: Mapping[str, str],
        scenario_name: str | None,
        glob_pattern: str | None = None,
        client_side_encryption: ClientSideEncryptionConfig | None = None,
    ) -> None:
        self.load_data_into_table(
            identifier,
            create_parquet_params(
                globfree_absolute_path,
                glob_pattern=glob_pattern,
                columns=columns,
                client_side_encryption=client_side_encryption,
            ),
            scenario_name=scenario_name,
        )
