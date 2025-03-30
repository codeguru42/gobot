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
    assert prop_value == Token(TokenType.COLOR, "B", line_number=1)
    assert next_token == Token(TokenType.EOF, "", line_number=1)


def test_parse_prop_values():
    token_iter = iter(tokens("[B][W]"))
    prop_values, next_token = parse_prop_values(next(token_iter), token_iter)
    assert prop_values == [Token(TokenType.COLOR, "B", line_number=1), Token(TokenType.COLOR, "W", line_number=1)]
    assert next_token == Token(TokenType.EOF, "", line_number=1)


def test_parse_property():
    token_iter = iter(tokens("B[dd]"))
    prop, next_token = parse_property(next(token_iter), token_iter)
    assert prop == Property(Token(TokenType.IDENT, "B", line_number=1), [Token(TokenType.POINT, "dd", line_number=1)])
    assert next_token == Token(TokenType.EOF, "", line_number=1)


@pytest.mark.parametrize(
    "input_string,expected",
    (
        (
            ";B[dd]",
            Node(Property(Token(TokenType.IDENT, "B", line_number=1), [Token(TokenType.POINT, "dd", line_number=1)])),
        ),
        (
            ";AB[dd][jj]",
            Node(
                Property(
                    Token(TokenType.IDENT, "AB", line_number=1),
                    [Token(TokenType.POINT, "dd", line_number=1), Token(TokenType.POINT, "jj", line_number=1)],
                )
            ),
        ),
        (
            ";GM[1]FF[4]",
            Node(
                [
                    Property(
                        Token(TokenType.IDENT, "GM", line_number=1),
                        [Token(TokenType.NUMBER, "1", line_number=1)],
                    ),
                    Property(
                        Token(TokenType.IDENT, "FF", line_number=1),
                        [Token(TokenType.NUMBER, "4", line_number=1)],
                    ),
                ],
            ),
        ),
    ),
)
def test_parse_node(input_string, expected):
    token_iter = iter(tokens(input_string))
    node, next_token = parse_node(next(token_iter), token_iter)
    assert node == expected
    assert next_token == Token(TokenType.EOF, "", line_number=1)


def test_parse_sequence():
    token_iter = iter(tokens(";B[dd];W[jj]"))
    expected = Sequence(
        [
            Node(Property(Token(TokenType.IDENT, "B", line_number=1), [Token(TokenType.POINT, "dd", line_number=1)])),
            Node(Property(Token(TokenType.IDENT, "W", line_number=1), [Token(TokenType.POINT, "jj", line_number=1)])),
        ]
    )
    sequence, next_token = parse_sequence(next(token_iter), token_iter)
    assert sequence == expected
    assert next_token == Token(TokenType.EOF, "", line_number=1)


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
                                Token(TokenType.IDENT, "B", line_number=1),
                                [Token(TokenType.POINT, "dd", line_number=1)],
                            )
                        ),
                        Node(
                            Property(
                                Token(TokenType.IDENT, "W", line_number=1),
                                [Token(TokenType.POINT, "jj", line_number=1)],
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
                                Token(TokenType.IDENT, "B", line_number=1),
                                [Token(TokenType.POINT, "dd", line_number=1)],
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
                                        Token(TokenType.IDENT, "B", line_number=1),
                                        [Token(TokenType.POINT, "jj", line_number=1)],
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
    assert next_token == Token(TokenType.EOF, "", line_number=1)


def test_parse_collection():
    token_iter = iter(tokens("(;B[dd];W[pp])(;B[pd];W[dp])"))
    expected = Collection(
        [
            GameTree(
                Sequence(
                    [
                        Node(
                            Property(
                                Token(TokenType.IDENT, "B", line_number=1),
                                [Token(TokenType.POINT, "dd", line_number=1)],
                            )
                        ),
                        Node(
                            Property(
                                Token(TokenType.IDENT, "W", line_number=1),
                                [Token(TokenType.POINT, "pp", line_number=1)],
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
                                Token(TokenType.IDENT, "B", line_number=1),
                                [Token(TokenType.POINT, "pd", line_number=1)],
                            )
                        ),
                        Node(
                            Property(
                                Token(TokenType.IDENT, "W", line_number=1),
                                [Token(TokenType.POINT, "dp", line_number=1)],
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
