from app.scanner import Token
from typing import Any


class Expr:
    def accept(self, visitor):
        return visitor.visit(self)


class Declaration:
    def accept(self, visitor):
        return visitor.visit(self)


class VariableDeclaration(Declaration):
    def __init__(self, name: Token, initializer: Expr):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visitVariableDeclaration(self)


class Stmt:
    def accept(self, visitor):
        return visitor.visit(self)


class Expression(Stmt):
    def __init__(self, expr: Expr):
        self.expr = expr

    def accept(self, visitor):
        return visitor.visitExpressionStatement(self)


class Print(Stmt):
    def __init__(self, expr: Expr):
        self.expr = expr

    def accept(self, visitor):
        return visitor.visitPrintStatement(self)


##########################################################


class Variable(Expr):
    def __init__(self, name: Token):
        self.name = name

    def accept(self, visitor):
        return visitor.visitVariableExpression(self)


class Literal(Expr):
    def __init__(self, value: Any):
        self.value = value

    def accept(self, visitor):
        return visitor.visitLiteralExpression(self)

    def __str__(self):
        return f"Literal: {self.value}"

    def __repr__(self):
        return self.__str__()


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitUnaryExpression(self)


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitBinaryExpression(self)


class Grouping(Expr):
    def __init__(self, expr: Expr):
        self.expr = expr

    def accept(self, visitor):
        return visitor.visitGroupingExpression(self)
