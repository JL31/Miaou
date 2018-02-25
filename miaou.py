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


# Initialisation de variables

serveur_lance = True
clients_connectes = []


# Boucle principale de lancement du serveur

while serveur_lance:
    
    # Vérification des demandes de connexion au serveur
    # Les demandes de connexions sont mises dans une liste : connexions_demandees
    
    connexions_demandees, wlist, xlist = select.select([connexion_principale], [], [], 0.05)
    
    
    # Récupération des sockets connectés (des clients) dans une liste des clients en attente d'être lus : clients_connectes
    
    for connexion in connexions_demandees:
        
        connexion_client, infos_client = connexion.accept() # Acceptation des demandes de connexion
        clients_connectes.append(connexion_client)          # Ajout du socket connecté à la liste des clients connectés
        
    
    # Ecoute des clients connectés
    
    clients_com = []
    
    try:
    # On essaie de récupérer la liste des clients qui ont envoyé un message sur le serveur
        
        clients_com, wlist, xlist = select.select(clients_connectes, [], [], 0.05)
        
    except select.error:
    # Gestion des cas d'erreur
        
        pass
        
    else:
    # Si la liste des clients qui ont envoyé un message sur le serveur a pu être récupérée on récupère le message envoyé
        
        for client in clients_com:
            
            msg_recu = client.recv(1024)
            fonctions_miaou.envoi_all(clients_connectes, msg_recu)
            
            msg_recu_decode = msg_recu.decode()
            if msg_recu == "fin":
                
                serveur_lance = False
                

# Fermeture des connexions - clients puis serveur

print("Fermeture des connexions")

for client in clients_connectes:
    
    client.close()
    

connexion_principale.close()


# "C:\Python27\Lib\idlelib\idle.bat" "$(FULL_CURRENT_PATH)"
