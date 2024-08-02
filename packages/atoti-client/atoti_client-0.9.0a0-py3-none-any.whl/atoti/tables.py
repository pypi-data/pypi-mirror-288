from collections.abc import Mapping, Set as AbstractSet
from contextlib import AbstractContextManager
from typing import Final, final

from typing_extensions import override

from ._atoti_client import AtotiClient
from ._collections import DelegatingMutableMapping
from ._column_description import ColumnDescription
from ._database_schema import DatabaseSchema, TableDescription
from ._doc import doc
from ._identification import TableIdentifier, TableName
from ._ipython import ReprJson, ReprJsonable
from ._java_api import JavaApi
from ._transaction import (
    TRANSACTION_DOC_KWARGS as _TRANSACTION_DOC_KWARGS,
    transact_data,
)
from .table import Table


@final
class Tables(DelegatingMutableMapping[TableName, Table], ReprJsonable):  # type: ignore[misc]
    r"""Manage the local :class:`~atoti.Table`\ s of a :class:`~atoti.Session`."""

    def __init__(
        self,
        *,
        atoti_client: AtotiClient,
        java_api: JavaApi,
        session_id: str,
    ):
        self._atoti_client: Final = atoti_client
        self._java_api: Final = java_api
        self._session_id: Final = session_id

    def _get_table_names(self, *, key: TableName | None) -> list[TableName]:
        assert self._atoti_client._graphql_client

        if key is None:
            result = self._atoti_client._graphql_client.get_table_names()
            return [table.name for table in result.tables]

        table = self._atoti_client._graphql_client.get_table_name(table_name=key).table
        return [table.name] if table else []

    @override
    def _get_delegate(self, *, key: TableName | None) -> Mapping[TableName, Table]:
        return {
            table_name: Table(
                TableIdentifier(table_name),
                atoti_client=self._atoti_client,
                java_api=self._java_api,
                scenario=None,
            )
            for table_name in self._get_table_names(key=key)
        }

    @override
    def _update_delegate(
        self,
        other: Mapping[TableName, Table],
        /,
    ) -> None:
        raise AssertionError(
            "Use `Session.create_table()` or other methods such as `Session.read_pandas()` to create a table.",
        )

    @override
    def _delete_delegate_keys(self, keys: AbstractSet[TableName], /) -> None:
        for key in keys:
            self._java_api.delete_table(TableIdentifier(key))

    @override
    def _repr_json_(self) -> ReprJson:
        return (
            dict(
                sorted(
                    {
                        table.name: table._repr_json_()[0] for table in self.values()
                    }.items(),
                ),
            ),
            {"expanded": False, "root": "Tables"},
        )

    @doc(**_TRANSACTION_DOC_KWARGS)
    def data_transaction(
        self,
        scenario_name: str | None = None,
        *,
        allow_nested: bool = True,
    ) -> AbstractContextManager[None]:
        """Create a data transaction to batch several data loading operations.

        * It is more efficient than doing each loading operation one after the other.
        * It avoids possibly incorrect intermediate states (e.g. if loading some new data requires dropping existing rows first).

        Note:
            Data transactions cannot be mixed with:

            * Long-running operations such as :meth:`~atoti.Table.load_kafka`.
            * Data model operations such as :meth:`~atoti.Table.join`, :meth:`~atoti.Session.read_parquet`, or defining a new measure.
            * Operations on parameter tables created from :meth:`~atoti.Cube.create_parameter_hierarchy_from_members` and :meth:`~atoti.Cube.create_parameter_simulation`.
            * Operations on other source scenarios than the one the transaction is started on.

        Args:
            {allow_nested}
            scenario_name: The name of the source scenario impacted by all the table operations inside the transaction.

        Example:
            >>> df = pd.DataFrame(
            ...     columns=["City", "Price"],
            ...     data=[
            ...         ("Berlin", 150.0),
            ...         ("London", 240.0),
            ...         ("New York", 270.0),
            ...         ("Paris", 200.0),
            ...     ],
            ... )
            >>> table = session.read_pandas(df, keys=["City"], table_name="Cities")
            >>> cube = session.create_cube(table)
            >>> extra_df = pd.DataFrame(
            ...     columns=["City", "Price"],
            ...     data=[
            ...         ("Singapore", 250.0),
            ...     ],
            ... )
            >>> with session.tables.data_transaction():
            ...     table += ("New York", 100.0)
            ...     table.drop(table["City"] == "Paris")
            ...     table.load_pandas(extra_df)
            >>> table.head().sort_index()
                       Price
            City
            Berlin     150.0
            London     240.0
            New York   100.0
            Singapore  250.0
            >>> table.drop()

            Nested transactions allowed:

            >>> def composable_function(session):
            ...     table = session.tables["Cities"]
            ...     with session.tables.data_transaction():
            ...         table += ("Paris", 100.0)
            >>> # The function can be called in isolation:
            >>> composable_function(session)
            >>> table.head().sort_index()
                   Price
            City
            Paris  100.0
            >>> with session.tables.data_transaction(
            ...     allow_nested=False  # No-op because this is the outer transaction.
            ... ):
            ...     table.drop()
            ...     table += ("Berlin", 200.0)
            ...     # The function can also be called inside another transaction and will contribute to it:
            ...     composable_function(session)
            ...     table += ("New York", 150.0)
            >>> table.head().sort_index()
                      Price
            City
            Berlin    200.0
            New York  150.0
            Paris     100.0

            Nested transactions not allowed:

            >>> def not_composable_function(session):
            ...     table = session.tables["Cities"]
            ...     with session.tables.data_transaction(allow_nested=False):
            ...         table.drop()
            ...         table += ("Paris", 100.0)
            ...     assert table.row_count == 1
            >>> # The function can be called in isolation:
            >>> not_composable_function(session)
            >>> with session.tables.data_transaction():
            ...     table.drop()
            ...     table += ("Berlin", 200.0)
            ...     # This is a programming error, the function cannot be called inside another transaction:
            ...     not_composable_function(session)
            ...     table += ("New York", 150.0)
            Traceback (most recent call last):
                ...
            RuntimeError: Cannot start this transaction inside another transaction since nesting is not allowed.
            >>> # The last transaction was rolled back:
            >>> table.head().sort_index()
                   Price
            City
            Paris  100.0

        See Also:
            :meth:`~atoti.Session.data_model_transaction`.

        """
        return transact_data(
            allow_nested=allow_nested,
            commit=lambda transaction_id: self._java_api.end_data_transaction(
                transaction_id,
                has_succeeded=True,
            ),
            rollback=lambda transaction_id: self._java_api.end_data_transaction(
                transaction_id,
                has_succeeded=False,
            ),
            session_id=self._session_id,
            start=lambda: self._java_api.start_data_transaction(
                scenario_name=scenario_name,
                initiated_by_user=True,
            ),
        )

    @property
    def schema(self) -> object:
        """Schema of the tables represented as a `Mermaid <https://mermaid.js.org>`__ entity relationship diagram.

        Each table is represented with 3 or 4 columns:

        #. whether the column's :attr:`~atoti.Column.default_value` is ``None`` (denoted with :guilabel:`nullable`) or not
        #. the column :attr:`~atoti.Column.data_type`
        #. (optional) whether the column is part of the table :attr:`~atoti.Table.keys` (denoted with :guilabel:`PK`) or not
        #. the column :attr:`~atoti.Column.name`

        Example:
            .. raw:: html

                <div class="mermaid">
                erDiagram
                  "Table a" {
                      _ String "foo"
                      nullable int "bar"
                  }
                  "Table b" {
                      _ int PK "bar"
                      _ LocalDate "baz"
                  }
                  "Table c" {
                      _ String PK "foo"
                      _ double PK "xyz"
                  }
                  "Table d" {
                      _ String PK "foo_d"
                      _ double PK "xyz_d"
                      nullable float "abc_d"
                  }
                  "Table a" }o--o| "Table b" : "`bar` == `bar`"
                  "Table a" }o..o{ "Table c" : "`foo` == `foo`"
                  "Table c" }o--|| "Table d" : "(`foo` == `foo_d`) & (`xyz` == `xyz_d`)"
                </div>

        """
        return DatabaseSchema(
            joins=self._java_api.get_joins(),
            tables={
                TableDescription(
                    name=table.name,
                    columns=[
                        ColumnDescription(
                            name=column_name,
                            data_type=table[column_name].data_type,
                            nullable=table[column_name].default_value is None,
                        )
                        for column_name in table
                    ],
                    keys=set(table.keys),
                )
                for table in self.values()
            },
        )
