from _typeshed import Incomplete as Incomplete
from collections.abc import Sequence
from pathlib import Path
from rdetoolkit.interfaces.filechecker import IInputFileChecker as IInputFileChecker
from rdetoolkit.models.rde2types import RawFiles as RawFiles

class InvoiceChecker(IInputFileChecker):
    out_dir_temp: Incomplete
    def __init__(self, unpacked_dir_basename: Path) -> None: ...
    def parse(self, src_dir_input: Path) -> tuple[RawFiles, Path | None]: ...

class ExcelInvoiceChecker(IInputFileChecker):
    out_dir_temp: Incomplete
    def __init__(self, unpacked_dir_basename: Path) -> None: ...
    def parse(self, src_dir_input: Path) -> tuple[RawFiles, Path | None]: ...
    def get_index(self, paths: Path, sort_items: Sequence) -> int: ...

class RDEFormatChecker(IInputFileChecker):
    out_dir_temp: Incomplete
    def __init__(self, unpacked_dir_basename: Path) -> None: ...
    def parse(self, src_dir_input: Path) -> tuple[RawFiles, Path | None]: ...

class MultiFileChecker(IInputFileChecker):
    out_dir_temp: Incomplete
    def __init__(self, unpacked_dir_basename: Path) -> None: ...
    def parse(self, src_dir_input: Path) -> tuple[RawFiles, Path | None]: ...
