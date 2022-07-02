import json
from actions import *
import random


class localGame():
    scores = json.loads(open("scores.json", "r").read())
    board = setupBoard()
    players = ()
    display = display()
    forbiddenNames = [""]
    winner = None
    turn = None
    topTextLabel = None
    continueVar = tkinter.IntVar()
    gameOver = tkinter.IntVar()

    def main(self):
        # clear all class variables
        self.board = setupBoard()
        self.players = ()
        self.display = display()
        self.forbiddenNames = [""]
        self.winner = None
        self.turn = None
        self.topTextLabel = None
        self.continueVar = tkinter.IntVar()
        self.gameOver = tkinter.IntVar()
        
        # clear frame
        clearFrame(display.root)

        # select user names and update into players
        self.selectUserNames()
        print("Selected names")

        # start game
        self.setupGame()
        print("game complete")

        # update scores
        self.updateScores()
        print("scores updated")

        # wait for continueVar to change
        self.display.root.wait_variable(self.continueVar)

        # quit root
        self.display.root.quit()

        # return
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

    # popup to select user. If the name is taken, ask the user if they want to use the existing score with tkinter
    def selectUserPopup(self,player):
        # create popup
        popup = tkinter.Toplevel(display.root)
        popup.title("Select User")
        popup.geometry("300x300")
        popup.resizable(False, False)

        # text to ask if user wants to use existing score
        text = tkinter.StringVar()
        text.set("Enter name for " + player + ":")
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
    
    def selectUser(self, user):
        while True:
            username = self.selectUserPopup(user)
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

        # add name to forbidden names
        self.forbiddenNames.append(username)
        
        return username

    def disableButtons(self):
        # disable all buttons
        for row in range(3):
            for column in range(3):
                self.display.root.grid_slaves(row=row+2, column=column)[0].config(command=lambda: None)

    def boardClick(self, row, column):
        # update board
        if self.turn == self.players[0]:
            self.board[row][column] = "x"
        else:
            self.board[row][column] = "o"

        # prevent user from clicking on a button twice
        if self.turn == self.players[0]:
            text = 'X'
        else:
            text = 'O'
        self.display.root.grid_slaves(row=row+2, column=column)[0].config(text=text, command=lambda: None)

        # change turn
        if self.turn == self.players[0]: # if it is x's turn
            self.turn = self.players[1] # change to o's turn
        else:
            self.turn = self.players[0] # else, change to o's turn

        # update top text and display
        # delete top text
        self.display.root.grid_slaves(row=0, column=0)[0].destroy()
        # create new top text
        self.topTextLabel = tkinter.Label(display.root, text="{}'s turn".format(self.turn), font=("Arial", 20), anchor="center")
        self.topTextLabel.grid(row=0, column=0, columnspan=3)
        self.display.root.update()
        
        # check if game is over
        winner = checkWinner(self.board)
        if winner != 'none':
            if winner == "x": # set winner to the player corresponding to the piece
                self.winner = self.players[0] # set winner to x
            else:
                self.winner = self.players[1] # set winner to o

            # update the top text
            self.display.root.grid_slaves(row=0, column=0)[0].config(text="{} won!".format(self.winner))

            # disable all buttons
            self.disableButtons()

            # add a continue button
            continueButton = tkinter.Button(self.display.root, text="Continue", font=("Arial", 20), command=lambda: self.continueVar.set(1))
            continueButton.grid(row=3, column=10)

            # update gameOver
            self.gameOver.set(1)


            
        else:
            # check if it's a tie
            if checkTie(self.board):
                self.winner = "tie"
                # update the top text
                self.display.root.grid_slaves(row=0, column=0)[0].config(text="Tie!")

                # disable all buttons
                self.disableButtons()

                # add a continue button
                continueButton = tkinter.Button(self.display.root, text="Continue", font=("Arial", 20), command=lambda: self.continueVar.set(1))
                continueButton.grid(row=3, column=10)

                # update gameOver
                self.gameOver.set(1)

    def displayBoard(self):
        # rename frame title to "game"
        display.root.title("game")

        # top text to show whose turn it is or who won
        topText = tkinter.StringVar()
        topText.set("{}'s turn".format(self.turn))
        self.topTextLabel = tkinter.Label(display.root, textvariable=topText, font=("Arial", 20), anchor="center")
        self.topTextLabel.grid(row=0, column=0, columnspan=3)

        # 3x3 grid of buttons
        for row in range(3):
            for column in range(3):
                # create button
                button = tkinter.Button(display.root, text="", command=lambda row=row, column=column: self.boardClick(row, column), font=("Arial", 50), anchor="center", width=3, height=3)
                button.grid(row=row+2, column=column)
        
        # wait for gameOver to update
        self.display.root.wait_variable(self.gameOver)

        return

    # select usernames for the two players. If the name is taken, ask the user if they want to use the existing score with tkinter
    def selectUserNames(self):
        # popup to select players
        print("Select players for x and y")
        self.players = (self.selectUser("X"), self.selectUser("O"))
        print("Players: " + str(self.players))
        return

    def setupGame(self):
        # determine who goes first
        self.turn = self.players[0]

        # display board
        self.displayBoard()

        return

    def updateScores(self): # calls when continue button is pressed
        # update scores
        if self.winner == self.players[0]:
            self.scores["local"][self.players[0]] += 1
        elif self.winner == self.players[1]:
            self.scores["local"][self.players[1]] += 1
        
        # update scores in file
        with open("scores.json", "w") as f:
            json.dump(self.scores, f)
        
        # display scores on the right
        # set scores to the string of text we want to display
        scores = "{}'s score: {}\n{}'s score: {}".format(self.players[0], self.scores["local"][self.players[0]], self.players[1], self.scores["local"][self.players[1]])
        # display scores
        scoresLabel = tkinter.Label(self.display.root, text=scores, font=("Arial", 20))
        scoresLabel.grid(row=3, column=4)