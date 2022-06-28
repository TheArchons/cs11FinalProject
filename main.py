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

# return the final piece location to win given the board and piece
def getWinningMove(board, piece):
    # check columns
    for i in range(3):
        # check if the column is occupied by another piece
        emptySpot = -1
        noMove = False
        for j in range(3):
            if board[i][j] == " ":
                if emptySpot != -1: # if there is an empty spot, break
                    noMove = True
                    break  # 2 empty spaces in the same row, no possible winning move
                emptySpot = j
            elif board[i][j] != piece:
                noMove = True
                break # occupied, no possible winning move
        if not noMove:
            return [i, emptySpot]
        
    # check rows
    for i in range(3):
        # check if the row is occupied by another piece
        emptySpot = -1
        noMove = False
        for j in range(3):
            if board[j][i] == " ":
                if emptySpot != -1:
                    noMove = True
                    break
                emptySpot = j
            elif board[j][i] != piece:
                noMove = True
                break
        
        if not noMove:
            return [emptySpot, i]

    # check diagonals
    emptySpot = -1
    noMove = False
    for i in range(3):
        if board[i][i] == " ":
            if emptySpot != -1:
                noMove = True
                break
            emptySpot = i
        elif board[i][i] != piece:
            noMove = True
            break
    if not noMove:
        return [emptySpot, emptySpot]
    
    emptySpot = -1
    noMove = False
    for i in range(3):
        if board[i][2-i] == " ":
            if emptySpot != -1:
                noMove = True
                break
            emptySpot = i
        elif board[i][2-i] != piece:
            noMove = True
            break
    if not noMove:
        return [emptySpot, 2-emptySpot]
    
    return [-1, -1] # no winning moves in the board

# try adjacents
def tryAdjacents(board, location):
    tries = {
        "up": [location[0]-1, location[1]],
        "down": [location[0]+1, location[1]],
        "left": [location[0], location[1]-1],
        "right": [location[0], location[1]+1],
        "upleft": [location[0]-1, location[1]-1],
        "upright": [location[0]-1, location[1]+1],
        "downleft": [location[0]+1, location[1]-1],
        "downright": [location[0]+1, location[1]+1]
    }
    adjacents = set()

    for key in tries:
        # skip if keys are below 0 or above 2
        if tries[key][0] < 0 or tries[key][0] > 2:
            continue
        if tries[key][1] < 0 or tries[key][1] > 2:
            continue
        # skip if the location is already occupied
        if board[tries[key][0]][tries[key][1]] != " ":
            continue
        adjacents.add(tuple(tries[key]))

    if len(adjacents) == 0:
        return None
    else:
        return adjacents

# find adjacents to a given piece in the board
def findAdjacents(board, piece):
    adjacents = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == piece:
                tempAdjacents = tryAdjacents(board, [i, j])
                if tempAdjacents != None:
                    # combine the adjacents with the existing set
                    adjacents = adjacents.union(tempAdjacents)
    return adjacents


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

    def placeRandom(self):
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

    def placeAdjacent(self, piece):
        adjacents = findAdjacents(self.board, piece)

        if (1, 1) in adjacents: # if the middle is open, place there
            self.board[1][1] = self.computer
            calculating()
            return True

        for i in [(0, 0), (0, 2), (2, 0), (2, 2)]: # if it is in the corners, place there
            if i in adjacents:
                self.board[i[0]][i[1]] = self.computer
                calculating()
                return True
        
        for i in [(0, 1), (1, 0), (1, 2), (2, 1)]: # if it is in the sides, place there
            if i in adjacents:
                self.board[i[0]][i[1]] = self.computer
                calculating()
                return True
        
        return False

    def empties(self):
        # check if the center is empty
        if self.board[1][1] == " ":
            self.board[1][1] = self.computer
            calculating()
            return
        
        # check if the corners are empty
        corners = [
            [0, 0],
            [0, 2],
            [2, 0],
            [2, 2]
        ]

        for key in corners:
            if self.board[key[0]][key[1]] == " ":
                self.board[key[0]][key[1]] = self.computer
                calculating()
                return
        
        # check if the sides are empty
        sides = [
            [0, 1],
            [1, 0],
            [1, 2],
            [2, 1]
        ]

        for key in sides:
            if self.board[key[0]][key[1]] == " ":
                self.board[key[0]][key[1]] = self.computer
                calculating()
                return

    def winningMove(self, piece):
        winningMove = getWinningMove(self.board, piece)
        if winningMove != [-1, -1]:
            self.board[winningMove[0]][winningMove[1]] = self.computer
            calculating()
            return True
        
        return False

    def computerEasy(self):
        # this ai will just pick a random spot
        # note: should be relatively easy to win, as long as you don't get unlucky
        self.placeRandom()

    def computerMedium(self):
        # this ai will win, block the player's win, or place a random piece
        # note: to beat this ai, the player must fork
        if self.winningMove(self.computer):
            return

        if self.winningMove(self.player):
            return

        # if there is no winning move, place a random piece
        self.placeRandom()
        
    def computerHard(self):
        # this ai will check in the following order:

        # 1. check if the computer can win, if so, win

        # 2. check if the player can win, if so, block

        # 3. check if the computer can place adjacent to one of the computer's pieces, if so, place there in the following order
        #   a. if the corners are open, place there
        #   b. if the sides are open, place there
        #   note: we do not need to check the center, because the computer's first piece will be in the center unless taken by the player

        # 4. check if the computer can place adjacent to one of the player's pieces, if so, place there in the following order
        #   a. if the middle is open, place there
        #   b. if the corners are open, place there
        #   c. if the sides are open, place there

        # 5. check if the center is empty, if so, take it

        # 6. check if the corners are empty, if so, take one of them

        # 7. check if the sides are empty, if so, take one of them

        # note: I believe the ai will never lose

        # check if the computer can win
        if self.winningMove(self.computer):
            return
        
        # check if the player can win
        if self.winningMove(self.player):
            return
        
        # check if the computer can place adjacent to one of the computer's pieces
        if self.placeAdjacent(self.computer) == True:
            return
        
        # check if the computer can place adjacent to one of the player's pieces
        if self.placeAdjacent(self.player) == True:
            return
        
        # check for empty locations
        self.empties()

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

def main():
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

main()