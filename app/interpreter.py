from typing import Any
from app.parser import Expr, Literal, Grouping, Unary, Binary
from app.scanner import TokenType


class Interpreter:
  def evaluate(self, expr: Expr):
    return expr.accept(self)
  
  def visit(self, expr: Expr):
    return expr.accept(self)
  
  def visitLiteralExpression(self, expr: Literal):
    return expr.value
  
  def visitGroupingExpression(self, expr: Grouping):
    return self.evaluate(expr.expr)
  
  def _isTruthy(self, val: Any) -> bool:
    if val is None:
      return False
    if isinstance(val, bool):
      return val
    return True
  
  def _isEqual(left: Any, right: Any) -> bool:
    if left is None:
      return right is None
    return left == right
    
  
  def visitBinaryExpression(self, expr: Binary):
    left = self.evaluate(expr.left)
    right = self.evaluate(expr.right)
    
    operator_type = expr.operator.type
    if operator_type == TokenType.GREATER:
      return float(left) > float(right)
    elif operator_type == TokenType.GREATER_EQUAL:
      return float(left) >= float(right)
    elif operator_type == TokenType.LESS:
      return float(left) < float(right)
    elif operator_type == TokenType.LESS_EQUAL:
      return float(left) <= float(right)
    elif operator_type == TokenType.EQUAL:
      return self._isEqual(left, right)
    elif operator_type == TokenType.BANG_EQUAL:
      return self._isEqual(left, right)
    elif operator_type == TokenType.MINUS:
      return float(left) - float(right)
    elif operator_type == TokenType.SLASH:
      return float(left) / float(right)
    elif operator_type == TokenType.STAR:
      return float(left) * float(right)
    elif operator_type == TokenType.PLUS:
      if isinstance(left,(float, int, complex)) and isinstance(right, (float, int, complex)):
        return float(left) + float(right)
      elif isinstance(left, str) and isinstance(right, str):
        return str(left) + str(right)
    return None
   
      
  
  def visitUnaryExpression(self, expr: Unary):
    right = self.evaluate(expr.right)
    
    if expr.operator.type == TokenType.MINUS:
      return -1 * (float(right))
    elif expr.operator.type == TokenType.BANG:
      return not self._isTruthy(right)
    return None
    
  
    
    