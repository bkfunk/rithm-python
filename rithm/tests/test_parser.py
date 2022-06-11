from rithm.ast_printer import ASTPrinter
from rithm.rithm import Rithm
from rithm.expr import Binary, Literal
from rithm.stmt import ExpressionStmt
from rithm.testing import std_str
from rithm.token import Token, TokenType as TT
from rich import print
from rich.pretty import pretty_repr, pprint

rtm = Rithm()


def scan_parse_repr(input: str) -> str:
    stmts = rtm().parse(rtm().scan(input))
    return std_str(pretty_repr(stmts))


def test_parse_basic_addition():
    assert scan_parse_repr("1 + 2.5") == std_str(
        """
        [
            ExpressionStmt(
                expr=Binary(
                    left=Literal(INTEGER=1),
                    operator=Token("+"),
                    right=Literal(FLOAT=2.5)
                )
            )
        ]
        """
    )


def test_parse_multiple_expressions():
    assert (
        scan_parse_repr(
            """ 
            2 + 9.2 + 19

            foo = 3
            """
        )
        == std_str(
            """
            [
                ExpressionStmt(
                    expr=Binary(
                        left=Binary(
                            left=Literal(INTEGER=2),
                            operator=Token("+"),
                            right=Literal(FLOAT=9.2)
                        ),
                        operator=Token("+"),
                        right=Literal(INTEGER=19)
                    )
                ),
                ExpressionStmt(
                    expr=Assignment(
                        name=Token(IDENTIFIER="foo"),
                        value=Literal(INTEGER=3)
                    )
                )
            ]
            """
        )
    )


def test_parse_string_assignment():
    assert (
        scan_parse_repr(
            """
            foo_bar = "hello"
            foo_baz = "hello there, sir!"
            """
        )
        == std_str(
            """[
                ExpressionStmt(
                    expr=Assignment(
                        name=Token(IDENTIFIER="foo_bar"),
                        value=Literal(STRING="hello")
                    )
                ),
                ExpressionStmt(
                    expr=Assignment(
                        name=Token(IDENTIFIER="foo_baz"),
                        value=Literal(STRING="hello there, sir!")
                    )
                )
            ]"""
        )
    )


def test_parse_block():
    assert (
        scan_parse_repr(
            """
            do
                x
                x = x + 1
            end
            """
        )
        == std_str(
            """[
                BlockStmt(
                    stmts=[
                        ExpressionStmt(
                            expr=Identifier(
                                IDENTIFIER="x"
                            )
                        ),
                        ExpressionStmt(
                            expr=Assignment(
                                name=Token(IDENTIFIER="x"),
                                value=Binary(
                                    left=Identifier(IDENTIFIER="x"),
                                    operator=Token("+"),
                                    right=Literal(INTEGER=1)
                                )
                            )
                        )
                    ]
                )
            ]"""
        )
    )


def test_parse_if():
    assert (
        scan_parse_repr(
            """
            if x > 3 do
                x = x + 1
            end
            """
        )
        == std_str(
            """
            [
                IfStmt(
                    condition=Binary(
                        left=Identifier(IDENTIFIER='x'),
                        operator=Token(">"),
                        right=Literal(INTEGER=3)
                    ),
                    then_branch=BlockStmt(
                        stmts=[
                            ExpressionStmt(
                                expr=Assignment(
                                    name=Token(IDENTIFIER='x'),
                                    value=Binary(
                                        left=Identifier(IDENTIFIER='x'),
                                        operator=Token('+'),
                                        right=Literal(INTEGER=1)
                                    )
                                )
                            )
                        ]
                    ),
                    else_branch=None
                )
            ]
            """
        )
    )

    assert (
        scan_parse_repr(
            """
    if x < 1.2 do
        "hello"
    else
        "goodbye"
    end
    """
        )
        == std_str(
            """[
            IfStmt(
                condition=Binary(),
            )
    ]"""
        )
    )
