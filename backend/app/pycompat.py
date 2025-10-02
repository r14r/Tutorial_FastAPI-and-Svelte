"""Compatibility helpers for runtime edge cases."""
from __future__ import annotations

import sys
from typing import ForwardRef


if sys.version_info >= (3, 13):  # pragma: no cover - runtime safeguard
    # Python 3.13 made ``typing.ForwardRef._evaluate`` require the ``recursive_guard``
    # keyword argument. Pydantic v1 still calls it positionally which raises
    # ``TypeError`` during FastAPI's import phase. Patching the method keeps the
    # older call signature while delegating to the updated implementation.
    _original_evaluate = ForwardRef._evaluate

    def _patched_evaluate(self, globalns, localns, *args, **kwargs):
        if args:
            recursive_guard = args[0]
            args = args[1:]
        else:
            recursive_guard = kwargs.get("recursive_guard")

        if recursive_guard is None:
            recursive_guard = set()

        kwargs["recursive_guard"] = recursive_guard
        return _original_evaluate(
            self,
            globalns,
            localns,
            *args,
            **kwargs,
        )

    ForwardRef._evaluate = _patched_evaluate  # type: ignore[attr-defined]
