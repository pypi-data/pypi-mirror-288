from collections.abc import Generator
from pathlib import Path
from rdetoolkit.config import Config as Config
from rdetoolkit.models.rde2types import RawFiles as RawFiles, RdeInputDirPaths as RdeInputDirPaths, RdeOutputResourcePath as RdeOutputResourcePath
from rdetoolkit.modeproc import _CallbackType

def check_files(srcpaths: RdeInputDirPaths, *, mode: str | None) -> tuple[RawFiles, Path | None]: ...
def generate_folder_paths_iterator(raw_files_group: RawFiles, invoice_org_filepath: Path, invoice_schema_filepath: Path) -> Generator[RdeOutputResourcePath, None, None]: ...
def run(*, custom_dataset_function: _CallbackType | None = ..., config: Config | None = ...) -> None: ...
