from app.scanner import Token
from typing import Any, Dict


class Environment:
    def __init__(self):
        self.values: Dict[str, Any] = {}

    def define(self, name: str, value: Any) -> None:
        """Define a new variable or update an existing one."""
        self.values[name] = value

    def get(self, name: Token) -> Any:
        """Get the value of a variable."""
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        raise RuntimeError(f"Undefined variable '{name.lexeme}'.")

    def assign(self, name: Token, value: Any) -> None:
        """Assign a new value to an existing variable."""
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
        else:
            raise RuntimeError(f"Undefined variable '{name.lexeme}'.")
