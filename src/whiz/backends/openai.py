import json
from functools import cached_property

import httpx

from .base import TokenBackend, define_llm_backend


class OpenAI(TokenBackend):
    @cached_property
    def headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def __call__(self, data_model, prompt):
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "serieux_schema",
                    "strict": True,
                    "schema": self.schema(data_model),
                },
            },
        }
        response = httpx.post(
            "https://api.openai.com/v1/chat/completions",
            headers=self.headers,
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        result = response.json()
        result_text = result["choices"][0]["message"]["content"]
        return self.deserialize(data_model, json.loads(result_text))


openai_config = define_llm_backend(
    "openai",
    OpenAI,
    defaults={"token": "${env:OPENAI_API_KEY}"},
    models=[
        "gpt-4o",
    ],
)
