import sys

from enum import Enum, auto
from typing import Any
from functools import partial

from app.scanner import tokenize
from app.parser import Parser, Expr
from app.ast_printer import AstPrinter
from app.interpreter import Interpreter

def print_value(val: Any):
    if val is None:
        print("nil")
        return
    if isinstance(val, bool):
        if val:
            print("true")
        else:
            print("false")
        return
    elif isinstance(val, (float, int)):
        # print(f'in print_val numeric: {val}')
        str_val = str(val)
        str_val = str_val.removesuffix(".0")
        if "." in str_val:
            str_val.removesuffix("0") 
        print(str_val)
        return
    else:
        print(val)

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command not in ["tokenize", "parse", "evaluate"]:
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
        else:
            parser = Parser(tokens[:-1])
            exprs = parser.parse()
            has_error = (not exprs or len(exprs) <= 0)
            if command == "parse":
                if exprs and len(exprs) > 0:
                    printer = AstPrinter()
                    # for expr in exprs:
                    print(printer.print(exprs[0]))
                else:
                    exit(65)
            elif command == "evaluate":
                interpreter = Interpreter()
                result = interpreter.evaluate(exprs[0])
                print_value(result)
            
        if has_error:
            exit(65)
    else:
        print("EOF  null") # Placeholder, remove this line when implementing the scanner


if __name__ == "__main__":
    main()
