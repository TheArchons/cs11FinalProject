import os
import json
import random
import time

# given a 2d array, return the winner only if each square is filled with x or y
def checkWinner(board):
    # check columns
    for i in range(3):
        if board[0][i] in ['x', 'o']:
            if board[0][i] == board[1][i] and board[1][i] == board[2][i]:
                return board[0][i]
    
    # check rows
    for i in range(3):
        if board[i][0] in ['x', 'o']:
            if board[i][0] == board[i][1] and board[i][1] == board[i][2]:
                return board[i][0]
    
    # check diagonals
    if board[0][0] in ['x', 'o']:
        if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
            return board[0][0]
    
    if board[0][2] in ['x', 'o']:
        if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
            return board[0][2]
    
    return "none"

# check if the game is over
def checkTie(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                return False
    return True

def calculating():
    # fake calculating
    # note: I added a bit of delay to make it seem like the computer is thinking
    print("calculating...")
    time.sleep(1)
    return

# setup a tic tac toe board as a 2d array
def setupBoard():
    board = []
    for i in range(3):
        board.append([])
        for j in range(3):
            board[i].append(" ")
    return board

# a local 1v1 game
def localGame():
    print()
    scores = json.loads(open("scores.json", "r").read())

    print("Welcome! Please enter your names: ")
    while True:
        playerX = input("X: ")
        if playerX in scores["local"]:
            useScore = input("name already taken, use existing score? (y/n)")
            if useScore == "y":
                break
            else:
                continue
        else:
            scores["local"][playerX] = 0
            break
    while True:
        playerO = input("O: ")
        if playerO in scores["local"]:
            useScore = input("name already taken, use existing score? (y/n)")
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
            print(board)
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
            print(board)
            while True:
                x = int(input("Please enter a row: "))
                y = int(input("Please enter a column: "))
                if board[x][y] == " ":
                    break
                print("That square is already taken")
            board[x][y] = "o"
            isXTurn = True
    print(board)

    # add scores
    if checkWinner(board) == "x":
        print("X wins!")
        scores["local"][playerX] += 1
    elif checkWinner(board) == "o":
        print("O wins!")
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
    return # return to menu

class computer():
    board = ""
    difficulty = ""
    player = ""
    computer = ""

    def __init__(self):
        # setup the board
        self.board = setupBoard()
        while True:
            self.difficulty = input("Please enter the difficulty (easy/medium/hard): ")
            if self.difficulty in ["easy", "medium", "hard"]:
                break
            else:
                print("Invalid difficulty")
        
        # pick if computer goes first or player goes first
        while True:
            player = input("Please enter if you start x, o, or pick randomly (x/o/random): ")
            if player in ["x", "o", "random"]:
                if player == "random":
                    player = random.choice(['x', 'o'])
                break
            else:
                print("Invalid input, please try again")
        
        # get the player to enter their name
        while True:
            playerName = input("Please enter your name: ")
            scores = json.loads(open("scores.json", "r").read())
            if playerName in scores["local"]:
                useScore = input("name already taken, use existing score? (y/n) ")
                if useScore == "y":
                    break
                else:
                    continue
            else:
                scores["local"][playerName] = 0
                break
        
        # play game

        # set player and computer to x or o
        if player == "x":
            isPlayerTurn = True
            self.computer = "o"
            self.player = "x"
        else:
            isPlayerTurn = False
            self.computer = "x"
            self.player = "o"
        
        while True:
            if isPlayerTurn:
                print()
                print("Your turn")
                print(self.board)
                while True:
                    x = int(input("Please enter a row: "))
                    y = int(input("Please enter a column: "))
                    if self.board[x][y] == " ":
                        break
                    print("That square is already taken")
                self.board[x][y] = player
                isPlayerTurn = False
            else:
                print()
                print("Computer's turn")
                if self.difficulty == "easy":
                    self.computerEasy()
                elif self.difficulty == "medium":
                    self.computerMedium()
                else:
                    self.computerHard()
                print(self.board)
                isPlayerTurn = True
            if checkWinner(self.board) != "none":
                break
            if checkTie(self.board):
                break
        
        # print winner and print scores
        if checkWinner(self.board) == self.player:
            print("You win!")
            scores["local"][playerName] += 1
            print(playerName + ": " + str(scores["local"][playerName]))
        elif checkWinner(self.board) == self.computer:
            print("Computer wins!")
            scores["local"]["computer"] += 1
            print("Computer: " + str(scores["local"]["computer"]))
        else:
            print("Tie!")
        
        # save scores
        open("scores.json", "w").write(json.dumps(scores))

        # press enter to return to menu
        input("Press enter to return to menu")
        print()

        return 

    def computerEasy(self):
        # find all empty spaces
        emptySpaces = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == " ":
                    emptySpaces.append([i, j])
        
        # pick a random empty space
        randomSpace = random.choice(emptySpaces)

        # place the computer's piece in the random space
        self.board[randomSpace[0]][randomSpace[1]] = self.computer

        calculating()

        return


    def computerMedium(self):

        pass
    def computerHard(self):

        pass

# online game
def remoteGame():
    print()
    return

def scoreboard():
    print()
    scores = json.loads(open("scores.json", "r").read())
    print("Local scores:")
    for key in scores["local"]:
        print(key + ": " + str(scores["local"][key]))

    print()

    print("Remote scores:")
    for key in scores["remote"]:
        print(key + ": " + str(scores["remote"][key]))
    
    input("press enter to continue...")
    print()
    

def menu():
    print("welcome to tic tac toe! PLease select an option:")
    print("1. Play against a computer (I'm lonely)")
    print("2. Play against a local player")
    print("3. Play against a remote player")
    print("4. Scoreboard")
    print("5. Quit")
    choice = input("Please enter your choice: ")
    return choice

# create scores.json if it doesn't exist
if not os.path.isfile("scores.json"):
    scores = {}
    scores["local"] = {"computer":0,}
    scores["remote"] = {}
    with open("scores.json", "w") as f:
        json.dump(scores, f)

choice = menu()
while choice != "5":
    if choice == "1":
        computer()
    elif choice == "2":
        localGame()
    elif choice == "3":
        print(checkWinner([["x", "x", " "], [" ", "y", " "], [" ", " ", "x"]]))
    elif choice == "4":
        scoreboard()
    else:
        print("Invalid choice", end="\n\n")
    choice = menu()