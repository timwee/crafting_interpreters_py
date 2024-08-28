import sys

from enum import Enum, auto
from typing import Any
from functools import partial

from app.scanner import tokenize
from app.parser import Parser, Expr
from app.ast_printer import AstPrinter

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command not in ["tokenize", "parse"]:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    # Uncomment this block to pass the first stage
    if file_contents:
        tokens, has_error = tokenize(file_contents)
        if command == "tokenize":
            for token in tokens:
                print(token)
        if command == "parse":
            parser = Parser(tokens[:-1])
            exprs = parser.parse()
            if exprs and len(exprs) > 0:
                printer = AstPrinter()
                # for expr in exprs:
                print(printer.print(exprs[0]))
            else:
                exit(65)
            
        if has_error:
            exit(65)
    else:
        print("EOF  null") # Placeholder, remove this line when implementing the scanner


if __name__ == "__main__":
    main()
