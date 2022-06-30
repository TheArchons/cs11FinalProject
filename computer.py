from actions import *
import random
import json

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
                printBoard(self.board)
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
        
        printBoard(self.board)
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