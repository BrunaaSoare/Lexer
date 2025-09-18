from enum import Enum

class TokenType:
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    RESERVED = "RESERVED"
    MATH_OPERATOR = "MATH_OPERATOR"
    REL_OPERATOR = "REL_OPERATOR"
    ASSIGNMENT = "ASSIGNMENT"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    ERROR = "ERROR"

class Token:
    def __init__(self, type_, value, line=None, column=None):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        if self.type == TokenType.ERROR and self.line is not None and self.column is not None:
            return f"<{self.type}, {self.value}, line={self.line}, col={self.column}>"
        else:
            return f"<{self.type}, {self.value}>"