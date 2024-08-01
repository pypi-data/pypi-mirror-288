import pandas as pd
from _typeshed import Incomplete
from pathlib import Path
from rdetoolkit.exceptions import StructuredError as StructuredError
from rdetoolkit.interfaces.filechecker import ICompressedFileStructParser as ICompressedFileStructParser
from rdetoolkit.invoicefile import check_exist_rawfiles as check_exist_rawfiles
from rdetoolkit.rdelogger import get_logger as get_logger

logger: Incomplete

class CompressedFlatFileParser(ICompressedFileStructParser):
    xlsx_invoice: Incomplete
    def __init__(self, xlsx_invoice: pd.DataFrame) -> None: ...
    def read(self, zipfile: Path, target_path: Path) -> list[tuple[Path, ...]]: ...

class CompressedFolderParser(ICompressedFileStructParser):
    xlsx_invoice: Incomplete
    def __init__(self, xlsx_invoice: pd.DataFrame) -> None: ...
    def read(self, zipfile: Path, target_path: Path) -> list[tuple[Path, ...]]: ...
    def validation_uniq_fspath(self, target_path: str | Path, exclude_names: list[str]) -> dict[str, list[Path]]: ...

def parse_compressedfile_mode(xlsx_invoice: pd.DataFrame) -> ICompressedFileStructParser: ...
