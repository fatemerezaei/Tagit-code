import socket

s = socket.socket()
host = "0.0.0.0"
port = 3780
s.bind((host, port))
s.listen(5)
c, addr = s.accept()
count = 0

host_nfq, port_nfq = "0.0.0.0", 3770
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
s.connect((host_nfq, port_nfq))
while (count < 10000000):
    message = c.recv(1024)
    count += 1
    print("read from client", message)
    
    
    
    message_cell = str("jjjjjjjjjjj")# delay
    s.sendall(message_cell.encode('utf-8'))
    print("sent to server", count)
    print()
