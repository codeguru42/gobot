from sgf.parser import parse_prop_value
from sgf.tokenizer import tokens, TokenType, Token


def test_parse_prop_value():
    token_iter = iter(tokens("[B]"))
    prop_value, next_token = parse_prop_value(next(token_iter), token_iter)
    assert prop_value == Token(TokenType.COLOR, "B")
    assert next_token == Token(TokenType.EOF, "")
