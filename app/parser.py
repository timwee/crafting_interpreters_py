from app.scanner import Token, TokenType
from typing import Any
import sys
from app.ast import Expr, Literal, Unary, Binary, Grouping, Print, Expression

class ParseError(Exception):
  def __init__(self, m):
        self.message = m
  def __str__(self):
      return self.message

class Parser:
    def __init__(self, tokens: list[Token]):
      self.tokens = tokens
      self.current = 0

    def parse_statements(self):
      try:
        statements = []
        while not self.is_at_end():
          statements.append(self.statement())
        return statements
      except ParseError as e:
        raise e
    
    def parse_expressions(self):
      try:
        exprs = []
        while not self.is_at_end():
          new_expr = self.expression()
          exprs.append(new_expr)
        return exprs
      except ParseError:
        return []
      
    def statement(self):
      if self.match(TokenType.PRINT):
        return self.print_statement()
      return self.expression_statement()
    
    def print_statement(self):
      value = self.expression()
      self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
      return Print(value)
    
    def expression_statement(self):
      expr = self.expression()
      self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
      return Expression(expr)
            
    def expression(self):
      return self.equality()
        
    def equality(self):
      expr = self.comparison()
      while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
        operator = self.previous()
        right = self.comparison()
        expr = Binary(expr, operator, right)  
      return expr

    def comparison(self):
      expr = self.term()
      while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
        operator = self.previous()
        right = self.term()
        expr = Binary(expr, operator, right)
      return expr

    def term(self): 
      expr = self.factor()
      while self.match(TokenType.MINUS, TokenType.PLUS):
        operator = self.previous()
        right = self.factor()
        expr = Binary(expr, operator, right)
      return expr
    
    def factor(self):
      expr = self.unary()
      while self.match(TokenType.SLASH, TokenType.STAR): 
        operator = self.previous()
        right = self.unary()
        expr = Binary(expr, operator, right)
      return expr

    def unary(self):
      if self.match(TokenType.BANG, TokenType.MINUS):
        operator = self.previous()
        right = self.unary()
        return Unary(operator, right)
      return self.primary()

    def primary(self):
      if self.match(TokenType.TRUE):
        return Literal(True)
      elif self.match(TokenType.FALSE):
        return Literal(False)
      elif self.match(TokenType.NUMBER, TokenType.STRING, TokenType.NIL):
        # print(f"in literal {self.previous().value}")
        return Literal(self.previous().value)
        
      if self.match(TokenType.LEFT_PAREN):
        expr = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
        return Grouping(expr)
      raise self.create_error(self.peek(), "Expect expression.")
        
        
    def match(self, *types: TokenType) -> bool:
      for type in types:
        if self.check(type):
          self.advance()
          return True
      return False
      
    def check(self, type: TokenType) -> bool:
      if self.is_at_end():
        return False
      return self.peek().type == type
    
    def previous(self) -> Token:
      return self.tokens[self.current - 1]
    
    def peek(self) -> Token:
      return self.tokens[self.current]
    
    def advance(self) -> Token:
      if not self.is_at_end():
        self.current += 1
      return self.previous()
        

    def is_at_end(self):
        return self.current >= len(self.tokens)
      
    def consume(self, type: TokenType, msg: str) -> Token:
      if self.check(type=type):
        return self.advance()
      raise self.create_error(self.peek(), msg)
    
    def create_error(self, token: Token, msg: str):
      if token.type == TokenType.EOF:
        print(f"[line {token.line}] Error at end: {msg}", file=sys.stderr)
      else:
        print(f"[line {token.line}] Error at {token.lexeme}: {msg}", file=sys.stderr)
      return ParseError(msg)
      