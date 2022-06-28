from main import getWinningMove

print(getWinningMove([["x", "x", " "],[" ", " ", " "],[" ", " ", " "]], "x"))

def test_getWinningMove():
    board = [[" ", " ", " "],[" ", " ", " "],[" ", " ", " "]]
    assert getWinningMove(board, "x") == [-1, -1]

    board = [["x", "x", " "],[" ", " ", " "],[" ", " ", " "]]
    assert getWinningMove(board, "x") == [0, 2]

    board = [["o", " ", " "],[" ", "o", " "],[" ", " ", " "]]
    assert getWinningMove(board, "o") == [2, 2]

    board = [[" ", " ", " "],["o", " ", " "],["o", " ", " "]]
    assert getWinningMove(board, "o") == [0, 0]