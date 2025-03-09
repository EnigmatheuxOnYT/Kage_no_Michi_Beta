# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 17:38:15 2025

@author: clementroux--benabou
"""


#############
"""Placer le fichier dans le même dossier que le reste des fichiers python"""
#############


import pygame
from Cinematics import Cinematics
from Audio import Music,Sound
from Fight import Fight
from Fight_assets import Fight_assets

class minigm_tutofight :
    
    def __init__ (self):
        ### Etats du mini-jeu ###
        
        #Si le jeu tourne
        self.running = True
        
        #Si le mini-jeu est entrain d'âtre joué
        self.playing = False
        
        #Si la phase de gameplay (entre l'intro et la fin) est active
        self.in_minigm = False
        
        ### Appel de la classe cinématique, on utilisera principalement self.cin.cinematic_frame() et self.cin.cinematics_bgs
        self.cin = Cinematics()
        self.fight = Fight()
        self.fight_assets = Fight_assets()
        
        ### Appel des classes pour l'audio, on utilisera principalement la fonction play() et les variables (aller voir le fichier)
        self.music,self.sound = Music(),Sound()
        
     
    ########## Démarrage du mini-jeu ##########
    def load (self):
        self.playing = True
        self.load_assets()
        self.fight.load ('mgm1',self.fight_assets.Musashi,[],[self.fight_assets.guerrier_takahiro],1)
     
    def load_assets(self):
        # Importer les images, sons etc.. ici (depuis "../data/assets")
        
        
        ### Importation de la police d'écriture (taille des textes des dialogues)
        self.font_MFMG30 = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf",30)
     
    ########## Intro/Fin ##########
    def intro(self,screen,saved):
        #Appeler ici la fonction self.cin.cinematic_frame()
        #Exemple d'utilisation que vous pouvez copier coller (attention, TOUJOURS finir l'appel par running=self.running):
        
        self.cin.ecran_noir(screen)
        self.cin.cinematic_frame(screen,'ine1',3,"Bonjour Sensei Hoshida.", "Merci encore une fois de m'avoir accepté en tant que disciple.", kind_info=[["SM","no_weapon"],[saved,"no_weapon"],["SH","no_weapon"],1],running=self.running)
        if saved == 'none':
            self.cin.cinematic_frame(screen,'ine1',3,"Rien n'est encore gagné, l'entraînement ne fait que de commencer.", kind_info=[["SM","no_weapon"],[saved,"no_weapon"],["SH","no_weapon"],3],running=self.running)
        if saved == 'KM':
            self.cin.cinematic_frame(screen,'ine1',3,"Bonjour à vous Sensei Hoshida.", "Je suis très reconnaissant de l'entraînement que vous offrez à mon grand frère!", kind_info=[[saved,"no_weapon"],["SM","no_weapon"],["SH","no_weapon"],1,True],running=self.running)
            self.cin.cinematic_frame(screen,'ine1',3,"Je vois que vous êtes tous les deux en bonne forme.","C'est un très bon signe. Musashi, il est l'heure de l'entraînement.", kind_info=[[saved,"no_weapon"],["SM","no_weapon"],["SH","no_weapon"],3],running=self.running)
            self.cin.cinematic_frame(screen,'ine1',3,"Oui Maître !", kind_info=[["SM","no_weapon"],[saved,"no_weapon"],["SH","no_weapon"],1,True],running=self.running)
        elif saved == 'KT':
            self.cin.cinematic_frame(screen,'ine1',3,"Salutations Maître.", "Moi et Musashi sommes prêts à endurer vos entraînements pour notre village.", kind_info=[[saved,"no_weapon"],["SM","no_weapon"],["SH","no_weapon"],1,True],running=self.running)
            self.cin.cinematic_frame(screen,'ine1',3,"Voilà 2 élèves prometteurs qui sont dignes pour mes enseignements.", "Suivez-moi, on va commencer l'entraînement d'ici peu.", kind_info=[[saved,"no_weapon"],["SM","no_weapon"],["SH","no_weapon"],3],running=self.running)
            self.cin.cinematic_frame(screen,'ine1',3,"Oui Maître !", kind_info=[[saved,"no_weapon"],["SM","no_weapon"],["SH","no_weapon"],1],running=self.running)
            self.cin.cinematic_frame(screen,'ine1',3,"Oui Maître !", kind_info=[["SM","no_weapon"],[saved,"no_weapon"],["SH","no_weapon"],1,True],running=self.running)
        self.cin.cinematic_frame(screen,'ine1',3,"(Tout à coup, Musashi se remémore un souvenir de son enfance)", kind_info=[["SM","no_weapon"],[saved,"no_weapon"],["SH","no_weapon"],0],running=self.running)
        self.cin.ecran_noir(screen)
        self.cin.cinematic_frame(screen,'mgm1',2,"Souvenez-vous que le combat se fait non seulement pour vaincre son ennemi,","mais pour lui octroyer respect et reconnaissance.",kind_info=[["SM","no_weapon"],["DY","no_weapon"],2])
        self.cin.cinematic_frame(screen,'mgm1',2,"Vous allez affronter de nombreux obstacles lors de vos péripéties,", "et il est important que vous gardiez en tête mes enseignements", "pour que vous puissiez vous défendre.",kind_info=[["SM","no_weapon"],["DY","no_weapon"],2])
        self.cin.cinematic_frame(screen,'mgm1',2,"Très bien. Musashi, fait nous une démonstration de ce que tu as appris", "jusqu'ici.",kind_info=[["SM","no_weapon"],["DY","no_weapon"],2])
        self.cin.cinematic_frame(screen,'mgm1',2,"Éliminez vos adversaires en utilisant votre attaque frontale et spéciale !", "Régénérez-vous de 30 PV avec vos potions de soin à disposition !", kind_info=[["SM","no_weapon"],["DY","no_weapon"],0])
        
        #À la toute fin de la fonction
        self.in_minigm = True
    
    def end(self,screen):
        #Appeler ici la fonction self.cin.cinematic_frame()
        
        
        #À la toute fin de la fonction
        self.playing = False
         
    ########## Partie 1 : évènements ##########
    def minigm_events (self):
        #Poser les évènements vérifiés dans la suite de la boucle for
        for event in pygame.event.get():
            #Vérification de la fermeture du jeu
            if event.type == pygame.QUIT:
                self.running = False
            pygame.event.post(event)
        
        self.fight.handle_imput()
        

        
    
    
    ########## Partie 2 : Mise à jour ##########
    def minigm_update (self):
        self.fight.update()
    
    
    ########## Partie 3 : Affichage ##########
    def minigm_draw (self,screen):
        #Remplissage avec du noir (fond)
        self.fight.draw(screen)
   
    ########## Boucle mini-jeu ##########
    def run (self,screen,saved='none',devomde=False):
        #L'argument saved permet de savoir quelle version de l'intro et de la fin afficher en fonction de qui a été sauvé. Il permet aussi d'afficher le bon sprite dans le mini-jeu le cas échéant 
        
        self.load()
        self.intro(screen,saved)
        
        while self.playing and self.running and self.in_minigm and self.fight.continuer:
            self.minigm_events()
            self.minigm_update()
            self.minigm_draw(screen)
            pygame.time.Clock().tick(60)
            
        if self.playing and self.running:
            self.end(screen)
        
        return self.running

#Lancement du mini-jeu
if __name__ == '__main__':
    pygame.init()
    
    icon = pygame.image.load("../data/assets/common/Icone_LOGO_V12.ico")
    pygame.display.set_icon(icon)
    cursor = pygame.image.load("../data/assets/common/Souris_V4.png")
    pygame.mouse.set_cursor((5,5),cursor)
    screen = pygame.display.set_mode((1280,720))
    pygame.display.set_caption("Kage no michi")
    
    minigm = minigm_tutofight()
    minigm.run(screen)
    pygame.quit()
    