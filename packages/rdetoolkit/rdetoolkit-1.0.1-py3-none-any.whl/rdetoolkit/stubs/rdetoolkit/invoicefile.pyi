import pandas as pd
from _typeshed import Incomplete
from pathlib import Path
from rdetoolkit import rde2util as rde2util
from rdetoolkit.exceptions import StructuredError as StructuredError
from rdetoolkit.models.rde2types import RdeFsPath as RdeFsPath, RdeOutputResourcePath as RdeOutputResourcePath
from rdetoolkit.rde2util import CharDecEncoding as CharDecEncoding, StorageDir as StorageDir, read_from_json_file as read_from_json_file
from typing import Any

def read_excelinvoice(excelinvoice_filepath: RdeFsPath) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: ...
def check_exist_rawfiles(dfexcelinvoice: pd.DataFrame, excel_rawfiles: list[Path]) -> list[Path]: ...
def overwrite_invoicefile_for_dpfterm(invoiceobj: dict[str, Any], invoice_dst_filepath: RdeFsPath, invoiceschema_filepath: RdeFsPath, invoice_info: dict[str, Any]) -> None: ...
def check_exist_rawfiles_for_folder(dfexcelinvoice: pd.DataFrame, rawfiles_tpl: tuple) -> list: ...

class InvoiceFile:
    invoice_path: Incomplete
    def __init__(self, invoice_path: Path) -> None: ...
    @property
    def invoice_obj(self) -> dict[str, Any]: ...
    def __getitem__(self, key: str) -> Any: ...
    def __setitem__(self, key: str, value: Any) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def read(self, *, target_path: Path | None = ...) -> dict: ...
    def overwrite(self, dst_file_path: Path, *, src_obj: Path | None = ...) -> None: ...
    @classmethod
    def copy_original_invoice(cls, src_file_path: Path, dst_file_path: Path) -> None: ...

class ExcelInvoiceFile:
    invoice_path: Incomplete
    def __init__(self, invoice_path: Path) -> None: ...
    def read(self, *, target_path: Path | None = ...) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: ...
    def overwrite(self, invoice_org: Path, dist_path: Path, invoice_schema_path: Path, idx: int) -> None: ...
    @staticmethod
    def check_intermittent_empty_rows(df: pd.DataFrame) -> None: ...

def backup_invoice_json_files(excel_invoice_file: Path | None, mode: str | None) -> Path: ...
def update_description_with_features(rde_resource: RdeOutputResourcePath, dst_invoice_json: Path, metadata_def_json: Path) -> None: ...

class RuleBasedReplacer:
    rules: Incomplete
    last_apply_result: Incomplete
    def __init__(self, *, rule_file_path: str | Path | None = ...) -> None: ...
    def load_rules(self, filepath: str | Path) -> None: ...
    def get_apply_rules_obj(self, replacements: dict[str, Any], source_json_obj: dict[str, Any] | None, *, mapping_rules: dict[str, str] | None = ...) -> dict[str, Any]: ...
    def set_rule(self, path: str, variable: str) -> None: ...
    def write_rule(self, replacements_rule: dict[str, Any], save_file_path: str | Path) -> str: ...

def apply_default_filename_mapping_rule(replacement_rule: dict[str, Any], save_file_path: str | Path) -> dict[str, Any]: ...
def apply_magic_variable(invoice_path: str | Path, rawfile_path: str | Path, *, save_filepath: str | Path | None = ...) -> dict[str, Any]: ...
