from gobot.goboard import GoString
from gobot.gotypes import Player, Point


def test_go_string_merge():
    p1 = Point(4, 4)
    p2 = Point(4, 5)
    string1 = GoString(Player.BLACK, {p1}, p1.neighbors())
    string2 = GoString(Player.BLACK, {p2}, p2.neighbors())
    expected = GoString(
        Player.BLACK, {p1, p2}, (set(p1.neighbors()) | set(p2.neighbors())) - {p1, p2}
    )
    result = string1.merge_with(string2)
    assert result == expected
