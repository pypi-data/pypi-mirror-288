from __future__ import annotations

from collections.abc import (
    Callable,
    Collection,
    Mapping,
    MutableMapping,
    Sequence,
    Set as AbstractSet,
)
from contextlib import AbstractContextManager, ExitStack
from datetime import datetime, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
from types import TracebackType
from typing import (
    TYPE_CHECKING,
    Annotated,
    Any,
    Final,
    Literal,
    final,
    overload,
)
from urllib.parse import urlparse
from warnings import warn

import pandas as pd
import pyarrow as pa
from _atoti_core import Plugin
from numpy.typing import NDArray
from pydantic import SkipValidation
from pydantic.dataclasses import dataclass
from typing_extensions import deprecated, override

from ._activeviam_client import ActiveViamClient
from ._arrow_utils import get_data_types_from_arrow
from ._atoti_client import AtotiClient
from ._basic_credentials import BasicCredentials
from ._collections import FrozenMapping, frozendict
from ._constant import Constant, ConstantValue
from ._context import Context
from ._data_source.csv import CsvDataSource, CsvPrivateParameters
from ._data_source.jdbc import JdbcDataSource
from ._data_source.parquet import ParquetDataSource
from ._data_type import DataType
from ._default_query_timeout import DEFAULT_QUERY_TIMEOUT as _DEFAULT_QUERY_TIMEOUT
from ._deprecated_warning_category import (
    DEPRECATED_WARNING_CATEGORY as _DEPRECATED_WARNING_CATEGORY,
)
from ._doc import doc
from ._docs_utils import (
    CLIENT_SIDE_ENCRYPTION_DOC as _CLIENT_SIDE_ENCRYPTION_DOC,
    CSV_KWARGS as _CSV_KWARGS,
    EXTERNAL_TABLE_KWARGS as _EXTERNAL_TABLE_KWARGS,
    PARQUET_KWARGS as _PARQUET_KWARGS,
    QUERY_KWARGS as _QUERY_KWARGS,
    SQL_KWARGS as _SQL_KWARGS,
    TABLE_CREATION_KWARGS as _TABLE_CREATION_KWARGS,
)
from ._endpoint import EndpointHandler
from ._generate_session_id import generate_session_id
from ._identification import ColumnIdentifier, IdentifierT_co, TableIdentifier
from ._ipython import find_corresponding_top_level_variable_name
from ._java_api import JavaApi
from ._jdbc import normalize_jdbc_url
from ._link import Link
from ._local_session import local_session
from ._local_session_only_feature_error import LocalSessionOnlyFeatureError
from ._operation import (
    Condition,
    ConditionCombinationOperatorBound,
    ConditionComparisonOperatorBound,
)
from ._pandas_utils import pandas_to_arrow
from ._plugins import PLUGINS
from ._pydantic import PYDANTIC_CONFIG as _PYDANTIC_CONFIG
from ._query_explanation import QueryExplanation
from ._spark_utils import write_spark_to_parquet
from ._split_globfree_absolute_path_and_glob_pattern import (
    split_globfree_absolute_path_and_glob_pattern,
)
from ._transaction import (
    TRANSACTION_DOC_KWARGS as _TRANSACTION_DOC_KWARGS,
    transact_data_model,
)
from ._typing import Duration
from ._widget import Widget
from .authentication import Authenticate, ClientCertificate
from .client_side_encryption_config import ClientSideEncryptionConfig
from .cube import Cube
from .cubes import Cubes
from .directquery import MultiColumnArrayConversion
from .directquery._external_aggregate_table import ExternalAggregateTable
from .directquery._external_aggregate_table._external_aggregate_tables import (
    ExternalAggregateTables,
)
from .directquery._external_database_connection_config import (
    ExternalDatabaseConnectionConfigT,
)
from .directquery._external_table_config import (
    ArrayConversionConfig,
    ExternalTableConfig,
)
from .directquery.external_database_connection import ExternalDatabaseConnection
from .directquery.external_table import ExternalTable
from .mdx_query_result import MdxQueryResult
from .security import Security
from .session_config._auto_distribution_config import AutoDistributionConfig
from .session_config.session_config import SessionConfig
from .table import Table
from .tables import Tables

if TYPE_CHECKING:
    from _atoti_server import (  # pylint: disable=nested-import,undeclared-dependency
        ServerSubprocess,
    )

    # pyspark is an optional dependency.
    from pyspark.sql import (  # pylint: disable=nested-import,undeclared-dependency
        DataFrame as SparkDataFrame,
    )
else:
    SparkDataFrame = object


_DEFAULT_LICENSE_MINIMUM_REMAINING_TIME = timedelta(days=7)


def _infer_table_name(
    globfree_path: str,
    glob_pattern: str | None,
    /,
) -> str:
    if glob_pattern is not None:
        raise ValueError("Cannot infer table name from glob pattern.")
    return Path(globfree_path).stem.capitalize()


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class _SessionStartPrivateParameters:
    address: str | None = None
    atoti_client: AtotiClient | None = None
    auto_distribution_config: AutoDistributionConfig | None = None
    # Enabling authentication by default makes it easy to detect an existing detached process: if an unauthenticated connection can be made on Py4J's default port it means it's a detached process.
    enable_py4j_auth: bool = True
    plugins: FrozenMapping[str, Plugin] | None = None
    py4j_server_port: int | None = None


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class _CreateTablePrivateParameters:
    is_parameter_table: bool = False


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class _CreateCubePrivateParameters:
    application_name: str | None = None


@final
class Session(AbstractContextManager["Session"]):
    """The entry point to interact with Atoti applications.

    A session holds data in :attr:`~atoti.Session.tables` and aggregates it in :attr:`~atoti.Session.cubes`.
    It also serves a web app for data exploration accessible with :attr:`~link`.

    It can be created with either :meth:`start` or :meth:`connect`.
    """

    def __init__(
        self,
        *args: Any,  # Remove after users had time to migrate from `0.8.x`.
        atoti_client: AtotiClient
        | None = None,  # Make non nullable after users had time to migrate from `0.8.x`.
        java_api: JavaApi
        | None = None,  # Remove default value after users had time to migrate from `0.8.x`.
        server_subprocess: ServerSubprocess
        | None = None,  # Remove default value after users had time to migrate from `0.8.x`.
        session_id: str
        | None = None,  # Make non nullable after users had time to migrate from `0.8.x`.
        **kwargs: Any,  # Remove after users had time to migrate from `0.8.x`.
    ):
        self._exit_stack: Final = ExitStack()

        # Remove after users had time to migrate from `0.8.x`.
        if args or kwargs or atoti_client is None or session_id is None:
            raise ValueError("Use `Session.start()` instead of `Session()`.")

        self._atoti_client: Final = atoti_client
        self._id: Final = session_id
        self.__java_api: Final = java_api
        self.__server_subprocess: Final = server_subprocess

    @classmethod
    def connect(  # type: ignore[return]
        cls,
        url: str,
        *,
        authentication: Annotated[Authenticate, SkipValidation]
        | ClientCertificate
        | None = None,
        certificate_authority: Path | None = None,
    ) -> Session:
        """Connect to an already started session.

        Args:
            url: The base URL of the session.
                The endpoint ``f"{url}/versions/rest"`` is expected to exist.
            authentication: The method used to authenticate against the session.
            certificate_authority: Path to the custom certificate authority file to use to verify the HTTPS connection.
                Required when the session has been configured with an SSL certificate that is not signed by some trusted public certificate authority.
        """
        session_id = generate_session_id()

        with ExitStack() as exit_stack:
            activeviam_client = exit_stack.enter_context(
                ActiveViamClient.create(
                    url,
                    authentication=authentication,
                    certificate_authority=certificate_authority,
                ),
            )
            atoti_client = AtotiClient(activeviam_client=activeviam_client)
            # For now, for performance reasons, connected sessions assume their cube discovery to be immutable.
            exit_stack.enter_context(atoti_client.cached_cube_discovery)
            session = cls(
                atoti_client=atoti_client,
                java_api=None,
                server_subprocess=None,
                session_id=session_id,
            )
            session._exit_stack.push(exit_stack.pop_all())
            return session

    @classmethod
    def _connect(  # type: ignore[return]
        cls,
        address: str,
        /,
        *,
        py4j_server_port: int | None = None,
    ) -> Session:
        with ExitStack() as exit_stack:
            atoti_client, java_api, server_subprocess, session_id = (
                exit_stack.enter_context(
                    local_session(
                        address=address,
                        config=SessionConfig(),
                        distributed=False,
                        enable_py4j_auth=False,
                        plugins=PLUGINS.default,
                        py4j_server_port=py4j_server_port,
                        start_application=False,
                    ),
                )
            )
            session = cls(
                atoti_client=atoti_client,
                java_api=java_api,
                server_subprocess=server_subprocess,
                session_id=session_id,
            )
            session._exit_stack.push(exit_stack.pop_all())
            return session

    @classmethod
    def start(  # type: ignore[return]
        cls,
        config: SessionConfig | None = None,
        /,
        **kwargs: Any,
    ) -> Session:
        """Start a new Atoti server subprocess and connect to it.

        If the :guilabel:`JAVA_HOME` environment variable is not defined or if it points to an unsupported Java version, the JVM from `jdk4py <https://github.com/activeviam/jdk4py>`__ will be used instead.

        Args:
            config: The config of the session.
        """
        private_parameters = _SessionStartPrivateParameters(**kwargs)

        if config is None:
            config = SessionConfig()

        plugins = private_parameters.plugins
        if plugins is None:
            plugins = PLUGINS.default

        with ExitStack() as exit_stack:
            atoti_client, java_api, server_subprocess, session_id = (
                exit_stack.enter_context(
                    local_session(
                        address=private_parameters.address,
                        config=config,
                        distributed=False,
                        enable_py4j_auth=private_parameters.enable_py4j_auth,
                        plugins=plugins,
                        py4j_server_port=private_parameters.py4j_server_port,
                        start_application=True,
                    ),
                )
            )
            session = cls(
                atoti_client=atoti_client,
                java_api=java_api,
                server_subprocess=server_subprocess,
                session_id=session_id,
            )
            session._warn_if_license_about_to_expire()

            for plugin in plugins.values():
                plugin.session_hook(session)

            session._exit_stack.push(exit_stack.pop_all())
            return session

    @override
    def __exit__(  # pylint: disable=too-many-positional-parameters
        self,
        exception_type: type[BaseException] | None,
        exception_value: BaseException | None,
        exception_traceback: TracebackType | None,
    ) -> None:
        self._exit_stack.__exit__(exception_type, exception_value, exception_traceback)

    def close(self) -> None:
        """Close this session and free all associated resources.

        The session cannot be used after calling this method.

        Closing a session frees its port so it can be reused by another session or another process.

        This method is called by the ``__del__()`` method so garbage collected sessions will automatically be closed.
        Python synchronously garbage collects objects as soon as their last (hard) reference is lost.
        In a notebook, it is thus possible to run the following cell multiple times without encountering a "port already in use" error:

        .. code-block:: python

            # (Re)assigning the `session` variable to garbage collect previous reference (if any).
            session = None
            # If a previous `session` was using port 1337, it is now free to use again (unless another process just took it).
            session = tt.Session.start(tt.SessionConfig(port=1337))

        Note:
            In a notebook, evaluating/printing an object creates long lasting references to it preventing the object from being garbage collected.
            The pattern shown above will thus only work if the `session` object was not used as the last expression of a cell.

        """
        self.__exit__(None, None, None)

    def __del__(self) -> None:
        # Use private method to avoid sending a telemetry event that would raise `RuntimeError: cannot schedule new futures after shutdown` when calling `ThreadPoolExecutor.submit()`.
        self.__exit__(None, None, None)

    @property
    def _java_api(self) -> JavaApi:
        if self.__java_api is None:
            raise LocalSessionOnlyFeatureError
        return self.__java_api

    @property
    def _server_subprocess(self) -> ServerSubprocess:
        if self.__server_subprocess is None:
            raise LocalSessionOnlyFeatureError
        return self.__server_subprocess

    @property
    def logs_path(self) -> Path:
        """Path to the session logs file."""
        return self._server_subprocess.logs_path

    @property
    def cubes(self) -> Cubes:
        return Cubes(
            atoti_client=self._atoti_client,
            get_widget_creation_code=self._get_widget_creation_code,
            java_api=self.__java_api,
            read_pandas=self.read_pandas,
            session_id=self._id,
        )

    @property
    def tables(self) -> Tables:
        return Tables(
            atoti_client=self._atoti_client,
            java_api=self._java_api,
            session_id=self._id,
        )

    @doc(
        **_TABLE_CREATION_KWARGS,
        keys_argument="""{"Date", "Product"}""",
        types_argument="""{"Date": tt.LOCAL_DATE, "Product": tt.STRING, "Quantity": tt.DOUBLE}""",
    )
    def create_table(
        self,
        name: str,
        *,
        types: Mapping[str, DataType],
        keys: AbstractSet[str] | Sequence[str] = frozenset(),
        partitioning: str | None = None,
        default_values: Mapping[str, ConstantValue | None] = frozendict(),
        **kwargs: Any,
    ) -> Table:
        """Create an empty table with columns of the given *types*.

        Args:
            name: The name of the table.
            types: The table column names and their corresponding :mod:`data type <atoti.type>`.
            {keys}
            {partitioning}
            {default_values}

        Example:
            >>> from datetime import date
            >>> table = session.create_table(
            ...     "Product",
            ...     keys={keys_argument},
            ...     types={types_argument},
            ... )
            >>> table.head()
            Empty DataFrame
            Columns: [Quantity]
            Index: []
            >>> table.append(
            ...     (date(2021, 5, 19), "TV", 15.0),
            ...     (date(2022, 8, 17), "Car", 2.0),
            ... )
            >>> table.head()
                                Quantity
            Date       Product
            2021-05-19 TV           15.0
            2022-08-17 Car           2.0

            Inserting a row with the same key values as an existing row replaces the latter:

            >>> table += (date(2021, 5, 19), "TV", 8.0)
            >>> table.head()
                                Quantity
            Date       Product
            2021-05-19 TV            8.0
            2022-08-17 Car           2.0

        """
        private_parameters = _CreateTablePrivateParameters(**kwargs)
        identifier = TableIdentifier(name)
        self._java_api.create_table(
            identifier,
            types=types,
            keys=[column_name for column_name in types if column_name in keys]
            if isinstance(keys, AbstractSet)
            else keys,
            partitioning=partitioning,
            default_values={
                column_name: None if value is None else Constant(value)
                for column_name, value in default_values.items()
            },
            is_parameter_table=private_parameters.is_parameter_table,
        )
        return self.tables[name]

    def connect_to_external_database(
        self,
        connection_config: ExternalDatabaseConnectionConfigT,
        /,
    ) -> ExternalDatabaseConnection[ExternalDatabaseConnectionConfigT]:
        """Connect to an external database using DirectQuery.

        Note:
            This feature is not part of the community edition: it needs to be `unlocked <../../how_tos/unlock_all_features.html>`__.

        Args:
            connection_config: The config to connect to the external database.
                Each `DirectQuery plugin <../reference.html#directquery>`__ has its own ``ConnectionConfig`` class.
        """
        self._java_api.connect_to_database(
            connection_config._database_key,
            url=connection_config._url,
            password=connection_config._password,
            options=connection_config._options,
        )
        return ExternalDatabaseConnection(
            database_key=connection_config._database_key,
            java_api=self._java_api,
        )

    @doc(
        **_EXTERNAL_TABLE_KWARGS,
        columns_argument="""{"SALE_ID": "Sale ID", "DATE": "Date", "PRODUCT": "Product", "QUANTITY": "Quantity"}""",
    )
    def add_external_table(
        self,
        external_table: ExternalTable[ExternalDatabaseConnectionConfigT],
        /,
        table_name: str | None = None,
        *,
        columns: Mapping[str, str] = frozendict(),
        config: ExternalTableConfig[ExternalDatabaseConnectionConfigT] | None = None,
    ) -> Table:
        """Add a table from an external database to the session.

        Args:
            external_table: The external database table from which to build the session table.
                Instances of such tables are obtained through an external database connection.
            table_name: The name to give to the table in the session.
                If ``None``, the name of the external table is used.
            {columns}
            config: The config to add the external table.
                Each `DirectQuery plugin <../reference.html#directquery>`__ has its own ``TableConfig`` class.

        Example:
            .. doctest:: add_external_table
                :hide:

                >>> import os
                >>> from atoti_directquery_snowflake import ConnectionConfig
                >>> connection_config = ConnectionConfig(
                ...     url="jdbc:snowflake://"
                ...     + os.environ["SNOWFLAKE_ACCOUNT_IDENTIFIER"]
                ...     + ".snowflakecomputing.com/?user="
                ...     + os.environ["SNOWFLAKE_USERNAME"]
                ...     + "&database=TEST_RESOURCES"
                ...     + "&schema=TESTS",
                ...     password=os.environ["SNOWFLAKE_PASSWORD"],
                ... )

            .. doctest:: add_external_table

                >>> external_database = session.connect_to_external_database(connection_config)
                >>> external_table = external_database.tables["TUTORIAL", "SALES"]
                >>> list(external_table)
                ['SALE_ID', 'DATE', 'SHOP', 'PRODUCT', 'QUANTITY', 'UNIT_PRICE']

            Add the external table, filtering out some columns and renaming the remaining ones:

            .. doctest:: add_external_table

                >>> from atoti_directquery_snowflake import TableConfig
                >>> table = session.add_external_table(
                ...     external_table,
                ...     table_name="sales_renamed",
                ...     columns={columns_argument},
                ...     config=TableConfig(keys=["Sale ID"]),
                ... )
                >>> table.head().sort_index()
                              Date Product  Quantity
                Sale ID
                S0007   2022-02-01   BED_2       1.0
                S0008   2022-01-31   BED_2       1.0
                S0009   2022-01-31   BED_2       1.0
                S0010   2022-01-31   BED_2       3.0
                S0019   2022-02-02   HOO_5       1.0

        """
        if table_name is None:
            table_name = external_table._identifier.table_name

        array_conversion = None
        clustering_columns = None
        keys = None

        if config is not None:
            if isinstance(config, ArrayConversionConfig):
                array_conversion = config.array_conversion

            clustering_columns = (
                frozenset(config.clustering_columns)
                if config.clustering_columns
                else None
            )
            keys = tuple(config.keys) if config.keys else None

        if array_conversion is not None:
            if isinstance(array_conversion, MultiColumnArrayConversion):
                self._java_api.add_external_multi_column_array_table(
                    external_table._database_key,
                    column_prefixes=array_conversion.column_prefixes,
                    clustering_columns=clustering_columns
                    if clustering_columns
                    else None,
                    columns=columns,
                    identifier=external_table._identifier,
                    keys=keys,
                    local_table_identifier=TableIdentifier(table_name),
                )
            else:
                self._java_api.add_external_table_with_multi_row_arrays(
                    external_table._database_key,
                    array_columns=array_conversion.array_columns,
                    clustering_columns=clustering_columns,
                    identifier=external_table._identifier,
                    index_column=array_conversion.index_column,
                    local_table_identifier=TableIdentifier(table_name),
                    columns=columns,
                )
        else:
            # Table without conversion
            self._java_api.add_external_table(
                external_table._database_key,
                clustering_columns=clustering_columns,
                columns=columns,
                identifier=external_table._identifier,
                keys=keys,
                local_table_identifier=TableIdentifier(table_name),
            )
        self._java_api.refresh()
        return self.tables[table_name]

    def _synchronize_with_external_database(self) -> None:
        self._java_api.synchronize_with_external_database()

    @property
    def _external_aggregate_tables(self) -> MutableMapping[str, ExternalAggregateTable]:
        return ExternalAggregateTables(
            java_api=self._java_api,
        )

    @doc(**_TABLE_CREATION_KWARGS, keys_argument="""{"Product"}""")
    def read_pandas(
        self,
        dataframe: pd.DataFrame,
        /,
        *,
        table_name: str,
        keys: AbstractSet[str] | Sequence[str] = frozenset(),
        partitioning: str | None = None,
        types: Mapping[str, DataType] = frozendict(),
        default_values: Mapping[str, ConstantValue | None] = frozendict(),
        **kwargs: Any,
    ) -> Table:
        """Read a pandas DataFrame into a table.

        All the named indices of the DataFrame are included into the table.
        Multilevel columns are flattened into a single string name.

        Args:
            dataframe: The DataFrame to load.
            {table_name}
            {keys}
            {partitioning}
            types: Types for some or all columns of the table.
                Types for non specified columns will be inferred from pandas dtypes.
            {default_values}

        Example:
            >>> dataframe = pd.DataFrame(
            ...     columns=["Product", "Price"],
            ...     data=[
            ...         ("phone", 600.0),
            ...         ("headset", 80.0),
            ...         ("watch", 250.0),
            ...     ],
            ... )
            >>> table = session.read_pandas(
            ...     dataframe, keys={keys_argument}, table_name="Pandas"
            ... )
            >>> table.head().sort_index()
                     Price
            Product
            headset   80.0
            phone    600.0
            watch    250.0

        """
        arrow_table = pandas_to_arrow(dataframe, types=types)
        return self.read_arrow(
            arrow_table,
            table_name=table_name,
            keys=keys,
            partitioning=partitioning,
            types=types,
            default_values=default_values,
            **kwargs,
        )

    @doc(**_TABLE_CREATION_KWARGS, keys_argument="""{"Product"}""")
    def read_arrow(
        self,
        table: pa.Table,  # pyright: ignore[reportUnknownParameterType]
        /,
        *,
        table_name: str,
        keys: AbstractSet[str] | Sequence[str] = frozenset(),
        partitioning: str | None = None,
        types: Mapping[str, DataType] = frozendict(),
        default_values: Mapping[str, ConstantValue | None] = frozendict(),
        **kwargs: Any,
    ) -> Table:
        """Read an Arrow Table into a table.

        Args:
            table: The Arrow Table to load.
            {table_name}
            {keys}
            {partitioning}
            types: Types for some or all columns of the table.
                Types for non specified columns will be inferred from arrow DataTypes.
            {default_values}

        Example:
            >>> import pyarrow as pa
            >>> arrow_table = pa.Table.from_arrays(
            ...     [
            ...         pa.array(["phone", "headset", "watch"]),
            ...         pa.array([600.0, 80.0, 250.0]),
            ...     ],
            ...     names=["Product", "Price"],
            ... )
            >>> arrow_table
            pyarrow.Table
            Product: string
            Price: double
            ----
            Product: [["phone","headset","watch"]]
            Price: [[600,80,250]]
            >>> table = session.read_arrow(
            ...     arrow_table, keys={keys_argument}, table_name="Arrow"
            ... )
            >>> table.head().sort_index()
                     Price
            Product
            headset   80.0
            phone    600.0
            watch    250.0

        """
        types_from_arrow = get_data_types_from_arrow(table)
        types = {**types_from_arrow, **types}
        created_table = self.create_table(
            table_name,
            types=types,
            keys=keys,
            partitioning=partitioning,
            default_values=default_values,
            **kwargs,
        )
        created_table.load_arrow(table)
        return created_table

    @doc(**_TABLE_CREATION_KWARGS)
    def read_spark(
        self,
        dataframe: SparkDataFrame,
        /,
        *,
        table_name: str,
        keys: AbstractSet[str] | Sequence[str] = frozenset(),
        partitioning: str | None = None,
        default_values: Mapping[str, ConstantValue | None] = frozendict(),
    ) -> Table:
        """Read a Spark DataFrame into a table.

        Args:
            dataframe: The DataFrame to load.
            {table_name}
            {keys}
            {partitioning}
            {default_values}

        """
        with TemporaryDirectory() as directory:
            path = Path(directory) / "spark"
            write_spark_to_parquet(dataframe, directory=path)
            return self.read_parquet(
                path,
                keys=keys,
                table_name=table_name,
                partitioning=partitioning,
                default_values=default_values,
            )

    @doc(
        **_TABLE_CREATION_KWARGS,
        **_CSV_KWARGS,
        **_CLIENT_SIDE_ENCRYPTION_DOC,
        columns_argument="""{"country": "Country", "area": "Region", "city": "City"}""",
        keys_argument="""{"Country"}""",
    )
    def read_csv(
        self,
        path: Path | str,
        /,
        *,
        keys: AbstractSet[str] | Sequence[str] = frozenset(),
        table_name: str | None = None,
        separator: str | None = ",",
        encoding: str = "utf-8",
        process_quotes: bool | None = True,
        partitioning: str | None = None,
        types: Mapping[str, DataType] = frozendict(),
        columns: Mapping[str, str] | Sequence[str] = frozendict(),
        array_separator: str | None = None,
        date_patterns: Mapping[str, str] = frozendict(),
        default_values: Mapping[str, ConstantValue | None] = frozendict(),
        client_side_encryption: ClientSideEncryptionConfig | None = None,
        **kwargs: Any,
    ) -> Table:
        """Read a CSV file into a table.

        Args:
            {path}
            {keys}
            table_name: The name of the table to create.
                Required when *path* is a glob pattern.
                Otherwise, defaults to the capitalized final component of the *path* argument.
            {separator}
            {encoding}
            {process_quotes}
            {partitioning}
            types: Types for some or all columns of the table.
                Types for non specified columns will be inferred from the first 1,000 lines.
            {columns}

                >>> import csv
                >>> from pathlib import Path
                >>> from tempfile import mkdtemp
                >>> directory = mkdtemp()
                >>> file_path = Path(directory) / "largest-cities.csv"
                >>> with open(file_path, "w") as csv_file:
                ...     writer = csv.writer(csv_file)
                ...     writer.writerows(
                ...         [
                ...             ("city", "area", "country", "population"),
                ...             ("Tokyo", "Kantō", "Japan", 14_094_034),
                ...             ("Johannesburg", "Gauteng", "South Africa", 4_803_262),
                ...             (
                ...                 "Barcelona",
                ...                 "Community of Madrid",
                ...                 "Madrid",
                ...                 3_223_334,
                ...             ),
                ...         ]
                ...     )

                Dropping the :guilabel:`population` column and renaming and reordering the remaining ones:

                >>> table = session.read_csv(
                ...     file_path,
                ...     columns={columns_argument},
                ...     keys={keys_argument},
                ... )
                >>> table.head().sort_index()
                                           Region          City
                Country
                Japan                       Kantō         Tokyo
                Madrid        Community of Madrid     Barcelona
                South Africa              Gauteng  Johannesburg

                Loading a headerless CSV file:

                >>> file_path = Path(directory) / "largest-cities-headerless.csv"
                >>> with open(file_path, "w") as csv_file:
                ...     writer = csv.writer(csv_file)
                ...     writer.writerows(
                ...         [
                ...             ("Tokyo", "Kantō", "Japan", 14_094_034),
                ...             ("Johannesburg", "Gauteng", "South Africa", 4_803_262),
                ...             (
                ...                 "Madrid",
                ...                 "Community of Madrid",
                ...                 "Spain",
                ...                 3_223_334,
                ...             ),
                ...         ]
                ...     )
                >>> table = session.read_csv(
                ...     file_path,
                ...     keys={keys_argument},
                ...     columns=["City", "Area", "Country", "Population"],
                ... )
                >>> table.head().sort_index()
                                      City                 Area  Population
                Country
                Japan                Tokyo                Kantō    14094034
                South Africa  Johannesburg              Gauteng     4803262
                Spain               Madrid  Community of Madrid     3223334

            {array_separator}
            {date_patterns}
            {default_values}
            {client_side_encryption}

        """
        private_parameters = CsvPrivateParameters(**kwargs)

        globfree_absolute_path, glob_pattern = (
            split_globfree_absolute_path_and_glob_pattern(
                path,
                ".csv",
            )
        )

        if table_name is None:
            table_name = _infer_table_name(globfree_absolute_path, glob_pattern)

        csv_file_format = CsvDataSource(
            load_data_into_table=self._java_api.load_data_into_table,
            discover_csv_file_format=self._java_api.discover_csv_file_format,
        ).discover_file_format(
            globfree_absolute_path,
            keys=set(keys),
            separator=separator,
            encoding=encoding,
            process_quotes=process_quotes,
            array_separator=array_separator,
            glob_pattern=glob_pattern,
            date_patterns=date_patterns,
            default_values={
                column_name: None if value is None else Constant(value)
                for column_name, value in default_values.items()
            },
            client_side_encryption=client_side_encryption,
            columns=columns,
            parser_thread_count=private_parameters.parser_thread_count,
            buffer_size_kb=private_parameters.buffer_size_kb,
        )
        types = {**csv_file_format.types, **types}

        table = self.create_table(
            table_name,
            types=types,
            keys=keys,
            partitioning=partitioning,
            default_values=default_values,
        )
        table.load_csv(
            path,
            columns=columns,
            separator=csv_file_format.separator,
            encoding=encoding,
            process_quotes=csv_file_format.process_quotes,
            array_separator=array_separator,
            date_patterns=date_patterns,
            client_side_encryption=client_side_encryption,
            parser_thread_count=private_parameters.parser_thread_count,
            buffer_size_kb=private_parameters.buffer_size_kb,
        )
        return table

    @doc(**_TABLE_CREATION_KWARGS, **_PARQUET_KWARGS, **_CLIENT_SIDE_ENCRYPTION_DOC)
    def read_parquet(
        self,
        path: Path | str,
        /,
        *,
        keys: AbstractSet[str] | Sequence[str] = frozenset(),
        columns: Mapping[str, str] = frozendict(),
        table_name: str | None = None,
        partitioning: str | None = None,
        default_values: Mapping[str, ConstantValue | None] = frozendict(),
        client_side_encryption: ClientSideEncryptionConfig | None = None,
    ) -> Table:
        """Read a Parquet file into a table.

        Args:
            {path}
            {keys}
            {columns}
            table_name: The name of the table to create.
                Required when *path* is a glob pattern.
                Otherwise, defaults to the capitalized final component of the *path* argument.
            {partitioning}
            {default_values}
            {client_side_encryption}

        """
        globfree_absolute_path, glob_pattern = (
            split_globfree_absolute_path_and_glob_pattern(
                path,
                ".parquet",
            )
        )

        if table_name is None:
            table_name = _infer_table_name(globfree_absolute_path, glob_pattern)

        inferred_types = ParquetDataSource(
            load_data_into_table=self._java_api.load_data_into_table,
            infer_types=self._java_api.infer_table_types_from_source,
        ).infer_parquet_types(
            globfree_absolute_path,
            keys=set(keys),
            glob_pattern=glob_pattern,
            client_side_encryption=client_side_encryption,
            columns=columns,
            default_values={
                column_name: None if value is None else Constant(value)
                for column_name, value in default_values.items()
            },
        )

        table = self.create_table(
            table_name,
            types=inferred_types,
            keys=keys,
            partitioning=partitioning,
            default_values=default_values,
        )
        table.load_parquet(
            path,
            client_side_encryption=client_side_encryption,
            columns=columns,
        )
        return table

    @doc(**_TABLE_CREATION_KWARGS)
    def read_numpy(
        self,
        array: NDArray[Any],
        /,
        *,
        columns: Sequence[str],
        table_name: str,
        keys: AbstractSet[str] | Sequence[str] = frozenset(),
        partitioning: str | None = None,
        types: Mapping[str, DataType] = frozendict(),
        default_values: Mapping[str, ConstantValue | None] = frozendict(),
    ) -> Table:
        """Read a NumPy 2D array into a new table.

        Args:
            array: The NumPy 2D ndarray to read the data from.
            columns: The names to use for the table's columns.
                They must be in the same order as the values in the NumPy array.
            {table_name}
            {keys}
            {partitioning}
            types: Types for some or all columns of the table.
                Types for non specified columns will be inferred from numpy data types.
            {default_values}

        """
        dataframe = pd.DataFrame(array, columns=list(columns))
        return self.read_pandas(
            dataframe,
            table_name=table_name,
            keys=keys,
            partitioning=partitioning,
            types=types,
            default_values=default_values,
        )

    def _infer_sql_types(
        self,
        sql: str,
        /,
        *,
        url: str,
        driver: str | None = None,
        keys: AbstractSet[str],
        default_values: Mapping[str, ConstantValue | None],
    ) -> dict[str, DataType]:
        from atoti_jdbc._infer_driver import (  # pylint: disable=nested-import,undeclared-dependency
            infer_driver,
        )

        url = normalize_jdbc_url(url)

        return JdbcDataSource(
            load_data_into_table=self._java_api.load_data_into_table,
            infer_types=self._java_api.infer_table_types_from_source,
        ).infer_sql_types(
            sql,
            keys=keys,
            default_values={
                column_name: None if value is None else Constant(value)
                for column_name, value in default_values.items()
            },
            url=url,
            driver=driver or infer_driver(url),
        )

    @doc(**_TABLE_CREATION_KWARGS, **_SQL_KWARGS, keys_argument="""{"ID"}""")
    def read_sql(
        self,
        sql: str,
        /,
        *,
        url: str,
        table_name: str,
        driver: str | None = None,
        keys: AbstractSet[str] | Sequence[str] = frozenset(),
        partitioning: str | None = None,
        types: Mapping[str, DataType] = frozendict(),
        default_values: Mapping[str, ConstantValue | None] = frozendict(),
    ) -> Table:
        """Create a table from the result of the passed SQL query.

        Args:
            {sql}
            {url}
            {driver}
            {table_name}
            {keys}
            {partitioning}
            types: Types for some or all columns of the table.
                Types for non specified columns will be inferred from the SQL types.
            {default_values}

        Example:
            .. doctest:: read_sql

                >>> table = session.read_sql(
                ...     "SELECT * FROM MYTABLE;",
                ...     url=f"h2:file:{{RESOURCES_PATH}}/h2-database;USER=root;PASSWORD=pass",
                ...     table_name="Cities",
                ...     keys={keys_argument},
                ... )
                >>> table.row_count
                5

            .. doctest:: read_sql
                :hide:

                Remove the edited H2 database from Git's working tree.
                >>> session.close()
                >>> import os
                >>> os.system(f"git checkout -- {{RESOURCES_PATH}}/h2-database.mv.db")
                0

        """
        inferred_types = self._infer_sql_types(
            sql,
            url=url,
            driver=driver,
            keys=set(keys),
            default_values=default_values,
        )
        types = {**inferred_types, **types}
        table = self.create_table(
            table_name,
            types=types,
            keys=keys,
            partitioning=partitioning,
            default_values=default_values,
        )
        table.load_sql(sql, url=url, driver=driver)
        return table

    @property
    def ready(self) -> bool:
        """Whether the session is ready or not.

        When ``False``, the server will reject most requests made by users without the :guilabel:`ROLE_ADMIN` role with an HTTP `503 Service Unavailable` status.

        Note:
            This property has no impact in the community edition since the :guilabel:`ROLE_ADMIN` role is always granted.

        This can be used to prevent queries from being made on a session that has not finished its initial setup process (tables and cubes creation, data loading, etc).
        """
        return self._java_api.get_readiness()

    @ready.setter
    def ready(self, ready: bool, /) -> None:
        self._java_api.set_readiness(ready)
        self._java_api.refresh()

    @deprecated(
        "`Session.start_transaction()` has moved to `Tables.data_transaction()`, replace `session.start_transaction()` with `session.tables.data_transaction()`.",
        category=_DEPRECATED_WARNING_CATEGORY,
    )
    def start_transaction(self) -> AbstractContextManager[None]:
        """Create a data transaction.

        :meta private:
        """
        return self.tables.data_transaction()

    @doc(
        **_TRANSACTION_DOC_KWARGS,
        base_keys_argument="""{"ID"}""",
        base_types_argument="""{"ID": "String", "Quantity": "int"}""",
    )
    def data_model_transaction(
        self,
        *,
        allow_nested: bool = True,
    ) -> AbstractContextManager[None]:
        """Create a data model transaction to batch multiple data model changes.

        Start the transaction with a ``with`` statement.
        The changes will be visible from other clients (e.g. Atoti UI) once the transaction is closed.

        Data model transactions offer "read-your-writes" behavior: changes made inside the transaction are visible to the following statements.

        Note:
            Data model transactions cannot be mixed with data loading operations.

        Attention:
            Data model transactions are work in progress:

            * atomicity and isolation are not guaranteed yet;
            * only measure-related changes are supported for now.

        Args:
            {allow_nested}

        Example:
            >>> base_table = session.create_table(
            ...     "Base",
            ...     keys={base_keys_argument},
            ...     types={base_types_argument},
            ... )
            >>> cube = session.create_cube(base_table)
            >>> h, l, m = cube.hierarchies, cube.levels, cube.measures
            >>> with session.data_model_transaction():
            ...     m["Quantity - 1"] = m["Quantity.SUM"] - 1
            ...
            ...     m["Quantity + 1"] = m["Quantity.SUM"] + 1
            ...     m["Quantity + 1"].description = "Just slightly off"
            ...     m["Quantity + 1"].folder = "Test"
            ...
            ...     m["Quantity + 2"] = m["Quantity + 1"] + 1
            ...     m["Quantity + 2"].formatter = "INT[# ###]"
            >>> base_table += ("123xyz", 1)
            >>> cube.query(
            ...     m["Quantity.SUM"],
            ...     m["Quantity - 1"],
            ...     m["Quantity + 1"],
            ...     m["Quantity + 2"],
            ... )
              Quantity.SUM Quantity - 1 Quantity + 1 Quantity + 2
            0            1            0            2           3

            With nested transactions allowed:

            >>> def add_foo(cube_name, /, *, session):
            ...     cube = session.cubes[cube_name]
            ...     m = cube.measures
            ...     with session.data_model_transaction():
            ...         m["foo"] = 2_000
            ...         m["foo"].formatter = "INT[# ###]"
            >>> with session.data_model_transaction():
            ...     add_foo(cube.name, session=session)
            ...     m["foo + 1"] = m["foo"] + 1

            With nested transactions not allowed:

            >>> def add_foo_and_query_it(cube_name, /, *, session):
            ...     cube = session.cubes[cube_name]
            ...     m = cube.measures
            ...     with session.data_model_transaction(allow_nested=False):
            ...         m["foo"] = 2_000
            ...         m["foo"].formatter = "INT[# ###]"
            ...     return cube.query(m["foo"])
            >>> add_foo_and_query_it(cube.name, session=session)
                 foo
            0  2000
            >>> with session.data_model_transaction():
            ...     add_foo_and_query_it(cube.name, session=session)
            Traceback (most recent call last):
                ...
            RuntimeError: Cannot start this transaction inside another transaction since nesting is not allowed.

        See Also:
            :meth:`~atoti.tables.Tables.data_transaction`.

        """

        def commit() -> None:
            for cube_name in self.cubes:
                self._java_api.publish_measures(cube_name)

        return transact_data_model(
            allow_nested=allow_nested,
            commit=commit,
            session_id=self._id,
        )

    def create_cube(
        self,
        base_table: Table,
        name: str | None = None,
        *,
        mode: Literal["auto", "manual", "no_measures"] = "auto",
        filter: Condition[  # noqa: A002
            ColumnIdentifier,
            ConditionComparisonOperatorBound,
            Constant | None,
            ConditionCombinationOperatorBound,
        ]
        | None = None,
        **kwargs: Any,
    ) -> Cube:
        """Create a cube based on the passed table.

        Args:
            base_table: The base table of the cube.
            name: The name of the created cube.
                Defaults to the name of the base table.
            mode: The cube creation mode:

                * ``auto``: Creates hierarchies for every key column or non-numeric column of the table, and measures for every numeric column.
                * ``manual``: Does not create any hierarchy or measure (except from the count).
                * ``no_measures``: Creates the hierarchies like ``auto`` but does not create any measures.

                Example:
                    >>> table = session.create_table(
                    ...     "Table",
                    ...     types={"id": tt.STRING, "value": tt.DOUBLE},
                    ... )
                    >>> cube_auto = session.create_cube(table)
                    >>> sorted(cube_auto.measures)
                    ['contributors.COUNT', 'update.TIMESTAMP', 'value.MEAN', 'value.SUM']
                    >>> list(cube_auto.hierarchies)
                    [('Table', 'id')]
                    >>> cube_no_measures = session.create_cube(table, mode="no_measures")
                    >>> sorted(cube_no_measures.measures)
                    ['contributors.COUNT', 'update.TIMESTAMP']
                    >>> list(cube_no_measures.hierarchies)
                    [('Table', 'id')]
                    >>> cube_manual = session.create_cube(table, mode="manual")
                    >>> sorted(cube_manual.measures)
                    ['contributors.COUNT', 'update.TIMESTAMP']
                    >>> list(cube_manual.hierarchies)
                    []

            filter: If not ``None``, only rows of the database matching this condition will be fed to the cube.
                It can also reduce costs when using DirectQuery since the filter will be applied to the queries executed on the external database to feed the cube.

                Example:
                    >>> df = pd.DataFrame(
                    ...     columns=["Product"],
                    ...     data=[
                    ...         ("phone"),
                    ...         ("watch"),
                    ...         ("laptop"),
                    ...     ],
                    ... )
                    >>> table = session.read_pandas(df, table_name="Filtered table")
                    >>> cube = session.create_cube(table, "Default")
                    >>> cube.query(
                    ...     cube.measures["contributors.COUNT"],
                    ...     levels=[cube.levels["Product"]],
                    ... )
                            contributors.COUNT
                    Product
                    laptop                   1
                    phone                    1
                    watch                    1
                    >>> filtered_cube = session.create_cube(
                    ...     table,
                    ...     "Filtered",
                    ...     filter=table["Product"].isin("watch", "laptop"),
                    ... )
                    >>> filtered_cube.query(
                    ...     filtered_cube.measures["contributors.COUNT"],
                    ...     levels=[filtered_cube.levels["Product"]],
                    ... )
                            contributors.COUNT
                    Product
                    laptop                   1
                    watch                    1

        """
        if name is None:
            name = base_table.name
        private_parameters = _CreateCubePrivateParameters(**kwargs)

        self._java_api.create_cube_from_table(
            name,
            application_name=private_parameters.application_name or name,
            table_identifier=base_table._identifier,
            mode=mode.upper(),
            filter=filter,
        )
        self._java_api.refresh()
        if self.ready:
            # AutoJoin distributed clusters if the session has been marked as ready
            self._java_api.auto_join_distributed_clusters(cube_name=name)
            self._java_api.refresh()

        return self.cubes[name]

    def create_scenario(self, name: str, *, origin: str | None = None) -> None:
        """Create a new source scenario.

        Args:
            name: The name of the scenario.
            origin: The scenario to fork.
        """
        self._java_api.create_scenario(name, parent_scenario_name=origin)

    def delete_scenario(self, name: str) -> None:
        """Delete the source scenario with the provided name if it exists."""
        self._java_api.delete_scenario(name)

    @property
    def scenarios(self) -> AbstractSet[str]:
        """Names of the source scenarios of the session."""
        return frozenset(self._java_api.get_scenarios())

    def _warn_if_license_about_to_expire(
        self,
        *,
        minimum_remaining_time: timedelta = _DEFAULT_LICENSE_MINIMUM_REMAINING_TIME,
    ) -> None:
        remaining_time = self._java_api.license_end_date - datetime.now()
        if remaining_time < minimum_remaining_time:
            message = f"""The{" embedded " if self._java_api.is_community_license else " "}license key is about to expire, {"update to Atoti's latest version or request an evaluation license key" if self._java_api.is_community_license else "contact ActiveViam to get a new license key"} in the coming {remaining_time.days} days."""
            warn(
                message,
                category=RuntimeWarning,
                stacklevel=2,
            )

    @property
    def widget(self) -> object:
        """Widget to visualize the data in the session interactively.

        Return it from a notebook code cell to display it.
        The widget will appear in the output of this cell and its state will be stored in the metadata of this cell.
        The widget state is automatically updated as the widget is modified through UI interactions.

        Supported notebook environments and their corresponding required dependency:

        * JupyterLab: :mod:`atoti-jupyterlab <atoti_jupyterlab>`.

        Note:
            Some notebook environments provide a cell metadata editor.
            It can be used in the rare situations where the widget state has to be edited manually.

            For instance, in JupyterLab, this editor can be found by opening the :guilabel:`Notebook tools` sidebar and expanding the :guilabel`Advanced Tools` section.
        """
        return Widget(
            block_until_loaded=self._block_until_widget_loaded,
            generate_authentication_headers=self._atoti_client.activeviam_client.generate_authentication_headers,
            get_creation_code=self._get_widget_creation_code,
            session_id=self._id,
            session_location=self._location,
        )

    @property
    def _location(self) -> Mapping[str, object]:
        if self.__java_api is None:
            return frozendict({"url": self.url})

        parsed_url = urlparse(self.url)

        return frozendict(
            {
                "https": parsed_url.scheme == "https",
                "port": parsed_url.port,
            },
        )

    @property
    def url(self) -> str:
        """URL of the session.

        See Also:
            :attr:`~atoti.Session.link`.
        """
        return self._atoti_client.activeviam_client.url

    @property
    @deprecated(
        "Accessing `Session.port` is deprecated, use `Session.url` instead (and parse it with `urllib.parse.urlparse` if necessary).",
        category=_DEPRECATED_WARNING_CATEGORY,
    )
    def port(self) -> int:
        """Port on which the session is exposed.

        :meta private:
        """
        parsed_url = urlparse(self.url)
        if parsed_url.port is not None:
            return parsed_url.port
        if parsed_url.scheme == "http":
            return 80
        if parsed_url.scheme == "https":
            return 443
        raise ValueError(f"Unsupported URL scheme: {parsed_url.scheme}.")

    @property
    def _basic_credentials(self) -> MutableMapping[str, str] | None:
        return BasicCredentials(java_api=self._java_api)

    @property
    def security(self) -> Security:
        return Security(
            activeviam_client=self._atoti_client.activeviam_client,
            basic_credentials=self._basic_credentials,
        )

    def wait(self) -> None:
        """Wait for the underlying server subprocess to terminate.

        This will prevent the Python process from exiting.
        """
        self._server_subprocess.wait()

    @property
    def link(self) -> Link:
        """Link to the session.

        Return it from a notebook code cell to display it.

        * If used inside JupyterLab with :mod:`atoti-jupyterlab <atoti_jupyterlab>` installed, the JupyterLab extension will try to reach the session in this order:

        #. `Jupyter Server Proxy <https://jupyter-server-proxy.readthedocs.io/>`__ if it is enabled.
        #. ``f"{session_protocol}//{jupyter_server_hostname}:{session_port}"``.
        #. :attr:`url`.

        * If used in another environment, :attr:`url` wil be used.

        When :attr:`url` is used and the session is running on another machine, the link may not be reachable.
        In that situation, the session may be reached from ``f"{public_ip_or_domain_of_machine_hosting_session}:{session_port}"``.

        A path can be added to the link with ``/``.

        Example:
            Linking to an existing dashboard:

            .. testcode::

                dashboard_id = "92i"
                session.link / "#/dashboard/{dashboard_id}"
        """
        return Link(session_location=self._location, session_url=self.url)

    def _get_data_types(
        self,
        identifiers: Collection[IdentifierT_co],
        /,
        *,
        cube_name: str,
    ) -> dict[IdentifierT_co, DataType]:
        return self.cubes[cube_name]._get_data_types(identifiers)

    @overload
    def query_mdx(
        self,
        mdx: str,
        /,
        *,
        context: Context = ...,
        explain: Literal[False] = ...,
        keep_totals: bool = ...,
        mode: Literal["pretty"] = ...,
        timeout: Duration = ...,
    ) -> MdxQueryResult: ...

    @overload
    def query_mdx(
        self,
        mdx: str,
        /,
        *,
        context: Context = ...,
        explain: Literal[False] = ...,
        keep_totals: bool = ...,
        mode: Literal["pretty", "raw"] = ...,
        timeout: Duration = ...,
    ) -> pd.DataFrame: ...

    @overload
    def query_mdx(
        self,
        mdx: str,
        /,
        *,
        context: Context = ...,
        explain: Literal[True],
        keep_totals: bool = ...,
        mode: Literal["pretty", "raw"] = ...,
        timeout: Duration = ...,
    ) -> QueryExplanation: ...

    @doc(**_QUERY_KWARGS)
    def query_mdx(
        self,
        mdx: str,
        /,
        *,
        context: Context = frozendict(),
        explain: bool = False,
        keep_totals: bool = False,
        mode: Literal["pretty", "raw"] = "pretty",
        timeout: Duration = _DEFAULT_QUERY_TIMEOUT,
    ) -> MdxQueryResult | pd.DataFrame | QueryExplanation:
        """Execute an MDX query.

        {widget_conversion}

        Args:
            mdx: The MDX ``SELECT`` query to execute.

                Regardless of the axes on which levels and measures appear in the MDX, the returned DataFrame will have all levels on rows and measures on columns.

                Example:
                    .. doctest:: query_mdx

                        >>> from datetime import date
                        >>> df = pd.DataFrame(
                        ...     columns=["Country", "Date", "Price"],
                        ...     data=[
                        ...         ("China", date(2020, 3, 3), 410.0),
                        ...         ("France", date(2020, 1, 1), 480.0),
                        ...         ("France", date(2020, 2, 2), 500.0),
                        ...         ("France", date(2020, 3, 3), 400.0),
                        ...         ("India", date(2020, 1, 1), 360.0),
                        ...         ("India", date(2020, 2, 2), 400.0),
                        ...         ("UK", date(2020, 2, 2), 960.0),
                        ...     ],
                        ... )
                        >>> table = session.read_pandas(
                        ...     df, keys=["Country", "Date"], table_name="Prices"
                        ... )
                        >>> cube = session.create_cube(table)

                    This MDX:

                    .. doctest:: query_mdx

                        >>> mdx = (
                        ...     "SELECT"
                        ...     "  NON EMPTY Hierarchize("
                        ...     "    DrilldownLevel("
                        ...     "      [Prices].[Country].[ALL].[AllMember]"
                        ...     "    )"
                        ...     "  ) ON ROWS,"
                        ...     "  NON EMPTY Crossjoin("
                        ...     "    [Measures].[Price.SUM],"
                        ...     "    Hierarchize("
                        ...     "      DrilldownLevel("
                        ...     "        [Prices].[Date].[ALL].[AllMember]"
                        ...     "      )"
                        ...     "    )"
                        ...     "  ) ON COLUMNS"
                        ...     "  FROM [Prices]"
                        ... )

                    Returns this DataFrame:

                    .. doctest:: query_mdx

                        >>> session.query_mdx(mdx, keep_totals=True)
                                           Price.SUM
                        Date       Country
                        Total               3,510.00
                        2020-01-01            840.00
                        2020-02-02          1,860.00
                        2020-03-03            810.00
                                   China      410.00
                        2020-01-01 China
                        2020-02-02 China
                        2020-03-03 China      410.00
                                   France   1,380.00
                        2020-01-01 France     480.00
                        2020-02-02 France     500.00
                        2020-03-03 France     400.00
                                   India      760.00
                        2020-01-01 India      360.00
                        2020-02-02 India      400.00
                        2020-03-03 India
                                   UK         960.00
                        2020-01-01 UK
                        2020-02-02 UK         960.00
                        2020-03-03 UK

                    But, if it was displayed into a pivot table, would look like this:

                    +---------+-------------------------------------------------+
                    | Country | Price.sum                                       |
                    |         +----------+------------+------------+------------+
                    |         | Total    | 2020-01-01 | 2020-02-02 | 2020-03-03 |
                    +---------+----------+------------+------------+------------+
                    | Total   | 3,510.00 | 840.00     | 1,860.00   | 810.00     |
                    +---------+----------+------------+------------+------------+
                    | China   | 410.00   |            |            | 410.00     |
                    +---------+----------+------------+------------+------------+
                    | France  | 1,380.00 | 480.00     | 500.00     | 400.00     |
                    +---------+----------+------------+------------+------------+
                    | India   | 760.00   | 360.00     | 400.00     |            |
                    +---------+----------+------------+------------+------------+
                    | UK      | 960.00   |            | 960.00     |            |
                    +---------+----------+------------+------------+------------+

                    .. doctest:: query_mdx
                        :hide:

                        Clear the session to isolate the multiple methods sharing this docstring.
                        >>> session._clear()

            {context}
            {explain}
            keep_totals: Whether the resulting DataFrame should contain, if they are present in the query result, the grand total and subtotals.
                {totals}

            {mode}

              {pretty}

              {raw}

            {timeout}

        See Also:
            :meth:`atoti.Cube.query`

        """
        if explain:
            return self._atoti_client.explain_mdx_query(
                context=context,
                mdx=mdx,
                timeout=timeout,
            )

        return self._atoti_client.execute_mdx_query(
            context=context,
            get_cube_discovery=self._atoti_client.get_cube_discovery,
            get_data_types=self._get_data_types,
            get_widget_creation_code=self._get_widget_creation_code,
            keep_totals=keep_totals,
            mdx=mdx,
            mode=mode,
            session_id=self._id,
            timeout=timeout,
        )

    def _get_widget_creation_code(self) -> str | None:
        session_variable_name = find_corresponding_top_level_variable_name(self)

        if not session_variable_name:
            return None

        property_name = "widget"
        assert hasattr(self, property_name)
        return f"{session_variable_name}.{property_name}"

    def _block_until_widget_loaded(self, widget_id: str) -> None:
        if self.__java_api is None:
            return

        self._java_api.block_until_widget_loaded(widget_id)

    def endpoint(
        self,
        route: str,
        *,
        method: Literal["POST", "GET", "PUT", "DELETE"] = "GET",
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Create a custom endpoint at ``/atoti/pyapi/{route}``.

        This is useful to reuse Atoti's built-in server instead of adding a `FastAPI <https://fastapi.tiangolo.com/>`__ or `Flask <https://flask.palletsprojects.com/>`__ server to the project.
        This way, when deploying the project in a container or a VM, only one port (the one of the Atoti server) can be exposed instead of two.
        Since custom endpoints are exposed by Atoti's server, they automatically inherit from the configured :func:`atoti.Session`'s *authentication* and *https* parameter.

        The decorated function must take three parameters with types :class:`atoti.pyapi.User`, :class:`atoti.pyapi.HttpRequest`, and :class:`atoti.Session` and return a response body as a Python data structure that can be converted to JSON.

        Args:
            route: The path suffix after ``/atoti/pyapi/``.
                For instance, if ``custom/search`` is passed, a request to ``/atoti/pyapi/custom/search?query=test#results`` will match.
                The route should not contain the query (``?``) or fragment (``#``).

                Path parameters can be configured by wrapping their name in curly braces in the route.
            method: The HTTP method the request must be using to trigger this endpoint.
                ``DELETE``, ``POST``, and ``PUT`` requests can have a body but it must be JSON.

        Example:
            .. doctest:: Session.endpoint
                :skipif: True

                >>> import httpx
                >>> df = pd.DataFrame(
                ...     columns=["Year", "Month", "Day", "Quantity"],
                ...     data=[
                ...         (2019, 7, 1, 15),
                ...         (2019, 7, 2, 20),
                ...     ],
                ... )
                >>> table = session.read_pandas(df, table_name="Quantity")
                >>> table.head()
                Year  Month  Day  Quantity
                0  2019      7    1        15
                1  2019      7    2        20
                >>> endpoints_base_url = f"{session.url}/atoti/pyapi"
                >>> @session.endpoint("tables/{table_name}/count", method="GET")
                ... def get_table_row_count(request, user, session):
                ...     table_name = request.path_parameters["table_name"]
                ...     return session.tables[table_name].row_count
                >>> httpx.get(
                ...     f"{endpoints_base_url}/tables/Quantity/count"
                ... ).raise_for_status().json()
                2
                >>> @session.endpoint("tables/{table_name}/rows", method="POST")
                ... def append_rows_to_table(request, user, session):
                ...     rows = request.body
                ...     table_name = request.path_parameters["table_name"]
                ...     session.tables[table_name].append(*rows)
                >>> httpx.post(
                ...     f"{endpoints_base_url}/tables/Quantity/rows",
                ...     json=[
                ...         {"Year": 2021, "Month": 5, "Day": 19, "Quantity": 50},
                ...         {"Year": 2021, "Month": 5, "Day": 20, "Quantity": 6},
                ...     ],
                ... ).status_code
                200
                >>> httpx.get(
                ...     f"{endpoints_base_url}/tables/Quantity/count"
                ... ).raise_for_status().json()
                4
                >>> table.head()
                Year  Month  Day  Quantity
                0  2019      7    1        15
                1  2019      7    2        20
                2  2021      5   19        50
                3  2021      5   20         6

        """
        if route[0] == "/" or "?" in route or "#" in route:
            raise ValueError(
                f"Invalid route '{route}'. It should not start with '/' and not contain '?' or '#'.",
            )

        def endpoint_decorator(callback: Callable[..., Any]) -> Callable[..., Any]:
            self._java_api.create_endpoint(
                http_method=method,
                route=route,
                handler=EndpointHandler(callback, session=self),
            )
            return callback

        return endpoint_decorator

    def export_translations_template(self, path: Path) -> None:
        """Export a template containing all translatable values in the session's cubes.

        Args:
            path: The path at which to write the template.
        """
        self._java_api.export_i18n_template(path)

    def _create_memory_analysis_report(self, directory: Path, /) -> None:
        """Create a memory analysis report.

        Args:
            directory: The path of the directory where the report will be created.
              Its parent directory must already exist.
        """
        assert directory.parent.is_dir()
        self._java_api.memory_analysis_export(directory.parent, directory.name)

    def _clear(self) -> None:
        if self.__java_api is None:
            return
        self.__java_api.clear_session()
