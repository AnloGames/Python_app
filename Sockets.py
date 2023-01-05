import socket


REQUEST = '''GET / HTTP/1.0

'''

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('127.0.0.1', 8000))
    s.settimeout(0.1)
    s.sendall(REQUEST.encode())
    b = s.recv(1024) + s.recv(1024)
    print(b.decode())