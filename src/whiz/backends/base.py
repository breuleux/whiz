from dataclasses import dataclass

from gifnoc import define
from serieux import serieux

backends = {}
model_registry = {}


@dataclass(kw_only=True)
class LLMBackend:
    model: str

    @property
    def serieux(self):
        return serieux

    def schema(self, data_model):
        return self.serieux.schema(data_model).compile(ref_policy="never")

    def deserialize(self, data_model, data):
        return self.serieux.deserialize(data_model, data)


@dataclass(kw_only=True)
class TokenBackend(LLMBackend):
    token: str


def define_llm_backend[T](
    name, data_model: type[T], *, defaults: dict = None, models: list[str] = []
) -> T:
    rval = define(field=name, model=data_model, defaults=defaults, lazy=True)
    backends[name] = rval
    for m in models:
        model_registry[m] = name
    return rval
