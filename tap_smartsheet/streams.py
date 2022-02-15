"""Stream type classes for tap-smartsheet."""

from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers
from singer_sdk.plugin_base import PluginBase as TapBaseClass
from singer.schema import Schema
from singer_sdk.typing import JSONTypeHelper

from re import sub

from tap_smartsheet.client import SmartsheetStream


def snake_case(s):
    """Converts a string to snake case.
    https://www.w3resource.com/python-exercises/string/python-data-type-string-exercise-97.php
    """
    return "_".join(
        sub(
            "([A-Z][a-z]+)", r" \1", sub("([A-Z]+)", r" \1", s.replace("-", " "))
        ).split()
    ).lower()


class SheetStream(SmartsheetStream):
    """Define custom stream."""

    def __init__(
        self,
        tap: TapBaseClass,
        sheet: Dict,
        name: Optional[str] = None,
        schema: Optional[Union[Dict[str, Any], Schema]] = None,
        path: Optional[str] = None,
    ) -> None:
        self.sheet_id = sheet["id"]
        name = "sheet_" + snake_case(sheet["name"])

        columns = tap.smartsheet_client.Sheets.get_columns(
            self.sheet_id, include_all=True
        ).to_dict()["data"]
        schema = th.PropertiesList()
        self.column_id_name_mapping = {}
        for column in columns:
            self.column_id_name_mapping[column["id"]] = column["title"]
            schema.append(
                th.Property(column["title"], self.column_type_mapping(column["type"]))
            )

        super().__init__(tap, schema.to_dict(), name)

    def column_type_mapping(self, s) -> JSONTypeHelper:
        """Maps for Smartsheet data types to SDK data types.

        https://smartsheet-platform.github.io/api-docs/#column-types"""
        return {
            "DATE": th.DateType,
            "DATETIME": th.DateTimeType,
            "ABSTRACT_DATETIME": th.DateTimeType,
        }.get(s, th.StringType)

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        """Retrieve sheets from the API and yield a record for each row."""
        sheet_rows = (
            self._tap.smartsheet_client.Sheets.get_sheet(self.sheet_id)
            .to_dict()
            .get("rows", [])
        )
        for row in sheet_rows:
            cells = row["cells"]
            yield {
                self.column_id_name_mapping[cell["columnId"]]: str(cell.get("value"))
                for cell in cells
            }
