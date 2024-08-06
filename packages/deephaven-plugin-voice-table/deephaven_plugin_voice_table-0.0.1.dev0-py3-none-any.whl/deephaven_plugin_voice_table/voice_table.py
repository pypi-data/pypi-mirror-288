from deephaven import ui
from deephaven.table import SortDirection, Table
from deephaven.column import Column
from deephaven_plugin_microphone import DeephavenPluginMicrophoneObject
import logging
import tempfile
import whisper

from .command_decoder import CommandDecoderResults, get_fuzzy_table_operations

logger = logging.getLogger(__name__)

print('logger name', logger.name)

model = whisper.load_model("base")


def _get_operations_display_str(operations: CommandDecoderResults) -> str:
    return " and ".join(
        list(
            map(
                lambda item: f"Filter {item[0]} on {item[1]}",
                operations["filters"].items(),
            )
        ) +
        list(
            map(
                lambda item: f"Sort {item[0]} {'descending' if item[1] == SortDirection.DESCENDING else ''}",
                operations["sorts"].items(),
            )
        )
    )


def _find_column(table: Table, name: str) -> Column:
    for c in table.columns:
        if c.name == name:
            return c
    raise IndexError(f"Column {name} not found")


def _is_numeric_column(column: Column):
    return str(column.data_type) in ["int", "long", "double"]


@ui.component
def ui_voice_table(table: Table):
    command, set_command = ui.use_state("")
    operations = ui.use_memo(
        lambda: get_fuzzy_table_operations(table, command), [command, table]
    )

    def compute_result_table():
        result_table = table
        for key, value in operations["filters"].items():
            col = _find_column(result_table, key)
            if _is_numeric_column(col):
                result_table = result_table.where(f"{key}={value}")
            else:
                result_table = result_table.where(f"{key}=`{value}`")
        
        for key, value in operations["sorts"].items():
            result_table = result_table.sort(key, value)

        return result_table

    result_table = ui.use_memo(compute_result_table, [operations, table])

    def handle_audio(data: bytes):
        try:
            with tempfile.NamedTemporaryFile(
                suffix=".wav", delete=False, mode="bx"
            ) as f:
                f.write(data)

                result = model.transcribe(f.name, fp16=False)

                logger.debug(f"Transcription result: {result}")

                set_command(result["text"])

        except Exception as e:
            logger.error(f"Error processing audio: {e}")

    return ui.flex(
        ui.flex(
            DeephavenPluginMicrophoneObject(on_audio=handle_audio),
            ui.text(_get_operations_display_str(operations)),
            align_items="center",
        ),
        result_table,
        direction="column",
        width="100%",
    )
