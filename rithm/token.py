from typing import Any, Container, List, Optional, Sequence, Tuple
from enum import Enum, auto
from dataclasses import dataclass


class TokenType(Enum):
    # Delimiters
    PAREN_OPEN = "("
    PAREN_CLOSE = ")"
    BRACE_OPEN = "{"
    BRACE_CLOSE = "}"
    BRACKET_OPEN = "["
    BRACKET_CLOSE = "]"
    TICK_OPEN = "`"
    TICK_CLOSE = "'"

    # Single character
    QUESTION_MARK = "?"
    AT_SIGN = "@"
    OCTOTHORPE = "#"
    COMMA = ","
    DOT = "."
    SEMICOLON = ";"
    COLON = ":"
    BANG = "!"
    QUOTE = '"'
    STAR = "*"
    SLASH = "/"
    PLUS = "+"
    MINUS = "-"
    CARET = "^"
    NEWLINE = "\n"

    # Literals
    TAB = "\t"
    SPACE = " "
    IDENTIFIER = auto()
    # COLNAME = auto()
    STRING = auto()
    INTEGER = auto()
    FLOAT = auto()

    # Operators
    EQUAL = "="
    EQUAL_EQUAL = "=="
    LESS_THAN = "<"
    LESS_EQUAL = "<="
    GREATER_THAN = ">"
    GREATER_EQUAL = ">="

    # Arrows
    ARROW_LEFT = "<-"
    ARROW_RIGHT = "->"
    DBL_ARROW_LEFT = "<=="
    DBL_ARROW_RIGHT = "==>"

    # Reserved Words
    DO = "do"
    END = "end"
    IF = "if"
    ELSE = "else"
    AS = "as"
    TRUE = "True"
    FALSE = "False"
    CLASS = "class"
    ALGO = "algo"
    AND = "and"
    OR = "or"

    # Other
    EOF = auto()

    def __repr__(self):
        # Reserved words: use name
        if isinstance(self._value_, str):
            if self._value_.upper() == self._name_:
                return self._name_
            return repr(self._value_)
        return self._name_


@dataclass
class Token:
    token_type: TokenType
    lexeme: str
    literal: Any
    line_no: int
    column: int

    def __rich_repr__(self):
        if self.token_type in (
            TokenType.IDENTIFIER,
            TokenType.STRING,
            TokenType.INTEGER,
            TokenType.FLOAT,
        ):
            yield self.token_type._name_, self.literal or self.lexeme
        else:
            yield self.token_type
        # if isinstance(self.token_type._value_, str):
        #     yield self.token_type
        # elif self.token_type == TokenType.IDENTIFIER:
        #     yield self.token_type._name_, self.lexeme
        # else:
        #     yield self.token_type._name_


def token_types(
    tokens: List[Token],
    ignore: Optional[Container[TokenType]] = (
        TokenType.SPACE,
        TokenType.NEWLINE,
        TokenType.TAB,
        TokenType.EOF,
    ),
) -> List[TokenType]:
    if ignore is None:
        ignore = []
    return [token.token_type for token in tokens if token.token_type not in ignore]
