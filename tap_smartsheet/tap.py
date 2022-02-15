"""Smartsheet tap class."""

from typing import List

import smartsheet

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers
from tap_smartsheet.streams import (
    SheetStream,
)


class TapSmartsheet(Tap):
    """Smartsheet tap class."""

    name = "tap-smartsheet"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "smartsheet_access_token",
            th.StringType,
            required=True,
            description="The token to authenticate against the API service",
        ),
    ).to_dict()

    @property
    def smartsheet_client(self):
        return smartsheet.Smartsheet(self.config["smartsheet_access_token"])

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        sheets = self.smartsheet_client.Sheets.list_sheets().to_dict()["data"]
        return [SheetStream(tap=self, sheet=sheet) for sheet in sheets]
