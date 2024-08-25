import sys

from enum import Enum, auto
from typing import Any
from functools import partial

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
    STRING = auto()
    NUMBER = auto()
    IDENTIFIER = auto()
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()
    
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
AND = partial(Token, type=TokenType.AND, lexeme="and", value=None)
CLASS = partial(Token, type=TokenType.CLASS, lexeme="class", value=None)
ELSE = partial(Token, type=TokenType.ELSE, lexeme="else", value=None)
FALSE = partial(Token, type=TokenType.FALSE, lexeme="false", value=None)    
FUN = partial(Token, type=TokenType.FUN, lexeme="fun", value=None)
FOR = partial(Token, type=TokenType.FOR, lexeme="for", value=None)
IF = partial(Token, type=TokenType.IF, lexeme="if", value=None)
NIL = partial(Token, type=TokenType.NIL, lexeme="nil", value=None)
OR = partial(Token, type=TokenType.OR, lexeme="or", value=None)
PRINT = partial(Token, type=TokenType.PRINT, lexeme="print", value=None)
RETURN = partial(Token, type=TokenType.RETURN, lexeme="return", value=None)
SUPER = partial(Token, type=TokenType.SUPER, lexeme="super", value=None)
THIS = partial(Token, type=TokenType.THIS, lexeme="this", value=None)
TRUE = partial(Token, type=TokenType.TRUE, lexeme="true", value=None)
VAR = partial(Token, type=TokenType.VAR, lexeme="var", value=None)
WHILE = partial(Token, type=TokenType.WHILE, lexeme="while", value=None)

RESERVED_WORDS_MAP = {
    "and": AND,
    "class": CLASS,
    "else": ELSE,
    "false": FALSE,
    "fun": FUN,
    "for": FOR,
    "if": IF,
    "nil": NIL,
    "or": OR,
    "print": PRINT,
    "return": RETURN,
    "super": SUPER,
    "this": THIS,
    "true": TRUE,
    "var": VAR,
    "while": WHILE,
}


RESERVED_WORDS = RESERVED_WORDS_MAP.keys()


class UnterminatedStringError(Exception):
    pass

def parse_string(src_str: str, cur_idx: int, line_idx: int) -> Token:
    str_start_idx = cur_idx
    str_end_idx = cur_idx + 1
    max_idx = len(src_str)
    while str_end_idx < max_idx and src_str[str_end_idx] != '"':
        if src_str[str_end_idx] == "\n":
          raise UnterminatedStringError("Unterminated string. newline encountered in the string")
        str_end_idx += 1
    if str_end_idx >= max_idx:
        raise UnterminatedStringError("Unterminated string.")
    lexeme = src_str[str_start_idx:str_end_idx+1]
    value = src_str[str_start_idx+1:str_end_idx]
    str_token = Token(type=TokenType.STRING, lexeme=lexeme, value=value, line=line_idx)
    return str_token

def parse_number(src_str: str, cur_idx: int, line_idx: int) -> Token:
    num_start_idx = cur_idx
    num_end_idx = cur_idx + 1
    dot_idx = -1
    while num_end_idx < len(src_str) and (src_str[num_end_idx].isdigit() or src_str[num_end_idx] == "."):
        if src_str[num_end_idx] == ".":
            if dot_idx != -1:
                raise Exception("Invalid number. Multiple dots in the number.")
            dot_idx = num_end_idx
        num_end_idx += 1
    if dot_idx == num_end_idx - 1:
        num_end_idx -= 1
    lexeme = src_str[num_start_idx:num_end_idx]
    value = float(lexeme)
    return Token(type=TokenType.NUMBER, lexeme=lexeme, value=value, line=line_idx)

def parse_identifier(src_str: str, cur_idx: int, line_idx: int) -> Token:
    id_start_idx = cur_idx
    id_end_idx = cur_idx + 1
    while id_end_idx < len(src_str) and (src_str[id_end_idx].isalnum() or src_str[id_end_idx] == "_"):
        id_end_idx += 1
    lexeme = src_str[id_start_idx:id_end_idx]
    return Token(type=TokenType.IDENTIFIER, lexeme=lexeme, value=None, line=line_idx)

def matches_reserved_word(src_str: str, cur_idx: int, line_idx: int) -> str:
    for word in RESERVED_WORDS:
        if src_str[cur_idx:cur_idx+len(word)] == word:
            return word
    return ""

def next_token(src_str: str, cur_idx: int, line_idx: int) -> Token:
    char = src_str[cur_idx]
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
        if cur_idx + 1 < len(src_str) and src_str[cur_idx + 1] == "=":
            return EQUAL_EQUAL(line=line_idx)
        else:
            return EQUAL(line=line_idx)
    elif char == "!":
        if cur_idx + 1 < len(src_str) and src_str[cur_idx + 1] == "=":
            return BANG_EQUAL(line=line_idx)
        else:
            return BANG(line=line_idx)
    elif char == "<":
        if cur_idx + 1 < len(src_str) and src_str[cur_idx + 1] == "=":
            return LESS_EQUAL(line=line_idx)
        else:
            return LESS(line=line_idx)
    elif char == ">":
        if cur_idx + 1 < len(src_str) and src_str[cur_idx + 1] == "=":
            return GREATER_EQUAL(line=line_idx)
        else:
            return GREATER(line=line_idx)
    elif char == "/":
        if cur_idx + 1 < len(src_str) and src_str[cur_idx + 1] == "/":
            return SLASH_SLASH(line=line_idx)
        else:
            return SLASH(line=line_idx)
    elif char == " ":
        return SPACE(line=line_idx)
    elif char == "\t":
        return TAB(line=line_idx)
    elif char == "\n":
        return NEWLINE(line=line_idx)
    elif char == '"':
        return parse_string(src_str, cur_idx, line_idx)
    elif char.isdigit():
        return parse_number(src_str, cur_idx, line_idx)
    else:
        if (reserved_word := matches_reserved_word(src_str, cur_idx, line_idx)):
            return RESERVED_WORDS_MAP[reserved_word](line=line_idx) 
        elif char.isalpha() or char == "_":
            return parse_identifier(src_str, cur_idx, line_idx)
        # print(f"Unexpected character: {char}", file=sys.stderr)
        raise Exception(f"Unexpected character: {char}")

def tokenize(file_contents: str) -> (list[Token], bool):
    line_idx = 1
    end_idx = len(file_contents)
    has_error = False
    tokens = []
    char_idx = 0
    while char_idx < end_idx:
        try:
            tok = next_token(file_contents, char_idx, line_idx)
            if tok.type == TokenType.SLASH_SLASH:
                while char_idx < end_idx and file_contents[char_idx] != "\n":
                    char_idx += 1
                continue
            else:
                if tok.type not in [TokenType.SPACE, TokenType.TAB, TokenType.NEWLINE]:
                    tokens.append(tok)
                char_idx += len(tok)
                if tok.type == TokenType.NEWLINE:
                    line_idx += 1
        except UnterminatedStringError as e:
            print(e, file=sys.stderr)
            print(f"[line {line_idx}] Error: Unterminated string.", file=sys.stderr)
            has_error = True
            # get to the next new line
            while char_idx < end_idx and file_contents[char_idx] != "\n":
                char_idx += 1
        except Exception as e:
            print(e, file=sys.stderr)
            print(f"[line {line_idx}] Error: Unexpected character: {file_contents[char_idx]}", file=sys.stderr)
            has_error = True
            char_idx += 1
    tokens.append(EOF(line=line_idx))
    return tokens, has_error