#set shell := ["powershell.exe", "-c"] # uncomment to use powershell

startOnlineDebian:
    cd /home/admin/tictactoe
    git pull
    nohup python3 server.py