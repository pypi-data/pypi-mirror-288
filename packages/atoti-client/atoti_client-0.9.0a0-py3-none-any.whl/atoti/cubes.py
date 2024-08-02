from collections.abc import Callable, Mapping, Set as AbstractSet
from typing import Final, final

from typing_extensions import override

from ._atoti_client import AtotiClient
from ._collections import DelegatingMutableMapping
from ._ipython import ReprJson, ReprJsonable
from ._java_api import JavaApi
from ._local_session_only_feature_error import LocalSessionOnlyFeatureError
from .cube import Cube, _ReadPandas


@final
class Cubes(DelegatingMutableMapping[str, Cube], ReprJsonable):  # type: ignore[misc]
    r"""Manage the :class:`~atoti.Cube`\ s of a :class:`~atoti.Session`."""

    def __init__(
        self,
        *,
        atoti_client: AtotiClient,
        get_widget_creation_code: Callable[[], str | None],
        java_api: JavaApi | None,
        read_pandas: _ReadPandas,
        session_id: str,
    ) -> None:
        self._atoti_client: Final = atoti_client
        self._get_widget_creation_code: Final = get_widget_creation_code
        self._java_api: Final = java_api
        self._read_pandas: Final = read_pandas
        self._session_id: Final = session_id

    def _get_cube_names(self, *, key: str | None) -> list[str]:
        # Remove `not self._java_api` once distributed sessions are supported.
        if not self._java_api or not self._atoti_client._graphql_client:
            cube_discovery = self._atoti_client.get_cube_discovery()
            return [
                cube_name
                for cube_name in cube_discovery.cubes
                if key is None or cube_name == key
            ]

        if key is None:
            return [
                cube.name
                for cube in self._atoti_client._graphql_client.get_cube_names().cubes
            ]

        cube = self._atoti_client._graphql_client.get_cube_name(cube_name=key).cube
        return [cube.name] if cube else []

    @override
    def _get_delegate(self, *, key: str | None) -> Mapping[str, Cube]:
        return {
            cube_name: Cube(
                cube_name,
                atoti_client=self._atoti_client,
                get_widget_creation_code=self._get_widget_creation_code,
                java_api=self._java_api,
                read_pandas=self._read_pandas,
                session_id=self._session_id,
            )
            for cube_name in self._get_cube_names(key=key)
        }

    @override
    def _update_delegate(
        self,
        other: Mapping[str, Cube],
        /,
    ) -> None:
        raise AssertionError("Use `Session.create_cube()` to create a cube.")

    @override
    def _delete_delegate_keys(self, keys: AbstractSet[str], /) -> None:
        if self._java_api is None:
            raise LocalSessionOnlyFeatureError

        for key in keys:
            self._java_api.delete_cube(key)

    @override
    def _repr_json_(self) -> ReprJson:
        """Return the JSON representation of cubes."""
        return (
            {name: cube._repr_json_()[0] for name, cube in sorted(self.items())},
            {"expanded": False, "root": "Cubes"},
        )
