import datetime
import os
import uuid
from dataclasses import dataclass
from typing import Dict, List

from wrapt import wrap_function_wrapper

from zenetics.client import APIClient

try:
    import openai
except ImportError:
    raise ImportError(
        "Please install the OpenAI Python package using `pip install openai`"
    )


@dataclass
class Result:
    content: str
    content_type: str

    def to_dict(self):
        return {
            "content": self.content,
            "content_type": self.content_type,
        }


@dataclass
class Message:
    role: str
    content: str
    version: str

    def to_dict(self):
        return {
            "role": self.role,
            "content": self.content,
            "version": self.version,
        }


@dataclass
class Prompt:
    version: str
    messages: List[Message]

    def to_dict(self):
        return {
            "version": self.version,
            "messages": [message.to_dict() for message in self.messages],
        }


@dataclass
class Completion:
    id: str
    type: str
    created_at: str
    model_params: Dict
    stats: Dict
    prompt: Prompt
    result: Result

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "created_at": self.created_at,
            "model_params": self.model_params,
            "stats": self.stats,
            "prompt": self.prompt.to_dict(),
            "result": self.result.to_dict(),
        }


@dataclass
class Session:
    id: str
    organization_id: str
    application_id: str
    created_at: str
    updated_at: str
    completions: List[Completion]

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "completions": [completion.to_dict() for completion in self.completions],
        }


class Zenetics:
    def __init__(self, api_key: str, app_id: str, api_client: APIClient):
        self.api_key = api_key
        self.app_id = app_id
        self.api_client = api_client

    def capture(self, request, result):

        session_result = None

        if len(result.choices) > 0:
            session_result = Result(
                content=result.choices[0].message.content,
                content_type="text",
            )

        now = datetime.datetime.now().isoformat()

        completion = Completion(
            id=str(uuid.uuid4()),
            type="text",
            created_at=now,
            model_params={},
            stats={},
            prompt=Prompt(
                version="1.0",
                messages=[
                    Message(
                        role=message["role"],
                        content=message["content"],
                        version="1.0",
                    )
                    for message in request["messages"]
                ],
            ),
            result=session_result,
        )

        session = Session(
            id=str(uuid.uuid4()),
            created_at=now,
            updated_at=now,
            completions=[completion],
            organization_id="default",
            application_id="default",
        )

        self.api_client.post(session.to_dict(), self.api_key)


api_key = os.environ.get("ZENETICS_API_KEY")
app_id = os.environ.get("ZENETICS_APP_ID")

if not api_key:
    raise ValueError("ZENETICS_API_KEY environment variable is required")

if not app_id:
    raise ValueError("ZENETICS_APP_ID environment variable is required")


api_client = APIClient("https://zenetics-api-gsdqjk6nma-ew.a.run.app")

zenetics = Zenetics(api_key, app_id, api_client)


def trace_function(wrapped, instance, args, kwargs):
    result = wrapped(*args, **kwargs)
    zenetics.capture(kwargs, result)
    return result


wrap_function_wrapper(
    "openai.resources.chat.completions",
    "Completions.create",
    trace_function,
)
