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

class minigm_memory :
    
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
        
        ### Appel des classes pour l'audio, on utilisera principalement la fonction play() et les variables (aller voir le fichier)
        self.music,self.sound = Music(),Sound()
        
     
    ########## Démarrage du mini-jeu ##########
    def load (self):
        self.playing = True
        self.load_assets()
     
    def load_assets(self):
        # Importer les images, sons etc.. ici (depuis "../data/assets")
        
        
        ### Importation de la police d'écriture (taille des textes des dialogues)
        self.font_MFMG30 = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf",30)
     
    ########## Intro/Fin ##########
    def intro(self,screen,saved):
        #Appeler ici la fonction self.cin.cinematic_frame()
        #Exemple d'utilisation que vous pouvez copier coller (attention, TOUJOURS finir l'appel par running=self.running):
        
        self.cin.cinematic_frame(screen,'mgm1',running=self.running)
        
        #À la toute fin de la fonction
        self.in_minigm = True
    
    def end(self,screen,saved):
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
        
        
        #Vérification des touches appuyées
        pressed_keys = pygame.key.get_pressed()
        
        #Vérification de la muise en plein écran
        if pressed_keys[pygame.K_F11]: 
            pygame.display.toggle_fullscreen()
            pygame.time.Clock().tick(5)
        
    
    
    ########## Partie 2 : Mise à jour ##########
    def minigm_update (self):
        pass
    
    
    ########## Partie 3 : Affichage ##########
    def minigm_draw (self,screen):
        #Remplissage avec du noir (fond)
        screen.fill((0,0,0))
        
        #Affichage, utiliser principalement la fonction screen.blit([surface à afficher],[ractangle dans lequel afficher la surface])
        
        #Mise à jour de l'écran
        pygame.display.flip()
    
   
    ########## Boucle mini-jeu ##########
    def run (self,screen,saved):
        #L'argument saved permet de savoir quelle version de l'intro et de la fin afficher en fonction de qui a été sauvé. Il permet aussi d'afficher le bon sprite dans le mini-jeu le cas échéant 
        
        self.load()
        self.intro(screen,saved)
        
        while self.playing and self.running and self.in_minigm:
            self.minigm_events()
            self.minigm_update()
            self.minigm_draw(screen)
            pygame.time.Clock().tick(60)
            
        if self.playing and self.running:
            self.end(screen,saved)
        
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
    
    minigm = minigm_memory()
    minigm.run(screen, 'KM')
    pygame.quit()
    