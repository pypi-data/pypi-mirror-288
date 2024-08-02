from __future__ import annotations

from collections.abc import Mapping, Sequence, Set as AbstractSet
from dataclasses import asdict
from typing import Final, Protocol, final

from pydantic.dataclasses import dataclass
from typing_extensions import override

from .._constant import Constant
from .._data_type import DataType
from .._identification import TableIdentifier
from .._pydantic import PYDANTIC_CONFIG
from ..client_side_encryption_config import ClientSideEncryptionConfig
from .data_source import DataSource, LoadDataIntoTable


@final
@dataclass(config=PYDANTIC_CONFIG, frozen=True, kw_only=True)
class CsvPrivateParameters:
    parser_thread_count: int | None = None
    buffer_size_kb: int | None = None


def create_csv_params(
    globfree_absolute_path: str,
    /,
    *,
    columns: Mapping[str, str] | Sequence[str],
    separator: str | None,
    encoding: str,
    process_quotes: bool | None,
    array_separator: str | None,
    glob_pattern: str | None,
    date_patterns: Mapping[str, str],
    client_side_encryption: ClientSideEncryptionConfig | None,
    parser_thread_count: int | None,
    buffer_size_kb: int | None,
) -> dict[str, object]:
    return {
        "absolutePath": globfree_absolute_path,
        "columns": {} if isinstance(columns, Sequence) else columns,
        "headers": columns if isinstance(columns, Sequence) else [],
        "separator": separator,
        "encoding": encoding,
        "processQuotes": process_quotes,
        "arraySeparator": array_separator,
        "globPattern": glob_pattern,
        "datePatterns": date_patterns,
        "clientSideEncryptionConfig": asdict(client_side_encryption)
        if client_side_encryption is not None
        else None,
        "parserThreads": parser_thread_count,
        "bufferSize": buffer_size_kb,
    }


@final
@dataclass(frozen=True, kw_only=True)
class CsvFileFormat:
    process_quotes: bool
    separator: str
    types: Mapping[str, DataType]


class _DiscoverCsvFileFormat(Protocol):
    def __call__(
        self,
        source_params: Mapping[str, object],
        /,
        *,
        keys: AbstractSet[str],
        default_values: Mapping[str, Constant | None],
    ) -> CsvFileFormat: ...


@final
class CsvDataSource(DataSource):
    def __init__(
        self,
        *,
        discover_csv_file_format: _DiscoverCsvFileFormat,
        load_data_into_table: LoadDataIntoTable,
    ) -> None:
        super().__init__(load_data_into_table=load_data_into_table)

        self._discover_csv_file_format: Final = discover_csv_file_format

    @property
    @override
    def key(self) -> str:
        return "CSV"

    def discover_file_format(
        self,
        globfree_absolute_path: str,
        /,
        *,
        keys: AbstractSet[str],
        separator: str | None,
        encoding: str,
        process_quotes: bool | None,
        array_separator: str | None,
        glob_pattern: str | None,
        date_patterns: Mapping[str, str],
        default_values: Mapping[str, Constant | None],
        client_side_encryption: ClientSideEncryptionConfig | None,
        columns: Mapping[str, str] | Sequence[str],
        parser_thread_count: int | None,
        buffer_size_kb: int | None,
    ) -> CsvFileFormat:
        source_params = create_csv_params(
            globfree_absolute_path,
            columns=columns,
            separator=separator,
            encoding=encoding,
            process_quotes=process_quotes,
            array_separator=array_separator,
            glob_pattern=glob_pattern,
            date_patterns=date_patterns,
            client_side_encryption=client_side_encryption,
            parser_thread_count=parser_thread_count,
            buffer_size_kb=buffer_size_kb,
        )
        return self._discover_csv_file_format(
            source_params,
            keys=keys,
            default_values=default_values,
        )

    def load_csv_into_table(
        self,
        identifier: TableIdentifier,
        globfree_absolute_path: str,
        /,
        *,
        columns: Mapping[str, str] | Sequence[str],
        scenario_name: str | None,
        separator: str | None,
        encoding: str,
        process_quotes: bool | None,
        array_separator: str | None,
        glob_pattern: str | None,
        date_patterns: Mapping[str, str],
        client_side_encryption: ClientSideEncryptionConfig | None,
        parser_thread_count: int | None,
        buffer_size_kb: int | None,
    ) -> None:
        source_params = create_csv_params(
            globfree_absolute_path,
            columns=columns,
            separator=separator,
            encoding=encoding,
            process_quotes=process_quotes,
            array_separator=array_separator,
            glob_pattern=glob_pattern,
            date_patterns=date_patterns,
            client_side_encryption=client_side_encryption,
            parser_thread_count=parser_thread_count,
            buffer_size_kb=buffer_size_kb,
        )
        self.load_data_into_table(
            identifier,
            source_params,
            scenario_name=scenario_name,
        )
