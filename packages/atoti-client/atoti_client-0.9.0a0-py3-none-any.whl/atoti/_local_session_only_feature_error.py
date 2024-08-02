from typing import final


@final
class LocalSessionOnlyFeatureError(RuntimeError):
    def __init__(self) -> None:
        super().__init__("This feature is only supported in local sessions.")
