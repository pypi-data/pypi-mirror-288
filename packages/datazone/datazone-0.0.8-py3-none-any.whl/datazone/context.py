from typing import Optional

from contextvars import ContextVar

inspect_mode = ContextVar("inspect_mode", default=False)
profile_context: ContextVar[Optional[str]] = ContextVar("profile_context", default=None)
