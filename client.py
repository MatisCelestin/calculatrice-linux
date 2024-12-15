import socket
import sys
import re
import logging
# On définit la destination de la connexion
host = '127.0.0.1'  # IP du serveur
port = 7000               # Port choisir par le serveur

class CustomFormatter(logging.Formatter):

    red = "\x1b[31;20m"
    reset = "\x1b[0m"
  

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno) 
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


try:
    print("toto")

except Exception as e:
    print(f"Failed to configure logging: {e}")
    sys.exit(1)

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    print("Connexion réussie à %s:%s", host, port)
    s.send("Ok".encode())
    data = s.recv(1024)
    print(f"Réponse reçue du serveur {host} : {repr(data)}")
    
    userMessage = input("Veuillez saisir une opération arithmétique : ")

    pattern = r'^(-?\d{1,5})\s*([+*-])\s*(-?\d{1,5})$'

    match= re.match(pattern, userMessage)
    if match:
        num1, operator, num2 = match.groups()
        num1, num2 = int(num1), int(num2)

        # Vérifiez si les nombres sont dans la plage [-100000, 100000]
        if -100000 <= num1 <= 100000 and -100000 <= num2 <= 100000:
            s.sendall(userMessage.encode("utf-8"))
            print("Message envoyé au serveur %s : %s", host, userMessage)
        else:
            raise ValueError("l'opération autorisée n'accepte que des nombres entiers compris entre -100000 et +100000")
    else:
        raise ValueError("l'opération autorisée n'accepte que les signes suivants (-,+,*) et des nombres entiers compris entre -100000 et +100000")
    
    data = s.recv(1024)
    s.close()
    print(repr(data.decode()))
    sys.exit(0)
   # Assurez-vous que le socket est fermé même en cas d'erreur
except socket.error as e :
    print("Impossible de se connecter au serveur %s sur le port %s", host, port)
    s.close()
    sys.exit(1)
# Close the connection.