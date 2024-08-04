import os
from openai_wrapper import openai


os.environ["OPENAI_API_KEY"] = "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"

openai.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Knock knock."},
        {"role": "assistant", "content": "Who's there?"},
        {"role": "user", "content": "Orange."},
    ],
    model="gpt-3.5-turbo",
)
