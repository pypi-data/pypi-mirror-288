from dataclasses import KW_ONLY

from pydantic.dataclasses import dataclass

from ._pydantic import PYDANTIC_CONFIG as _PYDANTIC_CONFIG


@dataclass(config=_PYDANTIC_CONFIG, frozen=True)
class KeyPair:  # pylint: disable=final-class (inherited by client side encryption configs)
    public_key: str
    """The public key."""

    private_key: str
    """The private key."""

    _: KW_ONLY
