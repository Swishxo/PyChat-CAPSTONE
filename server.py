import socket
import threading


# get address for server
SERVER = socket.gethostbyname("192.168.1.221")
print(SERVER)
# free port for chat
PORT = 8350

clients, names = [], []

# Create socket type and family
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))


# function to start the connection
def startchat():
    # listen for connections
    server.listen() # num of connections is optional

    # format to get messages from client
    format = "utf-8"
    while True:
        # client that connect
        conn, addr = server.accept()
        # send message to client
        conn.send("User".encode(format))

        # receive message from client
        user = conn.recv(1024).decode(format)
        # add user to name list
        names.append(user)
        # add new connection to client list
        clients.append(conn)

        # broadcast message
        broadcastMessage(f"{user} has entered".encode(format))

        # let client know they entered chat
        conn.send(f"{user} you entered the chat".encode(format))

        # thread handle multiple messages
        # and args is a tuple of conn and addr
        thread = threading.Thread(target=handle, args=(conn, addr))

        # execute multiple messages from multi clients
        thread.start()

        # clients connected
        print(f"active connections {threading.activeCount() - 1}")  # minus main thread


# method to handle the incoming messages
def handle(conn, addr):
    print(f"adrr: {addr}")

    connected = True
    # while a client is connected
    while connected:
        # receive incoming message
        message = conn.recv(1024)  # byte length

        # broadcast message
        broadcastMessage(message)

    # close the connection
    conn.close()


# method for broadcasting messages to sever and client
def broadcastMessage(message):
    for client in clients:
        # for every client send a message
        # initial msg being sent: "{user} Connected successful to chat
        client.send(message)


if __name__ == '__main__':
    startchat()