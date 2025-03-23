import pytest

from sgf.parser import (
    parse_prop_value,
    parse_prop_values,
    parse_property,
    Property,
    Node,
    parse_node,
    Sequence,
    parse_sequence,
    GameTree,
    parse_game_tree,
    parse_collection,
    Collection,
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
    node, next_token = parse_node(next(token_iter), token_iter)
    assert node == expected
    assert next_token == Token(TokenType.EOF, "")


def test_parse_sequence():
    token_iter = iter(tokens(";B[dd];W[jj]"))
    expected = Sequence(
        [
            Node(Property(Token(TokenType.IDENT, "B"), [Token(TokenType.POINT, "dd")])),
            Node(Property(Token(TokenType.IDENT, "W"), [Token(TokenType.POINT, "jj")])),
        ]
    )
    sequence, next_token = parse_sequence(next(token_iter), token_iter)
    assert sequence == expected
    assert next_token == Token(TokenType.EOF, "")


@pytest.mark.parametrize(
    "input_string,expected",
    (
        (
            "(;B[dd];W[jj])",
            GameTree(
                Sequence(
                    [
                        Node(
                            Property(
                                Token(TokenType.IDENT, "B"),
                                [Token(TokenType.POINT, "dd")],
                            )
                        ),
                        Node(
                            Property(
                                Token(TokenType.IDENT, "W"),
                                [Token(TokenType.POINT, "jj")],
                            )
                        ),
                    ]
                ),
                [],
            ),
        ),
        (
            "(;B[dd](;B[jj]))",
            GameTree(
                Sequence(
                    [
                        Node(
                            Property(
                                Token(TokenType.IDENT, "B"),
                                [Token(TokenType.POINT, "dd")],
                            )
                        ),
                    ]
                ),
                [
                    GameTree(
                        Sequence(
                            [
                                Node(
                                    Property(
                                        Token(TokenType.IDENT, "B"),
                                        [Token(TokenType.POINT, "jj")],
                                    )
                                ),
                            ]
                        ),
                        [],
                    )
                ],
            ),
        ),
    ),
)
def test_parse_game_tree(input_string, expected):
    token_iter = iter(tokens(input_string))
    game_tree, next_token = parse_game_tree(next(token_iter), token_iter)
    assert game_tree == expected
    assert next_token == Token(TokenType.EOF, "")


def test_parse_collection():
    token_iter = iter(tokens("(;B[dd];W[pp])(;B[pd];W[dp])"))
    expected = Collection(
        [
            GameTree(
                Sequence(
                    [
                        Node(
                            Property(
                                Token(TokenType.IDENT, "B"),
                                [Token(TokenType.POINT, "dd")],
                            )
                        ),
                        Node(
                            Property(
                                Token(TokenType.IDENT, "W"),
                                [Token(TokenType.POINT, "pp")],
                            )
                        ),
                    ]
                ),
                [],
            ),
            GameTree(
                Sequence(
                    [
                        Node(
                            Property(
                                Token(TokenType.IDENT, "B"),
                                [Token(TokenType.POINT, "pd")],
                            )
                        ),
                        Node(
                            Property(
                                Token(TokenType.IDENT, "W"),
                                [Token(TokenType.POINT, "dp")],
                            )
                        ),
                    ]
                ),
                [],
            ),
        ]
    )
    collection = parse_collection(next(token_iter), token_iter)
    assert collection == expected
