from typing import Final, final

from ._service import Service
from .default_roles import DefaultRoles
from .role_mapping import RoleMapping


@final
class LdapSecurity:
    """Manage LDAP security on the session.

    Note:
        This requires :attr:`atoti.SecurityConfig.sso` to be an instance of :class:`~atoti.LdapConfig`.

    Example:
        >>> session = tt.Session.start(
        ...     tt.SessionConfig(
        ...         security=tt.SecurityConfig(
        ...             sso=tt.LdapConfig(
        ...                 url="ldap://example.com:389",
        ...                 base_dn="dc=example,dc=com",
        ...                 user_search_base="ou=people",
        ...                 group_search_base="ou=roles",
        ...             )
        ...         )
        ...     )
        ... )
        >>> table = session.create_table("Restrictions example", types={"City": tt.STRING})
        >>> session.security.restrictions["ROLE_MATHS"] = table["City"] == "Paris"

        Roles from the authentication provider can be mapped to roles in the session:

        >>> session.security.ldap.role_mapping["MATHEMATICIANS"] = {
        ...     "ROLE_MATHS",
        ...     "ROLE_USER",
        ... }
        >>> sorted(session.security.ldap.role_mapping["MATHEMATICIANS"])
        ['ROLE_MATHS', 'ROLE_USER']

        Default roles can be given to users who have no individual or mapped roles granted:

        >>> session.security.ldap.default_roles.add("ROLE_USER")
        >>> session.security.ldap.default_roles
        {'ROLE_USER'}
    """

    def __init__(
        self,
        *,
        default_roles: DefaultRoles,
        role_mapping: RoleMapping,
        service: Service,
    ) -> None:
        self._default_roles: Final = default_roles
        self._role_mapping: Final = role_mapping
        self._service: Final = service

    @property
    def default_roles(self) -> DefaultRoles:
        return self._default_roles

    @property
    def role_mapping(self) -> RoleMapping:
        return self._role_mapping
