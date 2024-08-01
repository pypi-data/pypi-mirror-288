from _typeshed import Incomplete as Incomplete
from pathlib import Path
from typing import Any

class MetadataValidator:
    schema: Incomplete
    def __init__(self) -> None: ...
    def validate(self, *, path: str | Path | None = ..., json_obj: dict[str, Any] | None = ...) -> dict[str, Any]: ...

def metadata_validate(path: str | Path) -> None: ...

class InvoiceValidator:
    pre_basic_info_schema: Incomplete
    schema_path: Incomplete
    schema: Incomplete
    def __init__(self, schema_path: str | Path) -> None: ...
    def validate(self, *, path: str | Path | None = ..., obj: dict[str, Any] | None = ...) -> dict[str, Any]: ...

def invoice_validate(path: str | Path, schema: str | Path) -> None: ...
