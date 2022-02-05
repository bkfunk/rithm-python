from rithm.ast_printer import ASTPrinter
from rithm.rithm import Rithm
from rithm.expr import Binary, Literal
from rithm.stmt import ExpressionStmt
from rithm.token import Token, TokenType as TT
from rich import print

rtm = Rithm()

def print_all(stmts):
    printer = ASTPrinter()
    return [
        printer.get_string(stmt)
        for stmt in stmts
    ]

def test_parse_expressions():
    assert print_all(rtm().parse(rtm().scan("1 + 2.5"))) == [
        """
        ExpressionStmt(
            Binary(
                Literal(value=1, token_type=TT.INTEGER),
                Token(TT.PLUS),
                Literal(value=2.5, token_type=TT.FLOAT),
            )
        )"""
    ]


def test_parser():

    stmts = rtm().parse(
        rtm().scan(
            """ 
    2 + 9.2 + 19

    foo = 3
    """
        )
    )
    print("Statements: ", stmts)
    assert len(stmts) == 2
    assert isinstance(stmts[0], ExpressionStmt)
    assert isinstance(stmts[1], ExpressionStmt)
