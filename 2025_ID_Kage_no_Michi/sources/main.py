#Projet : Kage no Michi
#Auteurs : Alptan Korkmaz, Clément Roux--Bénabou, Maxime Rousseaux, Ahmed-Adam Rezkallah, Cyril Zhao


# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 23:11:45 2025

@author: clementroux--benabou
"""

import Loading
import pygame


class Main:
    
    def __init__ (self, screen):
        ######## Etats du jeu ##########
        self.running = True
        self.displayed = True
        self.loading_menu = True
        self.in_menu = False
        self.in_main_menu = False
        self.in_save_choice = False
        self.in_delete_file = False
        self.in_settings = False
        self.in_credits = False
        self.loading_save = False
        self.in_game = False
        self.in_gameplay = False
        ########## Création de la surface pour l'écran ##########
        self.screen = screen
        ########## Importation du module pygame pour les fps ##########
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        ########## Importation du menu et du jeu ##########
        Loading.display_loading(screen, 30,"Lanncement des modules")
        self.menu = Menu()
        Loading.display_loading(screen, 35,"Lanncement des modules")
        self.game = Game(self.screen)
        Loading.display_loading(screen, 85,"Lanncement des modules")
        self.music = Music()
        
    
    def handling_events(self):
        ########## Traitement des imputs du joueur (partie 1) ##########
        # Non fonctionnel
        #self.displayed = pygame.display.get_active()
        
        if self.running and self.displayed:
            for event in pygame.event.get():
                ##### Vérification de si le jeu est fermé (altF4 ou croix) #####
                if event.type == pygame.QUIT:
                    if self.in_game:
                        self.game.save_savefile()
                    self.running = False
                else:
                    ##### Vérification de la musique #####
                    pygame.event.post(event)
        
            self.pressed_keys = pygame.key.get_pressed()
            if self.pressed_keys[pygame.K_F11]:
                pygame.display.toggle_fullscreen()
                time.sleep(0.2)
        
            ##### Lance la vérification des évènements en fonction de l'état de jeu #####
            if self.in_menu:
                if self.in_main_menu:
                    self.running,self.in_main_menu,self.in_save_choice,self.in_settings,self.in_credits = self.menu.main_menu(self.running)
                elif self.in_save_choice:
                    if not self.in_delete_file:
                        self.game.loaded_save,self.in_menu,self.in_main_menu,self.in_save_choice,self.in_delete_file,self.loading_save = self.menu.save_choice()
                    else:
                        self.in_delete_file = self.menu.delete_file()
                elif self.in_settings:
                    self.in_main_menu,self.in_settings = self.menu.settings()
                elif self.in_credits:
                    self.in_main_menu,self.in_credits = self.menu.credits()
            elif self.in_game:
                self.in_game, self.in_gameplay, self.loading_menu = self.game.game_events(self.in_game, self.in_gameplay, self.loading_menu)
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.in_game:
                        self.game.save_savefile()
                    print("Quitté")                        
                    self.running = False
        
            pygame.event.clear()
        
    def update(self):
        ########## Mise à jour des éléments à afficher (partie 2) ##########
        if self.running and self.displayed:
            if self.loading_menu:
                self.running,self.loading_menu, self.in_menu, self.in_main_menu = self.menu.load_menu(self.running,self.loading_menu, self.in_menu, self.in_main_menu)
            elif self.in_menu:
                self.menu.cloud_move()
                if self.in_main_menu:
                    self.menu.main_menu_update()
                elif self.in_save_choice:
                    if not self.in_delete_file:
                        self.menu.save_choice_update()
                    else:
                        self.menu.delete_file_update()
                elif self.in_settings:
                            self.menu.settings_update()
                elif self.in_credits:
                            self.menu.credits_update()
            elif self.loading_save:
                self.loading_save,self.in_game = self.game.load_save(self.screen,self.loading_save)
                if self.game.loaded_save == 0:
                    self.in_gameplay = True
            elif self.in_game:
                self.in_gameplay = self.game.game_update(self.in_gameplay)
            else:
                #En cas d'état inattendu :
                print("Redémarrage du menu")
                self.loading_menu=True
        
            self.fps_showed = self.game.get_fps_showed()
            if self.fps_showed:
                self.IRT_fps = round(self.clock.get_fps(), 1)
                if self.IRT_fps >= 45:
                    self.fps_color = (0,255,0)
                    self.fps = 60
                elif self.IRT_fps >= 30:
                    self.fps_color = (255,255,0)
                    self.fps = 90
                elif self.IRT_fps >= 20:
                    self.fps_color = (255,127,0)
                    self.fps = 120
                else:
                    self.fps_color = (255,0,0)
                    self.fps = 180
            

    
    def display(self):
        ########## Dessin de l'écran (partie 3) ##########
        do_draw = True
        if self.running and self.displayed:
            self.screen.fill ((0,0,0))
            if self.in_menu :
                self.menu.draw_menu(self.screen,self.in_main_menu,self.in_save_choice,self.in_delete_file,self.in_settings,self.in_credits)
            elif self.in_game :
                do_draw = self.game.game_draw(self.screen,self.in_gameplay)

            if self.fps_showed:
                self.screen.blit(self.menu.font_MFMG15.render(str(self.IRT_fps),False,self.fps_color), pygame.Rect(0,0,50,20))
        if do_draw:
            pygame.display.flip()
    
    
    def run(self):
        ########## Boucle de jeu principale ##########
        while self.running :
            ##### partie 1 #####
            self.handling_events()
            ##### partie 2 #####
            self.update()
            ##### partie 3 #####
            self.display()
            ##### Passage d'une image (modifier la valeur pour changer les fps) #####
            self.clock.tick(self.fps)



if __name__ == "__main__":
    
    ########## Démarrage des modules pygame ##########    
    pygame.init()
    
    ########## Création de la fenêtre (ne pas modifier ou l'écran sera buggé) ##########
    icon = pygame.image.load("../data/assets/common/Icone_LOGO_V12.ico")
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Kage no Michi")
    cursor = pygame.image.load("../data/assets/common/Souris_V4.png")
    pygame.mouse.set_cursor((5,5),cursor)
    screen = pygame.display.set_mode((1280,720))
    
    Loading.display_loading(screen,5,text="Pygame initié")
    ########## Importation des autres modules ##########
    
    import copy
    import time
    Loading.display_loading(screen,10,text="Importation du menu")
    from Menu import Menu
    Loading.display_loading(screen,15,text="Importation du jeu")
    from Game import Game
    Loading.display_loading(screen,20,text="Importation de la musique")
    from Audio import Music
    
    ########## Importation de la classe principale ##########
    Loading.display_loading(screen,25,text="Importation du module principal")
    kage_no_michi = Main(screen)

    ########## Lancement du jeu ##########
    Loading.display_loading(screen,90,text="Lancement")
    kage_no_michi.run()
    
    ########## Fermeture du jeu ##########
    pygame.quit()