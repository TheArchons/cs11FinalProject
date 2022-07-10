#set shell := ["powershell.exe", "-c"] # uncomment to use powershell

startOnlineDebian:
    cd /home/admin/cs11FinalProject
    git pull
    nohup python3 server.py