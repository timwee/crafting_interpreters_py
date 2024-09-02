from app.ast import (
    Expr,
    Literal,
    Grouping,
    Unary,
    Binary,
    Assignment,
    Variable,
    Expression,
    VariableDeclaration,
    Print,
    Block,
)
from app.utils import stringify


class AstPrinter:
    def print(self, expression: Expr):
        if not expression:
            return "nil"
        return expression.accept(self)

    def visit(self, expression: Expr):
        # Instead of calling accept again, we need to handle each type of expression directly
        if isinstance(expression, Literal):
            return self.visitLiteralExpression(expression)
        elif isinstance(expression, Grouping):
            return self.visitGroupingExpression(expression)
        elif isinstance(expression, Unary):
            return self.visitUnaryExpression(expression)
        elif isinstance(expression, Binary):
            return self.visitBinaryExpression(expression)
        elif isinstance(expression, Assignment):
            return self.visitAssignmentExpression(expression)
        elif isinstance(expression, Variable):
            return self.visitVariableExpression(expression)
        elif isinstance(expression, Expression):
            return self.visitExpressionStatement(expression)
        elif isinstance(expression, VariableDeclaration):
            return self.visitVariableDeclaration(expression)
        elif isinstance(expression, Print):
            return self.visitPrintStatement(expression)
        elif isinstance(expression, Block):
            return self.visitBlockStatement(expression)
        else:
            raise ValueError(f"Unexpected expression type: {type(expression)}")

    def visitLiteralExpression(self, expression: Literal):
        if isinstance(expression.value, str):
            return f"{expression.value}"
        elif isinstance(expression.value, float):
            return f"{expression.value}"
        elif isinstance(expression.value, bool):
            return "true" if expression.value else "false"
        else:
            return "nil"

    def visitGroupingExpression(self, expression: Grouping):
        return f"(group {self.print(expression=expression.expr)})"

    def visitUnaryExpression(self, expression: Unary):
        return f"({expression.operator.lexeme} {self.print(expression.right)})"

    def visitBinaryExpression(self, expression: Binary):
        return f"({expression.operator.lexeme} {self.print(expression.left)} {self.print(expression.right)})"

    def visitAssignmentExpression(self, expression: Assignment):
        return f"(= {expression.name.lexeme} {self.print(expression.value)})"

    def visitVariableExpression(self, expression: Variable):
        return f"{expression.name.lexeme}"

    def visitVariableDeclaration(self, expression: VariableDeclaration):
        return f"(=var {expression.name.lexeme} {self.print(expression.initializer)})"

    def visitPrintStatement(self, expression: Print):
        return f"(print {self.print(expression.expr)})"

    def visitExpressionStatement(self, expression: Expression):
        return f"({self.print(expression.expr)})"

    def visitLiteralExpression(self, expression: Literal):
        val = expression.value
        if val is None:
            return "nil"
        elif isinstance(val, bool):
            if val:
                return "true"
            else:
                return "false"
        return f"{expression.value}"

    def visitBlockStatement(self, stmt: Block):
        return f"(block {[self.print(stmt) for stmt in stmt.statements]})"
