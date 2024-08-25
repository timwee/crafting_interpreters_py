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
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    BANG = auto()
    BANG_EQUAL = auto()
    EOF = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    SLASH = auto()
    SLASH_SLASH = auto()
    SPACE = auto()
    TAB = auto()
    NEWLINE = auto()
    
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
EQUAL = partial(Token, type=TokenType.EQUAL, lexeme="=", value=None)
EQUAL_EQUAL = partial(Token, type=TokenType.EQUAL_EQUAL, lexeme="==", value=None)
BANG = partial(Token, type=TokenType.BANG, lexeme="!", value=None)
BANG_EQUAL = partial(Token, type=TokenType.BANG_EQUAL, lexeme="!=", value=None)
LESS = partial(Token, type=TokenType.LESS, lexeme="<", value=None)
LESS_EQUAL = partial(Token, type=TokenType.LESS_EQUAL, lexeme="<=", value=None)
GREATER = partial(Token, type=TokenType.GREATER, lexeme=">", value=None)
GREATER_EQUAL = partial(Token, type=TokenType.GREATER_EQUAL, lexeme=">=", value=None)
SLASH = partial(Token, type=TokenType.SLASH, lexeme="/", value=None)
SLASH_SLASH = partial(Token, type=TokenType.SLASH_SLASH, lexeme="//", value=None)
SPACE = partial(Token, type=TokenType.SPACE, lexeme=" ", value=None)
TAB = partial(Token, type=TokenType.TAB, lexeme="\t", value=None)
NEWLINE = partial(Token, type=TokenType.NEWLINE, lexeme="\n", value=None)

def next_token(cur_line: str, cur_idx: int, line_idx: int) -> Token:
    char = cur_line[cur_idx]
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
    elif char == "=":
        if cur_idx + 1 < len(cur_line) and cur_line[cur_idx + 1] == "=":
            return EQUAL_EQUAL(line=line_idx)
        else:
            return EQUAL(line=line_idx)
    elif char == "!":
        if cur_idx + 1 < len(cur_line) and cur_line[cur_idx + 1] == "=":
            return BANG_EQUAL(line=line_idx)
        else:
            return BANG(line=line_idx)
    elif char == "<":
        if cur_idx + 1 < len(cur_line) and cur_line[cur_idx + 1] == "=":
            return LESS_EQUAL(line=line_idx)
        else:
            return LESS(line=line_idx)
    elif char == ">":
        if cur_idx + 1 < len(cur_line) and cur_line[cur_idx + 1] == "=":
            return GREATER_EQUAL(line=line_idx)
        else:
            return GREATER(line=line_idx)
    elif char == "/":
        if cur_idx + 1 < len(cur_line) and cur_line[cur_idx + 1] == "/":
            return SLASH_SLASH(line=line_idx)
        else:
            return SLASH(line=line_idx)
    elif char == " ":
        return SPACE(line=line_idx)
    elif char == "\t":
        return TAB(line=line_idx)
    elif char == "\n":
        return NEWLINE(line=line_idx)
    else:
        # print(f"Unexpected character: {char}", file=sys.stderr)
        raise Exception(f"Unexpected character: {char}")

def tokenize(file_contents: str) -> (list[Token], bool):
    lines = file_contents.split("\n")
    has_error = False
    tokens = []
    for line_idx, line_str in enumerate(lines):
        char_idx = 0
        while char_idx < len(line_str):
            try:
                tok = next_token(line_str, char_idx, line_idx)
                if tok.type == TokenType.SLASH_SLASH:
                    char_idx = len(line_str) # skip the rest of the line
                    continue
                else:
                    if tok.type not in [TokenType.SPACE, TokenType.TAB, TokenType.NEWLINE]:
                        tokens.append(tok)
                    char_idx += len(tok)
            except Exception as e:
                #print(e, file=sys.stderr)
                print(f"[line {line_idx + 1}] Error: Unexpected character: {line_str[char_idx]}", file=sys.stderr)
                has_error = True
                char_idx += 1
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
