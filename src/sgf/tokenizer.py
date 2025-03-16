from dataclasses import dataclass
from enum import Enum
from typing import Iterable


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


@dataclass
class Token:
    type: TokenType
    token: str


def tokens(input_stream: Iterable[str]) -> Iterable[Token]:
    for c in input_stream:
        match c:
            case "(":
                yield Token(TokenType.L_PAREN, c)
            case ")":
                yield Token(TokenType.R_PAREN, c)
            case "[":
                yield Token(TokenType.L_BRACKET, c)
            case "]":
                yield Token(TokenType.R_BRACKET, c)
            case ";":
                yield Token(TokenType.SEMI, c)
            case ":":
                yield Token(TokenType.COLON, c)
