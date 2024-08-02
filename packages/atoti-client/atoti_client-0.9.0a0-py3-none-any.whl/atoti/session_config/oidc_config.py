from collections.abc import Set as AbstractSet
from typing import Annotated, Literal, final

from pydantic import AfterValidator
from pydantic.dataclasses import dataclass

from .._pydantic import PYDANTIC_CONFIG as _PYDANTIC_CONFIG


def _normalize_role_claim(
    role_claim: str | tuple[str, ...],
    /,
) -> tuple[str, ...]:
    return (role_claim,) if isinstance(role_claim, str) else role_claim


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class OidcConfig:
    """The config to delegate authentication to an `OpenID Connect <https://openid.net/connect/>`__ provider (Auth0, Google, Keycloak, etc.).

    The user's roles are defined using :attr:`atoti.security.Security.oidc` and :attr:`~atoti.security.Security.individual_roles`.

    Example:
        >>> config = tt.OidcConfig(
        ...     provider_id="auth0",
        ...     issuer_url="https://example.auth0.com",
        ...     client_id="some client ID",
        ...     client_secret="some client secret",
        ...     name_claim="email",
        ...     scopes={"email", "profile"},
        ...     roles_claims={
        ...         "https://example.com/roles",
        ...         ("other", "path", "to", "roles"),
        ...     },
        ... )

    """

    provider_id: str
    """The name of the provider.

    It is used to build the redirect URL: ``f"{session_url}/login/oauth2/code/{provider_id}"``.
    """

    issuer_url: str
    """The issuer URL parameter from the provider's OpenID Connect configuration endpoint."""

    client_id: str
    """The app's client ID, obtained from the authentication provider."""

    client_secret: str
    """The app's client secret, obtained from the authentication provider."""

    use_client_secret_as_certificate: bool = False
    """If ``True``, the passed :attr:`client_secret` must be a client certificate instead of a random secret.
    This client certificate will be passed in the ``X-Cert`` header of the request made to the OIDC provider to retrieve an access token.
    """

    name_claim: str | None = None
    """The name of the claim in the ID token to use as the name of the user."""

    roles_claims: AbstractSet[
        Annotated[
            str | tuple[str, ...],
            AfterValidator(_normalize_role_claim),
        ]
    ] = frozenset()
    """The claims of the ID token from which to extract roles to use as keys in the :attr:`~atoti.security.oidc_security.OidcSecurity.role_mapping`.

    When an element of the set is a tuple, the tuple elements will be used as a path pointing to a nested value in the token.
    """

    scopes: AbstractSet[str] = frozenset()
    """The scopes to request from the authentication provider."""

    access_token_format: Literal["jwt", "opaque"] = "jwt"
    """The format of the access tokens delivered by the OIDC provider.

    Opaque tokens involve another request to the OIDC provider's user info endpoint to retrieve the user details.
    The URL of this user info endpoint will be fetched from the ``f"{issuer_url}/.well-known/openid-configuration"`` endpoint.

    See Also:
        Opaque tokens can be used with :class:`atoti.OAuth2ResourceOwnerPasswordAuthentication`.
    """
