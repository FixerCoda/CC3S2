from typing import Any, Mapping, Protocol


class HttpClient(Protocol):
    def get_json(
        self, url: str, headers: Mapping[str, str] | None = None, timeout: float = 2.0
    ) -> Any: ...
