from typing import Any
from app.parser import Expr, Literal, Grouping, Unary, Binary
from app.scanner import TokenType


class EvaluationError(Exception):
  def __init__(self, m):
        self.message = m
  def __str__(self):
      return self.message

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
  
  def _isEqual(self, left: Any, right: Any) -> bool:
    if left is None:
      return right is None
    return left == right
  
  def _checkNumberOperand(self, operand: Any) -> bool:
    if isinstance(operand, (int, float)):
      return True
    raise EvaluationError(f"{operand} must be a number")
  
  def _checkNumberOperands(self, left: Any, right: Any) -> bool:
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
      return True
    raise EvaluationError(f"both {left} and {right} must be a number")
    
  
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
      if isinstance(left,(float, int, complex)) and isinstance(right, (float, int, complex)):
        return float(left) + float(right)
      elif isinstance(left, str) and isinstance(right, str):
        return str(left) + str(right)
      else:
        raise EvaluationError(f"+ operator should be either numbers or strings, but encountered {left} and {right}")
    return None
   
      
  
  def visitUnaryExpression(self, expr: Unary):
    right = self.evaluate(expr.right)
    
    if expr.operator.type == TokenType.MINUS:
      self._checkNumberOperand(right)
      return -1 * (float(right))
    elif expr.operator.type == TokenType.BANG:
      return not self._isTruthy(right)
    return None
    
  
    
    