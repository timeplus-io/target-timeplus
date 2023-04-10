"""Timeplus target sink class, which handles writing streams."""

from __future__ import annotations

from singer_sdk import PluginBase
from singer_sdk.sinks import BatchSink

from timeplus import Stream, Environment


class TimeplusSink(BatchSink):
    """Timeplus target sink class."""

    def __init__(  # noqa: D107
        self,
        target: PluginBase,
        stream_name: str,
        schema: Dict,
        key_properties: Optional[List[str]],
    ) -> None:

        self.columns = []

        super().__init__(target, stream_name, schema, key_properties)

        # self.logger.info(f"__init__ stream:{stream_name}, schema {schema}")

        endpoint = self.config["endpoint"]
        apikey = self.config["apikey"]
        if endpoint[-1] == '/':
            endpoint = endpoint[0:len(endpoint) - 1]
        env = Environment().address(endpoint).apikey(apikey)
        self.env = env

        stream_list = Stream(env=env).list()
        all_streams = {s.name for s in stream_list}
        stream_exists = stream_name in all_streams
        self.logger.info(f"__init__ stream_exists:{stream_exists}")
        if not stream_exists:
            TimeplusSink.create_stream(env, stream_name, schema)

        # track the column names for batch data ingestion
        for name, v in schema['properties'].items():
            self.columns.append(name.strip())

    @staticmethod
    def create_stream(env, stream_name: str, schema: Dict):
        # singlel-column stream
        # Stream(env=env).name(stream.name).column('raw','string').create()

        tp_stream = Stream(env=env).name(stream_name.strip())
        for name, v in schema['properties'].items():
            tp_stream.column(name.strip(), TimeplusSink.type_mapping(v))

        tp_stream.create()

    @staticmethod
    def type_mapping(v) -> str:
        airbyte_type = v['type']
        if type(airbyte_type) is list:
            for t in list(airbyte_type):
                if t != 'null':
                    type_def = {'type': t}
                    if t == 'array':
                        type_def['items'] = v['items']
                    return TimeplusSink.type_mapping(type_def)
        if airbyte_type == 'number':
            return 'float'
        elif airbyte_type == 'integer':
            return 'integer'
        elif airbyte_type == 'boolean':
            return 'bool'
        elif airbyte_type == 'object':
            return 'string'
        elif airbyte_type == 'array':
            return f"array({TimeplusSink.type_mapping(v['items'])})"
        else:
            return 'string'

    def start_batch(self, context: dict) -> None:
        """Start a batch.

        Developers may optionally add additional markers to the `context` dict,
        which is unique to this batch.

        Args:
            context: Stream partition or context dictionary.
        """
        # self.logger.info(f"stream:{self.stream_name}, start_batch {context}")
        self.rows = []

    def process_record(self, record: dict, context: dict) -> None:
        # self.logger.info(f"process_record stream:{self.stream_name}, record: {record}, and context: {context}")
        """Process the record.

        Developers may optionally read or write additional markers within the
        passed `context` dict from the current batch.

        Args:
            record: Individual record in the stream.
            context: Stream partition or context dictionary.
        """
        row = []
        for name, v in record.items():
            row.append(v)
        self.rows.append(row)

    def process_batch(self, context: dict) -> None:
        """Write out any prepped records and return once fully written.

        Args:
            context: Stream partition or context dictionary.
        """
        # self.logger.info(f"process_batch stream:{self.stream_name},  {context}")

        Stream(env=self.env).name(self.stream_name.strip()
                                  ).ingest(self.columns, self.rows)
