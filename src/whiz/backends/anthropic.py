from functools import cached_property

import httpx

from .base import TokenBackend, define_llm_backend


class Anthropic(TokenBackend):
    @cached_property
    def headers(self):
        return {
            "x-api-key": self.token,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }

    def __call__(self, data_model, prompt):
        payload = {
            "model": self.model,
            "max_tokens": 4096,
            "tools": [
                {
                    "name": "record_analysis",
                    "description": "Record an analysis in well-structured JSON.",
                    "input_schema": self.schema(data_model),
                }
            ],
            "tool_choice": {"type": "tool", "name": "record_analysis"},
            "messages": [{"role": "user", "content": prompt}],
        }
        response = httpx.post(
            "https://api.anthropic.com/v1/messages",
            headers=self.headers,
            json=payload,
            timeout=30,
        )
        result = response.json()
        answer = result["content"][0]
        assert answer["type"] == "tool_use"
        assert answer["name"] == "record_analysis"
        result_dict = answer["input"]
        return self.deserialize(data_model, result_dict)


anthropic_config = define_llm_backend(
    "anthropic",
    Anthropic,
    defaults={"token": "${env:ANTHROPIC_API_KEY}"},
    models=[
        "claude-3-7-sonnet-latest",
    ],
)
