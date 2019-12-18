import socket
import time

host = '192.168.1.17'
port = 5000

#List of users entered in chatroom
clients = []

#UDP socket connection
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host,port))
s.setblocking(0)


quitting = False
print("Chat room server started...")

#Running server waiting for incoming messages
while not quitting:
    try:
        #receive messages from clients
        data, addr = s.recvfrom(1024)
        if "!Quit" in str(data):
            clients.remove(addr)
        #add new clients to list and send welcome message
        if addr not in clients:
            s.sendto((bytes("Welcome to the chatroom! To leave type !Quit", 'utf-8')), addr)
            clients.append(addr)
        #print messages in server window with date, time, address,client and data                     
        print(time.ctime(time.time()) + str(addr) + ": :" + str(data))
        #broadcast messages sent from client to all other clients
        for client in clients:
            if client != addr:	
                s.sendto(data, client)
    except:
        pass
#close socket connection
s.close()

