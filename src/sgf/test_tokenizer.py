import pytest

from sgf.tokenizer import Token, TokenType, tokens


@pytest.mark.parametrize(
    "input_string,expected_token",
    [
        ("(", Token(TokenType.L_PAREN, "(")),
        (")", Token(TokenType.R_PAREN, ")")),
        ("[", Token(TokenType.L_BRACKET, "[")),
        ("]", Token(TokenType.R_BRACKET, "]")),
        (";", Token(TokenType.SEMI, ";")),
        (":", Token(TokenType.COLON, ":")),
    ],
)
def test_tokenizer(input_string: str, expected_token: Token):
    assert list(tokens(input_string)) == [expected_token]
