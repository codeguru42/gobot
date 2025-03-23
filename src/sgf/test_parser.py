import pytest

from sgf.parser import (
    parse_prop_value,
    parse_prop_values,
    parse_property,
    Property,
    Node,
    parse_node,
    Sequence, parse_sequence,
)
from sgf.tokenizer import tokens, TokenType, Token


def test_parse_prop_value():
    token_iter = iter(tokens("[B]"))
    prop_value, next_token = parse_prop_value(next(token_iter), token_iter)
    assert prop_value == Token(TokenType.COLOR, "B")
    assert next_token == Token(TokenType.EOF, "")


def test_parse_prop_values():
    token_iter = iter(tokens("[B][W]"))
    prop_values, next_token = parse_prop_values(next(token_iter), token_iter)
    assert prop_values == [Token(TokenType.COLOR, "B"), Token(TokenType.COLOR, "W")]
    assert next_token == Token(TokenType.EOF, "")


def test_parse_property():
    token_iter = iter(tokens("B[dd]"))
    prop, next_token = parse_property(next(token_iter), token_iter)
    assert prop == Property(Token(TokenType.IDENT, "B"), [Token(TokenType.POINT, "dd")])
    assert next_token == Token(TokenType.EOF, "")


@pytest.mark.parametrize(
    "input_string,expected",
    (
        (
            ";B[dd]",
            Node(Property(Token(TokenType.IDENT, "B"), [Token(TokenType.POINT, "dd")])),
        ),
        (
            ";AB[dd][jj]",
            Node(
                Property(
                    Token(TokenType.IDENT, "AB"),
                    [Token(TokenType.POINT, "dd"), Token(TokenType.POINT, "jj")],
                )
            ),
        ),
    ),
)
def test_parse_node(input_string, expected):
    token_iter = iter(tokens(input_string))
    prop, next_token = parse_node(next(token_iter), token_iter)
    assert prop == expected
    assert next_token == Token(TokenType.EOF, "")


def test_parse_sequence():
    token_iter = iter(tokens(";B[dd];W[jj]"))
    expected = Sequence(
        [
            Node(Property(Token(TokenType.IDENT, "B"), [Token(TokenType.POINT, "dd")])),
            Node(Property(Token(TokenType.IDENT, "W"), [Token(TokenType.POINT, "jj")])),
        ]
    )
    node, next_token = parse_sequence(next(token_iter), token_iter)
    assert node == expected
    assert next_token == Token(TokenType.EOF, "")
