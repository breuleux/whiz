from typing import Type

import gifnoc

from .backends.base import backends, model_registry


def fill[T](
    data_model: Type[T] | str,
    prompt: str | None = None,
    *,
    backend: str | None = None,
    model: str | None = None,
    **backend_args,
) -> T:
    if prompt is None:
        prompt = "Generate to the best of your ability"
    if backend is None:
        assert model is not None
        if "::" in model:
            backend, model = model.split("::", 1)
        else:
            backend = model_registry[model]
    if model is not None:
        backend_args = {**backend_args, "model": model}
    with gifnoc.overlay({backend: backend_args}):
        return backends[backend](data_model, prompt)
