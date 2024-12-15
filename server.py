import socket
import re
from os import environ


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

port = int(environ.get("CALC_PORT"))
s.bind(('0.0.0.0', port))  
print(int(environ.get("CALC_PORT")))

s.listen(1)
conn, addr = s.accept()

while True:

    try:
        # On reçoit la string Hello du client
        data = conn.recv(1024)
        if not data: break
        print(f"Données reçues du client : {data}")

        conn.send("Hello".encode())

        # On reçoit le calcul du client
        data = conn.recv(1024)
        data = data.decode().strip("\n")
        for i in data:
            if i not in '0123456789 +-*':
                conn.close()
        # Evaluation et envoi du résultat
        
        res  = eval(data)
        conn.send(str(res).encode())
        
         
    except socket.error:
        print("Error Occured.")
        break

conn.close()