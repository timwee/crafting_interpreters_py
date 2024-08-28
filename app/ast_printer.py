from app.parser import Expr, Literal, Grouping, Unary, Binary

class AstPrinter:
    def print(self, expression: Expr):
      # print(f"expression: {expression}")
      return expression.accept(self)
      
    def visitLiteralExpression(self, expression: Literal):
        if isinstance(expression.value, str):
            return f'{expression.value}'
        elif isinstance(expression.value, float):
            return f"{expression.value}"
        elif isinstance(expression.value, bool):
            return "true" if expression.value else "false"
        else:
            return "nil"
          
    def visit(self, expression: Expr):
      return "expression"
    
    def visitGroupingExpression(self, expression: Grouping):
      return f'(group {self.print(expression=expression.expr)})'
    
    def visitUnaryExpression(self, expression: Unary):
      return f'({expression.operator.lexeme} {self.print(expression.right)})'