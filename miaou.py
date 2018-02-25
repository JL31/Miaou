# -*- coding: UTF-8 -*-

# Import des librairies

import socket
import select
import fonctions_miaou


# Informations de connexion - hote et port de connexion

hote = ''
port = 12800


# Création du serveur : création du scoket, liaison du socket, écoute du socket

connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_principale.bind((hote, port))
connexion_principale.listen(5)
print("Le serveur principal est lancé sur le port {}".format(port))


#

serveur_lance = True
clients_connectes = []

while serveur_lance:
	
	connexions_demandees, wlist, xlist = select.select([connexion_principale], [], [], 0.05)
	
	for connexion in connexions_demandees:
		
		connexion_client, infos_client = connexion.accept()
		clients_connectes.append(connexion_client)
		
	clients_com = []
	
	try:
		
		clients_com, wlist, xlist = select.select(clients_connectes, [], [], 0.05)
		
	except select.error:
		
		pass
		
	else:
		
		for client in clients_com:
			
			msg_recu = client.recv(1024)
			fonctions_miaou.envoi_all(connexion_client, msg_recu)
			
			msg_recu_decode = msg_recu.decode()
			if msg_recu == "fin":
				
				serveur_lance = False
				

# Fermeture des connexions - clients puis serveur

print("Fermeture des connexions")

for client in clients_connectes:
	
	client.close()
	
connexion_principale.close()


# "C:\Python27\Lib\idlelib\idle.bat" "$(FULL_CURRENT_PATH)"
