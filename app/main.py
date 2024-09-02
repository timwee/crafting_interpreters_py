import sys

from enum import Enum, auto
from typing import Any
from functools import partial

from app.scanner import tokenize
from app.parser import Parser, ParseError
from app.ast_printer import AstPrinter
from app.interpreter import Interpreter, EvaluationError
from app.utils import stringify


def print_value(val: Any):
    print(stringify(val))


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print(
            "Usage: ./your_program.sh <tokenize|parse|evaluate|run> <filename>",
            file=sys.stderr,
        )
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command not in ["tokenize", "parse", "evaluate", "run"]:
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

            if command == "parse":
                parser = Parser(tokens[:-1])
                exprs = parser.parse_expressions()
                has_error = not exprs or len(exprs) <= 0
                printer = AstPrinter()
                for expr in exprs:
                    print(printer.print(expr), file=sys.stderr)
                    if exprs and len(exprs) > 0:
                        # for expr in exprs:
                        print(printer.print(exprs[0]))
                    else:
                        exit(65)
            elif command == "evaluate":
                parser = Parser(tokens[:-1])
                exprs = parser.parse_expressions()
                has_error = not exprs or len(exprs) <= 0
                if has_error:
                    exit(65)
                interpreter = Interpreter()
                try:
                    result = interpreter.visit(exprs[0])
                    print_value(result)
                except EvaluationError as e:
                    print(e.message, file=sys.stderr)
                    print("[line 1]", file=sys.stderr)
                    exit(70)
            elif command == "run":
                for token in tokens:
                    print(token, file=sys.stderr)
                try:
                    parser = Parser(tokens[:-1])
                    stmts = parser.parse_statements()
                    # for stmt in stmts:
                    #     print(printer.print(stmt), file=sys.stderr)
                except ParseError as e:
                    print(e.message, file=sys.stderr)
                    print("[line 1]", file=sys.stderr)
                    exit(65)

                try:
                    interpreter = Interpreter()
                    result = interpreter.interpret(stmts)
                except EvaluationError as e:
                    print(e.message, file=sys.stderr)
                    print("[line 1]", file=sys.stderr)
                    exit(70)
                except RuntimeError as e:
                    exit(70)

        if has_error:
            exit(65)
    else:
        print(
            "EOF  null"
        )  # Placeholder, remove this line when implementing the scanner


if __name__ == "__main__":
    main()
