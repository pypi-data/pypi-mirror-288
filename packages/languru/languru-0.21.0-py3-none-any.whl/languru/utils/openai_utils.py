import hashlib
import json
from typing import Any, Dict, List, Literal, Sequence, Text, Union

from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat.chat_completion import ChatCompletion
from pyassorted.string.rand import rand_str

from languru.types.chat.completions import Message


def rand_openai_id(
    type: Literal[
        "chat_completion",
        "chatcmpl",
        "assistant",
        "asst",
        "thread",
        "message",
        "msg",
        "run",
    ]
) -> Text:
    if type in ("chat_completion", "chatcmpl"):
        return rand_chat_completion_id()
    elif type in ("assistant", "asst"):
        return rand_assistant_id()
    elif type == "thread":
        return rand_thread_id()
    elif type in ("message", "msg"):
        return rand_message_id()
    elif type == "run":
        return rand_run_id()
    else:
        raise ValueError(f"Invalid type: {type}")


def rand_chat_completion_id() -> Text:
    return f"chatcmpl-{rand_str(29)}"


def rand_assistant_id() -> Text:
    return f"asst_{rand_str(24)}"


def rand_thread_id() -> Text:
    return f"thread_{rand_str(24)}"


def rand_message_id() -> Text:
    return f"msg_{rand_str(24)}"


def rand_run_id() -> Text:
    return f"run_{rand_str(24)}"


def ensure_chat_completion_message_params(
    messages: (
        Sequence[ChatCompletionMessageParam]
        | Sequence[Dict[Text, Any]]
        | ChatCompletionMessageParam
        | Dict[Text, Any]
    )
) -> List[ChatCompletionMessageParam]:
    """Ensure the messages parameter is a list of ChatCompletionMessageParam objects."""

    if not messages:
        raise ValueError("The messages parameter is required.")

    return list([messages] if isinstance(messages, Dict) else messages)  # type: ignore


def ensure_openai_chat_completion_message_params(
    messages: Union[
        Sequence["Message"],
        Sequence[Dict[Text, Any]],
        Sequence[ChatCompletionMessageParam],
    ]
) -> List[ChatCompletionMessageParam]:
    """Ensure that the chat completion messages are in the correct format."""

    _messages: List[ChatCompletionMessageParam] = []
    for m in messages:
        if isinstance(m, Message):
            m_dict = m.model_dump()
            if m_dict.get("role") not in ["user", "assistant", "system"]:
                raise ValueError(f"Invalid role: {m_dict.get('role')}")
            _messages.append(m_dict)  # type: ignore
        elif isinstance(m, Dict):
            if m.get("role") not in ["user", "assistant", "system"]:
                raise ValueError(f"Invalid role: {m.get('role')}")
            _messages.append(m)  # type: ignore
        elif isinstance(m, ChatCompletionMessageParam.__args__):
            _messages.append(m)
        else:
            raise ValueError(f"Invalid message type: {m}")
    return _messages


def ensure_openai_chat_completion_content(chat_completion: "ChatCompletion") -> Text:
    """Ensure that the chat completion response content is returned."""

    chat_answer = chat_completion.choices[0].message.content
    if chat_answer is None:
        raise ValueError("Failed to get a response content from the OpenAI API.")
    return chat_answer


def messages_to_md5(messages: List[ChatCompletionMessageParam]) -> Text:
    """Convert messages to an MD5 hash."""

    return hashlib.md5(
        json.dumps(messages, sort_keys=True, default=str).encode()
    ).hexdigest()
