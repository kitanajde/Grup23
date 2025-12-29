# validation.py
import re

ARG_ALLOWED = re.compile(r'^[a-zA-Z0-9\s\-\_\.\,]{0,200}$')


def sanitize_arg(arg: str | None) -> str | None:
    if arg is None:
        return None
    if ARG_ALLOWED.match(arg):
        return arg
    raise ValueError("Argument contains disallowed characters")
