# coding: UTF-8

# Import des librairies

import socket
from Tkinter import *


# Définition des classes

class LogginClient(Frame):
    """
        Classe qui va demander le nom à l'utilisateur
    """
    
    def __init__(self, fenetre_loggin, connexion_miaou):
        """
            Constructeur de la classe qui demande le nom à l'utilisateur
        """
        
        Frame.__init__(self, fenetre_loggin, width = 150, height = 100)    # Constructeur de la classe parente
        
        self.fenetre_loggin = fenetre_loggin
        self.fenetre_loggin.title("Choix du loggin")
        
        self.connexion_miaou = connexion_miaou
        self.fenetre = None
        self.interface = None
        
        
        # Création de la zone de message d'information - ce sera un widget Label
        
        self.message_info = Label(fenetre_loggin, text = "Veuillez indiquer votre loggin")
        self.message_info.grid(row = 0)
        
        
        # Création de la zone de saisie du loggin - ce sera un widget Entry
        
        self.loggin_saisi = Entry(fenetre_loggin)
        self.loggin_saisi.grid(row = 1)
        
        
        # Création du bouton qui permet de quitter le tchat - ce sera un widget Button
        
        self.bouton_valider = Button(fenetre_loggin, text = "Valider", command = self.valider)
        self.bouton_valider.grid(row = 3)
        
    
    def valider(self):
        """
            Méthode qui permet de valider le loggin utilisateur
        """
        
        # Récupération du loggin
        
        self.loggin = self.loggin_saisi.get()
        
        
        # Vérification du loggin
        
        if not self.loggin.isalnum():
            
            self.message_info["text"] = "Erreur dans la saisie du loggin, veuillez recommencer"
            self.loggin_saisi.delete(0, END)
            
        else:
            
            self.fenetre_loggin.destroy()
            
            self.fenetre = Tk()
            self.interface = Interface(self.fenetre, self.connexion_miaou, self.loggin)
            self.interface.mainloop()
            

class Interface(Frame):
    """
        Classe de création de la fenêtre de tchat
    """
    
    def __init__(self, fenetre, connexion_miaou, loggin):
        """
            Constructeur de la classe de création de la fenêtre de tchat
        """
        
        # Définition des dimensions de la fenêtre d'interface
        
        Frame.__init__(self, fenetre, width = 250, height = 500)    # Constructeur de la classe parente
        
        self.fenetre = fenetre
        self.fenetre.title(loggin)
        
        self.msg_recu = b""
        self.loggin = loggin
        self.message = ""
        
        
        # Informations de connexion
        
        self.connexion_miaou = connexion_miaou
        
        
        # Création de la zone de lecture - ce sera un widget Text
        
        self.zone_lecture = Text(fenetre, state = DISABLED)
        self.zone_lecture.grid(row = 0)
        
        
        # Création de la zone de saisie de texte - ce sera un widget Entry
        
        self.ligne_texte_saisi = Entry(fenetre)
        self.ligne_texte_saisi.grid(row = 1, sticky = "we")
        self.ligne_texte_saisi.bind("<Return>", self.envoyer)
        
        
        # Création du bouton qui permet de quitter le tchat - ce sera un widget Button
        
        self.bouton_quitter = Button(fenetre, text = "Quitter", command = self.quit)
        self.bouton_quitter.grid(row = 2)
        
        
        # Appel à la méthode d'affichage du contenu du message reçu
        
        self.AMR()
        
    
    def envoyer(self, event):
        """
            Méthode qui permet d'envoyer le message saisi par l'utilisateur
        """
        
        self.msg = self.ligne_texte_saisi.get()
        self.ligne_texte_saisi.delete(0, END)
        
        self.message = "{0} >> {1}".format(self.loggin, self.msg)
        self.connexion_miaou.send(self.message.encode())
        
    
    def AMR(self):
        """
            Méthode qui permet d'afficher le contenu du message reçu dans la zone de réception des messages
        """
        
        # Réception et décodage du message
        
        self.connexion_miaou.setblocking(0)
        
        try:
            
            self.msg_recu = self.connexion_miaou.recv(1024)
            
        except:
            
            pass
            
        
        # Si le mesasge reçu n'est pas vide alors on le décode et on l'ajoute à la zone de réception des messages
        
        if self.msg_recu != b"":
            
            # Décodage du message
            
            self.msg_recu_decode = self.msg_recu.decode()
            
            
            # Affichage du message dans la zone de réception des messages
            
            self.zone_lecture["state"] = "normal"
            self.zone_lecture.insert(END, "{}\n".format(self.msg_recu_decode))
            self.zone_lecture["state"] = "disabled"
            
        
        self.msg_recu = b""
        self.fenetre.after(100, self.AMR)
        

# Informations de connexion - hote et port de connexion

hote = 'localhost'
port = 12800


# Création et connexion du client

connexion_miaou = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_miaou.connect((hote, port))
print("Connexion etablie avec le serveur sur le port {}\n".format(port))


# Création de la fenêtre

fenetre_loggin = Tk ()

loggin_client = LogginClient(fenetre_loggin, connexion_miaou)
loggin_client.mainloop()


# Fermeture de la connexion client

connexion_miaou.close()


# "C:\Python27\Lib\idlelib\idle.bat" "$(FULL_CURRENT_PATH)"

