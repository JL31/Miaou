# -*- coding: UTF-8 -*-

# Informations de connexion - hote et port de connexion

hote = 'localhost'
port = 12800


# Création et connexion du client

connexion_miaou = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_miaou.connect((hote, port))
print("Connexion établie avec le serveur sur le port {}\n".format(port))


# Boucle d'échange avec le serveur

msg = b""

while msg != b"fin":
	
	msg = input("> ")
	msg_encode = msg.encode()
	connexion_miaou.send(msg_encode)
	
	msg_recu = connexion_miaou.recv(1024)
	print("{}\n".format(msg_recu.decode()))
	

# Fermeture de la connexion client

connexion_miaou.close()


# "C:\Python27\Lib\idlelib\idle.bat" "$(FULL_CURRENT_PATH)"
