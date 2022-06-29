# this is running on my virtual private server

from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import json

hostName = "localhost"
hostPort = 8080

class server(BaseHTTPRequestHandler):
    # games format "username": {"board": [], "isXTurn": True, "opponent" : None}
    games = {}
    scores = {}

    def __init__(self):
        # load scores from file
        with open('remoteScores.json') as json_file:
            self.scores = json.load(json_file)

    # setup a tic tac toe board as a 2d array
    def setupBoard():
        board = []
        for i in range(3):
            board.append([])
            for j in range(3):
                board[i].append(" ")
        return board

    def do_GET(self):
        if self.path == "/players":
            # return a json list of players
            
            # create a list of players
            players = list(self.scores)

            # convert to json
            json_players = json.dumps(players)

            # return the json file
            payload = json_players
            print(payload)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', len(payload))
            self.end_headers()
            self.wfile.write(bytes(payload, "utf-8"))
            return
                
    def do_POST(self):
        if self.path == "/startGame":
            # start a new game
            # get username
            username = self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8')
            if username in self.games:
                # user is already in a game
                self.send_response(400)
                self.end_headers()
                return
            if username not in self.scores:
                # add user to scores if they don't exist
                self.scores[username] = 0
            
            self.send_response(200)
            self.end_headers()
            # create a new game
            self.games[username] = {"board": self.setupBoard(), "isXTurn": True, "opponent" : None}
            return

if __name__ == "__main__":
    # create remoteScores.json file
    if not os.path.exists("remoteScores.json"):
        with open("remoteScores.json", "w") as f:
            f.write("{}")

    webServer = HTTPServer((hostName, hostPort), server)
    print(f"Server started http://{hostName}:{hostPort}")
 
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
 
    webServer.server_close()
    print("Http server stopped.")