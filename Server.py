import socket
import csv
import threading
import random
import time
from random import randint
from Client import GamePlay, clearConsole
import os

database = []
player = []
socketPlayer = {}
room = {}
playerInGame ={}

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

#begin client-sever section

def getDatabase():
    with open('Database.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                # self.data[row[0]] = row[1]
                temp = [row[0], row[1], row[2], row[3], row[4], row[5], row[6]]
                database.append(temp)
                line_count += 1

def UpdateDatabase():
    with open('Database.csv', mode='w', newline='', encoding='utf-8') as csv_file:
        user_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        user_writer.writerow(["Username", " Password", " Fullname", " Date of birth", " Winning game", " Note", "Online check"])
        user_writer.writerows(database)

def getInfo():
    global HOST_NAME
    HOST_NAME = socket.gethostname()
    global HOST_ADDRESS
    HOST_ADDRESS = socket.gethostbyname(HOST_NAME)
    print(HOST_NAME)
    print(HOST_ADDRESS)

def choosePort():
    global PORT
    PORT = 12121 #int(input("Pls choose a port that will be used for connection: "))

def createServer():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM,0)
    soc.bind((HOST_ADDRESS, PORT)) #tuple
    soc.listen(2)
    nClient = 0
    try:
        while nClient < 5:
            try:
                clientConnection, clientAddr = soc.accept()
                nClient += 1
                print("Connected to Client: ", clientAddr)
                thr1 = threading.Thread(target = handleClient, args = (clientConnection, clientAddr))
                # thr1 = threading.Thread(target = handleClientDemo, args = (clientConnection, clientAddr))
                thr1.daemon = True
                thr1.start()
                nClient -= 1
            except:
                print("Client's connection error")
    finally:
        soc.close()
    
def handleClient(clientConnection, clientAddr):
    def caesar_decrypt(word):
        c = ''
        for i in word:
            if (i == ' '):
                c += ' '
            else:
                c += (chr(ord(i) - 3))
        return c
    isLogin = False
    while isLogin == False:
        if Login(clientConnection) == True:
            isLogin = True
            clientConnection.sendall('Login Successful'.encode("utf8"))
        else:
            clientConnection.sendall('Wrong username or password'.encode("utf8"))
            createNewUser = clientConnection.recv(1024).decode("utf8")
            if createNewUser == "create new user":
                hasEncryption = clientConnection.recv(1024).decode("utf8")
                newUserObjectList = clientConnection.recv(1024).decode("utf8").split(";")
                if hasEncryption == "Encrypted":
                    for i in range(len(newUserObjectList)):
                        newUserObjectList[i] = caesar_decrypt(newUserObjectList[i])
                database.append(newUserObjectList)
                UpdateDatabase()
                print('add to database and database file successful')

    # After login successful
    choiceAfterLoginSuccessful = ''
    while choiceAfterLoginSuccessful != "play game":
        choiceAfterLoginSuccessful = clientConnection.recv(1024).decode("utf8")
        if choiceAfterLoginSuccessful == "change password":
            ChangePassword(clientConnection)
        elif choiceAfterLoginSuccessful == "check user info":
            CheckUserinfo(clientConnection)
        elif choiceAfterLoginSuccessful == "setup info":
            SetUpInfo(clientConnection)

    # create room
    
    listOnlineUser = socketPlayer.keys()
    print(f"List online User: {listOnlineUser}")
    startingRoom(clientConnection)
    # if len(listOnlineUser) >= 2:
    #     GamePlay(player[0], player[1])

    # draft
    # clientConnection.sendall(content1.encode("utf8"))     #send
    # content2 = clientConnection.recv(1024).decode("utf8") #recieve
    
    # end draft
# create room

def startingRoom(clientConnection):
    startGameSignal = clientConnection.recv(1024).decode("utf8")
    while startGameSignal != 'start_game':
        startGameSignal = clientConnection.recv(1024).decode("utf8")
    joinRoomWithAnotherPlayer = False
    while joinRoomWithAnotherPlayer == False:
        listOnlineUser = socketPlayer.keys()
        clientConnection.sendall(';'.join(listOnlineUser).encode("utf8"))
        creatingIDRoomMessage = clientConnection.recv(1024).decode("utf8")
        clientConnection.sendall("justDoIt".encode("utf8"))
        hasInvitationMess = clientConnection.recv(1024).decode("utf8")
        if hasInvitationMess == "hasAInvitation":
            print("Terminated thread")
            return

        choosingUserNameMessage = clientConnection.recv(1024).decode("utf8")
        clientConnection.sendall("justDoIt ".encode("utf8"))
        hasInvitationMess = clientConnection.recv(1024).decode("utf8")
        if hasInvitationMess == "hasAInvitation":
            return
        
        listRoomInfo = clientConnection.recv(1024).decode("utf8").split(";")
        if Createroom(listRoomInfo[0], listRoomInfo[1], listRoomInfo[2]) == True:
            GamePlay(listRoomInfo[1], listRoomInfo[2])
            
def Createroom(roomID, username1, username2):
    socketPlayer[username2].sendall('SomeOneInviteYouToARoom;'.encode("utf8"))
    socketPlayer[username2].sendall(";".join([roomID, username1]).encode("utf8"))
    
    signalAcceptCreateRoom = socketPlayer[username2].recv(1024).decode("utf8")
    if signalAcceptCreateRoom == "Accept":
        socketPlayer[username1].sendall("Accepted_create_room".encode("utf8"))
        return True
    else:
        socketPlayer[username1].sendall("Rejected_create_room".encode("utf8"))
        return False


#end client-sever section

#begin Login section

def Login(clientConnection):
    def caesar_decrypt(word):
        c = ''
        for i in word:
            if (i == ' '):
                c += ' '
            else:
                c += (chr(ord(i) - 3))
        return c

    isEncrypted = clientConnection.recv(1024).decode("utf8")
    loginInfo = clientConnection.recv(1024).decode("utf8")
    ListloginInfo = loginInfo.split(';')
    username = ListloginInfo[0]
    password = ListloginInfo[1]
    if isEncrypted == 'Encrypted':
        username = caesar_decrypt(username)
        password = caesar_decrypt(password)
    if checkLogin(username, password) == True:
        player.append(username)
        socketPlayer.update({username: clientConnection})
        return True
    else:
        return False

def checkLogin(username, password):
    ValidAccount = False
    for i in range(len(database)):
        if username == database[i][0] and password == database[i][1]:
            database[i][6] = 'online'
            UpdateDatabase()
            ValidAccount = True
            return True
    return False

#end Login section

#beginning after login successful section

def CheckUserinfo(clientConnection):

    def check_username_find(clientConnection):
        name = clientConnection.recv(1024).decode("utf8")
        founded = False
        for i in range(len(database)):
            if name in database[i][0]:
                clientConnection.sendall("Found".encode("utf8"))
                founded = True
                break
        if founded == False:
            clientConnection.sendall("Not found".encode("utf8"))

    def check_username_online(clientConnection):
        name = clientConnection.recv(1024).decode("utf8")
        founded = False
        onlineStatus = 'offline'
        for i in range(len(database)):
            if name in database[i][0]:
                founded = True
                clientConnection.sendall("Found".encode("utf8"))
                if database[i][6] == 'online':
                    onlineStatus = 'online'
                break
        if founded == True:
            clientConnection.sendall(onlineStatus.encode("utf8"))

    def check_username_showfullname(clientConnection):
        name = clientConnection.recv(1024).decode("utf8")
        founded = False
        fullname = "something"
        for i in range(len(database)):
            if name in database[i][0]:
                founded = True
                clientConnection.sendall("Found".encode("utf8"))
                fullname = database[i][2]
                break
        if founded == True:
            clientConnection.sendall(fullname.encode("utf8"))

    def check_username_showdate(clientConnection):
        name = clientConnection.recv(1024).decode("utf8")
        founded = False
        date = "something"
        for i in range(len(database)):
            if name in database[i][0]:
                founded = True
                clientConnection.sendall("Found".encode("utf8"))
                date = database[i][3]
                break
        if founded == True:
            clientConnection.sendall(date.encode("utf8"))

    def check_username_showWinningGame(clientConnection):
        name = clientConnection.recv(1024).decode("utf8")
        founded = False
        winningGame = "something"
        for i in range(len(database)):
            if name in database[i][0]:
                founded = True
                clientConnection.sendall("Found".encode("utf8"))
                winningGame = database[i][4]
                break
        if founded == True:
            clientConnection.sendall(winningGame.encode("utf8"))

    def check_username_showNote(clientConnection):
        name = clientConnection.recv(1024).decode("utf8")
        founded = False
        winningGame = "something"
        for i in range(len(database)):
            if name in database[i][0]:
                founded = True
                clientConnection.sendall("Found".encode("utf8"))
                winningGame = database[i][5]
                break
        if founded == True:
            clientConnection.sendall(winningGame.encode("utf8"))

    def check_username_showall(clientConnection):
        name = clientConnection.recv(1024).decode("utf8")
        founded = False
        index = 0
        for i in range(len(database)):
            if name in database[i][0]:
                founded = True
                # print if user online or not
                clientConnection.sendall("Found".encode("utf8"))
                index = i
        if founded == True:
            clientConnection.sendall(';'.join(database[index]).encode("utf8"))

    choice = 0
    while choice != 8:
        choice = int(clientConnection.recv(1024).decode("utf8"))
        if choice == 1:
            check_username_find(clientConnection)
        elif choice == 2:
            check_username_online(clientConnection)
        elif choice == 3:
            check_username_showfullname(clientConnection)
        elif choice == 4:
            check_username_showdate(clientConnection)
        elif choice == 5:
            check_username_showWinningGame(clientConnection)
        elif choice == 6:
            check_username_showNote(clientConnection)
        elif choice == 7:
            check_username_showall(clientConnection)

def ChangePassword(clientConnection):
    def caesar_decrypt(word):
        c = ''
        for i in word:
            if (i == ' '):
                c += ' '
            else:
                c += (chr(ord(i) - 3))
        return c
    hasEncryption = clientConnection.recv(1024).decode("utf8")
    objectRecieve = clientConnection.recv(1024).decode("utf8")
    list = objectRecieve.split(';')
    print(f"list: {list}")
    if hasEncryption == "Encrypted":
        for i in range(len(list)):
            list[i] = caesar_decrypt(list[i])
        print("Decrypt success")
    for i in range(len(database)):
        if list[0] == database[i][0]:
            if list[1] == database[i][1]:
                database[i][1] = list[2]
                UpdateDatabase()
                clientConnection.sendall('change password successful'.encode("utf8"))
            else:
                clientConnection.sendall('wrong password'.encode("utf8"))
            break

def SetUpInfo(clientConnection):

    def SetFullname(clientConnection):
        object = clientConnection.recv(1024).decode("utf8")
        list = object.split(';')
        print(list)
        for i in range(len(database)):
            if database[i][0] == list[0]:
                database[i][2] = list[1]
                clientConnection.sendall('Set successful'.encode("utf8"))
                break

    def SetBirthday(clientConnection):
        object = clientConnection.recv(1024).decode("utf8")
        list = object.split(';')
        for i in range(len(database)):
            if database[i][0] == list[0]:
                database[i][3] = list[1]
                clientConnection.sendall('Set successful'.encode("utf8"))
                break

    def SetNote(clientConnection):
        object = clientConnection.recv(1024).decode("utf8")
        list = object.split(';')
        for i in range(len(database)):
            if database[i][0] == list[0]:
                database[i][5] = list[1]
                clientConnection.sendall('Set successful'.encode("utf8"))
                break

    choice = 0
    while choice != 4:
        choice = int(clientConnection.recv(1024).decode("utf8"))
        if choice == 1:
            SetFullname(clientConnection)
            UpdateDatabase()
        elif choice == 2:
            SetBirthday(clientConnection)
            UpdateDatabase()
        elif choice == 3:
            SetNote(clientConnection)
            UpdateDatabase()

#end after login successful section

#begin Game section

def GamePlay(username1, username2):
    
    print("PLAY GAME!!!!")
    
    def printTwoBoard():
        print(f"Board's {username1}")
        for row in board1:
            print(" ".join(row))
        print()
        print(f"Board's {username2}")
        for row in board2:
            print(" ".join(row))
        print()
    
    def convertStringToBoard(boardString):
        board = []
        boardString=boardString.split(";")
        for row in boardString:
            temp = row.split(",")
            board.append(temp)
        return board
    
    def isDestroyedAll(listShipBoard):
        return len(listShipBoard) == 0
    
    stringBoard1 = socketPlayer[username1].recv(1024).decode("utf8")
    print(f"Recieved Board from {username1}")
    stringBoard2 = socketPlayer[username2].recv(1024).decode("utf8")
    print(f"Recieved Board from {username2}")
    board1 = convertStringToBoard(stringBoard1)
    board2 = convertStringToBoard(stringBoard2)
    
    printTwoBoard()
    
    turnOrder = random.randint(1, 2)
    if turnOrder == 1:
        socketPlayer[username1].sendall('1'.encode("utf8"))
        socketPlayer[username2].sendall('2'.encode("utf8"))
        socket1 = socketPlayer[username1]
        socket2 = socketPlayer[username2]
    else:
        socketPlayer[username1].sendall('2'.encode("utf8"))
        socketPlayer[username2].sendall('1'.encode("utf8"))
        socket1 = socketPlayer[username2]
        socket2 = socketPlayer[username1]
        temp = board2
        board2 = board1
        board1 = temp
    
    listShipBoard1 = []
    listShipBoard2 = []
    
    for i in range(len(board1)):
        for j in range(len(board1[i])):
            if board1[i][j] == "X":
                listShipBoard1.append([i,j]) 
    for i in range(len(board2)):
        for j in range(len(board2[i])):
            if board2[i][j] == "X":
                listShipBoard2.append([i,j])
                
    def socket1Attack():
        socket1Bullet = socket1.recv(1024).decode("utf8").split(";")
        print(f"socket1's bullet: {socket1Bullet}")
        xSocket1 = int(socket1Bullet[0])
        ySocket1 = int(socket1Bullet[1])
        if board2[xSocket1][ySocket1] == "X":
            listShipBoard2.remove([xSocket1, ySocket1])
            if isDestroyedAll(listShipBoard2) == False:
                socket1.sendall('hit'.encode("utf8"))
                socket2.sendall(";".join(socket1Bullet).encode("utf8"))
                time.sleep(1)
                socket2.sendall("Continue waiting for socket2".encode("utf8"))
                socket1Attack()
            else:
                socket1.sendall('YouWin'.encode("utf8"))
                socket2.sendall(";".join(socket1Bullet).encode("utf8"))
                time.sleep(1)
                socket2.sendall("YouLose".encode("utf8"))
                endGameSignal2 = socket2.recv(1024).decode("utf8")
                print(f"endGameSignal2: {endGameSignal2}") ################
                if endGameSignal2 == "endGame":
                    socket1.sendall('endGame'.encode("utf8"))
                else:
                    socket1.sendall("Please send play again signal".encode("utf8"))
                    endGameSignal1 = socket1.recv(1024).decode("utf8")
                    if endGameSignal1 == "endGame":
                        socket2.sendall('endGame'.encode("utf8"))
                    else:
                        socket2.sendall('acceptPlayGame'.encode("utf8"))
        elif board2[xSocket1][ySocket1] == "O":
            socket1.sendall('Miss'.encode("utf8"))
            socket2.sendall(";".join(socket1Bullet).encode("utf8"))
            time.sleep(1)
            socket2.sendall('YourTurn'.encode("utf8"))
            socket2Attack()
    
    def socket2Attack():
        socket2Bullet = socket2.recv(1024).decode("utf8").split(";")
        print(f"socket2's bullet: {socket2Bullet}")
        xSocket2 = int(socket2Bullet[0])
        ySocket2 = int(socket2Bullet[1])
        if board1[xSocket2][ySocket2] == "X":
            listShipBoard1.remove([xSocket2, ySocket2])
            if isDestroyedAll(listShipBoard1) == False:
                socket2.sendall('hit'.encode("utf8"))
                socket1.sendall(";".join(socket2Bullet).encode("utf8"))
                time.sleep(1)
                socket1.sendall("Continue waiting for socket1".encode("utf8")) # them if vao neu socket1 thang roi
                socket2Attack()
            else:
                socket2.sendall('YouWin'.encode("utf8"))
                socket1.sendall(";".join(socket2Bullet).encode("utf8"))
                time.sleep(1)
                socket1.sendall("YouLose".encode("utf8"))
                endGameSignal1 = socket1.recv(1024).decode("utf8")
                print(f"endGameSignal1: {endGameSignal1}") ###################
                if endGameSignal1 == "endGame":
                    socket2.sendall('endGame'.encode("utf8"))
                else:
                    socket2.sendall("Please send play again signal".encode("utf8"))
                    endGameSignal2 = socket2.recv(1024).decode("utf8")
                    if endGameSignal2 == "endGame":
                        socket1.sendall('endGame'.encode("utf8"))
                    else:
                        socket1.sendall('acceptPlayGame'.encode("utf8"))
        elif board1[xSocket2][ySocket2] == "O":
            socket2.sendall('Miss'.encode("utf8"))
            socket1.sendall(";".join(socket2Bullet).encode("utf8"))
            time.sleep(1)
            socket1.sendall('YourTurn'.encode("utf8"))
            socket1Attack()
    
    socket1Attack()        
        
#end Game section

if (__name__=="__main__"):
    clearConsole()
    getInfo()
    choosePort()
    getDatabase()
    createServer()