# -*- coding: UTF-8 -*-

# Import des librairies

import socket
from threading import Thread
import sys
from Tkinter import *


# Définition des classes

class Interface(Frame):
    """
        Classe qui permet de définir l'interface du tchat côté client
    """
    
    def __init__(self, fenetre, connexion_miaou):
        """
            Constructeur de la classe
        """
        
        # Définition de la fenêtre d'interface
        
        Frame.__init__(self, fenetre, width = 250, height = 500)
        self.pack(fill = BOTH)
        
        
        # Socket du client
        
        self.connexion_miaou = connexion_miaou
        
        
        # Création de la zone de réception des messages - widget Text
        
        self.reception_msg = Text(self, state = DISABLED)
        self.reception_msg.grid(row = 0)
        
        
        # Création de la zone de saisie des messages - widget Entry
        
        # self.var_saisie_msg = StringVar()
        # self.saisie_msg = Entry(self, textvariable = self.var_saisie_msg)
        # self.saisie_msg.grid(row = 1, sticky = "we")
        # self.saisie_msg.bind("<Return>", self.envoi)
        
        self.saisie_msg = Entry(self)
        self.saisie_msg.grid(row = 1, sticky = "we")
        self.var_saisie_msg = self.saisie_msg.get()
        self.saisie_msg.bind("<Return>", self.envoi)
        
        
        # Création du bouton pour quitter le tchat - widget Button
        
        self.bouton_quitter = Button(self, text = "Quitter", command = self.quit)
        self.bouton_quitter.grid(row = 2)
        
        
        # Définition des thread
        
        # # # self.msg = self.connexion_miaou.recv(1024)
        
        # # # if self.msg == b"fin":
            
            # # # self.statut_client = False
            
        # # # self.saisie_msg.insert(1, self.msg.decode())
        
        # self.TRM = ReceptionMessage(self.connexion_miaou)
        # self.statut_client = self.TRM.statut_client
        # self.TRM.start()
        
        # self.TEM = EnvoiMessage(self.connexion_miaou)
        # self.TEM.start()
        
    
    def envoi(self, event):
        """
            Méthode qui permet d'envoyer des messages saisi par l'utilisateur
        """
        
        # print(">>> {}".format(self.var_saisie_msg))
        # self.saisie_msg.delete(0, END)
        # self.var_saisie_msg_str = str(self.var_saisie_msg)
        # self.msg_encode = self.var_saisie_msg_str.encode()
        # self.connexion_miaou.send(self.msg_encode)
        
        print(">>> {}".format(self.var_saisie_msg))
        self.saisie_msg.delete(0, END)
        self.msg_encode = self.var_saisie_msg.encode()
        self.connexion_miaou.send(self.msg_encode)
        

class ReceptionMessage(Thread):
    """
        Classe qui permet de gérer la réception des messages
    """
    
    def __init__(self, connexion_miaou):
        """
            Constructeur de la classe
        """
        
        Thread.__init__(self)
        self.connexion_miaou = connexion_miaou
        self.statut_client = True
        
    
    def run(self):
        """
            Méthode lancée à l'exécution du thread
        """
        
        self.msg = self.connexion_miaou.recv(1024)
        
        if self.msg == b"fin":
            
            self.statut_client = False
            
        sys.stdout.write(">> {}".format(self.msg.decode()))
        
        return self.statut_client
        

class EnvoiMessage(Thread):
    """
        Classe qui permet de gérer l'envoi des messages
    """
    
    def __init__(self, connexion_miaou):
        """
            Constructeur de la classe
        """
        
        Thread.__init__(self)
        self.connexion_miaou = connexion_miaou
        
    
    def run(self):
        """
            Méthode lancée à l'exécution du thread
        """
        
        self.saisie = sys.stdin.readline()
        print("1-")
        self.msg_encode = self.saisie.encode()
        connexion_miaou.send(self.msg_encode)
        

# Informations de connexion - hote et port de connexion

hote = 'localhost'
port = 12800


# Création et connexion du client

connexion_miaou = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_miaou.connect((hote, port))
print("Connexion etablie avec le serveur sur le port {}\n".format(port))


# Boucle d'échange avec le serveur

statut_client = True

fenetre = Tk()
interface = Interface(fenetre, connexion_miaou)
interface.mainloop()

# # # while statut_client:
    
    # # # TRM = ReceptionMessage(connexion_miaou)
    # # # statut_client = TRM.statut_client
    # # # TRM.start()
    
    # # # TEM = EnvoiMessage(connexion_miaou)
    # # # TEM.start()
    
    # saisie = sys.stdin.readline()
    # msg_encode = saisie.encode()
    # connexion_miaou.send(msg_encode)
    

interface.destroy()    


# Fermeture de la connexion client

connexion_miaou.close()


# "C:\Python27\Lib\idlelib\idle.bat" "$(FULL_CURRENT_PATH)"

