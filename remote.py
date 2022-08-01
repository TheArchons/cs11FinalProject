import requests
import json
from actions import *
import threading
# import asyncio

# get server ip from serverIP.txt
with open("serverIP.txt", "r") as f:
    serverIP = f.read()

class remoteGame():
    playerList = json.loads(requests.get(serverIP + "players").text)
    AmHost = False
    hostName = ""
    username = ""
    opponentName = ""
    opponentPiece = ""
    yourPiece = ""
    game = None
    continueVar = tkinter.IntVar()
    display = display()
    forbiddenNames = [""]
    opponentAction = tkinter.IntVar()
    topText = tkinter.StringVar()
    gameOver = tkinter.IntVar()

    def main(self):
        # reset variables
        self.resetVars()

        # clear frame
        clearFrame(display.root)

        # get player name
        self.getPlayerName()

        # join or start
        self.joinOrStart()

        if self.AmHost == True:
            # host game
            shouldQuit = self.hostGame()
            if shouldQuit == -1:
                display.root.quit()
                return
        else:
            # join game
            self.joinGame()
        
        # game
        self.gameFunc()

        # update scores
        self.updateScores()

        # wait for continue button
        display.root.wait_variable(self.continueVar)

        # return to menu
        display.root.quit()

        return

    def updateScores(self):
        self.game = json.loads(requests.get(serverIP + "games/" + self.hostName).text) # update game
        # disable all buttons
        self.disableAllButtons()

        # update top text to winner
        if self.game["winner"] == None:
            self.topText.set("Tie!")
        elif self.game["winner"] == self.username:
            self.topText.set("You won!")
        else:
            self.topText.set("You lost!")
        
        # show scores
        scoreBoard = requests.get(serverIP + "scores").text
        scoreBoard = json.loads(scoreBoard)
        scores = "Your score: " + str(scoreBoard[self.username]) + "\n" + self.opponentName + "'s score: " + str(scoreBoard[self.opponentName])
        scoresLabel = tkinter.Label(self.display.root, text=scores, font=("Arial", 20))
        scoresLabel.grid(row=3, column=4)

        # show continue button
        continueButton = tkinter.Button(self.display.root, text="Continue", font=("Arial", 30), command=lambda: self.continueVar.set(1))
        continueButton.grid(row=3, column=5)

        # send delete request to server
        requests.post(serverIP + "confirmDelete/" + self.hostName)

        return

    def disableButton(self, row, column):
        display.root.grid_slaves(row=row)[column].config(state="disabled")
        return
    
    def disableAllButtons(self):
        for i in range(3):
            for j in range(3):
                display.root.grid_slaves(row=i+2, column=j)[0].config(state="disabled")
        return
    
    # enable empty buttons
    def enableButtons(self):
        for i in range(3):
            for j in range(3):
                if self.game["board"][i][j] == " ":
                    display.root.grid_slaves(row=i+2, column=j)[0].config(state="normal")
        return

    # update the board text
    def updateBoard(self):
        for i in range(3):
            for j in range(3):
                display.root.grid_slaves(row=i+2, column=j)[0].config(text=self.game["board"][i][j])

    def opponentTurn(self):
        # disable all buttons
        self.disableAllButtons()

        # update top text to "Waiting for opponent..."
        self.topText.set("Waiting for opponent...")
        # show
        self.display.root.update()

        # wait for opponent to make a move
        while True:
            # get current game
            self.game = json.loads(requests.get(serverIP + "games/" + self.hostName).text)

            # if the game is over, return
            if self.game["isOver"] == True:
                self.updateBoard()
                self.display.root.update()
                self.gameOver.set(1)
                return

            # if it is your turn, update the board, enable all buttons and update top text to "Your Turn"
            if self.game["isXTurn"]:
                if self.yourPiece == "x":
                    self.updateBoard()
                    self.enableButtons()
                    self.topText.set("Your Turn")
                    self.display.root.update()
                    break
            else:
                if self.yourPiece == "o":
                    self.updateBoard()
                    self.enableButtons()
                    self.topText.set("Your Turn")
                    self.display.root.update()
                    break

            # wait for 0.5 seconds
            time.sleep(0.5)

    # when you click a button
    def boardClick(self, row, column):
        # send a post request to the server
        requests.post(serverIP + "move/" + self.hostName, data={"column": column, "row": row})

        # get current game
        self.game = json.loads(requests.get(serverIP + "games/" + self.hostName).text)

        # if the game is over, return
        if self.game["isOver"] == True:
            self.updateBoard()
            self.display.root.update()
            self.gameOver.set(1)
            return

        self.updateBoard()

        # call opponentTurn
        self.opponentTurn()

    def displayBoard(self):
        # clear frame
        clearFrame(display.root)

        # rename frame title to game
        display.root.title("Game")

        # get current game
        self.game = json.loads(requests.get(serverIP + "games/" + self.hostName).text)

        # set top text to "Your Turn"
        self.topText.set("Your Turn")
        # note: opponentTurn will update the top text if it is not your turn

        # add top text
        topTextLabel = tkinter.Label(display.root, textvariable=self.topText)
        topTextLabel.grid(row=0, column=0, columnspan=3)

        # add a 3x3 grid of buttons
        for row in range(3):
            for column in range(3):
                # create button
                button = tkinter.Button(display.root, text="", command=lambda row=row, column=column: self.boardClick(row, column), font=("Arial", 50), anchor="center", width=3, height=3)
                button.grid(row=row+2, column=column)
        
        # if it isn't your turn, wait for opponent to make a move
        if self.yourPiece == "o":
            self.opponentTurn()
        
        # wait for gameOver to update
        display.root.wait_variable(self.gameOver)
        

    def gameFunc(self):
        # display board
        self.displayBoard()


    def resetVars(self):
        self.playerList = json.loads(requests.get(serverIP + "players").text)
        self.AmHost = False
        self.hostName = ""
        self.username = ""
        self.opponentName = ""
        self.opponentPiece = ""
        self.yourPiece = ""
        self.game = None
        self.continueVar.set(0)
        self.opponentAction.set(0)
        self.forbiddenNames = [""]
        self.topText = tkinter.StringVar()
        self.gameOver = tkinter.IntVar()

    # no game popup
    def noGame(self):
        # create popup
        popup = tkinter.Toplevel(display.root)
        popup.title("No Game")
        popup.geometry("300x300")
        popup.resizable(False, False)

        # display error message
        text = tkinter.StringVar()
        text.set("No game found with that name.")
        textLabel = tkinter.Label(popup, textvariable=text)
        textLabel.pack()

        # add a try again button
        tryAgainButton = tkinter.Button(popup, text="Try Again", command=lambda: popup.destroy())
        tryAgainButton.pack()

        # wait for user to click try again button
        popup.wait_window(tryAgainButton)

        return

    # join remote game
    def joinGame(self):
        # get the opponent's name
        while True:
            hostName = self.namePopup("Enter the host's name")
            if hostName in self.forbiddenNames:
                self.forbiddenPopup()
                continue
            # check if the game exists
            players = requests.post(serverIP + "join/" + hostName, data=json.dumps({"name": self.username}))
            # if joining was successful
            if players.status_code == 200:
                # get the current game
                self.game = json.loads(requests.get(serverIP + "games/" + hostName).text)
                # update opponent name
                self.opponentName = hostName
                # update opponent piece
                self.opponentPiece = self.game["hostPiece"]
                # update your piece
                if self.opponentPiece == "x":
                    self.yourPiece = "o"
                else:
                    self.yourPiece = "x"
                # update self.hostName
                self.hostName = hostName
                break
            else:
                # popup error message
                self.noGame()
                continue

    #function to get opponent
    def getOpponent(self):
        while True:
            # get current game
            players = requests.get(serverIP + "games/" + self.username)

            # if the opponent has joined, break
            # if response is 200, then the opponent has joined
            if players.status_code == 200:
                # update opponent name
                players = json.loads(players.text)
                self.opponentName = players["opponent"]

                # update your piece
                self.yourPiece = players["hostPiece"]

                # update opponent piece
                if self.yourPiece == "x":
                    self.opponentPiece = "o"
                else:
                    self.opponentPiece = "x"
                
                # update self.opponentAction
                self.opponentAction.set(2)

                return

    # waiting for opponent
    def waitingForOpponent(self):
        # create popup
        popup = tkinter.Toplevel(display.root)
        popup.title("Waiting for Opponent")
        popup.geometry("300x300")
        popup.resizable(False, False)

        # add text to popup
        text = tkinter.StringVar()
        text.set("Waiting for opponent to join...")
        textLabel = tkinter.Label(popup, textvariable=text)

        # add a return to menu button
        returnButton = tkinter.Button(popup, text="Return to Menu", command=lambda: self.opponentAction.set(1))

        # add text and button to popup
        textLabel.pack()
        returnButton.pack()
        
        # call getOpponent function in a thread
        threading.Thread(target=self.getOpponent).start()

        # wait for opponent to join
        display.root.wait_variable(self.opponentAction)

        # destroy popup
        popup.destroy()

        # if opponentAction is 1, return to menu (return button pressed)
        if self.opponentAction.get() == 1:
            # close the game if returning to menu
            requests.post(serverIP + "closeGame/" + self.username)
            return -1
        # if opponentAction is 2, opponent has joined
        else:
            return

    # host game
    def hostGame(self):
        self.hostName = self.username

        # send a request to the server to host a game
        PostRequest = requests.post(serverIP + "startGame", data=json.dumps({"playerName": self.username}))
        if PostRequest.status_code == 400:
            self.forbiddenPopup()
            return -1
        
        # waiting for opponent
        return self.waitingForOpponent()

    # popup to ask if user wants to host or join a game
    def joinOrStart(self):
        # create popup
        popup = tkinter.Toplevel(display.root)
        popup.title("Join or Start a Game")
        popup.geometry("300x300")
        popup.resizable(False, False)

        # text to ask if user wants to host or join a game
        text = tkinter.StringVar()
        text.set("Join or Start a Game?")
        textLabel = tkinter.Label(popup, textvariable=text)
        textLabel.pack()

        # wait for update variable
        joinOrStartVar = tkinter.IntVar()
        joinButton = tkinter.Button(popup, text="Join", command=lambda: joinOrStartVar.set(0))
        joinButton.pack()
        startButton = tkinter.Button(popup, text="Start", command=lambda: joinOrStartVar.set(1))
        startButton.pack()

        # wait for user to click either button
        popup.wait_variable(joinOrStartVar)
        popup.destroy()

        # update AmHost variable
        if joinOrStartVar.get() == 0:
            self.AmHost = False
        else:
            self.AmHost = True

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

    def namePopup(self, title):
        # tkinter popup to get player name
        popup = tkinter.Toplevel(display.root)
        popup.title(title)
        popup.geometry("600x300")
        popup.resizable(False, False)

        # create a label and entry for the player name
        nameLabel = tkinter.Label(popup, text=title, font=("Arial", 20), anchor="center", width=30)
        nameLabel.grid(row=0, column=0, columnspan=2)
        nameEntry = tkinter.Entry(popup, font=("Arial", 20), width=30)
        nameEntry.grid(row=1, column=0, columnspan=2)

        # submit button
        submitVar = tkinter.IntVar()
        submitButton = tkinter.Button(popup, text="Submit", font=("Arial", 20), width=30, command=lambda: submitVar.set(1))
        submitButton.grid(row=2, column=0, columnspan=2)

        # wait for submit button to be pressed
        display.root.wait_variable(submitVar)

        username = nameEntry.get()

        # close popup when submit button is pressed
        popup.destroy()
        return username

    def getPlayerName(self):
        while True:
            # get player's name
            username = self.namePopup("Enter your name")

            # check if the name is forbidden
            if username in self.forbiddenNames:
                self.forbiddenPopup()
                continue
            elif username in self.playerList:
                useExisting = self.useExistingScorePopup() # popup if name in scores
                if useExisting:
                    break
            else: # name is not in scores, quit
                break
        
        # add to forbidden names
        self.forbiddenNames.append(username)

        # add to self.username
        self.username = username