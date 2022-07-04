from actions import *
import random
import json

class computer():
    board = ""
    difficulty = ""
    player = ""
    computer = ""
    continueVar = tkinter.IntVar()
    display = display()
    forbiddenNames = ["", "computer"]
    scores = json.loads(open("scores.json", "r").read())
    username = ""
    playerTurn = False
    gameOver = tkinter.IntVar()
    topText = None
    winner = None

    def __init__(self):
        # clear frame
        clearFrame(display.root)

        # setup the board
        self.board = setupBoard()

        # get the difficulty
        self.difficultyPopup()

        # ask the player to choose a piece
        self.pieceChoicePopup()

        # get the player to enter their name
        self.selectName()

        # play the game
        self.game()

        # continue screen
        self.continueScreen()

        # wait for continueVar
        self.display.root.wait_variable(self.continueVar)

        # quit root
        self.display.root.quit()

        return

        """while True:
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

        return"""

    def updateScores(self): # calls when continue button is pressed
        # update scores
        if self.winner == "computer":
            self.scores["local"]["computer"] += 1
        else:
            self.scores["local"][self.username] += 1
        
        # update scores in file
        with open("scores.json", "w") as f:
            json.dump(self.scores, f)
        
        # display scores on the right
        # set scores to the string of text we want to display
        scores = "{}'s score: {}\n{}'s score: {}".format(self.username, self.scores["local"][self.username], "Computer", self.scores["local"]["computer"])

        # display scores
        scoresLabel = tkinter.Label(self.display.root, text=scores, font=("Arial", 20))
        scoresLabel.grid(row=3, column=4)

    def continueScreen(self):
        # update top text to show winner
        if self.winner == "player":
            self.topText.set("You win!")
        elif self.winner == "computer":
            self.topText.set("Computer wins!")
        elif self.winner == "tie":
            self.topText.set("Tie!")
        
        # disable buttons (all buttons should already be disabled, but just in case)
        self.disableButtons()

        # update scores
        self.updateScores()

        # add a continue button
        continueButton = tkinter.Button(self.display.root, text="Continue", command=lambda: self.continueVar.set(1), font=("Arial", 20))
        continueButton.grid(row=3, column=5)
        return

    def disableButtons(self):
        for i in range(3):
            for j in range(3):
                display.root.grid_slaves(row=i+2, column=j)[0].config(state="disabled")
        return

    # enable empty buttons
    def enableButtons(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == " ":
                    display.root.grid_slaves(row=i+2, column=j)[0].config(state="normal")
        return

    def winCheck(self):
        winner = checkWinner(self.board)
        if winner != 'none': # if there is a winner
            if winner == self.computer:
                self.winner = "computer"
            else:
                self.winner = "player"
            self.gameOver.set(1)
            return True

        elif checkTie(self.board): # if there is a tie
            self.winner = "tie"
            self.gameOver.set(1)
            return True

        return False # no tie or winner

    def disableButton(self, row, column):
        display.root.grid_slaves(row=row)[column].config(state="disabled")
        return

    def boardClick(self, row, column):
        # disable button at row, column
        self.disableButton(row+2, column)

        # update board
        self.board[row][column] = self.player

        # update text of the button
        display.root.grid_slaves(row=row+2, column=column)[0].config(text=self.player)
        
        # check if player won. If not, call computer turn
        if not self.winCheck():
            self.computerTurn()

    def computerTurn(self):
        # disable all buttons
        self.disableButtons()

        # set top text to "Calculating..."
        self.topText.set("Calculating...")
        # show
        self.display.root.update()
        # wait for 1 second
        time.sleep(1)

        # get computer move
        row, col = 0, 0
        if self.difficulty == "easy":
            row, col = self.computerEasy()
        elif self.difficulty == "medium":
            row, col = self.computerMedium()
        else:
            row, col = self.computerHard()
        
        # update board text at row, col
        boardText = tkinter.StringVar()
        if self.computer == "x":
            boardText.set("X")
        else:
            boardText.set("O")
        
        self.display.root.grid_slaves(row=row+2, column=col)[0].config(textvariable=boardText)

        # set top text to "Your turn"
        self.topText.set("Your turn")

        # if not game over, enable buttons
        if not self.winCheck():
            self.enableButtons()

        return

    def displayBoard(self):
        # rename frame title to game
        display.root.title("Game")

        # top text to show whose turn it is or who won
        self.topText = tkinter.StringVar()
        self.topText.set("Your turn")
        self.topTextLabel = tkinter.Label(display.root, textvariable=self.topText, font=("Arial", 20), anchor="center")
        self.topTextLabel.grid(row=0, column=0, columnspan=3)

        # 3x3 grid of buttons
        for row in range(3):
            for column in range(3):
                # create button
                button = tkinter.Button(display.root, text="", command=lambda row=row, column=column: self.boardClick(row, column), font=("Arial", 50), anchor="center", width=3, height=3)
                button.grid(row=row+2, column=column)
        
        if not self.playerTurn: # if it's the computer's turn, call computerTurn() first
            self.computerTurn()

        # wait for gameOver to update
        self.display.root.wait_variable(self.gameOver)

        return

    def game(self):
        print("game")

        # display board
        self.displayBoard()

        # continueScreen
        self.continueScreen()
        return

    # forbidden name popup
    def forbiddenPopup(self):
        # create popup
        popup = tkinter.Toplevel(display.root)
        popup.title("ERROR: Forbidden Name")
        popup.geometry("300x300")
        popup.resizable(False, False)
        
        # text saying name is taken or forbidden
        text = tkinter.StringVar()
        text.set("ERROR: Name is taken or forbidden. \n Please try a different name.")
        textLabel = tkinter.Label(popup, textvariable=text)
        textLabel.pack()

        # continue button
        continueButton = tkinter.Button(popup, text="Continue", command=lambda: popup.destroy())
        continueButton.pack()

        # wait for user to click continue button
        popup.wait_window(continueButton)

        return

    # yes/no popup to use existing score
    def useExistingScorePopup(self):
        # create popup
        popup = tkinter.Toplevel(display.root)
        popup.title("Use Existing Score")
        popup.geometry("300x300")
        popup.resizable(False, False)

        # text to ask if user wants to use existing score
        text = tkinter.StringVar()
        text.set("Name already taken, use existing score?")
        textLabel = tkinter.Label(popup, textvariable=text)
        textLabel.pack()

        # yes button and no button
        yesNoVar = tkinter.IntVar() # 0 for yes, 1 for no
        yesButton = tkinter.Button(popup, text="Yes", command=lambda: yesNoVar.set(0))
        yesButton.pack()
        noButton = tkinter.Button(popup, text="No", command=lambda: yesNoVar.set(1))
        noButton.pack()

        # wait for user to click either button
        popup.wait_variable(yesNoVar)
        popup.destroy()

        # close popup when either button is clicked
        if yesNoVar.get() == 0:
            return True
        else:
            return False

    def selectUserPopup(self):
        # create popup
        popup = tkinter.Toplevel(display.root)
        popup.title("Select User")
        popup.geometry("300x300")
        popup.resizable(False, False)

        # text to ask if user wants to use existing score
        text = tkinter.StringVar()
        text.set("Enter your username")
        textLabel = tkinter.Label(popup, textvariable=text)
        textLabel.pack()

        # entry box to enter name
        name = tkinter.StringVar()
        nameEntry = tkinter.Entry(popup, textvariable=name)
        nameEntry.pack()

        # submit button with wait
        submitVar = tkinter.IntVar()
        submitButton = tkinter.Button(popup, text="Submit", command=lambda: submitVar.set(1))
        submitButton.pack()
        
        submitButton.wait_variable(submitVar)

        # close popup when submit button is clicked
        popup.destroy()
        return name.get()

    def selectName(self):
        print("select name")
        while True:
            username = self.selectUserPopup()
            if username in self.forbiddenNames:
                self.forbiddenPopup() # popup if name is taken
                continue
            if username in self.scores["local"]:
                useExisting = self.useExistingScorePopup() # popup if name in scores
                if useExisting:
                    break
            else:
                # add name to scores if it does not exist
                self.scores["local"][username] = 0
                with open("scores.json", "w") as f:
                    json.dump(self.scores, f)
                break
        # set self.username
        self.username = username

    # create a popup to ask the user to pick a piece and set the computer's piece
    def pieceChoicePopup(self):
        # create popup
        popup = tkinter.Toplevel(display.root)
        popup.title("Select piece")
        popup.geometry("300x300")

        # create text that says "Select piece"
        text = tkinter.Label(popup, text="Select piece", font=("Arial", 20))
        text.pack()

        # create buttons for x, o, and random and set the result to piece
        piece = tkinter.StringVar()
        x = tkinter.Button(popup, text="X", command=lambda: piece.set("x"))
        o = tkinter.Button(popup, text="O", command=lambda: piece.set("o"))
        randomPiece = tkinter.Button(popup, text="Random", command=lambda: piece.set("random"))
        x.pack()
        o.pack()
        randomPiece.pack()

        # wait for piece to be set
        self.display.root.wait_variable(piece)

        # set the computer's piece
        if piece.get() == "x":
            self.computer = "o"
        elif piece.get() == "o":
            self.computer = "x"
        else:
            self.computer = random.choice(['x', 'o'])
            if self.computer == "x":
                piece.set("o")
            else:
                piece.set("x")

        self.player = piece.get()
        
        # update playerTurn
        if self.player == "x":
            self.playerTurn = True
        else:
            self.playerTurn = False

        # close popup
        popup.destroy()

    def setdiff(self, difficulty):
        self.difficulty = difficulty
        self.continueVar.set(1)
        return

    # ask the user to pick easy, medium, or hard with tkinter
    def difficultyPopup(self):
        #create popup
        popup = tkinter.Toplevel(display.root)
        popup.title("Select difficulty")
        popup.geometry("300x300")

        # add text that says "Select difficulty"
        text = tkinter.Label(popup, text="Select difficulty", font=("Arial", 20))
        text.pack()
        easy = tkinter.Button(popup, text="Easy", command=lambda: self.setdiff("easy"))
        medium = tkinter.Button(popup, text="Medium", command=lambda: self.setdiff("medium"))
        hard = tkinter.Button(popup, text="Hard", command=lambda: self.setdiff("hard"))
        # add buttons for easy, medium, and hard
        easy.pack()
        medium.pack()
        hard.pack()

        # wait for continueVar
        self.display.root.wait_variable(self.continueVar)

        # reset continueVar
        self.continueVar.set(0)

        # close popup
        popup.destroy()

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

        return [randomSpace[0], randomSpace[1]]

    def placeAdjacent(self, piece):
        adjacents = findAdjacents(self.board, piece)

        if (1, 1) in adjacents: # if the middle is open, place there
            self.board[1][1] = self.computer
            calculating()
            return True, [i[0], i[1]]

        for i in [(0, 0), (0, 2), (2, 0), (2, 2)]: # if it is in the corners, place there
            if i in adjacents:
                self.board[i[0]][i[1]] = self.computer
                calculating()
                return True, [i[0], i[1]]
        
        for i in [(0, 1), (1, 0), (1, 2), (2, 1)]: # if it is in the sides, place there
            if i in adjacents:
                self.board[i[0]][i[1]] = self.computer
                calculating()
                return True, [i[0], i[1]]
        
        return False, []

    def empties(self):
        # check if the center is empty
        if self.board[1][1] == " ":
            self.board[1][1] = self.computer
            calculating()
            return [1, 1]
        
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
                return [key[0], key[1]]
        
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
                return [key[0], key[1]]

    def winningMove(self, piece):
        winningMove = getWinningMove(self.board, piece)
        if winningMove != [-1, -1]:
            self.board[winningMove[0]][winningMove[1]] = self.computer
            calculating()
            return True, winningMove
        
        return False, []

    def computerEasy(self):
        # this ai will just pick a random spot
        # note: should be relatively easy to win, as long as you don't get unlucky
        return self.placeRandom()

    def computerMedium(self):
        # this ai will win, block the player's win, or place a random piece
        # note: to beat this ai, the player must fork
        winning = self.winningMove(self.computer)
        if winning[0]:
            return winning[1]

        winning = self.winningMove(self.player)
        if winning[0]:
            return winning[1]

        # if there is no winning move, place a random piece
        return self.placeRandom()
        
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
        winning = self.winningMove(self.computer)
        if winning[0]:
            return winning[1]
        
        # check if the player can win
        winning = self.winningMove(self.player)
        if winning[0]:
            return winning[1]
        
        # check if the computer can place adjacent to one of the computer's pieces
        adjacent = self.placeAdjacent(self.computer)
        if adjacent[0]:
            return adjacent[1]
        
        # check if the computer can place adjacent to one of the player's pieces
        adjacent = self.placeAdjacent(self.player)
        if adjacent[0]:
            return adjacent[1]
        
        # check for empty locations
        return self.empties()