"""Timeplus target class."""

from __future__ import annotations

from singer_sdk.target_base import Target
from singer_sdk import typing as th

from target_timeplus.sinks import (
    TimeplusSink,
)


class TargetTimeplus(Target):
    """Sample target for Timeplus."""

    name = "target-timeplus"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "endpoint",
            th.StringType,
            description="Timeplus workspace endpoint",
            default="https://us.timeplus.cloud/wsId1234",
            required=True
        ),
        th.Property(
            "apikey",
            th.StringType,
            secret=True,  # Flag config as protected.
            description="Personal API key",
            required=True
        ),
    ).to_dict()

    default_sink_class = TimeplusSink


if __name__ == "__main__":
    TargetTimeplus.cli()
