from typing import Union

from rithm.visitor import Visitor
from rithm.expr import Expr, Literal, Binary
from rithm.stmt import ExpressionStmt, Stmt


class ASTPrinter(Visitor):
    def get_string(self, obj: Union[Expr, Stmt]) -> str:
        return obj.accept(self)

    def print(self, obj: Union[Expr, Stmt]):
        print(self.get_string(obj))

    def visit_literal_expr(self, expr: Literal):
        return f"Literal({expr.value!r})"

    def visit_binary_expr(self, expr: Binary):
        return (
            "Binary("
            + self.get_string(expr.left)
            + f" {expr.operator.token_type._value_} "
            + self.get_string(expr.right)
            + ")"
        )

    def visit_expression_stmt(self, stmt: ExpressionStmt):
        return "ExpressionStmt(" + self.get_string(stmt.expr) + ")"
