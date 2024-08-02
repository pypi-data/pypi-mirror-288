from __future__ import annotations

import pathlib
import tempfile
from collections.abc import Collection, Iterator, Mapping, Sequence
from datetime import timedelta
from functools import cached_property
from typing import TYPE_CHECKING, Any, Final, Literal, final

import pandas as pd
import pyarrow as pa
from numpy.typing import NDArray
from pydantic import PositiveInt
from typing_extensions import Self, deprecated, override

from ._arrow_utils import write_arrow_to_file
from ._atoti_client import AtotiClient
from ._check_column_condition_table import check_column_condition_table
from ._check_named_object_defined import check_named_object_defined
from ._collections import frozendict
from ._column_description import ColumnDescription
from ._constant import Constant
from ._data_source.arrow import ArrowDataSource
from ._data_source.csv import CsvDataSource, CsvPrivateParameters
from ._data_source.jdbc import JdbcDataSource
from ._data_source.kafka import KafkaDataSource
from ._data_source.parquet import ParquetDataSource
from ._database_schema import RelationshipOptionality
from ._default_query_timeout import DEFAULT_QUERY_TIMEOUT as _DEFAULT_QUERY_TIMEOUT
from ._deprecated_warning_category import (
    DEPRECATED_WARNING_CATEGORY as _DEPRECATED_WARNING_CATEGORY,
)
from ._doc import doc
from ._docs_utils import (
    CLIENT_SIDE_ENCRYPTION_DOC as _CLIENT_SIDE_ENCRYPTION_DOC,
    CSV_KWARGS as _CSV_KWARGS,
    PARQUET_KWARGS as _PARQUET_KWARGS,
    SQL_KWARGS as _SQL_KWARGS,
)
from ._identification import (
    ColumnIdentifier,
    ColumnName,
    HasIdentifier,
    TableIdentifier,
    TableName,
)
from ._ipython import KeyCompletable, ReprJson, ReprJsonable
from ._java import JAVA_MAX_INT as _JAVA_MAX_INT
from ._java_api import JavaApi
from ._jdbc import normalize_jdbc_url
from ._operation import (
    Condition,
    ConditionCombinationOperatorBound,
    ConditionComparisonOperatorBound,
    condition_to_dict,
)
from ._pandas_utils import pandas_to_arrow
from ._report import TableReport
from ._spark_utils import write_spark_to_parquet
from ._split_globfree_absolute_path_and_glob_pattern import (
    split_globfree_absolute_path_and_glob_pattern,
)
from ._typing import Duration
from .client_side_encryption_config import (
    ClientSideEncryptionConfig,
)
from .column import Column

if TYPE_CHECKING:
    # pyspark is an optional dependency.
    from pyspark.sql import (  # pylint: disable=nested-import,undeclared-dependency
        DataFrame as SparkDataFrame,
    )
else:
    SparkDataFrame = object


_Row = tuple[Any, ...] | Mapping[ColumnName, Any]


@final
# Not inheriting from `Mapping` to avoid confusion with `Mapping.__len__()` that returns the number of columns and `Table.row_count` that returns the number of rows.
# `Mapping`'s `keys()`, `values()`, and `items()` could also be misleading are not thus not implemented.
class Table(HasIdentifier[TableIdentifier], KeyCompletable, ReprJsonable):
    """In-memory table of a :class:`~atoti.Session`.

    Example:
        >>> table = session.create_table(
        ...     "Example",
        ...     types={"Product": "String", "Quantity": "int"},
        ... )

        Listing all the column names:

        >>> list(table)
        ['Product', 'Quantity']

        Testing if the table has a given column:

        >>> "Product" in table
        True
        >>> "Price" in table
        False

    """

    def __init__(
        self,
        identifier: TableIdentifier,
        /,
        *,
        atoti_client: AtotiClient,
        java_api: JavaApi,
        scenario: str | None,
    ) -> None:
        self._atoti_client: Final = atoti_client
        self.__identifier: Final = identifier
        self._java_api: Final = java_api
        self._scenario: Final = scenario

    @property
    def name(self) -> TableName:
        """Name of the table."""
        return self._identifier.table_name

    @property
    @override
    def _identifier(self) -> TableIdentifier:
        return self.__identifier

    @cached_property
    def _columns(self) -> frozendict[ColumnName, Column]:
        assert self._atoti_client._graphql_client

        table = check_named_object_defined(
            self._atoti_client._graphql_client.get_table_column_names(
                table_name=self.name,
            ).table,
            "table",
            self.name,
        )

        return frozendict(
            {
                column.name: Column(
                    ColumnIdentifier(
                        self._identifier,
                        column.name,
                    ),
                    get_column_data_type=self._java_api.get_column_data_type,
                    get_column_default_value=self._java_api.get_column_default_value,
                    set_column_default_value=self._java_api.set_column_default_value,
                    table_keys=self.keys,
                )
                for column in table.columns
            },
        )

    @property
    @deprecated(
        "`Table.columns` is deprecated, use `list(table)` instead.",
        category=_DEPRECATED_WARNING_CATEGORY,
    )
    def columns(self) -> Sequence[ColumnName]:
        """Names of the columns of the table.

        :meta private:
        """
        return list(self)

    @property
    def keys(self) -> Sequence[ColumnName]:
        """Names of the key columns of the table.

        Inserting a row containing key values equal to the ones of an existing row will replace the existing row with the new one:

        >>> table = session.create_table(
        ...     "Example",
        ...     keys=["Country", "City"],
        ...     types={
        ...         "Country": "String",
        ...         "City": "String",
        ...         "Year": "int",
        ...         "Population": "int",
        ...     },
        ... )
        >>> table.keys
        ('Country', 'City')
        >>> table += ("France", "Paris", 2000, 9_737_000)
        >>> table += ("United States", "San Diego", 2000, 2_681_000)
        >>> table.head().sort_index()
                                 Year  Population
        Country       City
        France        Paris      2000     9737000
        United States San Diego  2000     2681000
        >>> table += ("France", "Paris", 2024, 11_277_000)
        >>> table.head().sort_index()
                                 Year  Population
        Country       City
        France        Paris      2024    11277000
        United States San Diego  2000     2681000

        Key columns cannot have ``None`` as their :attr:`~atoti.Column.default_value`.
        """
        return self._keys

    @cached_property
    def _keys(self) -> tuple[ColumnName, ...]:
        assert self._atoti_client._graphql_client

        table = check_named_object_defined(
            self._atoti_client._graphql_client.get_table_keys(
                table_name=self.name,
            ).table,
            "table",
            self.name,
        )

        # Sort keys by column order.
        return tuple(
            column.name for column in table.columns if column.name in table.keys
        )

    @property
    def scenario(self) -> str | None:
        """Scenario on which the table is."""
        return self._scenario

    @property
    def _partitioning(self) -> str:
        """Table partitioning."""
        return self._java_api.get_table_partitioning(self._identifier)

    def join(
        self,
        target: Table,
        mapping: Condition[
            ColumnIdentifier,
            Literal["eq"],
            ColumnIdentifier,
            Literal["and"] | None,
        ]
        | None = None,
        /,
        *,
        target_optionality: RelationshipOptionality = "optional",
    ) -> None:
        """Define a join between this source table and the *target* table.

        There are two kinds of joins:

        * full join if all the key columns of the *target* table are mapped and the joined tables share the same locality (either both :class:`~atoti.Table` or both ``ExternalTable``).
        * partial join otherwise.

        Depending on the cube creation mode, the join will also generate different hierarchies and measures:

        * ``manual``: No hierarchy is automatically created.
          For partial joins, creating a hierarchy for each mapped key column is necessary before creating hierarchies for the other columns.
          Once these required hierarchies exist, hierarchies for the un-mapped key columns of the *target* table will automatically be created.
        * ``no_measures``: All the key columns and non-numeric columns of the *target* table will be converted into hierarchies.
          No measures will be created in this mode.
        * ``auto``: The same hierarchies as in the ``no_measures`` mode will be created.
          Additionally, columns of the base table containing numeric values (including arrays), except for columns which are keys, will be converted into measures.
          Columns of the *target* table with these types will not be converted into measures.

        Args:
            target: The other table to join.
            mapping: An equality-based condition from columns of this table to columns of the *target* table.
              If ``None``, the key columns of the *target* table with the same name as columns in this table will be used.
            target_optionality: The relationship optionality on the *target* table side.

              * ``"optional"`` declares no constraints: a row in the source table does not need to have a matching row in the *target* table.
              * ``"mandatory"`` declares that every row in the source table has at least one matching row in the *target* table at all time.
                In the future, this hint will enable some optimizations when incrementally refreshing DirectQuery data.

        Example:
            >>> sales_table = session.create_table(
            ...     "Sales",
            ...     types={"ID": tt.STRING, "Product ID": tt.STRING, "Price": tt.INT},
            ... )
            >>> products_table = session.create_table(
            ...     "Products",
            ...     types={"ID": tt.STRING, "Name": tt.STRING, "Category": tt.STRING},
            ... )
            >>> sales_table.join(
            ...     products_table, sales_table["Product ID"] == products_table["ID"]
            ... )

        """
        normalized_mapping: Mapping[str, str] | None = None

        if mapping is not None:
            check_column_condition_table(
                mapping,
                attribute_name="subject",
                expected_table_identifier=self._identifier,
            )
            check_column_condition_table(
                mapping,
                attribute_name="target",
                expected_table_identifier=target._identifier,
            )
            normalized_mapping = {
                source_identifier.column_name: target_identifier.column_name
                for source_identifier, target_identifier in condition_to_dict(
                    mapping,
                ).items()
            }

        self._java_api.create_join(
            self._identifier,
            target._identifier,
            mapping=normalized_mapping,
            target_optionality=target_optionality,
        )

    @property
    def scenarios(self) -> _TableScenarios:
        """All the scenarios the table can be on."""
        if self.scenario is not None:
            raise RuntimeError(
                "You can only create a new scenario from the base scenario",
            )

        return _TableScenarios(self, java_api=self._java_api)

    @property
    def _loading_report(self) -> TableReport:
        return TableReport(
            _clear_reports=self._java_api.clear_loading_report,
            _get_reports=self._java_api.get_loading_report,
            _identifier=self._identifier,
        )

    def __iter__(self) -> Iterator[ColumnName]:
        # Same signature as `Mapping.__iter__()`.
        return iter(self._columns)

    def __getitem__(self, key: ColumnName, /) -> Column:
        # Same signature as `Mapping.__getitem__()`.
        return self._columns[key]

    @property
    def row_count(self) -> int:
        """The number of rows in the table.

        Example:
            >>> table = session.create_table(
            ...     "Example",
            ...     types={"Product": "String", "Quantity": "int"},
            ... )
            >>> table.row_count
            0
            >>> table += ("Book", 3)
            >>> table.row_count
            1

        """
        return self._java_api.get_table_size(
            self._identifier,
            scenario_name=self.scenario,
        )

    @override
    def _get_key_completions(self) -> Collection[str]:
        return self._columns

    def append(self, *rows: _Row) -> None:
        """Add one or multiple rows to the table.

        If a row with the same keys already exist in the table, it will be overridden by the passed one.

        Args:
            rows: The rows to add.
                Rows can either be:

                * Tuples of values in the correct order.
                * Column name to value mappings.

                All rows must share the shame shape.
        """
        rows_df = pd.DataFrame(rows, columns=list(self))
        self.load_pandas(rows_df)

    def __iadd__(self, row: _Row) -> Self:
        self.append(row)
        return self

    def drop(
        self,
        filter: Condition[  # noqa: A002
            ColumnIdentifier,
            ConditionComparisonOperatorBound,
            Constant | None,
            ConditionCombinationOperatorBound,
        ]
        | None = None,
        /,
    ) -> None:
        """Delete some of the table's rows.

        Args:
            filter: Rows where this condition evaluates to ``True`` will be deleted.
                If ``None``, all the rows will be deleted.

        Example:
            >>> df = pd.DataFrame(
            ...     columns=["City", "Price"],
            ...     data=[
            ...         ("London", 240.0),
            ...         ("New York", 270.0),
            ...         ("Paris", 200.0),
            ...     ],
            ... )
            >>> table = session.read_pandas(df, keys=["City"], table_name="Cities")
            >>> table.head().sort_index()
                      Price
            City
            London    240.0
            New York  270.0
            Paris     200.0
            >>> table.drop((table["City"] == "Paris") | (table["Price"] <= 250.0))
            >>> table.head().sort_index()
                      Price
            City
            New York  270.0
            >>> table.drop()
            >>> table.head()
            Empty DataFrame
            Columns: [Price]
            Index: []
        """
        if filter is not None:
            check_column_condition_table(
                filter,
                attribute_name="subject",
                expected_table_identifier=self._identifier,
            )

        self._java_api.delete_rows_from_table(
            self._identifier,
            scenario_name=self.scenario,
            condition=filter,
        )

    @override
    def _repr_json_(self) -> ReprJson:
        return {
            name: column._repr_json_()[0] for name, column in self._columns.items()
        }, {"expanded": True, "root": self.name}

    def head(self, n: PositiveInt = 5) -> pd.DataFrame:
        """Return at most *n* random rows of the table.

        If the table has some :attr:`keys`, the returned DataFrame will be indexed by them.
        """
        result = self.query(max_rows=n)

        if self.keys:
            result = result.set_index(list(self.keys))

        return result

    @doc(**_CSV_KWARGS, **_CLIENT_SIDE_ENCRYPTION_DOC)
    def load_csv(
        self,
        path: pathlib.Path | str,
        /,
        *,
        columns: Mapping[str, str] | Sequence[str] = frozendict(),
        separator: str | None = ",",
        encoding: str = "utf-8",
        process_quotes: bool | None = True,
        array_separator: str | None = None,
        date_patterns: Mapping[str, str] = frozendict(),
        client_side_encryption: ClientSideEncryptionConfig | None = None,
        **kwargs: Any,
    ) -> None:
        """Load a CSV into this scenario.

        Args:
            {path}
            {columns}
            {separator}
            {encoding}
            {process_quotes}
            {array_separator}
            {date_patterns}
            {client_side_encryption}

        See Also:
            :meth:`~atoti.Session.read_csv` for examples.

        """
        private_parameters = CsvPrivateParameters(**kwargs)

        globfree_absolute_path, glob_pattern = (
            split_globfree_absolute_path_and_glob_pattern(path, ".csv")
        )

        CsvDataSource(
            load_data_into_table=self._java_api.load_data_into_table,
            discover_csv_file_format=self._java_api.discover_csv_file_format,
        ).load_csv_into_table(
            self._identifier,
            globfree_absolute_path,
            columns=columns,
            scenario_name=self.scenario,
            separator=separator,
            encoding=encoding,
            process_quotes=process_quotes,
            array_separator=array_separator,
            glob_pattern=glob_pattern,
            date_patterns=date_patterns,
            client_side_encryption=client_side_encryption,
            parser_thread_count=private_parameters.parser_thread_count,
            buffer_size_kb=private_parameters.buffer_size_kb,
        )

    def load_pandas(
        self,
        dataframe: pd.DataFrame,
        /,
    ) -> None:
        """Load a pandas DataFrame into this scenario.

        Args:
            dataframe: The DataFrame to load.
        """
        arrow_table = pandas_to_arrow(
            dataframe,
            types={column_name: self[column_name].data_type for column_name in self},
        )
        self.load_arrow(arrow_table)

    def load_arrow(
        self,
        table: pa.Table,  # pyright: ignore[reportUnknownParameterType]
        /,
    ) -> None:
        """Load an Arrow Table into this scenario.

        Args:
            table: The Arrow Table to load.
        """
        with tempfile.TemporaryDirectory() as directory:
            filepath = pathlib.Path(directory) / "table.arrow"
            write_arrow_to_file(table, filepath=filepath)
            ArrowDataSource(
                load_data_into_table=self._java_api.load_data_into_table,
            ).load_arrow_into_table(
                self._identifier,
                filepath,
                scenario_name=self.scenario,
            )

    def load_numpy(
        self,
        array: NDArray[Any],
        /,
    ) -> None:
        """Load a NumPy 2D array into this scenario.

        Args:
            array: The 2D array to load.
        """
        dataframe = pd.DataFrame(array, columns=list(self))
        self.load_pandas(dataframe)

    @doc(**_PARQUET_KWARGS, **_CLIENT_SIDE_ENCRYPTION_DOC)
    def load_parquet(
        self,
        path: pathlib.Path | str,
        /,
        *,
        columns: Mapping[str, str] = frozendict(),
        client_side_encryption: ClientSideEncryptionConfig | None = None,
    ) -> None:
        """Load a Parquet file into this scenario.

        Args:
            {path}
            {columns}
            {client_side_encryption}
        """
        globfree_absolute_path, glob_pattern = (
            split_globfree_absolute_path_and_glob_pattern(path, ".parquet")
        )
        ParquetDataSource(
            load_data_into_table=self._java_api.load_data_into_table,
            infer_types=self._java_api.infer_table_types_from_source,
        ).load_parquet_into_table(
            self._identifier,
            globfree_absolute_path,
            columns=columns,
            scenario_name=self.scenario,
            glob_pattern=glob_pattern,
            client_side_encryption=client_side_encryption,
        )

    def load_spark(
        self,
        dataframe: SparkDataFrame,
        /,
    ) -> None:
        """Load a Spark DataFrame into this scenario.

        Args:
            dataframe: The dataframe to load.
        """
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "spark"
            write_spark_to_parquet(dataframe, directory=path)
            self.load_parquet(path)

    def load_kafka(
        self,
        bootstrap_server: str,
        topic: str,
        *,
        group_id: str,
        batch_duration: Duration = timedelta(seconds=1),
        consumer_config: Mapping[str, str] = frozendict(),
    ) -> None:
        """Consume a Kafka topic and stream its records in the table.

        Note:
            This method requires the :mod:`atoti-kafka <atoti_kafka>` plugin.

        The records' key deserializer default to `StringDeserializer <https://kafka.apache.org/21/javadoc/org/apache/kafka/common/serialization/StringDeserializer.html>`__.

        The records' message must be a JSON object with columns' name as keys.

        Args:
            bootstrap_server: ``host[:port]`` that the consumer should contact to bootstrap initial cluster metadata.
            topic: Topic to subscribe to.
            group_id: The name of the consumer group to join.
            batch_duration: Time spent batching received events before publishing them to the table in a single transaction.
            consumer_config: Mapping containing optional parameters to set up the KafkaConsumer.
                The list of available params can be found `here <https://kafka.apache.org/10/javadoc/index.html?org/apache/kafka/clients/consumer/ConsumerConfig.html>`__.
        """
        KafkaDataSource(
            load_data_into_table=self._java_api.load_data_into_table,
        ).load_kafka_into_table(
            self._identifier,
            bootstrap_servers=bootstrap_server,
            topic=topic,
            group_id=group_id,
            batch_duration=batch_duration,
            consumer_config=consumer_config,
            scenario_name=self.scenario,
        )

    @doc(
        **_SQL_KWARGS,
        types="""{"ID": tt.INT, "CITY": tt.STRING, "MY_VALUE": tt.DOUBLE}""",
    )
    def load_sql(
        self,
        sql: str,
        *,
        url: str,
        driver: str | None = None,
    ) -> None:
        """Load the result of the passed SQL query into the table.

        Note:
            This method requires the :mod:`atoti-jdbc <atoti_jdbc>` plugin.

        Args:
            {sql}
            {url}
            {driver}

        Example:
            .. doctest:: load_sql

                >>> table = session.create_table("Cities", types={types}, keys=["ID"])
                >>> table.load_sql(
                ...     "SELECT * FROM MYTABLE;",
                ...     url=f"h2:file:{{RESOURCES_PATH}}/h2-database;USER=root;PASSWORD=pass",
                ... )
                >>> table.row_count
                5

            .. doctest:: load_sql
                :hide:

                Remove the edited H2 database from Git's working tree.
                >>> session.close()
                >>> import os
                >>> os.system(f"git checkout -- {{RESOURCES_PATH}}/h2-database.mv.db")
                0
        """
        from atoti_jdbc._infer_driver import (  # pylint: disable=nested-import,undeclared-dependency
            infer_driver,
        )

        url = normalize_jdbc_url(url)
        JdbcDataSource(
            load_data_into_table=self._java_api.load_data_into_table,
            infer_types=self._java_api.infer_table_types_from_source,
        ).load_sql_into_table(
            self._identifier,
            sql,
            driver=driver or infer_driver(url),
            scenario_name=self.scenario,
            url=url,
        )

    def query(
        self,
        *columns: Column,
        filter: Condition[  # noqa: A002
            ColumnIdentifier,
            ConditionComparisonOperatorBound,
            Constant,
            ConditionCombinationOperatorBound,
        ]
        | None = None,
        max_rows: PositiveInt = _JAVA_MAX_INT - 1,
        timeout: Duration = _DEFAULT_QUERY_TIMEOUT,
    ) -> pd.DataFrame:
        """Query the table to retrieve some of its rows.

        If the table has more than *max_rows* rows matching *filter*, the set of returned rows is unspecified and can change from one call to another.

        As opposed to :meth:`head`, the returned DataFrame will not be indexed by the table's :attr:`keys` since *columns* may lack some of them.

        Args:
            columns: The columns to query.
                If empty, all the columns of the table will be queried.
            filter: The filtering condition.
                Only rows matching this condition will be returned.
            max_rows: The maximum number of rows to return.
            timeout: The duration the query execution can take before being aborted.

        Example:
            >>> df = pd.DataFrame(
            ...     columns=["Continent", "Country", "Currency", "Price"],
            ...     data=[
            ...         ("Europe", "France", "EUR", 200.0),
            ...         ("Europe", "Germany", "EUR", 150.0),
            ...         ("Europe", "United Kingdom", "GBP", 120.0),
            ...         ("America", "United states", "USD", 240.0),
            ...         ("America", "Mexico", "MXN", 270.0),
            ...     ],
            ... )
            >>> table = session.read_pandas(
            ...     df,
            ...     keys=["Continent", "Country", "Currency"],
            ...     table_name="Prices",
            ... )
            >>> result = table.query(filter=table["Price"] >= 200)
            >>> result.set_index(list(table.keys)).sort_index()
                                              Price
            Continent Country       Currency
            America   Mexico        MXN       270.0
                      United states USD       240.0
            Europe    France        EUR       200.0

        """
        if not columns:
            columns = tuple(self[column_name] for column_name in self)

        for column in columns:
            column_table_name = column._identifier.table_identifier.table_name
            if column_table_name != self.name:
                raise ValueError(
                    f"Expected all columns to be from table `{self.name}` but got column `{column.name}` from table `{column_table_name}`.",
                )

        return self._atoti_client.execute_table_query(
            column_descriptions=[
                ColumnDescription(
                    name=column.name,
                    data_type=column.data_type,
                    nullable=column.default_value is None,
                )
                for column in columns
            ],
            filter=filter,
            max_rows=max_rows,
            scenario_name=self.scenario,
            table_name=self.name,
            timeout=timeout,
        )


@final
class _TableScenarios:
    def __init__(self, table: Table, /, *, java_api: JavaApi) -> None:
        self._java_api: Final = java_api
        self._table: Final = table

    def __getitem__(self, name: str, /) -> Table:
        """Get the scenario or create it if it does not exist."""
        return Table(
            self._table._identifier,
            atoti_client=self._table._atoti_client,
            java_api=self._java_api,
            scenario=name,
        )

    def __delitem__(self, name: str, /) -> None:
        raise RuntimeError(
            "You cannot delete a scenario from a table since they are shared between all tables."
            "Use the Session.delete_scenario() method instead.",
        )
