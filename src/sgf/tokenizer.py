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
    line_number: int


def parse_ident(c: str, input_iter: Iterator[str], line_number: int) -> tuple[Token, str]:
    token = [c]
    next_c = next(input_iter)
    try:
        while next_c.isupper():
            token.append(next_c)
            next_c = next(input_iter)
    finally:
        return Token(TokenType.IDENT, "".join(token), line_number), next_c


def parse_number(c: str, input_iter: Iterator[str], line_number: int) -> tuple[Token, str]:
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
        return Token(token_type, "".join(token), line_number), next_c


def parse_value(c: str, input_iter: Iterator[str], line_number: int) -> tuple[Token, str]:
    token_chars = []
    while c != "]":
        token_chars.append(c)
        c = next(input_iter)

    token_str = "".join(token_chars)
    re_number = r"[+-]?\d+"
    re_real = r"[+-]?\d+(\.\d+)?"
    match token_str:
        case "":
            return Token(TokenType.NONE, token_str, line_number), c
        case "B" | "W":
            return Token(TokenType.COLOR, token_str, line_number), c
        case _:
            if re.fullmatch(re_number, token_str):
                return Token(TokenType.NUMBER, token_str, line_number), c
            if re.fullmatch(re_real, token_str):
                return Token(TokenType.REAL, token_str, line_number), c
            if token_str.islower() and len(token_str) == 2:
                return Token(TokenType.POINT, token_str, line_number), c

            return Token(TokenType.TEXT, token_str, line_number), c


def tokens(input_stream: Iterable[str]) -> Iterable[Token]:
    input_iter = iter(input_stream)
    c = next(input_iter)
    line_number = 1
    try:
        while True:
            match c:
                case None:
                    raise StopIteration
                case "(":
                    yield Token(TokenType.L_PAREN, c, line_number)
                    c = next(input_iter)
                case ")":
                    yield Token(TokenType.R_PAREN, c, line_number)
                    c = next(input_iter)
                case "[":
                    yield Token(TokenType.L_BRACKET, c, line_number)
                    c = next(input_iter)
                    value, next_c = parse_value(c, input_iter, line_number)
                    yield value
                    c = next_c
                case "]":
                    yield Token(TokenType.R_BRACKET, c, line_number)
                    c = next(input_iter)
                case ";":
                    yield Token(TokenType.SEMI, c, line_number)
                    c = next(input_iter)
                case ":":
                    yield Token(TokenType.COLON, c, line_number)
                    c = next(input_iter)
                case "\n":
                    line_number += 1
                    c = next(input_iter)
                case _:
                    if c.isspace():
                        c = next(input_iter)
                    elif c.isupper():
                        token, next_c = parse_ident(c, input_iter, line_number)
                        yield token
                        c = next_c
                    else:
                        yield Token(TokenType.UNKNOWN, c, line_number)
                        c = next(input_iter)
    except StopIteration:
        yield Token(TokenType.EOF, "", line_number)
