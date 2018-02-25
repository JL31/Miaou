# -*- coding: UTF-8 -*-

# Définition des fonctions

def envoi_all(clients_connectes, msg_recu):
    """
        Fonction pour transférer un message à tous les utilisateurs du chat
    """
    
    for client in clients_connectes:
        
        client.send(msg_recu)
        
