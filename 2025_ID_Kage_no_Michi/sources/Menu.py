#Projet : Kage no Michi
#Auteurs : Alptan Korkmaz, Clément Roux--Bénabou, Maxime Rousseaux, Ahmed-Adam Rezkallah, Cyril Zhao


# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 20:29:01 2025

@author: clementroux--benabou
"""

import pygame
import random
from Savemgr import Savemgr
from Audio import Music,Sound
from credits.credits_format_py import credits

class Menu:
    
    def __init__ (self):
        self.savemgr = Savemgr()
        self.music = Music()
        self.sound = Sound()
        self.clicked_savefile = [False,0]
        self.mouse_on_button = {'play':False, 'settings':False, 'credits':False, 'quit':False, 'cancel':False, 'load':False, 'save':False, 'OK':False, 'delete(save)':False, 'cancel(delete)':False, 'delete(delete)':False}
        self.random_background = random.randint(1,4)
        
        ########## Importation des assets du menu et création des Rect correspnodants ##########
        ##### Menu principal #####
        ## Fond d'écran et logo ##
        if self.random_background == 1:
            self.menu_image = pygame.image.load("../data/assets/bgs/Fond_Menu_V1_1280p.png").convert()
        elif self.random_background == 2:
            self.menu_image = pygame.image.load("../data/assets/bgs/Fond_Menu_V2_1280p.png").convert()
        elif self.random_background == 3:
            self.menu_image = pygame.image.load("../data/assets/bgs/Fond_Menu_V3_1280p.png").convert()
        else:
            self.menu_image = pygame.image.load("../data/assets/bgs/Fond_Menu_V4_1280p.png").convert()
        self.logo_menu = pygame.image.load("../data/assets/menu/Title_V19_667p.png").convert_alpha()
        self.rect_menu_image = pygame.Rect(0,0,1280,720)
        self.rect_logo_menu = pygame.Rect(306,0,667,274)

        ## Boutons ##
        self.button_green_bg = pygame.image.load("../data/assets/buttons/Fond_Bouton_VERT_165p.png").convert_alpha()
        self.button_dgreen_bg = pygame.image.load("../data/assets/buttons/Fond_Bouton_VERTF_165p.png").convert_alpha()
        self.rect_button_play = pygame.Rect(557.5,333,165,60)
        self.rect_button_settings = pygame.Rect(557.5,408,165,60)
        self.rect_button_credits = pygame.Rect(557.5,483,165,60)
        self.button_red_bg = pygame.image.load("../data/assets/buttons/Fond_Bouton_ROUGE_165p.png").convert_alpha()
        self.button_dred_bg = pygame.image.load("../data/assets/buttons/Fond_Bouton_ROUGEF_165p.png").convert_alpha()
        self.rect_button_quit = pygame.Rect(557.5,558,165,60)
        ## Nuages ##
        self.menu_nuage1 = pygame.image.load("../data/assets/menu/Nuage_V3(2).png").convert_alpha()
        self.rect_nuage1 = pygame.Rect(-600,200,291,145)
        self.menu_nuage2 = pygame.image.load("../data/assets/menu/Nuage_V3(2).png").convert_alpha()
        self.rect_nuage2 = pygame.Rect(1280,40,291,145)
        self.menu_nuage3 = pygame.image.load("../data/assets/menu/Nuage_V3(2).png").convert_alpha()
        self.rect_nuage3 = pygame.Rect(1000,300,291,145)
        ##### Interfaces des menus #####
        ## Fond ##
        self.menu_save_background = pygame.image.load("../data/assets/menu/Fond_Menu_Sauvegarde.png").convert_alpha()
        self.rect_save_background = pygame.Rect(131,73,1018,573)
        self.menu_save_savefiles = pygame.image.load("../data/assets/menu/Emplacements_Menu_Sauvegarde_V2.png").convert_alpha()
        self.rect_save_savefiles_bg = pygame.Rect(131,73,1018,573)
        self.rect_save_savefiles = [pygame.Rect(228,134,192,378),pygame.Rect(438,134,192,378),pygame.Rect(648,134,192,378),pygame.Rect(858,134,200,379)]
        self.menu_save_delete_file_bg = pygame.image.load("../data/assets/menu/Interface_Suppression_Sauvegarde_V1.png").convert_alpha()
        self.rect_save_delete_file = pygame.Rect(440,210,400,300)
        ## 'Curseur' de sauvegarde ##
        self.menu_save_bordure = pygame.image.load("../data/assets/menu/Bordure_sauvegardes.png").convert_alpha()
        ## Boutons ##
        self.button_blue_bg = pygame.image.load("../data/assets/buttons/Fond_Bouton_BLEU_165p.png").convert_alpha()
        self.button_dblue_bg = pygame.image.load("../data/assets/buttons/Fond_Bouton_BLEUF_165p.png").convert_alpha()
        self.button_grey_bg = pygame.image.load("../data/assets/buttons/Fond_Bouton_GRIS_165p.png").convert_alpha()
        self.rect_save_button_load = pygame.Rect(228,524,165,60)
        self.rect_save_button_delete = pygame.Rect(557.5,524,165,60)
        self.rect_delete_button_delete = pygame.Rect(470,400,165,60)
        self.rect_delete_button_cancel = pygame.Rect(645,400,165,60)
        self.rect_settings_button_save = pygame.Rect(228,524,165,60)
        self.rect_credits_button_OK = pygame.Rect(228,524,165,60)
        self.rect_menus_button_cancel = pygame.Rect(887,524,165,60)
        
        ########## Polices de caractères ##########
        ##### Importation des Polices de caractères #####
        self.font_MFMG27 = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf",27)
        self.font_MFMG20 = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf",20)
        self.font_MFMG15 = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf",15)
        ##### Textes #####
        ## Boutons ##
        self.text_button_play = self.font_MFMG27.render("Jouer",False,(0,0,0))
        self.text_button_settings = self.font_MFMG27.render("Options",False,(0,0,0))
        self.text_button_credits = self.font_MFMG27.render("Crédits",False,(0,0,0))
        self.text_button_quit = self.font_MFMG27.render("Quitter",False,(0,0,0))
        self.text_button_load = self.font_MFMG27.render("Charger",False,(0,0,0))
        self.text_button_delete = self.font_MFMG27.render("Supprimer",False,(0,0,0))
        self.text_button_save = self.font_MFMG27.render("Sauvegarder",False,(0,0,0))
        self.text_button_OK = self.font_MFMG27.render("OK",False,(0,0,0))
        self.text_button_cancel = self.font_MFMG27.render("Annuler",False,(0,0,0))

        ## Crédits ##

        self.credits_text=[]
        for ligne in credits.split("/n"):
            self.credits_text.append(self.font_MFMG15.render(ligne,False,"black"))
        self.current_credits_y_offset=0
        
        
    ############### Chargement ###############
    
    def load_menu (self,running,loading_menu, in_menu, in_main_menu):
        saves_states = self.savemgr.check_saves()
        if saves_states == (True,True,True,True,True):
            self.load_savefiles_for_menu()
            ##### Musique #####
            self.music.play(self.music.menu,500)
            
            loading_menu = False
            in_menu = True
            in_main_menu = True
            #print("menu chargé")
            return running,loading_menu, in_menu, in_main_menu
        elif saves_states[0]:
            print("Fichier de sauvegardes vide, recréation des sauvegades (vides).")
            self.savemgr.rebuild_saves(saves_states[1:5])
            return False,False,False,False
        else:
            print("Pas de dossier de sauvegarde, recréation du dossier avec les sauvegardes (vides).")
            self.savemgr.rebuild_folder()
            return False,False,False,False

    def load_savefiles_for_menu (self):
        ##### Importation des données de sauvegarde pour les afficher #####
        self.save_data_for_menu = [self.savemgr.load(f"../data/saves/save{save}.json") for save in range(4)]
        ##### Affichage des sauvegardes #####
        self.text_saves_main = [self.font_MFMG20.render(f"Sauvegarde {save}",False,(0,0,0)) for save in range(4)]
        self.text_saves_chapter = [self.font_MFMG15.render(f"Chapitre {self.save_data_for_menu[save]['scene'][0]}",False,(0,0,0)) for save in range(4)]
        self.text_saves_episode = [self.font_MFMG15.render(f"Épisode {self.save_data_for_menu[save]['scene'][1]}",False,(0,0,0)) for save in range(4)]
        self.text_saves_level = [self.font_MFMG15.render(f"Niveau {self.save_data_for_menu[save]['tpt']['main'][5] if self.save_data_for_menu[save]['tpt']!=None else 0}",False,(0,0,0)) for save in range(4)]
        self.text_saves_blank = self.font_MFMG15.render("Nouvelle Sauvegarde",False,(0,0,0))
        
    ############### Partie 1 ###############
            
    def main_menu (self, running):
        in_main_menu = True
        in_save_choice = False
        in_settings = False
        in_credits = False
        ########## Traitement des imputs du joueur dans le menu (partie 1) ##########
        if in_main_menu:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    ##### Son #####
                    self.sound.play(self.sound.click)
                    ##### Détection du bouton cliqué #####
                    if self.rect_button_quit.collidepoint(pygame.mouse.get_pos()):
                        print("Jeu quitté")
                        running = False
                    elif self.rect_button_play.collidepoint(pygame.mouse.get_pos()):
                        in_main_menu = False
                        in_save_choice = True
                        self.clicked_savefile = [False,0]
                    elif self.rect_button_settings.collidepoint(pygame.mouse.get_pos()):
                        in_main_menu = False
                        in_settings = True
                        print ("Options lancées")
                    elif self.rect_button_credits.collidepoint(pygame.mouse.get_pos()):
                        in_main_menu = False
                        in_credits = True
                        self.current_credits_y_offset=0
                        print ("Crédits lancés")
        return running,in_main_menu,in_save_choice,in_settings,in_credits
    
    def save_choice (self):
        in_menu = True
        in_main_menu = False
        in_save_choice = True
        in_delete_file = False
        loading_save = False
        
        mouse_pos = pygame.mouse.get_pos()
        ########## Traitement des imputs du joueur dans l'interface de choix de sauvegarde (partie 1) ##########
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                ##### Son #####
                self.sound.play(self.sound.click)
                ##### sauvegardes cliquées #####
                if self.rect_save_savefiles[0].collidepoint(mouse_pos):
                    if self.clicked_savefile == [True,0]:
                        self.clicked_savefile = [False,0]
                    else:
                        self.clicked_savefile = [True,0]
                elif self.rect_save_savefiles[1].collidepoint(mouse_pos):
                    if self.clicked_savefile == [True,1]:
                        self.clicked_savefile = [False,1]
                    else:
                        self.clicked_savefile = [True,1]
                elif self.rect_save_savefiles[2].collidepoint(mouse_pos):
                    if self.clicked_savefile == [True,2]:
                        self.clicked_savefile = [False,2]
                    else:
                        self.clicked_savefile = [True,2]
                elif self.rect_save_savefiles[3].collidepoint(mouse_pos):
                    if self.clicked_savefile == [True,3]:
                        self.clicked_savefile = [False,3]
                    else:
                        self.clicked_savefile = [True,3]
                ##### Boutons #####
                elif self.rect_menus_button_cancel.collidepoint(mouse_pos):
                    in_save_choice = False
                    in_main_menu = True
                elif self.clicked_savefile[0]:
                    if self.rect_save_button_load.collidepoint(mouse_pos):
                        #pygame.mixer.music.fadeout(500)
                        in_menu = False
                        in_save_choice = False
                        loading_save = True
                    elif self.rect_save_button_delete.collidepoint(mouse_pos) and ((not self.save_data_for_menu[self.clicked_savefile[1]]['blank']) or self.clicked_savefile[1] == 0):
                        in_delete_file = True
        return self.clicked_savefile[1],in_menu,in_main_menu,in_save_choice, in_delete_file,loading_save
        
    def delete_file (self):
        in_delete_file = True
        ##### Interface de confirmation de suppression de sauvegarde #####
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                ##### Son #####
                self.sound.play(self.sound.click)
                ##### Détection du bouton cliqué #####
                if self.rect_delete_button_cancel.collidepoint(pygame.mouse.get_pos()):
                    in_delete_file = False
                elif self.rect_delete_button_delete.collidepoint(pygame.mouse.get_pos()):
                    self.savemgr.save(self.savemgr.generic_blank_file, f"../data/saves/save{self.clicked_savefile[1]}.json")
                    in_delete_file = False
                    self.load_savefiles_for_menu()
        return in_delete_file
    
    def settings (self):
        in_main_menu = False
        in_settings = True
        ########## Traitement des imputs du joueur dans les options (partie 1) ##########
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                ##### Son #####
                self.sound.play(self.sound.click)
                ##### Détection du bouton cliqué #####
                if self.rect_menus_button_cancel.collidepoint(pygame.mouse.get_pos()):
                    in_settings = False
                    in_main_menu = True
                elif self.rect_settings_button_save.collidepoint(pygame.mouse.get_pos()):
                    in_settings = False
                    in_main_menu = True
        return in_main_menu,in_settings
        
    def credits (self):
        in_main_menu = False
        in_credits = True
        ########## Traitement des imputs du joueur dans les crédits (partie 1) ##########
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                ##### Son #####
                self.sound.play(self.sound.click)
                ##### Détection du bouton cliqué #####
                if self.rect_credits_button_OK.collidepoint(pygame.mouse.get_pos()):
                    in_credits = False
                    in_main_menu = True
        return in_main_menu,in_credits
    
        
    
    ############### Partie 2 ###############
    
    def cloud_move (self):
        ########## Gestion du déplaement des nuages (partie 2) ##########
        if self.rect_nuage1.left >= 1280:
            self.rect_nuage1.right = 0
            self.rect_nuage1.top = random.randrange(0,300)
        else:
            self.rect_nuage1.move_ip(2,0)
        
        if self.rect_nuage2.right <= 0:
            self.rect_nuage2.left = 1280
            self.rect_nuage2.top = random.randrange(0,300)
        else:
            self.rect_nuage2.move_ip(-1,0)
        
        if self.rect_nuage3.right <= 0:
            self.rect_nuage3.left = 1280
            self.rect_nuage3.top = random.randrange(0,300)
        else:
            self.rect_nuage3.move_ip(-2,0)
    
    def main_menu_update (self):
        ########## Mise à jour des éléments du menu à afficher (partie 2) ##########
        if self.rect_button_quit.collidepoint(pygame.mouse.get_pos()):
            self.mouse_on_button['quit'] = True
        else:
            self.mouse_on_button['quit'] = False
        if self.rect_button_play.collidepoint(pygame.mouse.get_pos()):
            self.mouse_on_button['play'] = True
        else:
            self.mouse_on_button['play'] = False
        if self.rect_button_settings.collidepoint(pygame.mouse.get_pos()):
            self.mouse_on_button['settings'] = True
        else:
            self.mouse_on_button['settings'] = False
        if self.rect_button_credits.collidepoint(pygame.mouse.get_pos()):
            self.mouse_on_button['credits'] = True
        else:
            self.mouse_on_button['credits'] = False
    
    def save_choice_update (self):
        ########## Mise à jour des éléments de l'interface de choix de sauvegarde à afficher (partie 2) ##########
        if self.rect_menus_button_cancel.collidepoint(pygame.mouse.get_pos()):
            self.mouse_on_button['cancel'] = True
        elif self.rect_save_button_delete.collidepoint(pygame.mouse.get_pos()):
            self.mouse_on_button['delete(save)'] = True
        elif self.rect_save_button_load.collidepoint(pygame.mouse.get_pos()):
            self.mouse_on_button['load'] = True
        else:
            self.mouse_on_button['cancel'],self.mouse_on_button['delete(save)'],self.mouse_on_button['load'] = False,False,False

    def delete_file_update (self):
        if self.rect_delete_button_cancel.collidepoint(pygame.mouse.get_pos()):
            self.mouse_on_button['cancel(delete)'] = True
        else:
            self.mouse_on_button['cancel(delete)'] = False
        
        if self.rect_delete_button_delete.collidepoint(pygame.mouse.get_pos()):
            self.mouse_on_button['delete(delete)'] = True
        else:
            self.mouse_on_button['delete(delete)'] = False
    
    def settings_update (self):
        ########## Mise à jour des éléments des options à afficher (partie 2) ##########
        if self.rect_menus_button_cancel.collidepoint(pygame.mouse.get_pos()):
            self.mouse_on_button['cancel'] = True
        elif self.rect_settings_button_save.collidepoint(pygame.mouse.get_pos()):
            self.mouse_on_button['save'] = True
        else:
            self.mouse_on_button['cancel'], self.mouse_on_button['save'] = False,False
            

    def credits_update (self):
        ########## Mise à jour des éléments des crédits à afficher (partie 2) ##########
        if self.rect_credits_button_OK.collidepoint(pygame.mouse.get_pos()):
            self.mouse_on_button['OK'] = True
        else:
             self.mouse_on_button['OK'] = False

    
    ############### Partie 3 ###############
    
    def draw_menu(self, screen, in_main_menu, in_save_choice, in_delete_file, in_settings, in_credits):
        ########## Dessin du menu (partie 3) ##########
        screen.blit(self.menu_image, self.rect_menu_image)
        screen.blit(self.menu_nuage1, self.rect_nuage1)
        screen.blit(self.menu_nuage2, self.rect_nuage2)
        screen.blit(self.menu_nuage3, self.rect_nuage3)
        if in_main_menu:
            self.draw_main_menu(screen)
        elif in_save_choice:
            if not in_delete_file:
                self.draw_save_choice(screen)
            else:
                self.draw_delete_file(screen)
        elif in_settings:
            self.draw_settings(screen)
        elif in_credits:
            self.draw_credits(screen)
            
    def draw_main_menu (self, screen):
        ########## Dessin du menu principal (partie 3) ##########

        screen.blit(self.logo_menu, self.rect_logo_menu)
        if self.mouse_on_button['play']:
            screen.blit(self.button_dgreen_bg, self.rect_button_play)
        else:
            screen.blit(self.button_green_bg, self.rect_button_play)
        screen.blit(self.text_button_play,pygame.Rect(604,351,150,20))
        if self.mouse_on_button['settings']:
            screen.blit(self.button_dgreen_bg, self.rect_button_settings)
        else:
            screen.blit(self.button_green_bg, self.rect_button_settings)
        screen.blit(self.text_button_settings,pygame.Rect(592,426,150,20))
        if self.mouse_on_button['credits']:
            screen.blit(self.button_dgreen_bg, self.rect_button_credits)

        else:
            screen.blit(self.button_green_bg, self.rect_button_credits)
        screen.blit(self.text_button_credits,pygame.Rect(592,500,150,20))
        if self.mouse_on_button['quit']:
            screen.blit(self.button_dred_bg, pygame.Rect(559,559,165,60))
        else:
            screen.blit(self.button_red_bg, self.rect_button_quit)
        screen.blit(self.text_button_quit,pygame.Rect(592,574,150,20))
        
    def draw_save_choice (self, screen):
        ########## Dessin de l'interface de choix de sauvegarde (partie 3) ##########
        
        
        screen.blit(self.menu_save_background,self.rect_save_background)
        
        screen.blit(self.menu_save_savefiles,self.rect_save_savefiles_bg)
        
        
        if self.mouse_on_button['cancel']:
            screen.blit(self.button_dblue_bg,pygame.Rect(888.5,525.5,165,60))
        else:
            screen.blit(self.button_blue_bg,self.rect_menus_button_cancel)
        screen.blit(self.text_button_cancel,pygame.Rect(922,540,150,20))
        if self.clicked_savefile[0]:
            if self.mouse_on_button['load']:
                screen.blit(self.button_dgreen_bg,self.rect_save_button_load)
            else:
                screen.blit(self.button_green_bg,self.rect_save_button_load)
            if ((not self.save_data_for_menu[self.clicked_savefile[1]]['blank']) or self.clicked_savefile[1] == 0):
                if self.mouse_on_button['delete(save)']:
                    screen.blit(self.button_dred_bg,pygame.Rect(559,525.5,165,60))
                else:
                    screen.blit(self.button_red_bg,self.rect_save_button_delete)
            else:
                screen.blit(self.button_grey_bg,self.rect_save_button_delete)
        else:
            screen.blit(self.button_grey_bg,self.rect_save_button_load)
            screen.blit(self.button_grey_bg,self.rect_save_button_delete)
        screen.blit(self.text_button_delete,pygame.Rect(577,540,150,20))
        screen.blit(self.text_button_load,pygame.Rect(263,540,150,20))
        for save in range(4):
            screen.blit(self.text_saves_main[save],pygame.Rect(267+int(save*210),189,150,20))
            if self.save_data_for_menu[save]['blank']:
                screen.blit(self.text_saves_blank,pygame.Rect(252+int(save*210),273,150,20))
            else:
                screen.blit(self.text_saves_chapter[save],pygame.Rect(285+int(save*210),273,150,20))
                screen.blit(self.text_saves_episode[save],pygame.Rect(289+int(save*210),293,150,20))
                screen.blit(self.text_saves_level[save],pygame.Rect(293+int(save*210),313,150,20))
        if self.clicked_savefile[0]:
            screen.blit(self.menu_save_bordure,self.rect_save_savefiles[self.clicked_savefile[1]])
    
    def draw_delete_file (self,screen):
        ########## Dessin de l'interface de suppression de sauvegarde (partie 3) ##########
        screen.blit(self.menu_save_delete_file_bg,self.rect_save_delete_file)
        screen.blit(self.font_MFMG20.render(f"Supprimer la sauvegarde {self.clicked_savefile[1]} ?",False,(0,0,0)),pygame.Rect(505,300,300,50))
        if self.mouse_on_button['cancel(delete)']:
            screen.blit(self.button_dblue_bg, pygame.Rect(646.5,401.5,165,60))
        else:
            screen.blit(self.button_blue_bg, self.rect_delete_button_cancel)

        if self.mouse_on_button['delete(delete)']:
            screen.blit(self.button_dred_bg, pygame.Rect(471.5,401.5,165,60))
        else:
            screen.blit(self.button_red_bg, self.rect_delete_button_delete)
        screen.blit(self.text_button_cancel,pygame.Rect(680,416,150,20))
        screen.blit(self.text_button_delete,pygame.Rect(489.5,416,150,20))
    
    
    def draw_settings (self, screen):
        ########## Dessin des options (partie 3) ##########

        screen.blit(self.menu_save_background,self.rect_save_background)
        if self.mouse_on_button['cancel']:
            screen.blit(self.button_dblue_bg,pygame.Rect(888.5,525.5,165,60))
        else:
            screen.blit(self.button_blue_bg,self.rect_menus_button_cancel)
        screen.blit(self.text_button_cancel,pygame.Rect(922,540,150,20))
        if self.mouse_on_button['save']:
            screen.blit(self.button_dgreen_bg,self.rect_settings_button_save)
        else:
            screen.blit(self.button_green_bg,self.rect_settings_button_save)
        screen.blit(self.text_button_save,pygame.Rect(234,540,150,20))
    

    def get_credits_surface (self):
        surf = pygame.image.load("../data/assets/menu/Fond_Menu_Vide.png").convert_alpha()
        x,y=260,480-self.current_credits_y_offset
        for ligne in self.credits_text:
            surf.blit(ligne,(x,y))
            y+=15
        if y<-15:
            self.current_credits_y_offset=0
        self.current_credits_y_offset+=0.5
        return surf

    def draw_credits (self, screen):
        ########## Dessin des crédits (partie 3) ##########

        screen.blit(self.menu_save_background,self.rect_save_background)

        screen.blit(self.get_credits_surface(),(131,121))
        
        if self.mouse_on_button['OK']:
            screen.blit(self.button_dgreen_bg,self.rect_credits_button_OK)
        else:
            screen.blit(self.button_green_bg,self.rect_credits_button_OK)
        screen.blit(self.text_button_OK,pygame.Rect(295,540,150,20))
