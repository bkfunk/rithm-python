from dataclasses import dataclass
from typing import Any, List
from rithm.token import Token, TokenType as TT
from abc import ABC

from rithm.visitor import Visitor


@dataclass
class Expr:
    def accept(self, visitor: Visitor):
        method_name = f"visit_{self.__class__.__name__.lower()}_expr"
        method = getattr(visitor, method_name)
        return method(self)


@dataclass
class Literal(Expr):
    value: Any
    token_type: TT

    def __rich_repr__(self):
        yield self.token_type._name_, self.value
        # yield self.value


@dataclass
class Identifier(Expr):
    token: Token

    def __rich_repr__(self):
        yield self.token.token_type._name_, self.token.lexeme


@dataclass
class Assignment(Expr):
    name: Token
    value: Expr

    def __rich_repr__(self):
        yield "name", self.name
        yield "value", self.value


@dataclass
class Call(Expr):
    callee: Expr
    args: List[Expr]


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr


@dataclass
class Unary(Expr):
    operator: Token
    expr: Expr


@dataclass
class Grouping(Expr):
    expr: Expr
    open_token_type: TT
    close_token_type: TT
