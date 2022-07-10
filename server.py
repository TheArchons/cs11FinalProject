# this is running on my virtual private server

from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import json
import random

#hostName = "192.168.0.121"
hostName = "0.0.0.0"
hostPort = 1337

# create remoteScores.json file
if not os.path.exists("remoteScores.json"):
    with open("remoteScores.json", "w") as f:
        f.write("{}")

class server(BaseHTTPRequestHandler):
    # games format "username": {"board": [], "isXTurn": True, "opponent" : None, "gameOver": False, "confirmDelete": 0, "winner": None, "hostPiece": "x"}
    games = {}
    scores = json.load(open('remoteScores.json'))

    # setup a tic tac toe board as a 2d array
    def setupBoard(self):
        board = []
        for i in range(3):
            board.append([])
            for j in range(3):
                board[i].append(" ")
        return board

    # given a 2d array, return the winner only if each square is filled with x or y
    def checkWinner(self, board):
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

    # check if the game is a tie
    def checkTie(self, board):
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    return False
        return True

    def returnPayload(self, payload):
        # return the payload
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(payload))
        self.end_headers()
        self.wfile.write(bytes(payload, "utf-8"))
        return

    def do_GET(self):
        print("getting " + self.path)
        if self.path == "/players":
            # return a json list of players
            
            # create a list of players
            players = list(self.scores)

            # convert to json
            json_players = json.dumps(players)

            # return the json file
            self.returnPayload(json_players)
            return

        # if the path is /game/username
        
        if self.path.startswith("/games/"):
            # get the username
            username = self.path.split("/")[2]
            print(self.games, username)
            if username not in self.games:
                # user is not in a game
                self.send_response(400)
                self.end_headers()
                return
            # get the game
            game = self.games[username]
            # convert to json
            json_game = json.dumps(game)
            # if the game's opponent is None, then return 400, because an opponent has not been found
            if game["opponent"] is None:
                self.send_response(400)
                self.end_headers()
                return
            # return the json file
            self.returnPayload(json_game)
            return
        
        if self.path == "/scores":
            # return a json list of scores
            # convert to json
            json_scores = json.dumps(self.scores)
            # return the json file
            self.returnPayload(json_scores)

    def do_POST(self):
        print("posting " + self.path)
        if self.path == "/startGame":
            # start a new game
            # get username with decode
            username = self.rfile.read(int(self.headers['Content-Length'])).decode("utf-8").split("=")[1]
            print("username:", username)
            # if user is already in a game
            if username in self.games:
                self.send_response(400)
                self.end_headers()
                return
            
            if username not in self.scores:
                # add user to scores if they don't exist
                self.scores[username] = 0
                # save scores to file
                json.dump(self.scores, open('remoteScores.json', 'w'))
            
            self.send_response(200)
            self.end_headers()
            # create a new game
            self.games[username] = {
                "board": self.setupBoard(),
                "isXTurn": True,
                "opponent" : None,
                "isOver": False,
                "confirmDeletes": 0,
                "winner": None,
                "hostPiece" : random.choice(["x", "o"]),} # hostPiece is randomized
            return
        
        if self.path.startswith("/move/"): # if the path is /move/username
            # get the username
            username = self.path.split("/")[2]
            # get the game
            game = self.games[username]
            # get the move
            move = self.rfile.read(int(self.headers['Content-Length'])).decode("utf-8").split("&")
            # parse the move
            col = int(move[0].split("=")[1])
            row = int(move[1].split("=")[1])
            move = [row, col]

            # update the board
            if game["isXTurn"]:
                game["board"][move[0]][move[1]] = "x"
            else:
                game["board"][move[0]][move[1]] = "o"

            # check if the game is over
            winner = self.checkTie(game["board"])
            if winner == True:
                winner = "tie"
                game["isOver"] = True
            else:
                winner = self.checkWinner(game["board"])
                if winner == "x":
                    if game["hostPiece"] == "x":
                        game["winner"] = username
                        winner = game["winner"]
                    else:
                        game["winner"] = game["opponent"]
                        winner = game["winner"]
                elif winner == "o":
                    if game["hostPiece"] == "o":
                        game["winner"] = username
                        winner = game["winner"]
                    else:
                        game["winner"] = game["opponent"]
                        winner = game["winner"]
                if winner != "none":
                    game["isOver"] = True
                    self.scores[winner] += 1
                    # update the scores
                    json.dump(self.scores, open('remoteScores.json', 'w'))
            
            # update the game
            # update the current player
            game["isXTurn"] = not game["isXTurn"]
            # update the main dictionary
            self.games[username] = game
            
            # return code 200
            self.send_response(200)
            self.end_headers()
        
        if self.path.startswith("/join/"):
            # get the host's name
            hostName = self.path.split("/")[2]

            # check if the game exists, does not have an opponent
            if hostName not in self.games or self.games[hostName]["opponent"] is not None:
                # game does not exist
                self.send_response(400)
                self.end_headers()
                return

            # set the new player's opponent
            self.games[hostName]["opponent"] = username

            if username not in self.scores: # add user to scores if they don't exist
                # add user to scores if they don't exist
                self.scores[username] = 0
                # save scores to file
                json.dump(self.scores, open('remoteScores.json', 'w'))

            # send back response code
            self.send_response(200)
            self.end_headers()
            return
        
        if self.path.startswith("/confirmDelete/"):
            # get the username
            username = self.path.split("/")[2]
            # get the game
            game = self.games[username]
            # if the game is over, increment the confirmDeletes
            if game["isOver"]:
                game["confirmDeletes"] += 1
            # if confirmDeletes is 2 or more, delete the game
            if game["confirmDeletes"] >= 2:
                del self.games[username]
            else:
                # update the game
                self.games[username] = game
            # return code 200
            self.send_response(200)
            self.end_headers()
    
        if self.path.startswith("/closeGame/"):
            # get the username
            username = self.path.split("/")[2]
            # get the game
            game = self.games[username]
            # delete the game
            del self.games[username]
            self.send_response(200)
            self.end_headers()


if __name__ == "__main__":
    webServer = HTTPServer((hostName, hostPort), server)
    print(f"Server started http://{hostName}:{hostPort}")
 
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
 
    webServer.server_close()
    print("Http server stopped.")