import sys

from enum import Enum, auto
from typing import Any
from functools import partial
import sys

class TokenType(Enum):
    LEFT_PAREN = auto()
    LEFT_BRACE = auto()
    DOT = auto()
    COMMA = auto()
    PLUS = auto()
    STAR = auto()
    MINUS = auto()
    SEMICOLON = auto()
    RIGHT_BRACE = auto()
    RIGHT_PAREN = auto()
    EOF = auto()
    
    def __str__(self):
        return self.name

class Token:
    def __init__(self, type: TokenType, lexeme: str, value: Any, line: int):
        self.type = type
        self.lexeme = lexeme
        self.value = value
        self.line = line

    def __str__(self):
        value_str = str(self.value) if self.value is not None else "null"
        if self.type == TokenType.EOF:
            return f"{self.type} {self.lexeme} {value_str}"
        return f"{self.type} {self.lexeme} {value_str}"
    
    def __repr__(self):
        return self.__str__()
    
    def __len__(self):
        return len(self.lexeme)
    
EOF = partial(Token, type=TokenType.EOF, lexeme="", value=None)
LPAREN = partial(Token, type=TokenType.LEFT_PAREN, lexeme="(", value=None)
RPAREN = partial(Token, type=TokenType.RIGHT_PAREN, lexeme=")", value=None)
LBRACE = partial(Token, type=TokenType.LEFT_BRACE, lexeme="{", value=None)
RBRACE = partial(Token, type=TokenType.RIGHT_BRACE, lexeme="}", value=None)
DOT = partial(Token, type=TokenType.DOT, lexeme=".", value=None)
COMMA = partial(Token, type=TokenType.COMMA, lexeme=",", value=None)
PLUS = partial(Token, type=TokenType.PLUS, lexeme="+", value=None)
STAR = partial(Token, type=TokenType.STAR, lexeme="*", value=None)
MINUS = partial(Token, type=TokenType.MINUS, lexeme="-", value=None)
SEMICOLON = partial(Token, type=TokenType.SEMICOLON, lexeme=";", value=None)

def next_token(char: str, line_idx: int) -> Token:
    
    if char == "(":
        return LPAREN(line=line_idx)
    elif char == ")":
        return RPAREN(line=line_idx)
    elif char == "{":
        return LBRACE(line=line_idx)
    elif char == "}":
        return RBRACE(line=line_idx)
    elif char == ".":
        return DOT(line=line_idx)
    elif char == ",":
        return COMMA(line=line_idx)
    elif char == "+":
        return PLUS(line=line_idx)
    elif char == "-":
        return MINUS(line=line_idx)
    elif char == "*":
        return STAR(line=line_idx)
    elif char == ";":
        return SEMICOLON(line=line_idx)
    else:
        print(f"Unexpected character: {char}", file=sys.stderr)
        raise Exception(f"Unexpected character: {char}")

def tokenize(file_contents: str) -> (list[Token], bool):
    lines = file_contents.split("\n")
    has_error = False
    tokens = []
    for line_idx, line_str in enumerate(lines):
        for cur_idx, chr in enumerate(line_str):
            try:
                tokens.append(next_token(chr, line_idx))
            except Exception as e:
                print(e, file=sys.stderr)
                print(f"[line {line_idx + 1}] Error: Unexpected character: {chr}", file=sys.stderr)
                has_error = True
    tokens.append(EOF(line=line_idx))
    return tokens, has_error

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
        tokens, has_error = tokenize(file_contents)
        for token in tokens:
            print(token)
        if has_error:
            exit(65)
    else:
        print("EOF  null") # Placeholder, remove this line when implementing the scanner


if __name__ == "__main__":
    main()
