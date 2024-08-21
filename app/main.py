import sys

from enum import Enum, auto
from typing import Any

class TokenType(Enum):
    EOF = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()

    def __str__(self):
        return self.name

class Token:
    def __init__(self, type: TokenType, lexeme: str, value: Any):
        self.type = type
        self.lexeme = lexeme
        self.value = value

    def __str__(self):
        value_str = str(self.value) if self.value is not None else "null"
        return f"{self.type} {self.lexeme} {value_str}"
    
    def __repr__(self):
        return self.__str__()
    
    def __len__(self):
        return len(self.lexeme)
    
EOF = Token(TokenType.EOF, "", None)
LPAREN = Token(TokenType.LEFT_PAREN, "(", value=None)
RPAREN = Token(TokenType.RIGHT_PAREN, ")", value=None)

def next_token(file_contents: str, cur_idx: int) -> Token:
    if cur_idx >= len(file_contents):
        return EOF
    
    char = file_contents[cur_idx]

    if char == "(":
        return LPAREN
    elif char == ")":
        return RPAREN
    else:
        return EOF

def tokenize(file_contents):
    cur_idx = 0
    eof_idx = len(file_contents)
    
    tokens = []
    while cur_idx < eof_idx:
        tok = next_token(file_contents, cur_idx)
        tokens.append(tok)
        cur_idx += len(tok)
    tokens.append(EOF)
    return tokens

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    # Uncomment this block to pass the first stage
    if file_contents:
        tokens = tokenize(file_contents)
        for token in tokens:
            print(token)
    else:
        print("EOF  null") # Placeholder, remove this line when implementing the scanner


if __name__ == "__main__":
    main()
