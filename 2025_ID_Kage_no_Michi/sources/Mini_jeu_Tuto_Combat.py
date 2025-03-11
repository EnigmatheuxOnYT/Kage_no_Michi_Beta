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

        self.load_assets()


        loops = ['main','hint1',"hint2","hint3","hint4"]
        self.current_loop = 'main'
        self.is_current_loop_launched = False

        self.text1 = self.render("Choisissez l'ennemi à attaquer en cliquant dessus !")
        self.rect1 = self.get_rect(self.text1)
        self.text2 = self.render("Attaquez avec le bouton d'attaque !")
        self.rect2 = self.get_rect(self.text2)
        self.text3 = self.render("Utilisez une potion pour régénérer jusqu'à 30 points de vie !")
        self.rect3 = self.get_rect(self.text3)
        self.text4 = self.render("Utilisez votre attaque spéciale après 4 attaques normales !")
        self.rect4 = self.get_rect(self.text4)

    
    def render(self,text):return self.font_MFMG30.render(text,False,"black")
        
     
    ########## Démarrage du mini-jeu ##########
    def load (self):
        self.playing = True
        self.fight.load ('mgm1',self.fight_assets.Musashi,[],[self.fight_assets.pantin_de_combat],1)
     
    def load_assets(self):
        # Importer les images, sons etc.. ici (depuis "../data/assets")
        
        ### Importation de la police d'écriture (taille des textes des dialogues)
        self.font_MFMG30 = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf",30)
    
    def get_rect(self,text:pygame.surface.Surface):
        rect = text.get_rect()
        rect.midtop = (640,150)
        return rect
     
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
        self.cin.cinematic_frame(screen,'mgm1',2,"Souvenez-vous que le combat se fait non seulement pour vaincre son ennemi,","mais pour lui octroyer respect et reconnaissance.",kind_info=[["MJ","no_weapon"],["DY","no_weapon"],2])
        self.cin.cinematic_frame(screen,'mgm1',2,"Vous allez affronter de nombreux obstacles lors de vos péripéties,", "et il est important que vous gardiez en tête mes enseignements", "pour que vous puissiez vous défendre.",kind_info=[["MJ","no_weapon"],["DY","no_weapon"],2])
        self.cin.cinematic_frame(screen,'mgm1',2,"Très bien. Musashi, fait nous une démonstration de ce que tu as appris", "jusqu'ici.",kind_info=[["MJ","no_weapon"],["DY","no_weapon"],2])
        self.cin.cinematic_frame(screen,'mgm1',2,"Éliminez vos adversaires en utilisant votre attaque frontale et spéciale !", "Régénérez-vous de 30 PV avec vos potions de soin à disposition !", kind_info=[["MJ","no_weapon"],["DY","no_weapon"],0])
        
        #À la toute fin de la fonction
        self.in_minigm = True
    
    def end(self,screen):
        #Appeler ici la fonction self.cin.cinematic_frame()
        self.cin.cinematic_frame(screen,'mgm1',2,"Bravo. Tu as su faire tes preuves et tu as réussi à incorporer cet art en toi.", "Ne l'oublie pas, car tu seras sûrement confronté à un adversaire redoutable.", "Ne baisse jamais les bras.",kind_info=[["MJ","no_weapon"],["DY","no_weapon"],2])
        
        
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
        if self.current_loop == 'main' and not self.is_current_loop_launched :
            if self.fight.tour == 1 and self.fight.action == 'player':
                if not self.fight.is_target_choosen:
                    self.current_loop = 'hint1'
            elif self.fight.tour == 2 and self.fight.action == 'player':
                self.current_loop = 'hint3'
            elif self.fight.tour == 6 and self.fight.action == "player":
                self.current_loop = "hint4"
        if self.current_loop == 'hint1':
            if not self.is_current_loop_launched:
                self.is_current_loop_launched = True
                self.fight.set_allowed_action(False,False,False)
            if self.fight.is_target_choosen:
                self.is_current_loop_launched = False
                self.current_loop = 'hint2'
        if self.current_loop == 'hint2':
            if not self.is_current_loop_launched:
                self.is_current_loop_launched = True
                self.fight.set_allowed_action(True,False,False)
            if self.fight.action == 'ennemies':
                self.is_current_loop_launched = False
                self.current_loop = 'main'
        if self.current_loop == "hint3":
            if not self.is_current_loop_launched:
                self.fight.perso_player.hit(4)
                self.is_current_loop_launched = True
                self.fight.set_allowed_action(False,False,True)
            if self.fight.action == 'ennemies':
                self.is_current_loop_launched = False
                self.current_loop = 'main'
                self.fight.set_allowed_action(True,False,True)
        if self.current_loop == "hint4":
            if not self.is_current_loop_launched:
                self.is_current_loop_launched = True
                self.fight.set_allowed_action(False,True,False)
            if self.fight.action == 'ennemies':
                self.is_current_loop_launched = False
                self.current_loop = 'main'
                self.fight.set_allowed_action(True,True,True)
    
    ########## Partie 3 : Affichage ##########
    def minigm_draw (self,screen):
        #Remplissage avec du noir (fond)
        self.fight.draw(screen,do_refresh=False)
        if self.current_loop == 'hint1':
            screen.blit(self.text1,self.rect1)
        elif self.current_loop == 'hint2':
            screen.blit(self.text2,self.rect2)
        elif self.current_loop == 'hint3':
            screen.blit(self.text3,self.rect3)
        elif self.current_loop == 'hint4':
            screen.blit(self.text4,self.rect4)
        pygame.display.flip()



   
    ########## Boucle mini-jeu ##########
    def run (self,screen,saved='none',devmode=False):
        #L'argument saved permet de savoir quelle version de l'intro et de la fin afficher en fonction de qui a été sauvé. Il permet aussi d'afficher le bon sprite dans le mini-jeu le cas échéant 
        self.devmode = devmode
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
    