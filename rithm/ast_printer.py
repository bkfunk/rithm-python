from dataclasses import dataclass
from typing import Union
from rithm.token import Token, TokenType

from rithm.visitor import Visitor
from rithm.expr import Expr, Literal, Binary
from rithm.stmt import ExpressionStmt, Stmt


# class Indenter:


@dataclass
class ASTPrinter(Visitor):
    pretty: bool = True
    indent_level: int = 0
    tab_spaces: int = 4

    def indent(self, string: str) -> str:
        if self.pretty:
            self.indent_level += 1
            if self.tab_spaces is not None:
                tab = self.tab_spaces * self.indent_level * " "
            else:
                tab = self.indent_level * "\t"
            self.indent_level -= 1
            return tab + string
        return string

    def get_string(self, obj: Union[Expr, Stmt]) -> str:
        return obj.accept(self)

    def print(self, obj: Union[Expr, Stmt]):
        print(self.get_string(obj))

    def visit_token(self, token: Token) -> str:
        return self.visit_token_type(token.token_type)

    def visit_token_type(self, token_type: TokenType) -> str:
        return f"TT.{token_type._name_}"

    def visit_literal_expr(self, expr: Literal) -> str:
        return f"Literal({self.visit_token_type(expr.token_type)}: {expr.value!r})"

    def visit_binary_expr(self, expr: Binary) -> str:
        result = "Binary("
        with self.indent():
            result += (
                self.get_string(expr.left)
                + f" {self.visit_token(expr.operator)} "
                + self.get_string(expr.right)
            )
        result += ")"
        return result
        # return (
        #     "Binary(" + self.indent(

        #     )
        #     + ")"
        # )

    def visit_expression_stmt(self, stmt: ExpressionStmt) -> str:
        return "ExpressionStmt(" + self.indent(self.get_string(stmt.expr)) + ")"
