import socket
import time
from multiprocessing import Process
import multiprocessing

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        gdata = b''

        try:
            gs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            gs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            gs.connect((socket.gethostbyname('www.google.com'), 80))
            # payload = 'GET / HTTP/1.0\r\nHost: www.google.com\r\n\r\n'
            # gs.sendall(payload.encode())
            gs.shutdown(socket.SHUT_WR)

            while True:
                data = gs.recv(4096)
                if not data:
                    break
                gdata += data

        except Exception as e:
            print(e)
        finally:
            gs.close()

        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen()
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            
            conn.sendall(gdata)
            conn.close()

if __name__ == "__main__":
    p = Process(target=main)
    p.start()
    p.join()
