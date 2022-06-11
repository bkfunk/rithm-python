from dataclasses import dataclass, field
from typing import List, Optional
from rithm.expr import Expr
from rithm.visitor import Visitor


class Stmt:
    def accept(self, visitor: Visitor):
        method_name = (
            f"visit_{self.__class__.__name__.replace('Stmt', '_stmt').lower()}"
        )
        method = getattr(visitor, method_name)
        return method(self)


@dataclass
class BlockStmt(Stmt):
    stmts: List[Stmt] = field(default_factory=list)


@dataclass
class IfStmt(Stmt):
    condition: Expr
    then_branch: Stmt
    else_branch: Optional[Stmt]


@dataclass
class AlgoStmt(Stmt):
    pass


@dataclass
class ArrowStmt(Stmt):
    left: Expr
    right: Expr


@dataclass
class ExpressionStmt(Stmt):
    expr: Expr


# @dataclass
# class AssignmentStmt(Stmt):
#     name: str
#     value: Expr
#     # namespace: dict

#     """
#     """
