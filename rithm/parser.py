from dataclasses import Field, dataclass, field
from functools import wraps
from typing import Callable, Container, List, Sequence, Tuple, Optional, Union
from rithm.expr import Assignment, Binary, Expr, Grouping, Identifier, Literal, Unary
from rithm.logging import get_logger
from rithm.stmt import BlockStmt, ExpressionStmt, IfStmt, Stmt
import logging
from rithm.logging import get_logger

from rithm.token import Token, TokenType as TT
from rich import print
from rich.pretty import pretty_repr

WHITESPACE = (TT.SPACE, TT.TAB)

parse_logger = get_logger(__name__)


class ParseError(Exception):
    pass


def logged(fn):
    @wraps(fn)
    def log_fn(parser, *args, **kwargs):
        # tokens = parser.tokens[parser.current:]
        # tokens_str = ''.join([token.lexeme for token in tokens])
        # token_types = [token.token_type.name for token in tokens]

        indent = parser.depth * " "
        parse_logger.debug(
            f"{indent}{fn.__name__}"
        )  # with tokens: {tokens_str!r} {token_types}")

        parser.depth += 1
        result = fn(parser, *args, **kwargs)
        parser.depth -= 1
        return result

    return log_fn


@dataclass
class Parser:
    tokens: List[Token]
    current: int = field(default=0, init=False)
    depth: int = field(default=0, init=False)

    CLOSING_TOKENS = {
        TT.BRACKET_OPEN: TT.BRACKET_CLOSE,
        TT.PAREN_OPEN: TT.PAREN_CLOSE,
        TT.BRACE_OPEN: TT.BRACE_CLOSE,
    }

    @property
    def is_at_end(self) -> bool:
        # TODO: Should we check for EOF? Or just length of tokens?
        return self.current >= len(self.tokens)

    @property
    def prev_token(self) -> Token:
        return self.tokens[self.current - 1]

    @property
    def current_token(self) -> Token:
        return self.tokens[self.current]

    @property
    def next_token(self) -> Token:
        return self.tokens[self.current + 1]

    # def peek(self) -> Token:
    #     return self.tokens[self.current]

    def consume_and_advance(
        self, ignore: Optional[Container[TT]] = WHITESPACE
    ) -> Token:
        # Return current token, then move cursor
        # (or, equivalently, move cursor and return previous token)
        if ignore is not None:
            parse_logger.debug(f"Ignoring: {ignore}")
            try:
                while self.current_token.token_type in ignore:
                    parse_logger.debug(f"Ignored {self.current}: {self.current_token}")
                    self.current += 1
            except IndexError:
                pass
        parse_logger.debug(f"Consuming {self.current}: {self.current_token}")
        self.current += 1
        if not self.is_at_end:
            parse_logger.debug(
                f"New current token {self.current}: {self.current_token}"
            )
        return self.prev_token

    def match(
        self, *token_types: TT, ignore: Optional[Container[TT]] = WHITESPACE
    ) -> bool:
        if self.is_at_end:
            return False

        _old_current = self.current

        if ignore is not None:
            while self.current_token.token_type in ignore:
                self.current += 1
                if self.is_at_end:
                    self.current = _old_current
                    return False

        if self.current_token.token_type in token_types:
            parse_logger.debug(f"Matched: {self.current_token}")
            self.current = _old_current
            return True
        self.current = _old_current
        return False

    def synchronize(self):
        """Try to get to the next valid state"""
        parse_logger.debug(f"Synchronizing: {self.current_token}")
        while not self.is_at_end:
            if self.prev_token.token_type is TT.NEWLINE:
                parse_logger.debug(f"Synchronized at {self.current_token}")
                return
            self.consume_and_advance()

    def parse(self) -> List[Stmt]:
        parse_logger.debug(f"Parsing tokens: {pretty_repr(self.tokens)}")
        # parse_logger.debug(self.tokens)
        stmts = []
        while not self.is_at_end:
            try:
                parsed = self.parse_declaration()
                if parsed is not None:
                    stmts.append(parsed)
                # stmts.append(self.parse_declaration())
            except ParseError:
                self.synchronize()
        return stmts

    @logged
    def parse_declaration(self) -> Optional[Stmt]:
        parsed = self.parse_statement()
        return parsed

    @logged
    def parse_statement(self) -> Optional[Stmt]:
        self.depth = 0

        if self.match(TT.DO):
            return self.parse_block_statement()
        if self.match(TT.IF):
            return self.parse_if_statement()

        # if self.match(TT.IDENTIFIER):

        # Consume the next token and try to parse it as an expression
        parsed = self.parse_expression()

        if parsed is None:
            # If parsed is None, it means the token should be ignored.
            # If result should be ignored, then ignore it
            return

        # If we've parsed something, and then it's followed by either a newline or end-of-file,
        # then consume that terminator and return what we've parsed
        if self.match(TT.NEWLINE, TT.EOF):
            self.consume_and_advance()
            if isinstance(parsed, Expr):
                return ExpressionStmt(parsed)
            return parsed

        parse_logger.error(
            "Statement ended with no newline:"
            f" {parsed}\n{self.current_token}\n{self.next_token}"
        )
        raise ParseError("Statements must end in newline")

    @logged
    def parse_block_statement(self) -> BlockStmt:
        self.consume_and_advance(
            ignore=[*WHITESPACE, TT.NEWLINE]
        )  # Consume the DO token and spacing
        stmts = []

        while not self.match(TT.END):
            if self.match(TT.EOF):
                raise ParseError("No end to match opening do")
            next_stmt = self.parse_statement()
            if next_stmt is not None:
                stmts.append(next_stmt)

        end = self.consume_and_advance()  # Consume the END token
        parse_logger.debug("Got end:", end)

        return BlockStmt(stmts=stmts)

    # @logged
    def parse_if_statement(self) -> IfStmt:
        # TODO: What should delimit the if statement?
        self.consume_and_advance()  # Consume the IF token
        condition = self.parse_expression()
        then_branch = self.parse_statement()
        if self.match(TT.ELSE):
            self.consume_and_advance()  # Consume the ELSE token
            else_branch = self.parse_statement()
        else:
            else_branch = None

        # TODO: what happens if there's a blank line as the condition and/or then branch?
        if condition is None or then_branch is None:
            # TODO: Can then branch be empty?
            self.raise_error("If statement must have condition and then block")

        return IfStmt(
            condition=condition, then_branch=then_branch, else_branch=else_branch
        )

    # @logged
    # def parse_assigment_or_higher(self) -> Union[Expr, Stmt]:

    @logged
    def parse_expression(self) -> Optional[Expr]:
        # return self.parse_equality_or_higher()
        return self.parse_assignment_or_higher()

    # @logged
    def parse_assignment_or_higher(self) -> Optional[Expr]:
        expr = self.parse_equality_or_higher()

        if self.match(TT.EQUAL):
            equals = self.consume_and_advance()
            value = self.parse_assignment_or_higher()

            if isinstance(expr, Identifier):
                return self.log_and_parse(Assignment(expr.token, value))
        return expr

    def _parse_binary(
        self,
        higher_method: Callable,
        matching_tokens: Sequence[TT],
        ignore: Optional[Container[TT]] = WHITESPACE,
    ) -> Optional[Expr]:
        next_expr = higher_method()

        while self.match(*matching_tokens, ignore=ignore):
            operator = self.consume_and_advance(ignore=ignore)
            right = higher_method()
            next_expr = self.log_and_parse(
                Binary(left=next_expr, operator=operator, right=right)
            )

        return next_expr

    # @logged
    def parse_equality_or_higher(self) -> Optional[Expr]:
        return self._parse_binary(
            higher_method=self.parse_comparison_or_higher,
            matching_tokens=(TT.EQUAL_EQUAL,),
        )

    # @logged
    def parse_comparison_or_higher(self) -> Optional[Expr]:
        return self._parse_binary(
            higher_method=self.parse_add_sub_or_higher,
            matching_tokens=(
                TT.LESS_THAN,
                TT.LESS_EQUAL,
                TT.GREATER_THAN,
                TT.GREATER_EQUAL,
            ),
        )
        # next_expr = self.parse_add_sub_or_higher()

        # while self.match(TT.PLUS, TT.MINUS):
        #     comparison_operator = self.consume_and_advance()
        #     right = self.parse_add_sub_or_higher()
        #     next_expr = Binary(left=next_expr, operator=comparison_operator, right=right)

        # return next_expr

    # @logged
    def parse_add_sub_or_higher(self) -> Optional[Expr]:
        return self._parse_binary(
            higher_method=self.parse_mult_div_or_higher,
            matching_tokens=(TT.PLUS, TT.MINUS),
        )

    # @logged
    def parse_mult_div_or_higher(self) -> Optional[Expr]:
        return self._parse_binary(
            higher_method=self.parse_unary_or_higher,
            matching_tokens=(TT.STAR, TT.SLASH),
        )

    # @logged
    def parse_unary_or_higher(self) -> Optional[Expr]:
        if self.match(TT.BANG, TT.MINUS):
            operator = self.consume_and_advance()
            expr = self.parse_unary_or_higher()
            return self.log_and_parse(Unary(operator=operator, expr=expr))

        # If not a unary, than it must be a literal
        return self.parse_literal()

    # @logged
    def parse_call_or_higher(self) -> Optional[Expr]:
        expr = self.parse_primary_or_higher()
        # TODO: Parse arguments

    # @logged
    def parse_primary_or_higher(self) -> Optional[Expr]:
        expr = self.parse_literal()
        return expr

    # @logged
    def parse_literal(self) -> Optional[Expr]:
        literal_token = self.consume_and_advance()
        match literal_token.token_type:
            case TT.NEWLINE | TT.EOF:
                # Ignore empty lines
                return None
            case TT.FALSE:
                return self.log_and_parse(
                    Literal(value=False, token_type=literal_token.token_type)
                )
            case TT.TRUE:
                return self.log_and_parse(
                    Literal(value=True, token_type=literal_token.token_type)
                )
            case TT.STRING | TT.INTEGER | TT.FLOAT:
                return self.log_and_parse(
                    Literal(literal_token.literal, token_type=literal_token.token_type)
                )
            case TT.PAREN_OPEN | TT.BRACE_OPEN | TT.BRACKET_OPEN:
                expr = self.parse_expression()
                if self.match(self.CLOSING_TOKENS[literal_token.token_type]):
                    close_paren = self.consume_and_advance()
                    return self.log_and_parse(
                        Grouping(
                            expr,
                            open_token_type=literal_token.token_type,
                            close_token_type=close_paren.token_type,
                        )
                    )

                self.raise_error(
                    f"Opening delimiter {literal_token.token_type.value} has no closing"
                    " delimiter"
                )
            case TT.IDENTIFIER:
                return self.log_and_parse(Identifier(literal_token))

        self.raise_error(f"Could not parse {literal_token}")

    def raise_error(self, msg: str):
        parse_logger.error(msg)
        raise ParseError(msg)

    def log_and_parse(self, expr: Expr) -> Expr:
        parse_logger.debug(f"Parsed {expr}")
        return expr
