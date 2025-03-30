from dataclasses import dataclass
from typing import Iterable, Iterator

from sgf.tokenizer import Token, TokenType


@dataclass
class Property:
    ident: Token
    values: list[Token]


@dataclass
class Node:
    property: Property


@dataclass
class Sequence:
    nodes: list[Node]


@dataclass
class GameTree:
    mainline: Sequence
    variations: list["GameTree"]


@dataclass
class Collection:
    games: list[GameTree]


class UnexpectedTokenException(Exception):
    def __init__(self, token: Token):
        self.token = token

    def __str__(self):
        return f"Unexpected token '{self.token.token}' at line {self.token.line_number}"


def parse_prop_value(token: Token, token_iter: Iterator[Token]) -> tuple[Token, Token]:
    next_token = token
    if next_token.type == TokenType.L_BRACKET:
        value = next(token_iter)
        next_token = next(token_iter)
        if next_token.type == TokenType.R_BRACKET:
            return value, next(token_iter)
    raise UnexpectedTokenException(next_token)


def parse_prop_values(
    token: Token, token_iter: Iterator[Token]
) -> tuple[list[Token], Token]:
    values = []
    next_token = token
    while next_token.type == TokenType.L_BRACKET:
        value, next_token = parse_prop_value(next_token, token_iter)
        values.append(value)
    return values, next_token


def parse_property(token: Token, token_iter: Iterator[Token]) -> tuple[Property, Token]:
    if token.type == TokenType.IDENT:
        ident = token
        values, next_token = parse_prop_values(next(token_iter), token_iter)
        return Property(ident, values), next_token
    raise UnexpectedTokenException(token)


def parse_node(token: Token, token_iter: Iterator[Token]) -> tuple[Node, Token]:
    if token.type == TokenType.SEMI:
        prop, next_token = parse_property(next(token_iter), token_iter)
        return Node(prop), next_token
    raise UnexpectedTokenException(token)


def parse_sequence(token: Token, token_iter: Iterator[Token]) -> tuple[Sequence, Token]:
    nodes = []
    next_token = token
    while next_token.type == TokenType.SEMI:
        node, next_token = parse_node(token, token_iter)
        nodes.append(node)
    return Sequence(nodes), next_token


def parse_game_trees(token: Token, token_iter: Iterator[Token]) -> tuple[list[GameTree], Token]:
    game_trees = []
    next_token = token
    while next_token.type == TokenType.L_PAREN:
        game_tree, next_token = parse_game_tree(token, token_iter)
        game_trees.append(game_tree)
    return game_trees, next_token


def parse_game_tree(
    token: Token, token_iter: Iterator[Token]
) -> tuple[GameTree, Token]:
    if token.type == TokenType.L_PAREN:
        seq, next_token = parse_sequence(next(token_iter), token_iter)
        game_trees, next_token = parse_game_trees(next_token, token_iter)
        if next_token.type == TokenType.R_PAREN:
            return GameTree(seq, game_trees), next(token_iter)
    raise UnexpectedTokenException(token)


def parse_collection(token: Token, token_iter: Iterator[Token]) -> Collection:
    games = []
    next_token = token
    while next_token.type != TokenType.EOF:
        game, next_token = parse_game_tree(next_token, token_iter)
        games.append(game)
    return Collection(games)


def parse_sgf(tokens: Iterable[Token]) -> Collection:
    token_iter = iter(tokens)
    token = next(token_iter)
    return parse_collection(token, token_iter)
