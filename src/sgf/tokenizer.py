import re
from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Iterator


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
    EOF = "EOF"


@dataclass
class Token:
    type: TokenType
    token: str


def parse_ident(c: str, input_iter: Iterator[str]) -> tuple[Token, str]:
    token = [c]
    next_c = next(input_iter)
    try:
        while next_c.isupper():
            token.append(next_c)
            next_c = next(input_iter)
    finally:
        return Token(TokenType.IDENT, "".join(token)), next_c


def parse_number(c, input_iter):
    token_type = TokenType.NUMBER
    token = [c]
    next_c = next(input_iter)
    try:
        while next_c.isdigit():
            token.append(next_c)
            next_c = next(input_iter)

        if next_c == ".":
            token_type = TokenType.REAL
            token.append(next_c)
            next_c = next(input_iter)
            while next_c.isdigit():
                token.append(next_c)
                next_c = next(input_iter)
    finally:
        return Token(token_type, "".join(token)), next_c


def parse_value(c, input_iter):
    token_chars = []
    while c != "]":
        token_chars.append(c)
        c = next(input_iter)

    token_str = "".join(token_chars)
    re_number = r"[+-]?\d+"
    re_real = r"[+-]?\d+(\.\d+)?"
    match token_str:
        case "":
            return Token(TokenType.NONE, token_str), c
        case "B" | "W":
            return Token(TokenType.COLOR, token_str), c
        case _:
            if re.fullmatch(re_number, token_str):
                return Token(TokenType.NUMBER, token_str), c
            if re.fullmatch(re_real, token_str):
                return Token(TokenType.REAL, token_str), c
            if token_str.islower() and len(token_str) == 2:
                return Token(TokenType.POINT, token_str), c

            return Token(TokenType.TEXT, token_str), c


def tokens(input_stream: Iterable[str]) -> Iterable[Token]:
    input_iter = iter(input_stream)
    c = next(input_iter)
    try:
        while True:
            match c:
                case None:
                    raise StopIteration
                case "(":
                    yield Token(TokenType.L_PAREN, c)
                    c = next(input_iter)
                case ")":
                    yield Token(TokenType.R_PAREN, c)
                    c = next(input_iter)
                case "[":
                    yield Token(TokenType.L_BRACKET, c)
                    c = next(input_iter)
                    value, next_c = parse_value(c, input_iter)
                    yield value
                    c = next_c
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
                    if c.isspace():
                        c = next(input_iter)
                    elif c.isupper():
                        token, next_c = parse_ident(c, input_iter)
                        yield token
                        c = next_c
                    else:
                        yield Token(TokenType.UNKNOWN, c)
                        c = next(input_iter)
    except StopIteration:
        yield Token(TokenType.EOF, "")
