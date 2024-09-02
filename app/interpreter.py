from typing import Any
from app.ast import (
    Expr,
    Literal,
    Grouping,
    Unary,
    Binary,
    Print,
    Expression,
    Stmt,
    Variable,
    VariableDeclaration,
    Assignment,
)
from app.scanner import TokenType
import sys
from app.utils import stringify
from app.environment import Environment
import pprint
from app.ast_printer import AstPrinter


class EvaluationError(Exception):
    def __init__(self, m):
        self.message = m

    def __str__(self):
        return self.message


class Interpreter:

    def __init__(self):
        self.environment = Environment()

    def interpret(self, stmts: list[Stmt]):
        # try:
        printer = AstPrinter()
        for stmt in stmts:
            print("in interpret:", printer.print(stmt), file=sys.stderr)
            if not stmt:
                continue
            self.evaluate(stmt)

    # except Exception as e:
    #     raise e

    def evaluate(self, stmt: Stmt):
        if isinstance(stmt, Expr):
            return self.visit(stmt)
        elif isinstance(stmt, Print):
            return self.visitPrintStatement(stmt)
        elif isinstance(stmt, Expression):
            return self.visitExpressionStatement(stmt)
        elif isinstance(stmt, VariableDeclaration):
            return self.visitVariableDeclaration(stmt)
        else:
            raise ValueError(f"Unexpected statement type: {type(stmt)}")

    def visitPrintStatement(self, stmt: Print):
        value = self.visit(stmt.expr)
        print(stringify(value))
        return None

    def visitExpressionStatement(self, stmt: Expression):
        self.evaluate(stmt.expr)
        return None

    def visitAssignmentExpression(self, expr: Assignment):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def visit(self, expr: Expr):
        if isinstance(expr, Literal):
            return self.visitLiteralExpression(expr)
        elif isinstance(expr, Grouping):
            return self.visitGroupingExpression(expr)
        elif isinstance(expr, Unary):
            return self.visitUnaryExpression(expr)
        elif isinstance(expr, Binary):
            return self.visitBinaryExpression(expr)
        elif isinstance(expr, Assignment):
            return self.visitAssignmentExpression(expr)
        elif isinstance(expr, Variable):
            return self.visitVariableExpression(expr)
        elif isinstance(expr, Expression):
            return self.visitExpressionStatement(expr)
        elif isinstance(expr, VariableDeclaration):
            return self.visitVariableDeclaration(expr)
        elif isinstance(expr, Print):
            return self.visitPrintStatement(expr)
        else:
            raise ValueError(f"Unexpected expression type: {type(expr)}")

    def visitLiteralExpression(self, expr: Literal):
        return expr.value

    def visitGroupingExpression(self, expr: Grouping):
        return self.evaluate(expr.expr)

    def visitVariableExpression(self, expr: Variable):
        return self.environment.get(expr.name)

    def visitVariableDeclaration(self, stmt: VariableDeclaration):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)
        return value

    def _isTruthy(self, val: Any) -> bool:
        if val is None:
            return False
        if isinstance(val, bool):
            return val
        return True

    def _isEqual(self, left: Any, right: Any) -> bool:
        if left is None:
            return right is None
        return left == right

    def _checkNumberOperand(self, operand: Any) -> bool:
        if isinstance(operand, (float)):
            return True
        raise EvaluationError(f"Operand must be a number")

    def _checkNumberOperands(self, left: Any, right: Any) -> bool:
        if isinstance(left, (float)) and isinstance(right, (float)):
            return True
        raise EvaluationError(f"Operands must be numbers")

    def visitBinaryExpression(self, expr: Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        operator_type = expr.operator.type
        if operator_type == TokenType.GREATER:
            self._checkNumberOperands(left, right)
            return float(left) > float(right)
        elif operator_type == TokenType.GREATER_EQUAL:
            self._checkNumberOperands(left, right)
            return float(left) >= float(right)
        elif operator_type == TokenType.LESS:
            self._checkNumberOperands(left, right)
            return float(left) < float(right)
        elif operator_type == TokenType.LESS_EQUAL:
            self._checkNumberOperands(left, right)
            return float(left) <= float(right)
        elif operator_type == TokenType.EQUAL_EQUAL:
            return self._isEqual(left, right)
        elif operator_type == TokenType.BANG_EQUAL:
            return not self._isEqual(left, right)
        elif operator_type == TokenType.MINUS:
            self._checkNumberOperands(left, right)
            return float(left) - float(right)
        elif operator_type == TokenType.SLASH:
            self._checkNumberOperands(left, right)
            return float(left) / float(right)
        elif operator_type == TokenType.STAR:
            self._checkNumberOperands(left, right)
            return float(left) * float(right)
        elif operator_type == TokenType.PLUS:
            if isinstance(left, (float, int, complex)) and isinstance(
                right, (float, int, complex)
            ):
                return float(left) + float(right)
            elif isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)
            else:
                raise EvaluationError(
                    f"+ operator should be either numbers or strings, but encountered {left} and {right}"
                )
        return None

    def visitUnaryExpression(self, expr: Unary):
        right = self.evaluate(expr.right)

        if expr.operator.type == TokenType.MINUS:
            print(
                f"in visitUnary minus, right: {right}, {isinstance(right, (int, float))}",
                file=sys.stderr,
            )
            self._checkNumberOperand(right)
            return -1 * (float(right))
        elif expr.operator.type == TokenType.BANG:
            return not self._isTruthy(right)
        return None
