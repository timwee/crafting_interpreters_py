from app.scanner import Token
from typing import Any, Dict
import sys


class Environment:

    def __init__(self, enclosing=None):
        self.values: Dict[str, Any] = {}
        self.enclosing = enclosing

    def define(self, name: str, value: Any) -> None:
        """Define a new variable or update an existing one."""
        self.values[name] = value

    def get(self, name: Token) -> Any:
        """Get the value of a variable."""
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        elif self.enclosing:
            return self.enclosing.get(name)
        else:
            msg = f"Undefined variable '{name.lexeme}'."
            print(msg, file=sys.stderr)
            print(f"[line {name.line}]", file=sys.stderr)
            raise RuntimeError(msg)

    def assign(self, name: Token, value: Any) -> None:
        """Assign a new value to an existing variable."""
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
        elif self.enclosing:
            self.enclosing.assign(name, value)
        else:
            msg = f"Undefined variable '{name.lexeme}'."
            print(msg, file=sys.stderr)
            print(f"[line {name.line}]", file=sys.stderr)
            raise RuntimeError(msg)
