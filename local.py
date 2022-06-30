import json
from actions import *

# a local 1v1 game
def localGame():
    print()
    scores = json.loads(open("scores.json", "r").read())

    print("Welcome! Please enter your names: ")
    while True:
        playerX = input("X: ")
        if playerX in scores["local"]:
            useScore = input("name already taken, use existing score? (y/n) ")
            if useScore == "y":
                break
            else:
                continue
        else:
            scores["local"][playerX] = 0
            break
    while True:
        playerO = input("O: ")
        if playerO == playerX:
            print("names must be different")
            continue
        if playerO in scores["local"]:
            useScore = input("name already taken, use existing score? (y/n) ")
            if useScore == "y":
                break
            else:
                continue
        else:
            scores["local"][playerO] = 0
            break

    board = setupBoard()
    isXTurn = True
    while checkWinner(board) == "none" and not checkTie(board):
        if isXTurn:
            print()
            print("X's turn")
            printBoard(board)
            while True:
                x = int(input("Please enter a row: "))
                y = int(input("Please enter a column: "))
                if board[x][y] == " ":
                    break
                print("That square is already taken")
            board[x][y] = "x"
            isXTurn = False
        else:
            print()
            print("O's turn")
            printBoard(board)
            while True:
                x = int(input("Please enter a row: "))
                y = int(input("Please enter a column: "))
                if board[x][y] == " ":
                    break
                print("That square is already taken")
            board[x][y] = "o"
            isXTurn = True
    printBoard(board)

    # add scores
    if checkWinner(board) == "x":
        print("{} wins!".format(playerX))
        scores["local"][playerX] += 1
    elif checkWinner(board) == "o":
        print("{} wins!".format(playerO))
        scores["local"][playerO] += 1
    else:
        print("Tie!")
    print()

    # print scores
    print("Current scores:")
    print(playerX + ": " + str(scores["local"][playerX]))
    print(playerO + ": " + str(scores["local"][playerO]))

    # save scores
    open("scores.json", "w").write(json.dumps(scores))

    # press enter to continue
    input("Press enter to continue...")
    print()

    return # return to menu