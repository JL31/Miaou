# -*- coding: UTF-8 -*-

def envoi_all(connexion_client, msg_recu):
	"""
		Fonction pour transférer un message à tous les utilisateurs du chat
	"""
	
	for client in clients_com:
		
		client.send(msg_recu)
		
