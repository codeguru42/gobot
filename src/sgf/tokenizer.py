from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Iterator, Tuple


class TokenType(Enum):
    L_PAREN = "("
    R_PAREN = ")"
    L_BRACKET = "["
    R_BRACKET = "]"
    SEMI = ";"
    COLON = ":"
    NONE = "NONE"
    NUMBER = "NUMBER"
    REAL = "REAL"
    DOUBLE = "DOUBLE"
    COLOR = "COLOR"
    SIMPLE_TEXT = "SIMPLE_TEXT"
    TEXT = "TEXT"
    POINT = "POINT"
    MOVE = "MOVE"
    STONE = "STONE"
    IDENT = "IDENT"
    UNKNOWN = "UNKNOWN"


@dataclass
class Token:
    type: TokenType
    token: str


def parse_ident(c: str, input_stream: Iterator[str]) -> Tuple[Token, str]:
    token = [c]
    next_c = next(input_stream)
    try:
        while next_c.isupper():
            token.append(next_c)
            next_c = next(input_stream)
    finally:
        return Token(TokenType.IDENT, "".join(token)), next_c


def tokens(input_stream: Iterable[str]) -> Iterable[Token]:
    input_iter = iter(input_stream)
    c = next(input_iter)
    try:
        while True:
            match c:
                case "(":
                    yield Token(TokenType.L_PAREN, c)
                    c = next(input_iter)
                case ")":
                    yield Token(TokenType.R_PAREN, c)
                    c = next(input_iter)
                case "[":
                    yield Token(TokenType.L_BRACKET, c)
                    c = next(input_iter)
                case "]":
                    yield Token(TokenType.R_BRACKET, c)
                    c = next(input_iter)
                case ";":
                    yield Token(TokenType.SEMI, c)
                    c = next(input_iter)
                case ":":
                    yield Token(TokenType.COLON, c)
                    c = next(input_iter)
                case _:
                    if c.isupper():
                        token, next_c = parse_ident(c, input_iter)
                        yield token
                        c = next_c
                    else:
                        yield Token(TokenType.UNKNOWN, c)
                        c = next(input_iter)
    except StopIteration:
        pass