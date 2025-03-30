import pytest

from sgf.tokenizer import Token, TokenType, tokens


@pytest.mark.parametrize(
    "input_string,expected_tokens",
    [
        (
            "(",
            (
                Token(TokenType.L_PAREN, "(", line_number=1),
                Token(TokenType.EOF, "", line_number=1),
            ),
        ),
        (
            ")",
            (
                Token(TokenType.R_PAREN, ")", line_number=1),
                Token(TokenType.EOF, "", line_number=1),
            ),
        ),
        (
            "[",
            (
                Token(TokenType.L_BRACKET, "[", line_number=1),
                Token(TokenType.EOF, "", line_number=1),
            ),
        ),
        (
            "]",
            (
                Token(TokenType.R_BRACKET, "]", line_number=1),
                Token(TokenType.EOF, "", line_number=1),
            ),
        ),
        (
            ";",
            (
                Token(TokenType.SEMI, ";", line_number=1),
                Token(TokenType.EOF, "", line_number=1),
            ),
        ),
        (
            ":",
            (
                Token(TokenType.COLON, ":", line_number=1),
                Token(TokenType.EOF, "", line_number=1),
            ),
        ),
        (
            "FOOBAR",
            (
                Token(TokenType.IDENT, "FOOBAR", line_number=1),
                Token(TokenType.EOF, "", line_number=1),
            ),
        ),
        (
            "( )",
            (
                Token(TokenType.L_PAREN, "(", line_number=1),
                Token(TokenType.R_PAREN, ")", line_number=1),
                Token(TokenType.EOF, "", line_number=1),
            ),
        ),
        (
            "[123]",
            (
                Token(TokenType.L_BRACKET, "[", line_number=1),
                Token(TokenType.NUMBER, "123", line_number=1),
                Token(TokenType.R_BRACKET, "]", line_number=1),
                Token(TokenType.EOF, "", line_number=1),
            ),
        ),
        (
            "[+123]",
            (
                Token(TokenType.L_BRACKET, "[", line_number=1),
                Token(TokenType.NUMBER, "+123", line_number=1),
                Token(TokenType.R_BRACKET, "]", line_number=1),
                Token(TokenType.EOF, "", line_number=1),
            ),
        ),
        (
            "[-123]",
            (
                Token(TokenType.L_BRACKET, "[", line_number=1),
                Token(TokenType.NUMBER, "-123", line_number=1),
                Token(TokenType.R_BRACKET, "]", line_number=1),
                Token(TokenType.EOF, "", line_number=1),
            ),
        ),
        (
            "[12.3]",
            (
                Token(TokenType.L_BRACKET, "[", line_number=1),
                Token(TokenType.REAL, "12.3", line_number=1),
                Token(TokenType.R_BRACKET, "]", line_number=1),
                Token(TokenType.EOF, "", line_number=1),
            ),
        ),
        (
            "[ab]",
            (
                Token(TokenType.L_BRACKET, "[", line_number=1),
                Token(TokenType.POINT, "ab", line_number=1),
                Token(TokenType.R_BRACKET, "]", line_number=1),
                Token(TokenType.EOF, "", line_number=1),
            ),
        ),
        (
            "[B]",
            (
                Token(TokenType.L_BRACKET, "[", line_number=1),
                Token(TokenType.COLOR, "B", line_number=1),
                Token(TokenType.R_BRACKET, "]", line_number=1),
                Token(TokenType.EOF, "", line_number=1),
            ),
        ),
        (
            "[W]",
            (
                Token(TokenType.L_BRACKET, "[", line_number=1),
                Token(TokenType.COLOR, "W", line_number=1),
                Token(TokenType.R_BRACKET, "]", line_number=1),
                Token(TokenType.EOF, "", line_number=1),
            ),
        ),
    ],
)
def test_tokenizer(input_string: str, expected_tokens: tuple[Token]):
    assert tuple(tokens(input_string)) == expected_tokens
