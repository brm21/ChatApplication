import socket
import threading
import time 

threadLock = threading.Lock()

shutdown = False
#thread function for receiving messages
def receiving(name, sock):
    while not shutdown:
        try:
            #thread locks are used so there is no inteference when receiving messages
            threadLock.acquire()
            while True:
                #when a message is received, size max 1024 bytes. Print message to screen
                data, addr = sock.recvfrom(1024)
                print (str(data))
        except:
            pass
        finally:
            #release threadlock and continue
            threadLock.release()


#thread function for sending messages
def sending(name, sock):
    while not shutdown:
        try:
            #lock thread to prevent interference while sending messages
            threadLock.acquire()
            while True:
                #send data with address to server, max size 1024 bytes
                data, addr = sock.sendmsg(1024)
        except:
            pass
        finally:
            #release thread lock and continue
            threadLock.release()

#host address echos back real ip address
#Port 0 is used in order to generate random port
host = '127.0.0.1'
port = 0

server = ('192.168.1.17', 5000)

#UDP socket connection
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

#start receiving thread
rThread = threading.Thread(target=receiving, args=("RecvThread", s))
rThread.start()

#start sending thread
sThread = threading.Thread(target=sending, args=("SendThread", s))
sThread.start()

#alias will be used to distinguish who is sending the message
#once in chatroom message will broadcast to other clients to notify them they have entered the chat
#sleep used in order to ensure data is fully sent before continuing
alias = input("Please enter your name: ")
s.sendto(bytes(alias + " has entered the chat.",'utf-8'), server)
time.sleep(0.3)

message = input()

#continue an open connection to send messages until user decides to leave chatroom
while message != '!Quit':
    if message != '':
        #message needs to be encoded into data as bytes before sent to the server
        s.sendto(bytes(alias + ": " + message, 'utf-8'), server)
        time.sleep(0.3)

    message = input()
    
#when leaving chatroom, final message will be broadcasted to other clients to notify them of you leaving    
s.sendto(bytes(alias + " has left the chatroom.", 'utf-8'), server)

shutdown = True

#close receiving thread
#close sending thead
rThread.join()
sThread.join()
#close socket
s.close()
