import json
import string
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Generator,
    Iterable,
    List,
    NamedTuple,
    Optional,
    Sequence,
    Text,
    Tuple,
    TypeVar,
    Union,
    cast,
    overload,
)

from openai.types.beta.threads.message import Message as ThreadsMessage
from pydantic import BaseModel
from rich import box
from rich import print as rich_print
from rich.style import StyleType
from rich.table import Table
from rich.text import Text as RichText

from languru.config import console, logger
from languru.types.chat.completions import Message

if TYPE_CHECKING:
    from openai.types.chat import ChatCompletionMessageParam

T = TypeVar("T")


def should_str_or_none(value: Text | Any) -> Optional[Text]:
    if isinstance(value, Text):
        return value
    elif value is None:
        return None
    logger.warning(f"Value {value} is not a string, returning None")
    return None


def should_str(value: Text | Any) -> Text:
    if should_str_or_none(value) is None:
        raise ValueError(f"Value {value} is not a string")
    return value


def must_list_or_none(
    value: List[T] | Any, return_none_if_empty: bool = False
) -> Optional[List[T]]:
    if isinstance(value, List):
        if return_none_if_empty and len(value) == 0:
            return None
        return value
    elif isinstance(value, Tuple):
        if return_none_if_empty and len(value) == 0:
            return None
        return list(value)
    elif value is None:
        return None
    else:
        return [value]


def must_list(value: List[T] | Any) -> List[T]:
    to_items = must_list_or_none(value)
    if to_items is None:
        raise ValueError(f"Could not convert {value} to a list")
    return to_items


def debug_print(
    *values: Any,
    title: Text = "Debug Print",
    box: box.Box | None = box.HEAVY_HEAD,
    colors: List[StyleType] = [
        "bright_blue",
        "bright_cyan",
        "bright_green",
        "bright_magenta",
    ],
) -> None:
    if not values:
        return
    tb = Table(title=RichText(title), box=box, show_header=False)
    for idx, value in enumerate(values):
        style = colors[idx % len(colors)]
        if isinstance(value, BaseModel):
            tb.add_row(value.model_dump_json(indent=2), style=style)
        elif isinstance(value, dict):
            tb.add_row(json.dumps(value, indent=2, ensure_ascii=False), style=style)
        else:
            tb.add_row(str(value), style=style)
    rich_print(tb)


def replace_right(source_str: Text, old: Text, new: Text, occurrence: int = -1) -> Text:
    return source_str[::-1].replace(old[::-1], new[::-1], occurrence)[::-1]


def str_strong_casefold(text: Text) -> Text:
    return text.strip().replace("-_. ", "").casefold()


def remove_punctuation(input_string: Text, extra_punctuation: Text = "") -> Text:
    """Remove punctuations from the input string."""

    extended_punctuation = (
        string.punctuation + "，？！（）【】《》“”‘’；：" + extra_punctuation
    )
    translator = str.maketrans("", "", extended_punctuation)
    return input_string.translate(translator)


def ensure_list(value: Any) -> List:
    if isinstance(value, Sequence):
        return list(value)
    if value is None:
        return []
    return [value]


def display_messages(
    messages: Union[
        Sequence["Message"],
        Sequence[Dict[Text, Any]],
        Sequence["ChatCompletionMessageParam"],
        Sequence["ThreadsMessage"],
    ],
    *,
    is_print: bool = True,
    table_title: Text = "Messages",
    table_width: int = 120,
    extra_newline_table_start: bool = True,
    extra_newline_message_end: bool = True,
) -> Text:
    """Display messages in a human-readable format."""

    if not messages:
        raise ValueError("No messages to display.")

    # Convert messages to dictionaries
    _messages = [
        m.model_dump() if isinstance(m, BaseModel) else dict(m) for m in messages
    ]

    # Initialize output
    out = ""
    table: Optional["Table"] = None
    if is_print:
        table = Table(title=table_title, width=table_width)
        table.add_column("Role", justify="right", style="bold cyan")
        table.add_column("Content", justify="left")

    # Read messages
    for m in _messages:
        role = str(m.get("role") or "Unknown").capitalize()
        content = m.get("content") or "n/a"
        if isinstance(content, List):  # OpenAI Threads messages
            _content = ""
            for content_block in content:
                content_block = cast(Dict, content_block)
                if content_block.get("type") == "image_file":
                    _image_file = content_block.get("image_file") or {}
                    _image_id = _image_file.get("file_id") or "n/a"
                    _content += f"<image_file file_id={_image_id}/>"
                elif content_block.get("type") == "image_url":
                    _image_url = content_block.get("image_url") or {}
                    _url = _image_url.get("url") or "n/a"
                    _content += f"<image_url url={_url}/>"
                elif content_block.get("type") == "text":
                    _content_text = content_block.get("text") or {}
                    _content_text_value = _content_text.get("value") or "n/a"
                    _content += str(_content_text_value)
                else:
                    _content += str(content_block)
            content = _content
        else:
            content = str(content)

        content = content.strip()
        if extra_newline_message_end:
            content += "\n"
        if is_print:
            table = cast(Table, table)
            table.add_row(role.rjust(9), content)
        out += f"\n\n{role.capitalize()}:\n{content}"
        out = out.strip()

    if is_print:
        if extra_newline_table_start:
            console.print("\n")
        console.print(table)
    return out


def named_tuples_to_dicts(named_tuples: Sequence[NamedTuple]) -> List[Dict]:
    """Convert named tuples to dictionaries."""

    return [nt._asdict() for nt in named_tuples]


def json_dumps(data: Any, indent: Optional[Union[int, Text]] = None) -> Text:
    return json.dumps(data, indent=indent, ensure_ascii=False)


def dummy_generator_func(
    generator: Union[
        Generator[T, None, None],
        Iterable[T],
    ],
) -> Callable[[], Generator[T, None, None]]:
    """Create a dummy generator function."""

    def dummy_generator() -> Generator[T, None, None]:
        for item in generator:
            yield item

    return dummy_generator


def display_object(obj: object) -> Text:
    """Display an object in a human-readable format."""

    return f"{obj.__class__.__module__}.{obj.__class__.__name__}"


@overload
def model_dump(obj: Sequence) -> List[Dict]: ...


@overload
def model_dump(obj: None) -> None: ...


@overload
def model_dump(obj: Any) -> Dict: ...


def model_dump(obj: Any) -> Optional[Union[Dict, List[Dict]]]:
    """Dump the model in a dictionary format."""

    if obj is None:
        return None
    elif isinstance(obj, BaseModel):
        return obj.model_dump()
    elif isinstance(obj, Sequence) and not isinstance(obj, Text):
        return [model_dump(item) for item in obj]
    return json.loads(json.dumps(obj, default=str))
