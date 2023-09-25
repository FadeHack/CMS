import socket

def lawyer_program():
    # get the hostname
    host = socket.gethostname()
    port = 1234  # initiate port no above 1024

    lawyer_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    lawyer_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    lawyer_socket.listen(2)
    conn, address = lawyer_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("from connected client: " + str(data))
        data = input(' -> ')
        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    lawyer_program()