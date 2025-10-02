"""Compatibility helpers for runtime edge cases."""
from __future__ import annotations

import sys
import types
from typing import ForwardRef


try:  # pragma: no cover - defensive import
    import bcrypt  # type: ignore[import-not-found]
except Exception:  # pragma: no cover - bcrypt might not be installed yet
    bcrypt = None  # type: ignore[assignment]


if bcrypt is not None and not hasattr(bcrypt, "__about__"):
    # Passlib 1.7 relies on the ``bcrypt`` package exposing a ``__about__``
    # module with a ``__version__`` attribute. Bcrypt 4 removed that module,
    # keeping only a top-level ``__version__`` string which triggers an
    # ``AttributeError`` during Passlib's import phase. Recreate the missing
    # module so Passlib can read the version it expects. ``types.SimpleNamespace``
    # mirrors the previous module object closely enough for Passlib's needs.
    about = types.SimpleNamespace(__version__=getattr(bcrypt, "__version__", ""))
    bcrypt.__about__ = about  # type: ignore[attr-defined]


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

    # SQLAlchemy 2.0.41 tightened its ``TypingOnly`` guard in a way that became
    # incompatible with Python 3.13's updated ``typing`` module. The ORM defines
    # a few helper classes that intentionally inherit from ``TypingOnly`` while
    # also providing extra attributes which now triggers an ``AssertionError``
    # during import. The upstream project relaxed this guard in later releases,
    # but pinning a patched version is not always possible for workshop
    # attendees. To keep the tutorial code runnable we soften the guard locally
    # by ignoring that specific assertion while letting other errors bubble up.
    try:  # pragma: no cover - defensive import
        from sqlalchemy.util import langhelpers
    except Exception:  # pragma: no cover - SQLAlchemy might not be installed yet
        langhelpers = None  # type: ignore[assignment]

    if langhelpers is not None:  # pragma: no branch - simple runtime patch
        _orig_init_subclass = langhelpers.TypingOnly.__init_subclass__

        def _patched_init_subclass(cls, *args, **kwargs):
            try:
                _orig_init_subclass(cls, *args, **kwargs)
            except AssertionError as exc:
                if "directly inherits TypingOnly" not in str(exc):
                    raise

        langhelpers.TypingOnly.__init_subclass__ = _patched_init_subclass  # type: ignore[assignment]
