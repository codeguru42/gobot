import pytest

from sgf.tokenizer import Token, TokenType, tokens


@pytest.mark.parametrize(
    "input_string,expected_tokens",
    [
        ("(", (Token(TokenType.L_PAREN, "("), Token(TokenType.EOF, ""))),
        (")", (Token(TokenType.R_PAREN, ")"), Token(TokenType.EOF, ""))),
        ("[", (Token(TokenType.L_BRACKET, "["), Token(TokenType.EOF, ""))),
        ("]", (Token(TokenType.R_BRACKET, "]"), Token(TokenType.EOF, ""))),
        (";", (Token(TokenType.SEMI, ";"), Token(TokenType.EOF, ""))),
        (":", (Token(TokenType.COLON, ":"), Token(TokenType.EOF, ""))),
        ("FOOBAR", (Token(TokenType.IDENT, "FOOBAR"), Token(TokenType.EOF, ""))),
        (
            "( )",
            (
                Token(TokenType.L_PAREN, "("),
                Token(TokenType.R_PAREN, ")"),
                Token(TokenType.EOF, ""),
            ),
        ),
        (
            "[123]",
            (
                Token(TokenType.L_BRACKET, "["),
                Token(TokenType.NUMBER, "123"),
                Token(TokenType.R_BRACKET, "]"),
                Token(TokenType.EOF, ""),
            ),
        ),
        (
            "[+123]",
            (
                Token(TokenType.L_BRACKET, "["),
                Token(TokenType.NUMBER, "+123"),
                Token(TokenType.R_BRACKET, "]"),
                Token(TokenType.EOF, ""),
            ),
        ),
        (
            "[-123]",
            (
                Token(TokenType.L_BRACKET, "["),
                Token(TokenType.NUMBER, "-123"),
                Token(TokenType.R_BRACKET, "]"),
                Token(TokenType.EOF, ""),
            ),
        ),
        (
            "[12.3]",
            (
                Token(TokenType.L_BRACKET, "["),
                Token(TokenType.REAL, "12.3"),
                Token(TokenType.R_BRACKET, "]"),
                Token(TokenType.EOF, ""),
            ),
        ),
        (
            "[ab]",
            (
                Token(TokenType.L_BRACKET, "["),
                Token(TokenType.POINT, "ab"),
                Token(TokenType.R_BRACKET, "]"),
                Token(TokenType.EOF, ""),
            ),
        ),
        (
            "[B]",
            (
                Token(TokenType.L_BRACKET, "["),
                Token(TokenType.COLOR, "B"),
                Token(TokenType.R_BRACKET, "]"),
                Token(TokenType.EOF, ""),
            ),
        ),
        (
            "[W]",
            (
                Token(TokenType.L_BRACKET, "["),
                Token(TokenType.COLOR, "W"),
                Token(TokenType.R_BRACKET, "]"),
                Token(TokenType.EOF, ""),
            ),
        ),
    ],
)
def test_tokenizer(input_string: str, expected_tokens: tuple[Token]):
    assert tuple(tokens(input_string)) == expected_tokens
