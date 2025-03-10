#Projet : Kage no Michi
#Auteurs : Alptan Korkmaz, Clément Roux--Bénabou, Maxime Rousseaux, Ahmed-Adam Rezkallah, Cyril Zhao


# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 15:47:37 2025

@author: clementroux--benabou
"""

import pygame
from typing import List,Union
from Characters_sprites import Characters_sprites
from Audio import Music,Sound

class Cinematics:
    def __init__(self):
        self.cinematic_running = True
        self.sprites = Characters_sprites().for_cinematics
        self.music = Music()
        self.sound = Sound()
        self.font_MFMG60 = self.load(60,'MadouFutoMaruGothic','ttf')
        self.font_MFMG30 = self.load(30,'MadouFutoMaruGothic','ttf')
        self.font_MFMG25 = self.load(25,'MadouFutoMaruGothic','ttf')
        self.text_bg = self.load('cinematics','Parchemin_Dialogues_V3')
        self.next_indicator = [self.load('cinematics','Fleche_Gauche_V2'),self.load('cinematics',"Fleche_Droite_V2")]
        self.current_last_letter = [0,0,0]
        self.alpha = 0
        self.lowercase = False
        self.current_font_color = 'black'
        self.is_lowercase_auto_fixed = False
        self.text_bg_rect = pygame.Rect(0,390,1280,330)
        ########## Noms ##########
        self.names = {'none': self.font_MFMG25.render("",False,(0,0,0)),
                      "P" : self.font_MFMG25.render('Pancarte',False,(0,0,0)),
                      'N':  self.font_MFMG30.render("…",False,(0,0,0)),
                      '?': self.font_MFMG25.render("???",False,(0,0,0)),
                      'SM': self.font_MFMG25.render("Shikisha Musashi",False,(0,0,0)),
                      'MJ': self.font_MFMG25.render("Shikisha Musashi",False,(0,0,0)),
                      'SH': self.font_MFMG25.render("Sensei Hoshida",False,(0,0,0)),
                      'SA': self.font_MFMG25.render("Senshi Akuma",False,(0,0,0)),
                      'TK': self.font_MFMG25.render("Takahiro Korijo",False,(0,0,0)),
                      'KM': self.font_MFMG25.render("Keiko musashi",False,(0,0,0)),
                      'KT': self.font_MFMG25.render("Kurosawa Takeshi",False,(0,0,0)),
                      'JM': self.font_MFMG25.render("Jizo Ma",False,(0,0,0)),
                      'Y?': self.font_MFMG25.render("Yoshirō",False,(0,0,0)),
                      'DY': self.font_MFMG25.render("Yoshirō",False,(0,0,0)),
                      'TW': self.font_MFMG25.render("Guerrier Takahiro",False,(0,0,0)),
                      'TW_H': self.font_MFMG25.render("Guerrier Takahiro",False,(0,0,0)),
                      'TWs' : self.font_MFMG25.render("Guerriers Takahiro",False,(0,0,0)),
                      'VL1' : self.font_MFMG25.render("Villageois",False,(0,0,0)),
                      'VL2' : self.font_MFMG25.render("Villageois",False,(0,0,0)),
                      'VL3' : self.font_MFMG25.render("Villageoise",False,(0,0,0)),
                      }
        
        self.rect_names = pygame.Rect(60,460,200,50)
        
        ########## Dictionnaire des fonds de cinématiques ##########
        self.cinematics_bgs = {'forest1': self.load("bgs","Fond_Menu_V2_1280p").convert(),
                               'forest2': self.load("bgs","Fond_Entrée_Forêt_Dense_1").convert(),
                               'forest3':0,
                               'black': pygame.Surface((1280,720)),
                               'bamboo1' : self.load("bgs","Fond_Forêt_Bambou_1").convert(),
                               'bamboo2' : self.load("bgs","Fond_Forêt_Bambou_2").convert(),
                               'bamboo3' : self.load("bgs","Fond_Forêt_Bambou_3").convert(),
                               'bamboo4' : self.load("bgs","Fond_Forêt_Bambou_4").convert(),
                               'bamboo5' : self.load("bgs","Fond_Forêt_Bambou_5").convert(),
                               'village1':self.load("bgs","Fond_Menu_V4_1280p").convert(),
                               'village2':self.load("bgs","Fond_Menu_V1_1280p").convert(),
                               'mgm1' : self.load("bgs","Fond_Magome_Intacte_1").convert(),
                               'mgm2' : self.load("bgs","Fond_Magome_Intacte_2").convert(),
                               'mgm3' : self.load("bgs","Fond_Magome_Intacte_Nuit_1").convert(),
                               'mgm4' : self.load("bgs","Fond_Magome_Intacte_Nuit_2").convert(),
                               'mgm5' : self.load("bgs","Fond_Magome_Detruit_3").convert(),
                               'mgm6' : self.load("bgs","Fond_Magome_Encendres_1").convert(),
                               'mgm7' : self.load("bgs","Fond_Magome_Encendres_2").convert(),
                               'mgm8' : self.load("bgs","Fond_Souvenir_Magome_Jardin_2").convert(),
                               'ine1' : self.load("bgs","Fond_Ine_Dojo_Arene_1").convert(),
                               'doj1' : self.load("bgs","Ine_Dojo_1").convert(),
                               'doj2' : self.load("bgs","Fond_Ine_Dojo_Arene_Nuit_1").convert(),
                               'tkh1' : self.load("bgs","Fond_Planque_Takahiro_Nuit_1").convert(),
                               'tkh2' : self.load("bgs","Fond_Planque_Takahiro_Jour_1").convert(),
                               'azw1' : self.load("bgs","Fond_Aizuwakamatsu_2").convert(),
                               'azw2' : self.load("bgs","Fond_Aizuwakamatsu_Détruit_1").convert(),
                               'azw3' : self.load("bgs","Fond_Aizuwakamatsu_Détruit_2").convert()
                               }
        
        ########## Rects pour les sprites ##########
        self.rects_caracters = {'right': pygame.Rect(1042,128,238,593),
                                #'right2': pygame.Rect(912,128,238,593),
                                'right2': pygame.Rect(865,128,238,593),
                                'tkhright': pygame.Rect(876,128,404,593),
                                'left': pygame.Rect(0,128,238,593)
                                }
    
    def load(self,d,file,ext='png'):
        if ext == 'ttf':
            return pygame.font.Font(f"../data/assets/fonts/{file}.ttf",d)
        return pygame.image.load(f"../data/assets/{d}/{file}.{ext}")
    
    def switch_lowercase (self,state:bool,fixed=False):
        """
        

        Parameters
        ----------
        state : bool
            REMPLIR.
        fixed : 
            NE PAS REMPLIR.

        Returns
        -------
        None.

        """
        if not (self.lowercase == state and fixed):
            self.is_lowercase_auto_fixed = fixed
        
        if self.lowercase and fixed and not self.is_lowercase_auto_fixed:
            pass
        else:
            self.lowercase = state
        
        if self.lowercase:
            self.current_font_color = (90,90,90)
            self.font_MFMG30.set_italic(True)
        else:
            self.current_font_color = 'black'
            self.font_MFMG30.set_italic(False)
            
    def fix_line(self,line):
        ### Suppression des parenthèses (non fonctionnel)
        #if len(line) > 1:
        #    if line[0] == '(' and line[len(line)-1] ==")":
        #        self.switch_lowercase(True,True)
        #        line = line[1:len(line)-2]
        #    else:
        #        self.switch_lowercase(False,True)
        output_line = ""
        point_note=0
        for i in range(len(line)):
            added_char=""
            char=line[i]
            
            if char ==".":
                point_note+=1
            else:
                if point_note==1:
                    if char not in [" ","."]:
                        added_char = " "
                elif point_note==2:
                    if char==" ":
                        added_char="."
                    else:
                        added_char = ". "
                point_note=0
            if char in ["?","!"] and not espace:
                added_char=" "
            if i in [0,len(line)-1] and char==" ":
                new_char=""
            elif char in ["‘","’","’"]:
                new_char="'"
            elif char == "…":
                new_char = "..."
            else:
                new_char = char
            
            new_char=added_char+new_char
            output_line+=new_char
            espace = char==" "
        return output_line
    
    ########## Fonctions pratiques pour créer les cinématiques ##########
    
    def cinematic_frame(self, screen:pygame.surface.Surface, bg:str, kind:int=0, line1:str="", line2:str="", line3:str="", kind_info:list=[], running:bool=True):
        """
        Parameters
        ----------
        screen : pygame.surface.Surface
            Surface de l'écran sur laquelle la cinématique sera affichée.
        bg : str
            Fond d'écran, doit faire partie des fonds disponibles dans self.cinematics_bgs.
        kind : int, optional
            Nombre de personnages qui seront affichés (0,1,2 ou 3). Par défaut sans personne affiché : 0.
        line1 : str, optional
            Première ligne. Par défaut vide : "". De longueur 78 ou moins.
        line2 : str, optional
            Deuxième ligne. Par défaut vide : "". De longueur 78 ou moins.
        line3 : str, optional
            Troisième ligne. Par défaut vide : "". De longueur 78 ou moins.
        kind_info : list, optional
            Informations supplémentaires sur les personnages à afficher :
                Si kind vaut 1 :
                    - Renseigner le nom du personnage à afficher,
                    - Le nom du personnage qui parle ('N' pour le narrateur),
                    - L'arme du personnage,
                    - Le côté ('right' ou 'left').
                Sinon :
                    - Une liste par personnage affiché, dans l'ordre des personnages affichés de droite à gauche. Chaque liste contient dans cet ordre :
                        - Le personnage (inclut dans le dictionnaire self.names)
                        - L'arme qu'il porte (uniquement 'no_weapon' pour le moment)
                    - Le numéro du personnage qui parle (de droite à gauche (1,2,3 ou 0 pour le narrateur)).
                    - (optionnel) S'il y a 3 personnages, le 5e élément de la liste est un booléen pour indiquer si les personnages à droite doivent changer de place avant de parler.
                    - (optionnel) En 6e argument, la liste des personnages présents devant être affichés avec "???".
            Par défaut vide : [].

        Returns
        -------
        Affiche l'image de la cinématique sur la surface screen.
        
        None.
        """
        line1 = self.fix_line(line1)
        line2 = self.fix_line(line2)
        line3 = self.fix_line(line3)
        
        assert type(screen) == pygame.surface.Surface, "L'écran n'est pas défini correctement."
        assert bg in list(self.cinematics_bgs.keys()), "Le fond n'est pas dans la liste des fonds"
        assert kind in [0,1,2,3], "Le nombre de personnage (kind) doit être entre 0 et 3"
        assert type(line1) == str, "La ligne 1 n'est pas une chaîne de caractères"
        assert len(line1) <= 78, f"La ligne 1 est trop longue ({len(line1)-78} caractère(s) en trop)."
        assert type(line2) == str, "La ligne 2 n'est pas une chaîne de caractères."
        assert len(line2) <= 78, f"La ligne 2 est trop longue ({len(line2)-78} caractère(s) en trop)."
        assert type(line3) == str, "La ligne 3 n'est pas une chaîne de caractères."
        assert len(line3) <= 78, f"La ligne 3 est trop longue ({len(line3)-78} caractère(s) en trop)."
        assert type(kind_info) == list, "Les informations supplémentaires ne sont pas dans une liste."
        if kind == 1:
            assert len(kind_info) >= 3, f"L'argument kind_info doit âtre au moins de longueur 3 (ici, il est de longueur {len(kind_info)})."
            assert kind_info[0] in list(self.names.keys()), "Le nom du personnage n'est pas dans la liste."
            assert kind_info[1] in list(self.names.keys()), "Le nom du personnage qui parle n'est pas dans la liste."
            assert kind_info[2] in ['no_weapon'], "Le personnage n'a pas cette arme."
            try:
                assert kind_info[3] in ['left','right'], "Le côté est incorrect."
            except:
                pass
        elif kind>=2:
            assert len(kind_info) >= kind+1, f"L'argument kind_info doit âtre au moins de longueur {kind+1} (ici, il est de longueur {len(kind_info)})."
            for i in range(kind):
                assert type(kind_info[i]) == list, f"Le personage ({i}) n'est pas dans une liste"
                assert len(kind_info[i]) ==  2, f"Le personage ({i}) n'est pas de la bonne longueur"
                assert kind_info[i][0] in list(self.names.keys()), f"Le nom du personage ({i}) n'est pas dans la liste({kind_info[i][0],list(self.names.keys())})"
                assert kind_info[i][1] in ['no_weapon','cin07'], f"Le personage ({i}) n'a pas cette arme"
            assert kind_info[kind] in [i for i in range(kind+1)], "Le personage qui parle est incorrect"
            if kind==3:
                try:
                    if kind_info[4] != None:
                        assert type(kind_info[4]) == bool, "La propriété swap en 5e position doit être booléene ou None"
                except:
                    pass
        try:
            assert type(kind_info[5]) == list
            for char in kind_info[5]:
                assert char in list(self.names.keys()), f"{char} n'est pas un personnage de la liste"
            try:
                assert type(kind_info[6]) == bool
            except:
                pass
        except:
            pass
        assert type(running) == bool
        
        
        if self.cinematic_running and running:
            
            #Fix du bug 16 (jamais vu un truc aussi bancal)
            self.current_bg = bg
            self.current_kind = kind
            self.current_kind_info = kind_info
            
            side='right'
            swap = False
            unknown = []
            
            try:
                if type(kind_info[4]) == bool:
                    swap = kind_info[4]
                try:
                    if type(kind_info[5]) == list:
                        unknown = kind_info[5]
                except:
                    unknown = []
            except:
                pass
            
            
            if kind == 0:
                self.simple_cinematic_frame(screen,bg,line1,line2,line3)
            elif kind == 1:
                try:
                    if kind_info[3] in ['right','left']:
                        side = kind_info[3]
                except:
                    pass
                self.dialog1_frame(screen,bg,kind_info[0],kind_info[1],kind_info[2],side,unknown,line1,line2,line3)
            elif kind == 2:
                self.dialog2_frame(screen,bg,kind_info[0],kind_info[1],kind_info[2],unknown,line1,line2,line3)
            elif kind == 3:
                self.dialog3_frame(screen,bg,kind_info[0],kind_info[1],kind_info[2],kind_info[3],swap,unknown,line1,line2,line3)
            else:
                print (f"type de cinématique incorrecte ({kind})")

    def simple_cinematic_frame (self, screen, bg, line1="", line2="", line3=""):
        ########## Image sans dialogue ##########
        
        screen.blit(self.cinematics_bgs[bg], pygame.Rect(0,0,1280,720))
        self.display_text_and_wait(screen,line1,line2,line3,'N')

    def dialog1_frame (self, screen, bg, char, talking, wpn,side, unknown, line1="", line2="", line3=""):
        ########## Image dialogue avec 1 personnage ##########
        side2 = side
        if char == 'TK' and side == 'right':
            side2 = 'tkhright'
        screen.blit(self.cinematics_bgs[bg], pygame.Rect(0,0,1280,720))
        if talking == 'N':
            screen.blit(self.sprites[char][side][wpn]['secondary'],self.rects_caracters[side])
        else:
            screen.blit(self.sprites[char][side][wpn]['main'],self.rects_caracters[side2])
        self.display_text_and_wait(screen,line1,line2,line3,talking,unknown)
    
    def dialog2_frame (self, screen, bg, char1, char2, talking_char, unknown, line1="", line2="", line3=""):
        ########## Image dialogue avec 2 personnages ##########
        side_in_case = 'right'
        if char1[0] == 'TK':
            side_in_case = 'tkhright'
        screen.blit(self.cinematics_bgs[bg], pygame.Rect(0,0,1280,720))
        if talking_char == 0:
            screen.blit(self.sprites[char1[0]]['right'][char1[1]]['secondary'],self.rects_caracters[side_in_case])
            screen.blit(self.sprites[char2[0]]['left'][char2[1]]['secondary'],self.rects_caracters['left'])
            self.display_text_and_wait(screen,line1,line2,line3,'N',unknown)
        elif talking_char == 1:
            screen.blit(self.sprites[char1[0]]['right'][char1[1]]['main'],self.rects_caracters[side_in_case])
            screen.blit(self.sprites[char2[0]]['left'][char2[1]]['secondary'],self.rects_caracters['left'])
            self.display_text_and_wait(screen,line1,line2,line3,char1[0],unknown)
        elif talking_char == 2:
            screen.blit(self.sprites[char1[0]]['right'][char1[1]]['secondary'],self.rects_caracters[side_in_case])
            screen.blit(self.sprites[char2[0]]['left'][char2[1]]['main'],self.rects_caracters['left'])
            self.display_text_and_wait(screen,line1,line2,line3,char2[0],unknown)
        
    def dialog3_frame (self, screen, bg, char1, char2, char3, talking_char, swap, unknown, line1="", line2="", line3=""):
        ######### Vérifie s'il faut faire un échange ##########
        if swap:
            self.swap_characters(screen,bg,char1,char2,char3)
            
        ########## Image dialogue avec 3 personnages ##########
        screen.blit(self.cinematics_bgs[bg], pygame.Rect(0,0,1280,720))
        if talking_char == 0:
            screen.blit(self.sprites[char2[0]]['right'][char2[1]]['secondary'],self.rects_caracters['right2'])
            screen.blit(self.sprites[char1[0]]['right'][char1[1]]['secondary'],self.rects_caracters['right'])
            screen.blit(self.sprites[char3[0]]['left'][char3[1]]['secondary'],self.rects_caracters['left'])
            self.display_text_and_wait(screen,line1,line2,line3,'N',unknown)
        elif talking_char == 1:
            screen.blit(self.sprites[char2[0]]['right'][char2[1]]['secondary'],self.rects_caracters['right2'])
            screen.blit(self.sprites[char1[0]]['right'][char1[1]]['main'],self.rects_caracters['right'])
            screen.blit(self.sprites[char3[0]]['left'][char3[1]]['secondary'],self.rects_caracters['left'])
            self.display_text_and_wait(screen,line1,line2,line3,char1[0],unknown)
        elif talking_char == 2:
            screen.blit(self.sprites[char2[0]]['right'][char2[1]]['main'],self.rects_caracters['right2'])
            screen.blit(self.sprites[char1[0]]['right'][char1[1]]['secondary'],self.rects_caracters['right'])
            screen.blit(self.sprites[char3[0]]['left'][char3[1]]['secondary'],self.rects_caracters['left'])
            self.display_text_and_wait(screen,line1,line2,line3,char2[0],unknown)
        elif talking_char == 3:
            screen.blit(self.sprites[char2[0]]['right'][char2[1]]['secondary'],self.rects_caracters['right2'])
            screen.blit(self.sprites[char1[0]]['right'][char1[1]]['secondary'],self.rects_caracters['right'])
            screen.blit(self.sprites[char3[0]]['left'][char3[1]]['main'],self.rects_caracters['left'])
            self.display_text_and_wait(screen,line1,line2,line3,char3[0],unknown)

    def display_text_and_wait (self,screen,line1,line2,line3,char,unknown=[]):
        ########## Gère localement l'affichage et la gestion des imputs pour l'image présente ##########
        screen.blit(self.text_bg,pygame.Rect(0,390,1280,330))
        
        if char in unknown:
            name = '?'
        else:
            name = char
        
        screen.blit(self.names[name],self.rect_names)
            
        
        pygame.display.flip()
        pygame.event.clear()
        
        
        self.current_last_letter = [0,0,0]
        written = False
        next_indicator_frame = 1
        next_frame = False
        keys_cooldown = True
        #is_displayed = True
        
        
        while self.cinematic_running and not next_frame:
            #if not pygame.display.get_active():
            #    is_displayed = False
            #elif is_displayed == False:
            #    self.cinematic_frame(screen,self.current_bg,self.current_kind,line1,line2,line3,self.current_kind_info)
            #    return None
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.cinematic_running = False
                    pygame.event.post(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    ##### Son #####
                    self.sound.play(self.sound.click)
                    ##### Passage à la prochaine image si toutes les lettres sont affichées #####
                    if self.current_last_letter == [len(line1),len(line2),len(line3)]:
                        next_frame = True
                    elif not written:
                        self.current_last_letter = [len(line1),len(line2),len(line3)]
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_F11]: 
                pygame.display.toggle_fullscreen()
                pygame.time.Clock().tick(5)
                
                #Fix du bug 16 (jamais vu un truc aussi bancal)
                self.cinematic_frame(screen,self.current_bg,self.current_kind,line1,line2,line3,self.current_kind_info)
                return None
                
            elif pressed_keys[pygame.K_SPACE] or pressed_keys[pygame.K_RETURN] or pressed_keys[pygame.K_RIGHT]:
                ##### Passage à la prochaine image si toutes les lettres sont affichées et que le cooldonw est terminé #####
                if not keys_cooldown:
                    if self.current_last_letter == [len(line1),len(line2),len(line3)]:
                        next_frame = True
                    elif not written:
                        self.current_last_letter = [len(line1),len(line2),len(line3)]
                    keys_cooldown = True
            elif keys_cooldown:
                keys_cooldown = False
            
            if not written:
                if self.current_last_letter[0] < len(line1):
                    self.current_last_letter[0] += 1
                elif self.current_last_letter[1] < len(line2):
                    self.current_last_letter[1] += 1
                elif self.current_last_letter[2] < len(line3):
                    self.current_last_letter[2] += 1
                else:
                    written = True
                    
            else:
                if next_indicator_frame == 60:
                    next_indicator_frame = 1
                else:
                    next_indicator_frame += 1
            
            
            self.text_line1 = self.font_MFMG30.render(line1[:self.current_last_letter[0]],False,self.current_font_color)
            self.text_line2 = self.font_MFMG30.render(line2[:self.current_last_letter[1]],False,self.current_font_color)
            self.text_line3 = self.font_MFMG30.render(line3[:self.current_last_letter[2]],False,self.current_font_color)
            
            screen.blit(self.text_bg,pygame.Rect(0,390,1280,330))
            screen.blit(self.names[name],self.rect_names)
            
            
            screen.blit(self.text_line1,pygame.Rect(60,500,1180,50))
            screen.blit(self.text_line2,pygame.Rect(60,550,1180,50))
            screen.blit(self.text_line3,pygame.Rect(60,600,1180,50))
            
            if written:
                if next_indicator_frame > 30:
                    screen.blit(self.next_indicator[1],pygame.Rect(1200,640,50,50))
                else:
                    screen.blit(self.next_indicator[0],pygame.Rect(1200,640,50,50))
                
                
            
            pygame.display.flip()
            pygame.time.Clock().tick(60)
        
    def ecran_noir (self, screen:pygame.surface.Surface):
        ########## Affiche un fondu au noir ##########
        
        noir = pygame.Surface((1280,720), pygame.SRCALPHA)
        
        for alpha in range(0,256,3):
            
            noir.fill((0, 0, 0, alpha))
            screen.blit(noir, (0, 0))
            pygame.display.flip()
            pygame.time.Clock().tick(60)
        
    def swap_characters(self,screen,bg,char1,char2,char3):
        ########## Les personnages échangent de place à l'écran ##########
        keys_cooldown = True
        
        for pos_chars in range(912,1043,5):
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    ##### Son #####
                    self.sound.play(self.sound.click)
                    return None
            
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_F11]: 
                pygame.display.toggle_fullscreen()
                pygame.time.Clock().tick(5)
            elif pressed_keys[pygame.K_SPACE] or pressed_keys[pygame.K_RETURN] or pressed_keys[pygame.K_RIGHT]:
                ##### Passage au texte si toutes les lettres sont affichées et que le cooldonw est terminé #####
                if not keys_cooldown:
                    return None
            elif keys_cooldown:
                keys_cooldown = False
            
            
            screen.blit(self.cinematics_bgs[bg], pygame.Rect(0,0,1280,720))
            screen.blit(self.sprites[char3[0]]['left'][char3[1]]['secondary'],self.rects_caracters['left'])
            rect_char2 = pygame.Rect(1955-pos_chars,128,238,593)
            rect_char1 = pygame.Rect(pos_chars,128,238,593)
            if pos_chars <= 971:
                screen.blit(self.sprites[char1[0]]['right'][char1[1]]['secondary'],rect_char1)
                screen.blit(self.sprites[char2[0]]['right'][char1[1]]['secondary'],rect_char2)
            else:
                screen.blit(self.sprites[char2[0]]['right'][char1[1]]['secondary'],rect_char2)
                screen.blit(self.sprites[char1[0]]['right'][char1[1]]['main'],rect_char1)
            screen.blit(self.text_bg,pygame.Rect(0,390,1280,330))
            pygame.display.flip()
        
    def choice_frame (self,screen:pygame.surface.Surface,bg:str,kind:list=[0,4],choices:List[str]=["","","",""],chars:List[List[str]]=[],timer:int=0)-> List[Union[str,int]] :
        """
        Parameters
        ----------
        screen : pygame.surface.Surface
            Surface de l'écran sur laquelle la cinématique sera affichée.
        bg : str
            Fond d'écran, doit faire partie des fonds disponibles dans self.cinematics_bgs.
        kind : List[int], optional
            Dans cet ordre :
                - Nombre de personnages qui seront affichés (0,1,2 ou 3). Par défaut sans personne affiché : 0.
                - Nombre de choix proposés au joueur.
        choices : List[str], optional
            Une liste des choix proposés au joueur, de même longueur que le deuxième paramètre de kind
        chars : List[List[str]], optional
            Une liste contenant une liste par parsonnage à afficher. Chacune des listes de personnage contient dans l'ordre :
                    - L'abréviation du nom.
                    - Le style du personnage.
        timer : int, optional
            Le temps (en milisecondes) qu'à le joueur pour répondre. Mettre -1 pour laisser un temps infini.
        

        Returns
        -------
        Affiche et conserve le choix à l'écran.
        
        Retourne une liste contenant en premier élément la raison pour laquelle la fonction s'est terminée :
            - 'QUIT' pour la fermeture du jeu.
                - Second élément : 0.
            - 'timer_end' pour la fin du temps.
                - Second élément : 0.
            - 'choice' pour un choix :
                - Le second élément est l'entier (de 1 à 4) correspondant au choix fait (dans l'ordre des choix entrés dans choices)
        """
        
        assert type(screen)==pygame.surface.Surface, "screen n'est pas une surface affichable"
        assert bg in list(self.cinematics_bgs.keys()), "le fond ne fait pas partie de la liste des fonds disponibles (voir self.cinematic_bgs)"
        assert type(kind)==list, "kind doit être une liste"
        assert len(kind)==2, "kind doit être de longueur 2"
        assert kind[0] in [0,1,2,3], "le nombre de personnages doit être un entier entre 1 et 3"
        assert kind[1] in [2,3,4], "le nombre de choix doit être entre 2 et 4"
        assert type(choices)==list, "choices doit être la liste des choix"
        assert len(choices) == kind[1], f"il doit y avoir autant de choix que le second paramètre de kind ({kind[1]})"
        for i in choices:
            assert type(i)==str, f"les choix doivent être des chaînes de caractères, ce n'est pas le cas du choix {i+1}"
            assert len(i) <= 19, f"le choix {i} est trop long ({len(i)-19} caractère(s) en trop)"
        assert type(chars)==list, "les personnages doivent être rangés dans une liste"
        assert len(chars)==kind[0], f"il doit y avoir autant de personnages que le premier paramètre de kind ({kind[0]})"
        for i in chars:
            assert type(i)==list, "chaque personnage doit être une liste"
            assert i[0] in list(self.sprites.keys()), f"{i[0]} ne fait pas partie de la liste des persos : {list(self.sprites.keys())}"
            assert i[1] in list(self.sprites[i[0]]['right'].keys())+list(self.sprites[i[0]]['left'].keys()), f"le personnage {i[0]} n'a pas l'apparence {i[1]}"
        assert type(timer)==int, "timer doit correspondre à un temps en milisecondes, donc un entier"
        assert timer>=-1, "le timer doit avoir un temps positif ou valant -1"
        
        chosen = False
        timer_end = False
        
        button_light_surface = pygame.image.load("../data/assets/buttons/Fond_Bouton_VERT_400p.png")
        button_dark_surface = pygame.image.load("../data/assets/buttons/Fond_Bouton_VERTF_400p.png")

        current_buttons_surfaces = {str(i):button_light_surface for i in range(kind[1])}
        buttons_rects = {str(i):button_light_surface.get_rect() for i in range (kind[1])}
        
        
        choices_objects = {"0":{},"1":{},"2":{},"3":{}}
        for i in range(kind[1]):
            choices_objects[str(i)]["surface"] = self.font_MFMG30.render(choices[i],False,'black')
            choices_objects[str(i)]["rect"] = choices_objects[str(i)]["surface"].get_rect()


        
        if kind[1] in [2,3,4]:
            left_var={}
            if kind[1]==4:
                a=2
            else:
                a=kind[1]
            d=(1280-a*buttons_rects["0"].width)/(a+1)
            for i in range(a):
                r=buttons_rects["0"].width*i + d*i
                left_var[str(i)]=r+d
                if kind[1] in [2,3]:
                    buttons_rects[str(i)].midleft=(left_var[str(i)],555)


        if kind[1] == 2:
            for i in range(2):
                choices_objects[str(i)]["rect"].center = buttons_rects[str(i)].center
        elif kind[1] == 3:
            #buttons_rects["0"].center = (640,500)
            #choices_objects["0"]["rect"].center = (640,500)
            for i in range(3):
                choices_objects[str(i)]["rect"].center = buttons_rects[str(i)].center
        elif kind[1] == 4:
            for i in range (4):
                buttons_rects[str(i)].midleft = (left_var[str(i%2)],500+110*(i//2))
                choices_objects[str(i)]["rect"].center = buttons_rects[str(i)].center

        depart_timer = pygame.time.get_ticks()
        cooldown = True

        while not chosen and not timer_end:
            if timer != 0:
                remaining_time=max(timer-pygame.time.get_ticks()+depart_timer,0)
                if remaining_time == 0:
                    timer_end = True
                    return ['timer_end',0]
                else:
                    timer_text = self.font_MFMG60.render(str(round(remaining_time/1000,1)),False,'red')
                    timer_rect = timer_text.get_rect()
                    timer_rect.topleft = (0,0)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.event.post(event)
                    return ['QUIT',0]
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.sound.play(self.sound.click)
                    for i in range(kind[1]):
                        if buttons_rects[str(i)].collidepoint(pygame.mouse.get_pos()):
                            chosen = True
                            return ['choice',i+1]
            
            if pygame.key.get_pressed()[pygame.K_F11]:
                if not cooldown:
                    pygame.display.toggle_fullscreen()
            else:
                cooldown=False
            
            for i in range(kind[1]):
                if buttons_rects[str(i)].collidepoint(pygame.mouse.get_pos()):
                    current_buttons_surfaces[str(i)] = button_dark_surface
                else:
                    current_buttons_surfaces[str(i)] = button_light_surface



            screen.blit(self.cinematics_bgs[bg], pygame.Rect(0,0,1280,720))

            if kind[0]==2:
                sides=['right','left']
                rect_sides = ['right','left']
            else:
                sides=['right','right','left']
                rect_sides = ['right','right2','left']
            for i in range(kind[0]):
                screen.blit(self.sprites[chars[i][0]][sides[i]][chars[i][1]]["secondary"],self.rects_caracters[rect_sides[i]])
            
            screen.blit(self.text_bg,self.text_bg_rect)

            for i in range(kind[1]):
                screen.blit(current_buttons_surfaces[str(i)],buttons_rects[str(i)])
                screen.blit(choices_objects[str(i)]["surface"],choices_objects[str(i)]["rect"])
            
            if timer!=0:
                screen.blit(timer_text,timer_rect)
            
            pygame.display.flip()
    
    def refresh_fullscreen(self):
        pass
    
    ########## Cinématiques ##########
    
    def final_death (self,screen,saved="none"):
        self.cinematic_frame(screen, 'mgm5', 0, "Musashi n'aura pas réussi à venger son village.", "Il mourut dans la réalisation que sa mort signifgiait sûrement la fin", "de son village.")
        self.ecran_noir(screen)
    
    def final_loose (self,screen,saved ="none"):
        self.cinematic_frame(screen, 'mgm1', 3, "Shikisha Musashi quitte le dojo, l'esprit troublé.", "Il retourne au village, mais le souvenir de ses échecs le hantera", "pour le restant de ses jours.", kind_info=[["SM","no_weapon"],[saved,"no_weapon"],["SH", "no_weapon"], 0])
    
    def cinematic_01 (self, screen,saved='none'):
        self.music.play(self.music.intro,500)
        self.cinematic_frame(screen, 'mgm1', 0, 'Magome, un petit village reculé, perdu dans les forêts du Japon médiéval.','Ici, la vie est rude. Les récoltes sont maigres.','Et les guerres de clans rendent l\'existence encore plus précaire.')
        self.cinematic_frame(screen, 'mgm1', 0, 'Dans ce lieu marqué par les inégalités, les riches dominent','tandis que les plus pauvres luttent pour survivre.')
        self.cinematic_frame(screen, 'mgm1', 0, 'C\'est dans ce village que naît Shikisha Musashi.','Issu d\'une famille de fermiers, il grandit dans la pauvreté.')
        self.cinematic_frame(screen, 'mgm1', 0, 'Dès son plus jeune âge, Musashi montre un talent particulier pour','organiser et inspirer ceux qui l\'entourent.',"Il est le chef de sa bande d'amis.")
        self.cinematic_frame(screen, 'mgm1', 0, 'Lorsqu\'un problème survient, il rassemble les villageois pour trouver','une solution, devenant peu à peu une figure respectée.')
        self.cinematic_frame(screen, 'mgm1', 0, 'Les habitants commencent à l\'appeler "le chef d\'orchestre",','un surnom qui reflète son aptitude à guider et à régler les conflits.','Malgré son jeune âge, Musashi est déjà un symbole d\'espoir dans ce village.')
        self.music.play(self.music.theme_tkh1)
        self.cinematic_frame(screen, 'mgm4', 0, 'Cette nuit-là, une atmosphère étrange plane sur Magome.')
        self.cinematic_frame(screen, 'mgm4', 0, 'Le silence est lourd, seulement brisé par le bruit des pas','d\'hommes armés approchant dans l\'ombre.',"Ce sont les guerriers du clan Takahiro.")
        self.cinematic_frame(screen, 'mgm4', 2, 'Les ordres sont clairs. Pillez tout ce que vous trouvez et brûlez le reste.', kind_info=[['TW','no_weapon'],['TW_H','no_weapon'],1])
        self.cinematic_frame(screen, 'mgm4', 2, 'Compris. Pas de quartier. Ils doivent comprendre qui commande ici.', kind_info=[['TW','no_weapon'],['TW_H','no_weapon'],2])
        self.cinematic_frame(screen, 'mgm5', 0, 'Des torches illuminent soudainement le ciel. Les cris éclatent.')
        self.cinematic_frame(screen, 'mgm5', 0, 'Le chaos s\'empare du village. Les flammes dévorent les maisons,','et les villageois courent dans toutes les directions,','tentant de sauver leurs vies ou leurs proches.')
        self.cinematic_frame(screen, 'mgm5', 0, 'Dans la confusion, Shikisha se retrouve face à une situation critique.')
        self.cinematic_frame(screen, 'mgm5', 0, 'Devant lui, deux visages familiers :','- Sa sœur Keiko, piégée dans une maison en feu,','- Et son ami Takeshi, aux prises avec deux guerriers du clan Takahiro.')
        self.cinematic_frame(screen, 'mgm5', 2, 'Shikisha, aide-moi ! Je suis coincée !' ,kind_info=[['KT','no_weapon'],['KM','no_weapon'],2])
        self.cinematic_frame(screen, 'mgm5', 2, 'Musashi, par ici ! Je ne tiendrai pas longtemps seul contre eux !',kind_info=[['KT','no_weapon'],['KM','no_weapon'],1])
        self.cinematic_frame(screen, 'mgm5', 2, 'Le cœur de Musashi se serre.','Le temps presse, et il sait qu\'il devra faire un choix','qui changera à jamais son existence et celle des siens.', kind_info=[['KT','no_weapon'],['KM','no_weapon'],0])
    
    def cinematic_02 (self, screen, saved='none'):
        self.ecran_noir(screen)
        self.music.play(self.music.theme_tkh1)
        self.cinematic_frame(screen, 'mgm6', 0, "Les premières lueurs de l\'aube peinent à percer l\'épaisse fumée", "qui enveloppe Magome.", "Les cris de la nuit se sont tus, remplacés par un silence pesant.")
        self.cinematic_frame(screen, 'mgm6', 0, "Quelques survivants errent parmi les débris, le regard vide.","D'autres s'affairent à éteindre les derniers foyers.")
        self.cinematic_frame(screen, 'mgm6', 2, "Shikisha Musashi reste immobile, les mains tremblantes,", "son esprit hanté par les derniers évènements.", kind_info=[['SM','no_weapon'],[saved,'no_weapon'],0])
        if saved == 'none':
            self.cinematic_frame(screen, 'mgm6', 1, "Il fixe les ruines du temple effondré, là où Keiko et Takeshi ont péri.", "Le souvenir de leurs cris le hante.", "Il serre les poings, ses ongles s\'enfonçant dans sa paume.", kind_info=['SM','N','no_weapon'])
            self.cinematic_frame(screen, 'mgm6', 1, "Je les ai abandonnés... Je les ai regardés mourir.", kind_info=['SM','SM','no_weapon'])
            self.cinematic_frame(screen, 'mgm6', 1, "Sa respiration est troublée par ses sanglots.","Sa tristesse, puis sa colère se confondent.", "Elles sont chaque seconde plus intenses.", kind_info=['SM','N','no_weapon'])
            self.cinematic_frame(screen, 'mgm6', 1, "Qu'ai-je fait... ? Pourquoi n\'ai-je pas agi ?", "J'aurais pu sauver Keiko, j'aurais pu sauver Takeshi...", "Mais je les ai laissés là... mourir dans cette fumée...", kind_info=['SM','SM','no_weapon'])
            self.cinematic_frame(screen, 'mgm6', 1, "Je les ai abandonnés...", "C\'est moi qui ai provoqué ça, tout est de ma faute...", "Je... je n\'étais pas prêt... je ne suis pas prêt...", kind_info=['SM','SM','no_weapon'])
            self.cinematic_frame(screen, 'mgm6', 1, "Ses pensées tourbillonnent, dans un flot de remords et de haine.", "Musashi se renferme sur lui-même.","Il est perdu dans un dialogue interne, à peine audible.", kind_info=['SM','N','no_weapon'])
            self.cinematic_frame(screen, 'mgm6', 1, "Je... suis un monstre... pourquoi suis-je encore là ?", "J\'ai tout détruit, tout...", kind_info=['SM','SM','no_weapon'])
            self.cinematic_frame(screen, 'mgm6', 2, "Une silhouette familière s\'approche, le sortant de sa confusion :", "le doyen du village, Yoshirō, le visage grave.", kind_info=[['SM','no_weapon'],['Y?','no_weapon'],0])
            self.cinematic_frame(screen, 'mgm6', 2, "Musashi... je... je suis désolé pour eux.", kind_info=[['SM','no_weapon'],['Y?','no_weapon'],2])
            self.cinematic_frame(screen, 'mgm6', 2, "J\'aurais dû faire quelque chose, Yoshirō !", "Mais je n\'ai rien fait ! Rien !", kind_info=[['SM','no_weapon'],['Y?','no_weapon'],1])
            self.cinematic_frame(screen, 'mgm6', 2, "Tu ne peux pas changer le passé.", "Mais si tu laisses cette culpabilité te consumer,", "tu condamnes tout le village.", kind_info=[['SM','no_weapon'],['Y?','no_weapon'],2])
            self.sound.scary_effect.play()
            self.cinematic_frame(screen, 'mgm6', 2, "Les mots de Yoshirō ne l\'apaisent pas." ,"La haine continue de grandir dans son cœur,", "dirigée contre lui-même, contre les envahisseurs, contre le monde entier.", kind_info=[['SM','no_weapon'],['Y?','no_weapon'],0])
        elif saved == 'KM':
            self.cinematic_frame(screen, 'mgm6', 2, "Shikisha... tu vas bien ?", "Depuis que... depuis tout à l\'heure, tu n'as pas dit un mot.", kind_info=[['SM','no_weapon'],['KM','no_weapon'],2])
            self.cinematic_frame(screen, 'mgm6', 2, "Keiko... c\'est de ma faute. J\'aurais dû trouver un moyen...", "J\'aurais dû sauver tout le monde.", kind_info=[['SM','no_weapon'],['KM','no_weapon'],1])
            self.cinematic_frame(screen, 'mgm6', 2, "Non, tu as fait ce que tu pouvais.", "Si tu n'avais rien fait, je ne serais pas là.", "Takeshi aurait compris... comme moi, il croyait en toi.", kind_info=[['SM','no_weapon'],['KM','no_weapon'],2])
        elif saved == 'KT':
            self.cinematic_frame(screen, 'mgm6', 2, "Musashi... dis quelque chose. Tu ne peux pas rester comme ça.", kind_info=[['SM','no_weapon'],['KT','no_weapon'],2])
            self.cinematic_frame(screen, 'mgm6', 2, "Keiko... elle... c\'était ma sœur, Takeshi.","Comment peux-tu me demander d\'aller de l\'avant ?", kind_info=[['SM','no_weapon'],['KT','no_weapon'],1])
            self.cinematic_frame(screen, 'mgm6', 2, "Parce que c\'est ce qu\'elle aurait voulu.","Tu sais qu\'elle n\'aurait jamais voulu que tu t\'effondres comme ça.", "Elle croyait en toi, tout comme moi.", kind_info=[['SM','no_weapon'],['KT','no_weapon'],2])
        self.cinematic_frame(screen, 'mgm6', 2, "Yoshirō, le doyen du village, voyant la lutte dans les yeux de Musashi,", "s'approche lentement.", kind_info=[['SM','no_weapon'],['Y?','no_weapon'],0])
        self.cinematic_frame(screen, 'mgm6', 2, "Musashi, tu dois nous écouter.", "Le village a besoin d\'un leader, maintenant plus que jamais.", kind_info=[['SM','no_weapon'],['Y?','no_weapon'],2])
        self.cinematic_frame(screen, 'mgm6', 2, "Yoshirō... Je ne sais pas si je suis capable de continuer.", kind_info=[['SM','no_weapon'],['Y?','no_weapon'],1])
        self.cinematic_frame(screen, 'mgm6', 2, "Si ce n\'est pas toi, alors qui ?", "Tu as toujours guidé ce village. Les enfants te regardent comme un héros.", "C\'est le moment de nous montrer cette force, Musashi.", kind_info=[['SM','no_weapon'],['Y?','no_weapon'],2])
        self.cinematic_frame(screen, 'mgm6', 2, "Yoshirō pose une main ferme sur son épaule.", "Musashi sent alors une étincelle de détermination renaître en lui,", "bien que son cœur reste lourd de remords.", kind_info=[['SM','no_weapon'],['Y?','no_weapon'],0])
        self.cinematic_frame(screen, 'mgm6', 2, "D\'accord... dites-moi ce que je dois faire.", kind_info=[['SM','no_weapon'],['Y?','no_weapon'],1])
        self.cinematic_frame(screen, 'mgm6', 2, "Commençons par rassembler les villageois.", "Explique-leur ce qu\'ils doivent faire.", "Nous devons nous organiser si nous voulons survivre à une autre attaque.", kind_info=[['SM','no_weapon'],['Y?','no_weapon'],2])
    
    def cinematic_03 (self, screen, saved='none'):
        self.music.play(self.music.exploration)
        self.cinematic_frame(screen, 'mgm6', 2, "Mais Musashi sait que cela ne suffit pas.", "Alors que le soleil se couche, il se tient devant ce qui reste de sa maison.", "Une décision mûrit en lui.", kind_info=[['SM','no_weapon'],[saved,'no_weapon'],0])
        self.cinematic_frame(screen, 'mgm6', 2, "Je dois partir... trouver des alliés, des armes.", "Si je reste ici, je ne pourrai pas aller de l'avant.", kind_info=[['SM','no_weapon'],[saved,'no_weapon'],1])
        self.cinematic_frame(screen, 'mgm6', 2, "Musashi, le cœur encore lourd mais l\'esprit décidé, prépare ses affaires.", "Il est prêt à quitter Magome pour chercher de l\'aide et des alliés,", "guidé par l\'espoir de sauver ce qui reste de son village.", kind_info=[['SM','no_weapon'],[saved,'no_weapon'],0])
        if saved == "KT":
            self.cinematic_frame(screen, 'mgm6', 2, "Musashi, mettons nous en route pour le village d'Ine.", "Ce n'est pas loin d'ici, on y trouvera peut-être quelque chose.", kind_info=[['SM','no_weapon'],[saved,'no_weapon'],2])
        elif saved=="KM":
            self.cinematic_frame(screen, 'mgm6', 2, "Shikisha, mettons nous en route pour le village d'Ine.", "Ce n'est pas loin d'ici, on y trouvera peut-être quelque chose.", kind_info=[['SM','no_weapon'],[saved,'no_weapon'],2])
        else:
            self.cinematic_frame(screen, 'mgm6', 2, "Je devrais me mettre en route pour le village d'Ine.", "Ce n'est pas loin d'ici, j'y trouverai peut-être quelque chose.", kind_info=[['SM','no_weapon'],[saved,'no_weapon'],2])
        self.ecran_noir(screen)
    
    def cinematic_04 (self, screen, saved='none'):
        self.music.play(self.music.menu)
        self.cinematic_frame(screen, "bamboo2", 0, "Mars 1664, ère Edo, alentours du village d'Ine.")
        if saved == 'none':
            self.cinematic_frame(screen, "bamboo2", 1, "Il faut que je devienne plus fort, que je les tue tous.", "J\'ai besoin de m\'améliorer pour pouvoir venger mon village.", "Pour l\'instant, je suis trop faible, je dois devenir un Samouraï.", kind_info = ["SM","SM","no_weapon"])
            self.cinematic_frame(screen, "bamboo2", 1, "Hmm ? Tiens ? un village ? Voyons voir cela de plus près...", kind_info = ["SM","SM","no_weapon"])
            self.cinematic_frame(screen, "bamboo2", 2, "Bienvenue au village d'Ine !", "Petit village de pêcheurs prêts à vous servir.", "Venez découvrir nos spécialités poissonnières !", kind_info=[['SM','no_weapon'],['P','no_weapon'],2])
            self.cinematic_frame(screen, "bamboo2", 1, "Heureusement qu\'il y a un village à côté.", "Je vais pouvoir ravitailler mes provisions et me préparer à l\'entraînement.", "Qui sait? Peut-être vais-je trouver un Dojo...", kind_info = ["SM","SM","no_weapon"])
        elif saved == 'KM':
            self.cinematic_frame(screen, "bamboo2", 2, "Grand frère, maintenant que tu as pris la décision de venger notre village,", "comment comptes-tu t\'y prendre ?", "Je crois que ces guerriers sont sous l\'autorité d\'un certain Takahiro.", kind_info=[['SM','no_weapon'],['KM','no_weapon'],2])
            self.cinematic_frame(screen, "bamboo2", 2, "Ça risque d\'être très dangereux n\'est-ce pas ?", kind_info=[['SM','no_weapon'],['KM','no_weapon'],2])
            self.cinematic_frame(screen, "bamboo2", 2, "Ne t\'inquiète pas Keiko. Maintenant le village est tombé en cendres,", "ce n\'est plus le moment de s'inquiéter.", "Si jamais Takeshi était là, il m\'aurait dit de continuer mon chemin.", kind_info=[['SM','no_weapon'],['KM','no_weapon'],1])
            self.cinematic_frame(screen, "bamboo2", 2, "Je ne compte pas rester les bras croisés.", "Je veux m\'entraîner pour mettre fin à cette organisation.", "Je deviendrai un Samuraï.", kind_info=[['SM','no_weapon'],['KM','no_weapon'],1])
            self.cinematic_frame(screen, "bamboo2", 2, "Je vois, mais je n'aime pas qu'on s'expose à de si grands dangers.", "Je préfère essayer d'éviter les combats.", "Je ne suis pas sûre de pouvoir faire face à l\'un de ses guerriers.", kind_info=[['SM','no_weapon'],['KM','no_weapon'],2])
            self.cinematic_frame(screen, "bamboo2", 2, "Ne t\'en fais pas, je ne serai jamais très loin.", "Rappelle-toi que nous, les Musashi, nous ne reculons devant aucun obstacle.", "Quoi qu'il arrive, nous nous battrons toujours pour rester en vie.", kind_info=[['SM','no_weapon'],['KM','no_weapon'],1])
            self.cinematic_frame(screen, "bamboo2", 2, "Merci beaucoup Shikisha. Je suis contente de t\'avoir.", "Takeshi serait ravi de te voir progresser et évoluer lors de ton voyage.", "Ah ! Je crois qu\'on est près d\'un village. Voyons de plus près la pancarte...", kind_info=[['SM','no_weapon'],['KM','no_weapon'],2])
            self.cinematic_frame(screen, "bamboo2", 2, "Bienvenue au village d\'Ine !", "Petit village de pêcheurs prêts à vous servir.", "Venez découvrir nos spécialités poissonnières !", kind_info=[['KM','no_weapon'], ['P','no_weapon'],2])
            self.cinematic_frame(screen, "bamboo2", 2, "Mais c\'est parfait !", "On va pouvoir acheter tout ce dont on aura besoin pour ce voyage toi et moi !", "Je suis partante pour qu\'on fasse un tour dans ce lieu.", kind_info=[['SM','no_weapon'],['KM','no_weapon'],2])
            self.cinematic_frame(screen, "bamboo2", 2, "Qui sait ? Il peut y avoir un maître samouraï dans les parages !","Viens, on y va !", kind_info=[['SM','no_weapon'],['KM','no_weapon'],2])
            self.cinematic_frame(screen, "bamboo2", 2, "Tu as raison. Allons-y, on n\'a pas de temps à perdre !", kind_info=[['SM','no_weapon'],['KM','no_weapon'],1])
        elif saved == 'KT':
            self.cinematic_frame(screen, "bamboo2", 2, "Garde la tête haute, Musashi.", "Moi-même j\'ai perdu des membres de ma famille durant mon enfance.", "Nous partageons la même souffrance.", kind_info=[['SM','no_weapon'],['KT','no_weapon'],2])
            self.cinematic_frame(screen, "bamboo2", 2, "Cependant, c\'est grâce à toi, aujourd\'hui, que je suis encore en vie.", "Et si tu avais sauvé Keiko à ma place, je ne t\'en aurais pas voulu.", kind_info=[['SM','no_weapon'],['KT','no_weapon'],2])
            self.cinematic_frame(screen, "bamboo2", 2, "Merci mille fois, Takeshi.", "J\'étais complètement perdu, et il fallait agir de toute urgence.", kind_info=[['SM','no_weapon'],['KT','no_weapon'],1])
            self.cinematic_frame(screen, "bamboo2", 2, "Je me demande encore si j\'ai fait le bon choix," , "heureusement que j\'ai pu au moins te sauver.", "Mais je ne pourrai jamais pardonner à ce Takahiro ce qu\'il nous a fait.", kind_info=[['SM','no_weapon'],['KT','no_weapon'],1])
            self.cinematic_frame(screen, "bamboo2", 2, "Je suis du même avis. Si tu comptes venger le village, alors moi aussi.", "Pour ça, devenons plus forts, plus agiles et plus sages.", kind_info=[['SM','no_weapon'],['KT','no_weapon'],2])
            self.cinematic_frame(screen, "bamboo2", 2, "Exactement, devenons des Samouraïs !", "Pour honorer ceux qui ont péri dans notre village.", "Tiens, voici justement un village. Il y a même une pancarte :", kind_info=[['SM','no_weapon'],['KT','no_weapon'],1])
            self.cinematic_frame(screen, "bamboo2", 2, "Bienvenue au village d\'Ine !", "Petit village de pêcheurs prêts à vous servir.", "Venez découvrir nos spécialités poissonnières !", kind_info=[['KT','no_weapon'], ['P','no_weapon'],2])
            self.cinematic_frame(screen, "bamboo2", 2, "C\'est l\'heure Musashi.", "Il est temps de s'entraîner pour la bataille qui nous attend.", kind_info=[['SM','no_weapon'],['KT','no_weapon'],2])
            self.cinematic_frame(screen, "bamboo2", 2, "Essayons de rassembler les vivres nécessaires pour notre voyage,", "et de chercher un maître pour nous apprendre l'art du Samuraï", "Allons-y mon cher camarade.", kind_info=[['SM','no_weapon'],['KT','no_weapon'],2])
            self.cinematic_frame(screen, "bamboo2", 2, "Je n\'aurais pas mieux dit. Allons voir ce village d\'Ine." , kind_info=[['SM','no_weapon'],['KT','no_weapon'],1])
            
    def cinematic_05 (self, screen, saved='none'):
        self.music.play(self.music.exploration)
        if saved == 'none':
            self.cinematic_frame(screen, 'mgm1', 2, "Excusez-moi monsieur. Y aurait-il un maître samouraï dans les parages ?", "Je suis à la recherche d'un maître Samouraï pour m'entraîner.", kind_info=[['SM','no_weapon'],['SH','no_weapon'],1])
            self.cinematic_frame(screen, 'mgm1', 2, "Un maître Samouraï ? Hmm...", "Je crois bien qu'il y en a un dans notre village.", kind_info=[['SM','no_weapon'],['SH','no_weapon'],2,None,False,['SH']])
            self.cinematic_frame(screen, 'mgm1', 2, "Ah oui ? Pouvez-vous me dire où il habite ?", "Je vous en serais très reconnaissant.", kind_info=[['SM','no_weapon'],['SH','no_weapon'],1])
            self.cinematic_frame(screen, 'mgm1', 2, "Bien sûr... à une seule condition.", kind_info=[['SM','no_weapon'],['SH','no_weapon'],2,None,False,['SH']])
            self.cinematic_frame(screen, 'mgm1', 2, "Et qu'est-ce donc ?", kind_info=[['SM','no_weapon'],['SH','no_weapon'],1,['SH']])
            self.cinematic_frame(screen, 'mgm1', 2, "Dites-moi pourquoi vous voulez devenir plus fort.", "Ceux qui cherchent la puissance comme vous ont toujours une bonne raison.", kind_info=[['SM','no_weapon'],['SH','no_weapon'],2,None,False,['SH']])
            self.cinematic_frame(screen, 'mgm1', 2, "J'ai en effet une très bonne raison de le faire.", "Récemment, mon village a été détruit par l'armée du clan Takahiro.", "Ils étaient sans pitié, et mon village n'est plus qu'un tas de cendres.", kind_info=[['SM','no_weapon'],['SH','no_weapon'],1])
            self.cinematic_frame(screen, 'mgm1', 2, "Me trouvez-vous raisonnable dans ma quête de pouvoir ?", kind_info=[['SM','no_weapon'],['SH','no_weapon'],1])
            self.cinematic_frame(screen, 'mgm1', 2, "Je comprends très bien vos ressentis et vos objectifs.", "Se venger n'est pas toujours le mieux, mais qui suis-je pour juger ?", "Très bien, je vais donc vous dire où est le maître Samouraï du village.", kind_info=[['SM','no_weapon'],['SH','no_weapon'],2,None,False,['SH']])
            self.cinematic_frame(screen, 'mgm1', 2, "Merci mille fois ! Où dois-je aller ?", kind_info=[['SM','no_weapon'],['SH','no_weapon'],1])
            self.cinematic_frame(screen, 'mgm1', 2, "Nulle part. Il se trouve juste devant vous.", kind_info=[['SM','no_weapon'],['SH','no_weapon'],2,None,False,['SH']])
            self.cinematic_frame(screen, 'mgm1', 2, "Devant moi ? Vous êtes un maître Samouraï ??", kind_info=[['SM','no_weapon'],['SH','no_weapon'],1])
            self.cinematic_frame(screen, 'mgm1', 2, "En effet, je l'étais, mais je peux vous entraîner.", kind_info=[['SM','no_weapon'],['SH','no_weapon'],2,None,False,['SH']])
            self.cinematic_frame(screen, 'mgm1', 2, "D'ailleurs, j'ai oublié les présentations.", "Je me nomme Haruto Hoshida.", "Désormais, vous m'appellerez Sensei Hoshida, je serai votre enseignant.", kind_info=[['SM','no_weapon'],['SH','no_weapon'],2])
            self.cinematic_frame(screen, 'mgm1', 2, "Merci d'accepter de m'entraîner, Sensei Hoshida.", kind_info=[['SM','no_weapon'],['SH','no_weapon'],1])
            self.cinematic_frame(screen, 'mgm1', 2, "Bien. Rejoins-moi dans mon dojo au nord du village.", "Nous verrons si tu es prêt à être entraîné.", kind_info=[['SM','no_weapon'],['SH','no_weapon'],2])
            
        elif saved == 'KM':
            self.cinematic_frame(screen, 'mgm1', 3, "Excusez-moi monsieur. Mon grand frère est à la recherche d'un maître samouraï.", "Savez-vous si on peut en trouver dans les parages ?", kind_info=[['KM','no_weapon'],['SM','no_weapon'],['SH','no_weapon'],1])
            self.cinematic_frame(screen, 'mgm1', 3, "Je peux vous renseigner, mais dîtes-moi :", "Pourquoi recherchez-vous une personne de cette carrure ?", kind_info=[['KM','no_weapon'],['SM','no_weapon'],['SH','no_weapon'],3,False,['SH']])
            self.cinematic_frame(screen, 'mgm1', 3, "Pour devenir plus fort bien sûr.", "Notre village a été détruit par le clan Takahiro.", "Nous ne pouvons pas les laisser continuer leurs actions.", kind_info=[['SM','no_weapon'],['KM','no_weapon'],['SH','no_weapon'],1,True])
            self.cinematic_frame(screen, 'mgm1', 3, "Je vois, cela est très intéressant.", "Ce n'est pas tous les jours qu'on demande à un pêcheur s'il connaît", "des maîtres samouraïs.", kind_info=[['SM','no_weapon'],['KM','no_weapon'],['SH','no_weapon'],3,False,['SH']])
            self.cinematic_frame(screen, 'mgm1', 3, "Oui, c'est vrai que demander à un pêcheur est inhabituel.", "Mais qui sait ? Il peut y avoir un Samouraï à tout moment autour de nous.", kind_info=[['KM','no_weapon'],['SM','no_weapon'],['SH','no_weapon'],1,True])
            self.cinematic_frame(screen, 'mgm1', 3, "C'est vrai. Qui sait ?", "Un Samouraï sait se fondre dans le décor.", kind_info=[['KM','no_weapon'],['SM','no_weapon'],['SH','no_weapon'],3,False,['SH']])
            self.cinematic_frame(screen, 'mgm1', 3, "Ce serait tout de même un miracle s'il y en avait un ici.", kind_info=[['SM','no_weapon'],['KM','no_weapon'],['SH','no_weapon'],1,True])
            self.cinematic_frame(screen, 'mgm1', 3, "Regardez de plus près.", "Vous saurez qu'il y a bien un maître Samouraï dans le village.", kind_info=[['SM','no_weapon'],['KM','no_weapon'],['SH','no_weapon'],3,False,['SH']])
            self.cinematic_frame(screen, 'mgm1', 3, "Hmm? Mais pourtant après avoir rencontré les habitants du village,", "ils ne semblent pas avoir ce genre de profession...", kind_info=[['KM','no_weapon'],['SM','no_weapon'],['SH','no_weapon'],1,True])
            self.cinematic_frame(screen, 'mgm1', 3, "Mais non Keiko !", "Cela voudrait dire que le maître du Samouraï se trouve juste devant nous !", kind_info=[['SM','no_weapon'],['KM','no_weapon'],['SH','no_weapon'],1,True])
            self.cinematic_frame(screen, 'mgm1', 3, "Vous avez tout compris. Je suis en effet un maître Samouraï à la retraite.", "Je me présente. Je suis Haruto Hoshida.","Désormais, vous m'appellerez Sensei Hoshida, je serai votre enseignant.", kind_info=[['SM','no_weapon'],['KM','no_weapon'],['SH','no_weapon'],3])
            self.cinematic_frame(screen, 'mgm1', 3, "Bien. Rejoignez-moi dans mon dojo au nord du village.", "Nous verrons si tu es prêt à être entraîné.", kind_info=[['SM','no_weapon'],['KM','no_weapon'],['SH','no_weapon'],3])
        
        elif saved == 'KT':
            self.cinematic_frame(screen, 'mgm1', 3, "Excusez-moi, monsieur...", kind_info=[['SM','no_weapon'],['KT','no_weapon'],['SH','no_weapon'],1])
            self.cinematic_frame(screen, 'mgm1', 3, "Hmm ? Vous semblez bien jeunes pour être des pêcheurs.", "Que cherchez-vous ici ?", kind_info=[['SM','no_weapon'],['KT','no_weapon'],['SH','no_weapon'],3,False,['SH']])
            self.cinematic_frame(screen, 'mgm1', 3, "Nous ne sommes pas là pour la pêche, mais pour trouver un maître Samouraï.", "On nous a dit qu'un tel maître vivait dans ce village.", "Savez-vous où il se trouve ?", kind_info=[['KT','no_weapon'],['SM','no_weapon'],['SH','no_weapon'],1,True])
            self.cinematic_frame(screen, 'mgm1', 3, "Un maître Samouraï ? Voilà une requête bien audacieuse.", "Et pourquoi voulez-vous apprendre l'art du sabre ?", kind_info=[['KT','no_weapon'],['SM','no_weapon'],['SH','no_weapon'],3,False,['SH']])
            self.cinematic_frame(screen, 'mgm1', 3, "Notre village a été détruit par le clan Takahiro.", "Ils ont massacré nos proches et réduit nos maisons en cendres.", kind_info=[['SM','no_weapon'],['KT','no_weapon'],['SH','no_weapon'],1,True])
            self.cinematic_frame(screen, 'mgm1', 3, "Nous voulons devenir plus forts, non seulement pour nous venger,", "mais pour protéger ce qui reste de notre village.", kind_info=[['SM','no_weapon'],['KT','no_weapon'],['SH','no_weapon'],1])
            self.cinematic_frame(screen, 'mgm1', 3, "Hmmm...", kind_info=[['SM','no_weapon'],['KT','no_weapon'],['SH','no_weapon'],3,False,['SH']])
            self.cinematic_frame(screen, 'mgm1', 3, "Je vois... Une quête de puissance motivée par la perte.", "Mais dites-moi, jeunes hommes, êtes-vous prêts à sacrifier tout ce que", "vous êtes pour cette vengeance ?", kind_info=[['SM','no_weapon'],['KT','no_weapon'],['SH','no_weapon'],3,False,['SH']])
            self.cinematic_frame(screen, 'mgm1', 3, "Nous le sommes.", "Nous avons survécu à ce massacre, et nous ne reculerons devant rien.", kind_info=[['KT','no_weapon'],['SM','no_weapon'],['SH','no_weapon'],1,True])
            self.cinematic_frame(screen, 'mgm1', 3, "Très bien. Le maître que vous cherchez... c'est moi.", "Je suis en effet un maître Samouraï à la retraite. Je me nomme Haruto Hoshida.", "Désormais, vous m'appellerez Sensei Hoshida, je serai votre enseignant.", kind_info=[['KT','no_weapon'],['SM','no_weapon'],['SH','no_weapon'],3])
            self.cinematic_frame(screen, 'mgm1', 3, "Mais avant de m'enseigner à nouveau l'art que j'ai laissé derrière moi,", "je veux être convaincu de votre détermination.", "", kind_info=[['KT','no_weapon'],['SM','no_weapon'],['SH','no_weapon'],3])
            self.cinematic_frame(screen, 'mgm1', 3, "Bien. Rejoignez-moi dans mon dojo au nord du village.", "Nous verrons si vous êtes prêts à être entraînés.", kind_info=[['KT','no_weapon'],['SM','no_weapon'],['SH','no_weapon'],3])
      
    def cinematic_06 (self,screen,saved='none'):
        self.music.play(self.music.exploration)
        self.cinematic_frame(screen, "bamboo2", 0, "Cela fait plus d'une semaine que Shikisha s'entraîne pour devenir un Samouraï.","Il continue ses efforts, cherche à briser ses limites pour se reconstruire.")
        self.cinematic_frame(screen, "bamboo2", 0, "En ce moment même...")
        self.cinematic_frame(screen, "tkh1", 1, "Les trésors...les richesses...la gloire...la puissance...","Tout ce que recherche un homme pour devenir maître de son environnement.",kind_info=['TK','TK','no_weapon','right',None,['TK']])
        self.cinematic_frame(screen, "tkh1", 1, "Certains disent que la médiocrité est un choix tout aussi simple et efficace","pour vivre heureux...",kind_info=['TK','TK','no_weapon','right',None,['TK']])
        self.cinematic_frame(screen, "tkh1", 1, "Ces gens sont des déchets, ils méritent leur vie médiocre.","Leur manque d'inspiration, de prise de risques, voire de conquête personnelle","me dégoûtent.",kind_info=['TK','TK','no_weapon','right',None,['TK']])
        self.cinematic_frame(screen, "tkh1", 1, "Et c'est pour cela que je dominerai le Japon et le monde entier.","Ceux qui ne cherchent pas à changer deviendront des êtres","sous-développés et réprimés par la société. Ici, l'évolution est sacrée.",kind_info=['TK','TK','no_weapon','right',None,['TK']])
        self.cinematic_frame(screen, "tkh1", 1, "Karasu, Hayato.",kind_info=['TK','TK','no_weapon','right',None,['TK']])
        self.cinematic_frame(screen, "tkh1", 2, "Nous sommes prêts à vous servir, maître.",kind_info=[['TK','no_weapon'],['TWs','no_weapon'],2,None,None,['TK']])
        self.cinematic_frame(screen, "tkh1", 2, "Espionnez le village d'Ine.","Une rumeur s'est propagée sur le retour d'un maître Samouraï en ce lieu.","Je redoute la naissance de nouveaux Samouraïs dans les parages.",kind_info=[['TK','no_weapon'],['TWs','no_weapon'],1,None,None,['TK']])
        self.cinematic_frame(screen, "tkh1", 2, "Essayez de vous emparer de toutes les informations que vous pouvez","récupérer à ce sujet si on doit se préparer à la moindre contre attaque.",kind_info=[['TK','no_weapon'],['TWs','no_weapon'],1,None,None,['TK']])
        self.cinematic_frame(screen, "tkh1", 2, "A vos ordres !",kind_info=[['TK','no_weapon'],['TWs','no_weapon'],2,None,None,['TK']])
        self.ecran_noir(screen)
    
    def cinematic_07 (self,screen,saved='none'):
        self.music.play(self.music.exploration)
        texts = {'none':"Takeshi..Keiko..Vous verrez, je vous vengerai ainsi que Magome.",'KM':"Takeshi...Tu verra, je te vengerai ainsi que Magome.",'KT':"Keiko...Tu verra, je te vengerai ainsi que Magome."}
        self.cinematic_frame(screen, "bamboo2", 0, "En ce moment même...")
        if saved == 'none':
            self.sound.swoosh1.play()
            self.cinematic_frame(screen, "ine1", 2, "Ha ! Hooh... Ryah !", kind_info=[['SM','no_weapon'],['SH','no_weapon'],1])
            self.cinematic_frame(screen, "ine1", 2, "Évite tout mouvement inutile.", "Tu dois agir non seulement rapidement mais aussi correctement.", "La technique surpasse toujours la puissance.", kind_info=[['SM','no_weapon'],['SH','no_weapon'],2])
            self.sound.swoosh2.play()
            self.cinematic_frame(screen, "ine1", 2, "Oui Sensei Hoshida ! Hyah ! Ho ! Ha !", kind_info=[['SM','no_weapon'],['SH','no_weapon'],1])
            self.cinematic_frame(screen, "ine1", 2, "Arrêtons-nous là. Tu as bien travaillé. Il faut que tu récupères tes forces", "avant de continuer. C'est en utilisant la totalité de ton énergie que tu", "pourras observer de très grands progrès.", kind_info=[['SM','no_weapon'],['SH','no_weapon'],2])
            self.cinematic_frame(screen, "ine1", 2, "Compris", kind_info=[['SM','no_weapon'],['SH','no_weapon'],1])
            
        elif saved == 'KM':
            self.cinematic_frame(screen, "ine1", 2, "Ne retenez pas vos coups, Sensei Hoshida !", kind_info=[['SM','no_weapon'],['SH','no_weapon'],1])
            self.cinematic_frame(screen, "ine1", 2, "Ce serait plutôt à moi de te le dire !", kind_info=[['SM','no_weapon'],['SH','no_weapon'],2])
            self.cinematic_frame(screen, "ine1", 2, "L'élève et le maître sont en plein duel.","L'entraînement commence à devenir féroce.", kind_info=[['SM','no_weapon'],['SH','no_weapon'],0])
            self.cinematic_frame(screen, "ine1", 3, "Allez grand frère! Tu peux le faire !", kind_info=[['SM','no_weapon'],['SH','no_weapon'],['KM','no_weapon'],3])
            self.sound.swoosh1.play()
            self.cinematic_frame(screen, "ine1", 2, "Ha ! Ryah ! Ooh.. Hyah !", kind_info=[['SM','no_weapon'],['SH','no_weapon'],1])
            self.cinematic_frame(screen, "ine1", 2, "Tu manques de vitesse Musashi ! Et tu es assez prévisible !", "Ta défense est trop faible... Ici !", kind_info=[['SM','no_weapon'],['SH','no_weapon'],2])
            self.sound.swoosh3.play()
            self.cinematic_frame(screen, "ine1", 2, "Aïe ! Même pas mal !", kind_info=[['SM','no_weapon'],['SH','no_weapon'],1])
            self.cinematic_frame(screen, "ine1", 2, "C'est bien, continue comme ça... Il faut que tu te surpasses chaque jour !", kind_info=[['SM','no_weapon'],['SH','no_weapon'],2])
            self.cinematic_frame(screen, "ine1", 2, "La prochaine fois, la victoire sera à moi !", kind_info=[['SM','no_weapon'],['SH','no_weapon'],1])
            self.cinematic_frame(screen, "ine1", 2, "J'ai hâte de voir ça. Sur ce, reposons-nous.", "Le repos après un entraînement est indispensable pour progresser.", kind_info=[['SM','no_weapon'],['SH','no_weapon'],2])
            self.cinematic_frame(screen, "ine1", 2, "Très bien Sensei. Je vais faire un tour dans le dojo pendant ce temps.", "Keiko, tu m'accompagnes ?", kind_info=[['SM','no_weapon'],['KM','no_weapon'],['SH','no_weapon'],1])
            self.cinematic_frame(screen, "ine1", 2, "Désolée, je dois aller faire ma gymnastique.", kind_info=[['KM','no_weapon'],['SM','no_weapon'],['SH','no_weapon'],1, True])
            self.cinematic_frame(screen, "ine1", 2, "Comme tu veux.", kind_info=[['SM','no_weapon'],['KM','no_weapon'],['SH','no_weapon'],1, True])
            
        elif saved == 'KT':
            self.cinematic_frame(screen, "ine1", 2, "Est-ce que tu es prêt Musashi ?","Il faut se donner à fond !", kind_info=[['SM','no_weapon'],['KT','no_weapon'],2])
            self.cinematic_frame(screen, "ine1", 2, "Bien sûr que je le suis. Je ne compte pas me retenir.", kind_info=[['SM','no_weapon'],['KT','no_weapon'],1])
            self.cinematic_frame(screen, "ine1", 2, "Alors on y va ! Hyah !", kind_info=[['SM','no_weapon'],['KT','no_weapon'],2])
            self.cinematic_frame(screen, "ine1", 2, "C'est parti ! Ryah !", kind_info=[['SM','no_weapon'],['KT','no_weapon'],1])
            self.cinematic_frame(screen, "ine1", 2, "Par ici !", kind_info=[['SM','no_weapon'],['KT','no_weapon'],1])
            self.cinematic_frame(screen, "ine1", 2, "Bien joué, mais tu ne t'attendras pas à ça !", kind_info=[['SM','no_weapon'],['KT','no_weapon'],2])
            self.sound.swoosh4.play()
            self.cinematic_frame(screen, "ine1", 2, "Kh... Je m'y attendais pas ! Mais ce n'est qu'un coup de chance !", kind_info=[['SM','no_weapon'],['KT','no_weapon'],1])
            self.cinematic_frame(screen, "ine1", 1, "Ils ont un niveau de coordination inimaginable...", "C'est comme si leurs cœurs battaient en rythme.", kind_info=['SH','SH','no_weapon',None,None,None,True])            
            self.cinematic_frame(screen, "ine1", 2, "Il est temps d'en finir Musashi. Hah !", kind_info=[['SM','no_weapon'],['KT','no_weapon'],2])            
            self.cinematic_frame(screen, "ine1", 2, "Tu as tout compris. Huah !", kind_info=[['SM','no_weapon'],['KT','no_weapon'],1])
            self.sound.swoosh3.play()
            self.cinematic_frame(screen, "ine1", 2, "Raaaah !", kind_info=[['SM','no_weapon'],['KT','no_weapon'],2])
            self.ecran_noir(screen)
            self.cinematic_frame(screen, "ine1", 1, "Interrésant...","Le duel s'est terminé par une égalité...", kind_info=['SH','SH','no_weapon',None,None,None,True])
            self.cinematic_frame(screen, "ine1", 2, "On dirait qu'on ne saura pas qui est le plus fort entre nous deux.", kind_info=[['SM','no_weapon'],['KT','no_weapon'],1])
            self.cinematic_frame(screen, "ine1", 2, "Dommage. On va en finir une autre fois.", kind_info=[['SM','no_weapon'],['KT','no_weapon'],1])
            self.cinematic_frame(screen, "ine1", 3, "Superbe duel vous deux.", "Musashi, il faut que tu anticipes un peu plus le mouvements de tes", "adversaires.", kind_info=[['SM','no_weapon'],['KT','no_weapon'],['SH','no_weapon'],3])
            self.cinematic_frame(screen, "ine1", 2, "Takeshi, essaie de prendre plus souvent l'initiative.", "Ainsi, tu pourras te créer encore plus d'opportunités.", kind_info=[['SM','no_weapon'],['KT','no_weapon'],['SH','no_weapon'],3])
            self.cinematic_frame(screen, "ine1", 2, " Bien, prenons une pause.", "Il faut reprendre des forces avant la prochaine séance.", kind_info=[['SM','no_weapon'],['KT','no_weapon'],['SH','no_weapon'],3])
            self.cinematic_frame(screen, "ine1", 2, "Super. Je vais prendre quelque chose à manger. Tu as faim Musashi ?", kind_info=[['SM','no_weapon'],['KT','no_weapon'],2])
            self.cinematic_frame(screen, "ine1", 2, "Hmm...Pas encore, mais merci de me l'avoir demandé.", "Je vais faire un tour dans le dojo pendant ce temps.", kind_info=[['SM','no_weapon'],['KT','no_weapon'],1])
            self.cinematic_frame(screen, "ine1", 2, "Pas de problème. On se retrouve tout-à l'heure", kind_info=[['SM','no_weapon'],['KT','no_weapon'],2])
            self.cinematic_frame(screen, "ine1", 2, "Bon apétit !", kind_info=[['SM','no_weapon'],['KT','no_weapon'],1])
        
        self.ecran_noir(screen)
        self.cinematic_frame(screen, "doj2", 1, "1 semaine est passée..Je suis étonné de pouvoir m'améliorer à", "une telle vitesse. Si je continue comme ça, je deviendrai un samouraï", "en à peine 1 mois.", kind_info=['SM','SM','no_weapon'])
        self.cinematic_frame(screen, "doj2", 1, texts[saved], "Je protégerai ceux qui me tiennent à cœur.", kind_info=['SM','SM','no_weapon'])
        self.cinematic_frame(screen, "doj2", 2, "Bon Karasu. A ce que je vois, la rumeur du maître samouraï s'avère vraie.", "Je pense qu'on a tout ce qu'il nous faut.", kind_info=[['TW','no_weapon'],['TW_H','no_weapon'],1])
        self.cinematic_frame(screen, "doj2", 2, "Essayons de rester un peu plus pour obtenir le plus d'informations possible.", "Le maître nous récompensera !", kind_info=[['TW','no_weapon'],['TW_H','no_weapon'],2])
        self.lowercase = True
        self.cinematic_frame(screen, "doj2", 3, "Qui sont ces gens qui sont là depuis tout-à l'heure ?", "Des intrus ? Est-ce qu'ils nous espionnent ? Il faut les arrêter !", kind_info=[['TW','no_weapon'],['TW_H','cin07'],['SM','no_weapon'],3,])
        self.cinematic_frame(screen, "doj2", 3, "Que faire ? Je les suis ? Je préviens Sensei ?", "Je ne sais pas quoi faire...", kind_info=[['TW','no_weapon'],['TW_H','cin07'],['SM','no_weapon'],3,])
        self.lowercase = False
    
    def cinematic_08 (self,screen, choose=1):
        self.music.play(self.music.exploration)
        self.lowercase = True
        if choose == 1:
            self.cinematic_frame(screen, "doj2", 3, "Pas le choix. Je dois prévenir Hoshida immédiatement !", kind_info=[['TW','no_weapon'],['TW_H','cin07'],['SM','no_weapon'],3,])
            self.lowercase = False
            self.ecran_noir(screen)
            self.sound.scary_effect.play
            self.cinematic_frame(screen, "ine1", 2,"Sensei Hoshida ! On a un gros problème !",kind_info=[["SH","no_weapon"],["SM","no_weapon"],2])
            self.cinematic_frame(screen, "ine1", 2,"Hm ? Que se passe-t-il Musashi ?",kind_info=[["SH","no_weapon"],["SM","no_weapon"],1])
            self.cinematic_frame(screen, "ine1", 2,"Des espions sont venus surveiller notre entraînement !", "Je pense qu'il faut les arrêter avant que ça empire.", "Je crois qu'ils proviennent du clan Takahiro.",kind_info=[["SH","no_weapon"],["SM","no_weapon"],2])
            self.cinematic_frame(screen, "ine1", 2,"Pas besoin.", "Ils auront beau obtenir nos techniques de combats, ils n'auront pas", "la possibilité d'appliquer tout ce que je t'aurai appris.",kind_info=[["SH","no_weapon"],["SM","no_weapon"],1])
            self.cinematic_frame(screen, "ine1", 2,"Donc on va juste les laisser partir ? Sans rien faire ?", "Je pense qu'ils peuvent devenir encore plus forts qu'on ne le pense...", kind_info=[["SH","no_weapon"],["SM","no_weapon"],2])
            self.cinematic_frame(screen, "ine1", 2,"Ne t'inquiète pas. S'ils comptent utiliser mes techniques,", "on va ajouter encore plus d'intensité à tes entraînements pour que", "tu sois prêt le moment venu.", kind_info=[["SH","no_weapon"],["SM","no_weapon"],1])
            self.cinematic_frame(screen, "ine1", 2,"Par ailleurs, c'était très noble de ta part de me prévenir au lieu de", "les suivre ou de les attaquer directement.", "Tu es largement digne de devenir un samouraï.",kind_info=[["SH","no_weapon"],["SM","no_weapon"],1])
            self.ecran_noir(screen)
        elif choose == 2:
            self.cinematic_frame(screen, "doj2", 3, "Tant pis, je vais les suivre et recueillir le plus d'informations possible.", kind_info=[['TW','no_weapon'],['TW_H','cin07'],['SM','no_weapon'],3,])
            self.lowercase = False
        elif choose == 3:
            self.cinematic_frame(screen, "doj2", 3, "Ils ne doivent surtout pas s'échapper ! Il faut les empêcher !", kind_info=[['TW','no_weapon'],['TW_H','cin07'],['SM','no_weapon'],3,])
            self.lowercase = False
            self.cinematic_frame(screen, "doj2", 3, "Ne pensez que vous allez vous enfuir !", "Je compte vous battre ici et maintenant !", kind_info=[['TW','no_weapon'],['TW_H','no_weapon'],['SM','no_weapon'],3,])
            self.cinematic_frame(screen, "doj2", 3, "Pff, tu penses vraiment nous battre tous les deux ?", "Franchement tu nous sous-estimes.", kind_info=[['TW','no_weapon'],['TW_H','no_weapon'],['SM','no_weapon'],2,])
            self.cinematic_frame(screen, "doj2", 3, "Ne viens pas demander pitié quand tu perdras.", kind_info=[['TW','no_weapon'],['TW_H','no_weapon'],['SM','no_weapon'],1,])
        else:
            print("Si vous êtes sur la sauvegarde développeur, merci de paramétrer un choix avec la commande /choice 2 [choix]. Sinon, votre sauvegarde est corrompue")
        
    def cinematic_09 (self, screen, saved="none"):
        self.music.play(self.music.menu)
        if saved == 'none':
            self.cinematic_frame(screen, "ine1", 0, "Ainsi, Musashi continue son entraînement avec Sensei Hoshida.", "Chaque jour, il continue à se dépasser, à s'améliorer et à progresser.",)
            self.ecran_noir(screen)
            self.cinematic_frame(screen, 'ine1', 0, "Un mois plus tard...")
            self.cinematic_frame(screen, 'ine1', 2, "Mon cher élève, je te félicite d'avoir participé à cet entraînement", "et d'avoir donné 100% de tes capacités quotidiennement.", "Désormais, je te nomme officiellement Samouraï. Tu l'as bien mérité.", kind_info=[["SM","no_weapon"],["SH","no_weapon"],2])
            self.cinematic_frame(screen, "ine1", 2, "Merci beaucoup de m'avoir entraîné, Sensei Hoshida.", "Je ferai bon usage de vos cours et je vous prouverai que vous avez choisi le", "bon élève.", kind_info=[["SM","no_weapon"],["SH","no_weapon"],1])
            self.cinematic_frame(screen, 'ine1', 2, "J'ai hâte de voir cela. Tiens, voici 100 pièces pour ton voyage.", "N'hésite pas à les utiliser pour t'équiper, te nourrir ou te renforcer.", "Sur ce, j'espère que tu accompliras de nombreux exploits.", kind_info=[["SM","no_weapon"],["SH","no_weapon"],2])
            self.cinematic_frame(screen, 'ine1', 2, "C'est sûr ! À la prochaine Sensei Hoshida !", kind_info=[["SM","no_weapon"],["SH","no_weapon"],1])
            self.cinematic_frame(screen, 'ine1', 2, "Bon voyage Musashi ! Fais attention à toi !", kind_info=[["SM","no_weapon"],["SH","no_weapon"],2])
            self.cinematic_frame(screen, 'ine1', 3, "Devenu samouraï, Musashi décide de partir à la recherche", "d'un village pour s'équiper afin de se préparer au long combat qui l'attend", "contre le clan Takahiro, celui qui a détruit son village natal.", kind_info=[["KT","no_weapon"],["SM","no_weapon"],["SH","no_weapon"],0])
        elif saved == 'KM':
            self.cinematic_frame(screen, "ine1", 0, "Ainsi, Musashi continue son entraînement avec Sensei Hoshida.", "Chaque jour, il continue à se dépasser, à s'améliorer et à progresser.",)
            self.ecran_noir(screen)
            self.cinematic_frame(screen, 'ine1', 0, "Un mois plus tard...")
            self.cinematic_frame(screen, 'ine1', 3, "Mon cher élève, je te félicite d'avoir participé à cet entraînement", "et d'avoir donné 100% de tes capacités quotidiennement.", "Désormais, je te nomme officiellement Samouraï. Tu l'as bien mérité.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH","no_weapon"],3])
            self.cinematic_frame(screen, "ine1", 3, "Merci beaucoup de m'avoir entraîné, Sensei Hoshida.", "Je ferai bon usage de vos cours et je vous prouverai que vous avez choisi le", "bon élève.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH","no_weapon"],1])
            self.cinematic_frame(screen, 'ine1', 3, "J'ai hâte de voir cela. Tenez, voici 50 pièces chacun pour votre voyage.", "N'hésitez pas à les utiliser pour vous équiper, nourrir ou vous renforcer.", "Sur ce, j'espère que vous accomplirez de nombreux exploits.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH","no_weapon"],3])
            self.cinematic_frame(screen, 'ine1', 3, "C'est sûr ! À la prochaine Sensei Hoshida !", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH","no_weapon"],1])
            self.cinematic_frame(screen, 'ine1', 3, "A la prochaine ! Merci d'avoir entraîné mon grand frère !", kind_info=[["KM","no_weapon"],["SM","no_weapon"],["SH","no_weapon"],1,True])
            self.cinematic_frame(screen, 'ine1', 3, "Bon voyage Shikisha et Keiko ! Faites attention à vous !", kind_info=[["KM","no_weapon"],["SM","no_weapon"],["SH","no_weapon"],3])
            self.cinematic_frame(screen, 'ine1', 3, "Musashi devenu samouraï, lui et sa sœur décident de partir à la recherche", "d'un village pour s'équiper afin de se préparer au long combat qui les attend", "contre le clan Takahiro, celui qui a détruit leur village natal.", kind_info=[["KM","no_weapon"],["SM","no_weapon"],["SH","no_weapon"],0])
        elif saved == 'KT':
            self.cinematic_frame(screen, "ine1", 0, "Ainsi, Musashi et Takeshi continuent leur entraînement avec Sensei Hoshida.", "Chaque jour, il continuent à se dépasser, à s'améliorer et à progresser.",)
            self.ecran_noir(screen)
            self.cinematic_frame(screen, 'ine1', 0, "Un mois plus tard...")
            self.cinematic_frame(screen, 'ine1', 3, "Mes chers élèves, je vous félicite d'avoir participé à cet entraînement", "et d'avoir donné 100% de vos capacités quotidiennement.", "Désormais, je vous nomme officiellement Samouraïs. Vous l'avez bien mérité.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["SH","no_weapon"],3])
            self.cinematic_frame(screen, "ine1", 3, "Merci beaucoup de m'avoir entraîné, Sensei Hoshida.", "Je ferai bon usage de vos cours et je vous prouverai que vous avez choisi le", "bon élève.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["SH","no_weapon"],1])
            self.cinematic_frame(screen, 'ine1', 3, "Je vous suis très reconnaissant Sensei Hoshida.", "Vous nous avez très bien enseignés.", kind_info=[["KT","no_weapon"],["SM","no_weapon"],["SH","no_weapon"],1,True])
            self.cinematic_frame(screen, 'ine1', 3, "J'ai hâte de voir cela. Tenez, voici 50 pièces chacun pour votre voyage.", "N'hésitez pas à les utiliser pour vous équiper, nourrir ou vous renforcer.", "Sur ce, j'espère que vous accomplirez de nombreux exploits.", kind_info=[["KT","no_weapon"],["SM","no_weapon"],["SH","no_weapon"],3])
            self.cinematic_frame(screen, 'ine1', 3, "C'est sûr ! À la prochaine Sensei Hoshida !", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["SH","no_weapon"],1,True])
            self.cinematic_frame(screen, 'ine1', 3,  "À la prochaine maître !", kind_info=[["KT","no_weapon"],["SM","no_weapon"],["SH","no_weapon"],1,True])
            self.cinematic_frame(screen, 'ine1', 3, "Bon voyage Musashi et Takeshi ! Faites attention à vous !", kind_info=[["KT","no_weapon"],["SM","no_weapon"],["SH","no_weapon"],3])
            self.cinematic_frame(screen, 'ine1', 3, "Devenus samouraïs, Musashi et Takeshi décident de partir à la recherche", "d'un village pour s'équiper afin de se préparer au long combat qui les attend", "contre le clan Takahiro, celui qui a détruit leur village natal.", kind_info=[["KT","no_weapon"],["SM","no_weapon"],["SH","no_weapon"],0])
        self.ecran_noir(screen)
    
    def cinematic_10(self, screen, saved="none"):
        #cinématique vérifiée
        if saved == 'none':
            self.cinematic_frame(screen,'bamboo1', 1, "Un nouveau départ. Je suis enfin devenu un samouraï. Je vais enfin pouvoir", "venger Magome. Allons à la ville d'Aizuwakamatsu,on n'a plus de temps à ", "perdre. Hm? (Un ennemi ?)",  kind_info=["SM", "SM", "no_weapon", "right"])
            self.cinematic_frame(screen,'bamboo1', 1, "Montrez vous ! Je sais que vous vous trouvez à l'intérieur de cette caravane.",  kind_info=["SM","SM", "no_weapon","right"])
            self.ecran_noir(screen)
            self.cinematic_frame(screen, "bamboo1", 2, "Tiens ? Un samouraï ?", kind_info=[['SM','no_weapon'], ['JM','no_weapon'], 2, None, None, ['JM']])
            self.cinematic_frame(screen, 'bamboo1', 2, "Qui êtes-vous ? Que faîtes vous ici ? Expliquez vous !", kind_info=[['SM','no_weapon'], ['JM','no_weapon'], 1])
            self.cinematic_frame(screen, "bamboo1", 2, "Calmez-vous jeune homme. Je ne souhaite pas vous faire de mal. Avant de me","poser des questions, pourriez-vous au moins vous présenter ?", kind_info=[['SM','no_weapon'], ['JM','no_weapon'], 2, None, None, ['JM']])
            self.cinematic_frame(screen, 'bamboo1', 2, "C'est vrai. Veuillez m'excuser de mon impolitesse. Je suis Shikisha Musashi.", "Je viens du village de Magome, et je suis récemment devenu un samouraï.","Enchanté. Et vous ?", kind_info=[['SM','no_weapon'], ['JM','no_weapon'], 1])
            self.cinematic_frame(screen, 'bamboo1', 2, "Je suis Juzo Ma, un marchand. Je collecte de nombreux produits pour pouvoir", "les revendre ensuite. Voudriez-vous bien jeter un coup d'œil à mes","marchandises ? ", kind_info=[['SM','no_weapon'], ['JM','no_weapon'], 2])
            self.cinematic_frame(screen, 'bamboo1', 2, "Très bien. Je suis intéressé par vos offres. Que vendez-vous ?", kind_info=[['SM','no_weapon'], ['JM','no_weapon'], 1])
            self.cinematic_frame(screen, 'bamboo1', 2, "Je vends de tout. Talismans, potions, nourriture, etc. Auriez-vous une","préférence?", kind_info=[['SM','no_weapon'], ['JM','no_weapon'], 2])
            self.cinematic_frame(screen, 'bamboo1', 2, "Dans ce cas là, vous devez avoir des armes, n'est-ce pas ?", kind_info=[['SM','no_weapon'], ['JM','no_weapon'], 1])
            self.cinematic_frame(screen, 'bamboo1', 2, "Absolument! Actuellement, je possède une arme très destructrice. Le “Tengoku", "No Ikari”.(La colère du Paradis)", kind_info=[['SM','no_weapon'], ['JM','no_weapon'], 2])
            self.cinematic_frame(screen, 'bamboo1', 2, "“Tengoku no Ikari”? Je n'en ai jamais entendu parler. Pourquoi porte-elle","ce nom ?", kind_info=[['SM','no_weapon'], ['JM','no_weapon'], 1])
            self.cinematic_frame(screen, 'bamboo1', 2, "La légende raconte que cette lame incarnerait le châtiment de Dieu. On la", "classait comme l'une des 7 épées légendaires. Tous ceux qui sont touchés", "par cette arme périssent en voyant leurs âmes séparées de leurs corps. ", kind_info=[['SM','no_weapon'], ['JM','no_weapon'], 2])
            self.cinematic_frame(screen, 'bamboo1', 2, "C'est pour cela que je la vends pour 100 pièces d'or. Elle est très rare,","et possède beaucoup de valeur. Alors ? Êtes-vous prêt à l'acheter ?", kind_info=[['SM','no_weapon'], ['JM','no_weapon'], 2])
        elif saved == 'KM':
            self.cinematic_frame(screen,'bamboo1', 2, "Le moment est enfin arrivé. Je suis enfin devenu un samouraï.",   kind_info=[['SM','no_weapon'], ['KM','no_weapon'], 1])
            self.cinematic_frame(screen,'bamboo1', 2, "Oui, tu es resté déterminé et tu as réussi à atteindre tes objectifs. Tu es","incroyable grand frère !",   kind_info=[['SM','no_weapon'], ['KM','no_weapon'], 2])
            self.cinematic_frame(screen,'bamboo1', 2, "Merci Keiko, mais c'est aussi grâce à toi que tu me pousses à continuer ce", "voyage. Ensemble, la famille Musashi ne périra jamais. ",   kind_info=[['SM','no_weapon'], ['KM','no_weapon'], 1])
            self.cinematic_frame(screen,'bamboo1', 2, "Très bien dit Shikisha. Ne restons pas les bras croisés et poursuivons ce", "voyage !",   kind_info=[['SM','no_weapon'], ['KM','no_weapon'], 2])
            self.cinematic_frame(screen,'bamboo1', 2, "En effet. Allons-y Keiko. Ne perdons pas de temps !",   kind_info=[['SM','no_weapon'], ['KM','no_weapon'], 1])
            self.ecran_noir(screen)
            self.cinematic_frame(screen,'bamboo1', 2, "Tiens, Shikisha. On dirait qu'il y a une caravane au milieu de la route.",   kind_info=[['SM','no_weapon'], ['KM','no_weapon'], 2])
            self.cinematic_frame(screen,'bamboo1', 2, "C'est vrai. Se pourrait-il qu'il y ait un marchand ?",   kind_info=[['SM','no_weapon'], ['KM','no_weapon'], 1])
            self.cinematic_frame(screen, "bamboo1", 0, "(Les buissons bougent derrière la caravane)")
            self.cinematic_frame(screen,'bamboo1', 2, "Hm? Un ennemi ?. Montrez vous ! Je sais que vous vous trouvez à l'intérieur", "de cette caravane.",   kind_info=[['SM','no_weapon'], ['KM','no_weapon'], 1])
            self.cinematic_frame(screen, "bamboo1", 0, "(Une figure apparaît)")
            self.cinematic_frame(screen, "bamboo1", 3, "Tiens ? Un samouraï ?", kind_info=[['SM','no_weapon'], ['KM','no_weapon'],['JM','no_weapon'], 3, None, ['JM']])
            self.cinematic_frame(screen,'bamboo1', 3, "Qui êtes-vous ? Que faîtes vous ici ? Expliquez vous !",   kind_info=[['SM','no_weapon'], ['KM','no_weapon'],['JM','no_weapon'], 1])
            self.cinematic_frame(screen, "bamboo1", 3, "Calmez-vous jeune homme. Je ne souhaite pas vous faire de mal. Avant", "de me poser des questions, pourriez-vous au moins vous présenter ?", kind_info=[['SM','no_weapon'], ['KM','no_weapon'],['JM','no_weapon'], 3, None, ['JM']])
            self.cinematic_frame(screen,'bamboo1', 3, "C'est vrai. Veuillez m'excuser de mon impolitesse. Je suis Shikisha Musashi.", "Je viens du village de Magome, et je suis récemment devenu un samouraï.","Enchanté. Et vous ?",   kind_info=[['SM','no_weapon'], ['KM','no_weapon'],['JM','no_weapon'], 1])
            self.cinematic_frame(screen,'bamboo1', 3, "Je suis Keiko Musashi, sa sœur. Ravi de vous rencontrer. Et vous ?",   kind_info=[['KM','no_weapon'],['SM','no_weapon'],['JM','no_weapon'], 1, True])
            self.cinematic_frame(screen, "bamboo1", 3, "Je suis Juzo Ma, un marchand. Je collecte de nombreux produits pour pouvoir", "les revendre ensuite. Voudriez-vous bien jeter un coup d'œil à mes", "marchandises ?", kind_info=[['KM','no_weapon'],['SM','no_weapon'],['JM','no_weapon'], 3])
            self.cinematic_frame(screen,'bamboo1', 3, "Shikisha, je pense qu'il pourrait y avoir des armes ou des armures pour", "t'équiper. Voyons voir de plus près ce qu'il pourrait vendre.",   kind_info=[['KM','no_weapon'],['SM','no_weapon'],['JM','no_weapon'], 1])
            self.cinematic_frame(screen,'bamboo1', 3, "Pas bête chère sœur. Marchand Juzo, que vendez-vous?",   kind_info=[['SM','no_weapon'], ['KM','no_weapon'],['JM','no_weapon'], 1, True])
            self.cinematic_frame(screen, "bamboo1", 3, "Je vends de tout. Talismans, potions, nourriture, etc. Auriez-vous une", "préférence?", kind_info=[['SM','no_weapon'], ['KM','no_weapon'],['JM','no_weapon'], 3])
            self.cinematic_frame(screen,'bamboo1', 3, "Dans ce cas là, vous devez avoir des armes, n'est-ce pas ?",   kind_info=[['SM','no_weapon'], ['KM','no_weapon'],['JM','no_weapon'], 1])
            self.cinematic_frame(screen, "bamboo1", 3, "Absolument ! Actuellement, je possède une arme très destructrice. Le", "“Tengoku No Ikari”. (La colère du Paradis)", kind_info=[['SM','no_weapon'], ['KM','no_weapon'],['JM','no_weapon'], 3])
            self.cinematic_frame(screen,'bamboo1', 3, "“Tengoku no Ikari”? Je n'en ai jamais entendu parler. Pourquoi porte-"," elle ce nom ?",   kind_info=[['SM','no_weapon'], ['KM','no_weapon'],['JM','no_weapon'], 1])
            self.cinematic_frame(screen, "bamboo1", 3, "La légende raconte que cette lame incarnerait le châtiment de Dieu. On la", "classe comme l'une des 7 épées légendaires. Tous ceux qui sont touchés", "par cette arme périssent en voyant leurs âmes séparées de leurs corps.  ", kind_info=[['SM','no_weapon'], ['KM','no_weapon'],['JM','no_weapon'], 3])
            self.cinematic_frame(screen, "bamboo1", 3, "C'est pour cela que je la vends pour 100 pièces d'or. Elle est très rare, et", "possède beaucoup de valeur. Alors ? Êtes-vous prêt à l'acheter ?", kind_info=[['SM','no_weapon'], ['KM','no_weapon'],['JM','no_weapon'], 3])


        elif saved == 'KT':
            self.cinematic_frame(screen,'bamboo1', 2, "Le moment est enfin venu Takeshi. Nous sommes devenus des samouraïs.",   kind_info=[['SM','no_weapon'], ['KT','no_weapon'], 1])
            self.cinematic_frame(screen,'bamboo1', 2, "Après 1 mois d'entraînement acharné, nous allons enfin pouvoir venger Magome.", "Cela ne sera pas facile Musashi. Il faudra continuer à travailler dur","si on veut battre le clan Takahiro.",  kind_info=[['SM','no_weapon'], ['KT','no_weapon'], 2])
            self.cinematic_frame(screen,'bamboo1', 2, "En effet. Il ne faut surtout pas s'arrêter à notre niveau actuel. On peut", "toujours aller plus loin. Pour l'instant, le but, c'est d'atteindre le", "village d'Aizuwakamatsu pour pouvoir bien s'équiper lors du combat final.",   kind_info=[['SM','no_weapon'], ['KT','no_weapon'], 1])
            self.cinematic_frame(screen,'bamboo1', 2, "Utilisons ces pièces à bon escient. Tu es prêt Musashi ? Traversons cette", "forêt !",   kind_info=[['SM','no_weapon'], ['KT','no_weapon'], 2])
            self.cinematic_frame(screen,'bamboo1', 2, "On y va Takeshi ! Ensemble, nous sommes invincibles !",   kind_info=[['SM','no_weapon'], ['KT','no_weapon'], 1])
            self.ecran_noir(screen)
            self.cinematic_frame(screen,'bamboo1', 2, "Sois vigilant Musashi, un ennemi semble être caché dans les parages.",   kind_info=[['SM','no_weapon'], ['KT','no_weapon'], 2])
            self.cinematic_frame(screen,'bamboo1', 2, "Hm? Un ennemi ?. Cela semble bien être le cas. Il se cache dans cette", "caravane.",   kind_info=[['SM','no_weapon'], ['KT','no_weapon'], 1])
            self.cinematic_frame(screen,'bamboo1', 2, "Je m'en occupe. Montrez vous ! Je sais que vous vous trouvez à l'intérieur", "de cette caravane.",   kind_info=[['SM','no_weapon'], ['KT','no_weapon'], 2])
            self.cinematic_frame(screen, "bamboo1", 3, "Tiens ? Des voyageurs ? Plus spécifiquement des samouraïs ?", kind_info=[['SM','no_weapon'], ['KT','no_weapon'],['JM','no_weapon'], 3, None, ['JM']])
            self.cinematic_frame(screen,'bamboo1', 3, "Qui êtes-vous ? Que faîtes vous ici ? Expliquez vous !",   kind_info=[['SM','no_weapon'], ['KT','no_weapon'],['JM','no_weapon'], 1])
            self.cinematic_frame(screen, "bamboo1", 3, "Calmez-vous jeunes hommes. Je ne souhaite pas vous faire de mal. Avant de", "me poser des questions, pourriez-vous au moins vous présenter ?", kind_info=[['SM','no_weapon'], ['KT','no_weapon'],['JM','no_weapon'], 3, None, ['JM']])
            self.cinematic_frame(screen,'bamboo1', 3, "C'est vrai. Veuillez nous excuser.",   kind_info=[['SM','no_weapon'], ['KT','no_weapon'],['JM','no_weapon'], 1])
            self.cinematic_frame(screen,'bamboo1', 3, "Je m'excuse aussi. Je suis Kurosawa Takeshi, un samouraï. ",   kind_info=[['SM','no_weapon'], ['KT','no_weapon'],['JM','no_weapon'], 2])
            self.cinematic_frame(screen,'bamboo1', 3, "Je suis Shikisha Musashi. Nous provenons tous les deux du village de Magome", "et nous sommes récemment devenus des samouraïs. ",   kind_info=[['SM','no_weapon'], ['KT','no_weapon'],['JM','no_weapon'], 1])
            self.cinematic_frame(screen,'bamboo1', 3, "Enchanté de faire votre connaissance. Et vous ?",   kind_info=[['KT','no_weapon'],['SM','no_weapon'],['JM','no_weapon'], 1, True])
            self.cinematic_frame(screen, "bamboo1", 3, "Je suis Juzo Ma, un marchand. Je collecte de nombreux produits pour pouvoir", "les revendre ensuite. Voudriez-vous bien jeter un coup d'œil à mes", "marchandises ?", kind_info=[['KT','no_weapon'],['SM','no_weapon'],['JM','no_weapon'], 3])
            self.cinematic_frame(screen,'bamboo1', 3, "Un marchand qui vend divers types d'objets ? On a peut-être la possibilité de","s'équiper au préalable.",   kind_info=[['KT','no_weapon'],['SM','no_weapon'],['JM','no_weapon'], 1])
            self.cinematic_frame(screen,'bamboo1', 3, "Je suis du même avis. Très bien. Que vendez-vous?",   kind_info=[['SM','no_weapon'], ['KT','no_weapon'],['JM','no_weapon'], 1, True])
            self.cinematic_frame(screen, "bamboo1", 3, "Je vends de tout. Talismans, potions, nourriture, etc. Auriez-vous une", "préférence?", kind_info=[['SM','no_weapon'], ['KT','no_weapon'],['JM','no_weapon'], 3])
            self.cinematic_frame(screen,'bamboo1', 3, "Dans ce cas là, vous devez avoir des armes, n'est-ce pas ?",   kind_info=[['SM','no_weapon'], ['KT','no_weapon'],['JM','no_weapon'], 1])
            self.cinematic_frame(screen, "bamboo1", 3, "Absolument ! Actuellement, je possède une arme très destructrice. Le", "“Tengoku No Ikari”. (La colère du Paradis)", kind_info=[['SM','no_weapon'], ['KT','no_weapon'],['JM','no_weapon'], 3])
            self.cinematic_frame(screen,'bamboo1', 3, "“Tengoku no Ikari”? Je n'en ai jamais entendu parler. Pourquoi porte-"," elle ce nom ?",   kind_info=[['SM','no_weapon'], ['KT','no_weapon'],['JM','no_weapon'], 1])
            self.cinematic_frame(screen, "bamboo1", 3, "La légende raconte que cette lame incarnerait le châtiment de Dieu. On la", "classe comme l'une des 7 épées légendaires. Tous ceux qui sont touchés", "par cette arme périssent en voyant leurs âmes séparées de leurs corps.", kind_info=[['SM','no_weapon'], ['KT','no_weapon'],['JM','no_weapon'], 3])
            self.cinematic_frame(screen, "bamboo1", 3, "C'est pour cela que je la vends pour 100 pièces d'or. Elle est très rare, et", "possède beaucoup de valeur. Alors ? Êtes-vous prêt à l'acheter ?", kind_info=[['SM','no_weapon'], ['KT','no_weapon'],['JM','no_weapon'], 3])
        self.ecran_noir(screen)

        
    def cinematic_11 (self, screen, saved="none", choose=1):
        #cinématique vérifiée
        if saved == 'none':
            if choose == 1:
                self.cinematic_frame(screen, 'bamboo1', 2, "Marché conclu. J'achète votre arme.", kind_info=[['SM','no_weapon'], ['JM','no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo1', 2, "Ravi de faire affaire avec vous.", kind_info=[['SM','no_weapon'], ['JM','no_weapon'], 2])
                self.cinematic_frame(screen, 'bamboo1', 2, "Le“Tengoku no Ikari”... J'en prendrai bien soin.", kind_info=[['SM','no_weapon'], ['JM','no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo1', 2, "Faîtes en bon usage. Vous ne le regretterez pas.", kind_info=[['SM','no_weapon'], ['JM','no_weapon'], 2])
                self.cinematic_frame(screen, 'bamboo1', 2, "Je vous en remercie ! Faîtes attention à vous !", kind_info=[['SM','no_weapon'], ['JM','no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo1', 2, "Merci jeune homme ! N'hésite pas à revenir me voir !", kind_info=[['SM','no_weapon'], ['JM','no_weapon'], 2])
                self.cinematic_frame(screen, "bamboo1", 0, "Musashi obtient l'une des 7 épées légendaires: Le“Tengoku no Ikari”et","poursuit son voyage pour venger son village natal. Sera-t-elle conforme", "aux attentes de notre samouraï ? A suivre dans le prochain épisode.")
            elif choose == 2:
                self.cinematic_frame(screen, 'bamboo1', 2, "Je vous remercie de votre offre, mais je vais devoir refuser.",kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo1', 2, "Ah bon ? Dommage. Peut-être une prochaine fois.", kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], 2])
                self.cinematic_frame(screen, 'bamboo1', 2, "En effet, peut-être une prochaine fois.", kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo1', 2, "Si on se retrouve, n'hésitez pas à me faire part de ce que vous recherchez.", kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], 2])
                self.cinematic_frame(screen, 'bamboo1', 2, "Compris ! On se retrouvera lorsque le moment viendra.",kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo1', 2, "Sur ce, à la prochaine jeune homme ! ",kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], 2])
                self.cinematic_frame(screen, 'bamboo1', 2, "A la prochaine marchand Juzo ! Faîtes très attention lors de votre voyage ! ",kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], 1])
                self.cinematic_frame(screen, "bamboo1", 0,"Musashi poursuit son voyage pour venger son village natal. Arrivera-t-il", "à atteindre sa destination ? A suivre dans le prochain épisode.")
            elif choose == 3:
                self.cinematic_frame(screen, 'bamboo1', 2, "J'aimerais bien vous prendre cette arme, en échange d'un service que vous", "pourriez me proposer.",kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo1', 2, "Un service tu dis ? Je vois, tu me dois donc un service si jamais tu", "prends cette lame.", kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], 2])
                self.cinematic_frame(screen, 'bamboo1', 2, "En effet. Je dois venger mon village natal qui a été détruit par le clan", "Takahiro. C'est un cas assez urgent pour moi. Je vous en fais la promesse.",kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo1', 2, "Hmm... D'accord, j'accepte ton offre. Actuellement, je n'ai pas de service", "à te demander pour mon travail mais je t'en ferai part lorsqu'on se", "retrouvera.", kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], 2])
                self.cinematic_frame(screen, 'bamboo1', 2, "Voici le“Tengoku no Ikari”. Fais-en bon usage et fais très attention,", "notamment aux ennemis que tu rencontreras. ", kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], 2])
                self.cinematic_frame(screen, 'bamboo1', 2, "C'est noté. Je resterai prudent lors de mon voyage. Encore une fois, je", "vous remercie de votre bienveillance.",kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo1', 2, "Aucun problème, on peut dire que c'est un cadeau en premier lieu. N'oublie", "pas ta promesse et on se reverra aussitôt! Bon courage pour ta quête Musashi !", kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], 2])
                self.cinematic_frame(screen, 'bamboo1', 2, "Entendu ! Bon courage à vous aussi marchand Juzo !",kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], 1])
                self.cinematic_frame(screen, "bamboo1", 0,"Musashi obtient l'une des 7 épées légendaires: Le“Tengoku no Ikari”et", "poursuit son voyage pour venger son village natal. Sera-t-il conforme", "aux attentes de notre samouraï ? A suivre dans le prochain épisode.")
            elif choose == 4:
                self.cinematic_frame(screen, 'bamboo1', 2, "Pardonnez moi, mais je n'aurais pas le choix de vous le prendre de force. Je","ne vais pas dépenser mon argent sur une arme qui pourrait être une arnaque.",kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo1', 2, "Es-tu si sûr de ça mon garçon? Je te déconseille fortement de me sous-estimer.", kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], 2])
                self.cinematic_frame(screen, 'bamboo1', 2, "Je vous retourne la même réponse. Si vous me passez gentiment cette arme, je ","ne vous tuerai pas.",kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo1', 2, "Essaie encore, jeune homme. Tu vas regretter d'avoir dit de tels propos.", kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], 2])
        elif saved == 'KM':
            if choose == 1:
                self.cinematic_frame(screen, 'bamboo1', 3, "Marché conclu. J'achète votre arme.",kind_info=[['SM', 'no_weapon'],['KM', 'no_weapon'], ['JM', 'no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo1', 3, "Ravi de faire affaire avec vous.",kind_info=[['SM', 'no_weapon'],['KM', 'no_weapon'], ['JM', 'no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo1', 3, "Super grand frère ! Te voilà bien équipé en cours de route !",kind_info=[['KM', 'no_weapon'],['SM', 'no_weapon'], ['JM', 'no_weapon'], 1, True])
                self.cinematic_frame(screen, 'bamboo1', 3, "Le“Tengoku no Ikari”... J'en prendrai bien soin.",kind_info=[['SM', 'no_weapon'],['KM', 'no_weapon'], ['JM', 'no_weapon'], 1, True])
                self.cinematic_frame(screen, 'bamboo1', 3, "Faîtes en bon usage. Vous ne le regretterez pas.",kind_info=[['SM', 'no_weapon'],['KM', 'no_weapon'], ['JM', 'no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo1', 3, "Je vous en remercie ! Faîtes attention à vous !",kind_info=[['SM', 'no_weapon'],['KM', 'no_weapon'], ['JM', 'no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo1', 3, "En effet, merci à vous ! Faîtes attention à vous !",kind_info=[['KM', 'no_weapon'],['SM', 'no_weapon'], ['JM', 'no_weapon'], 1, True])
                self.cinematic_frame(screen, 'bamboo1', 3,"Merci jeune homme et sa sœur ! N'hésitez pas à revenir me voir !",kind_info=[['KM', 'no_weapon'],['SM', 'no_weapon'], ['JM', 'no_weapon'], 3])
                self.cinematic_frame(screen, "bamboo1", 0,"Musashi obtient l'une des 7 épées légendaires : Le“Tengoku no Ikari”et","poursuit son voyage pour venger son village natal. Sera-t-elle conforme","aux attentes de notre samouraï ? A suivre dans le prochain épisode.")
            elif choose == 2:
                self.cinematic_frame(screen, 'bamboo1', 3, "Je vous remercie de votre offre, mais je vais devoir refuser.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo1', 3,"Tu ne comptes pas acheter cette arme ? Cela pourrait-être utile.",kind_info=[['KM', 'no_weapon'],['SM', 'no_weapon'], ['JM', 'no_weapon'], 1, True])
                self.cinematic_frame(screen, 'bamboo1', 3, "Ah bon ? Dommage. Peut-être une prochaine fois.",kind_info=[['KM', 'no_weapon'],['SM', 'no_weapon'], ['JM', 'no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo1', 3, "En effet, peut-être une prochaine fois.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'], 1, True])
                self.cinematic_frame(screen, 'bamboo1', 3,"Si on se retrouve, n'hésitez pas à me faire part de ce que vous recherchez.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo1', 3, "Compris ! On se retrouvera lorsque le moment viendra.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo1', 3, "Sur ce, à la prochaine jeune homme et jeune fille!",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo1', 3,"A la prochaine marchand Juzo! Faîtes très attention lors de votre voyage !",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo1', 3, "A la prochaine !",kind_info=[['KM', 'no_weapon'],['SM', 'no_weapon'], ['JM', 'no_weapon'], 1, True])
                self.cinematic_frame(screen, "bamboo1", 0, "Musashi poursuit son voyage pour venger son village natal. Arrivera-t-il à","atteindre sa destination ? A suivre dans le prochain épisode.")
            elif choose == 3:
                self.cinematic_frame(screen, 'bamboo1', 3,"J'aimerais bien vous prendre cette arme, en échange d'un service que vous","pourriez me proposer.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo1', 3,"Un service tu dis ? Je vois, tu me dois donc un service si jamais tu prends","cette lame.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo1', 3,"En effet. Je dois venger mon village natal qui a été détruit par le clan","Takahiro.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo1', 3,"C'est un cas assez urgent pour moi. Je vous en fais la promesse.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo1', 3,"Hmm... D'accord, j'accepte ton offre. Actuellement, je n'ai pas de service","à te demander pour mon travail mais je t'en ferai part lorsqu'on se","retrouvera.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo1', 3,"Voici le“Tengoku no Ikari”. Fais-en bon usage et fais très attention,","notamment aux ennemis que tu rencontreras.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo1', 3,"Il faudra que tu sois plus vigilent Shikisha si jamais tu comptes battre","le clan Takahiro.",kind_info=[['KM', 'no_weapon'],['SM', 'no_weapon'], ['JM', 'no_weapon'], 1, True])
                self.cinematic_frame(screen, 'bamboo1', 3,"C'est noté. Je resterai prudent lors de mon voyage. Encore une fois, je vous","remercie de votre bienveillance.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'], 1, True])
                self.cinematic_frame(screen, 'bamboo1', 3,"Aucun problème, on peut dire que c'est un cadeau en premier lieu. N'oublie","pas ta promesse et on se reverra aussitôt !",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo1', 3,"Bon courage pour ta quête Musashi ! Ainsi que toi Keiko !",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo1', 3,"Entendu ! Bon courage à vous aussi marchand Juzo !",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'], 1])
                self.cinematic_frame(screen, "bamboo1", 0,"Musashi obtient l'une des 7 épées légendaires: Le“Tengoku no Ikari”et","poursuit son voyage pour venger son village natal. Sera-t-elle conforme","aux attentes de notre samouraï ? A suivre dans le prochain épisode.")
            elif choose == 4:
                self.cinematic_frame(screen, 'bamboo1', 3,"Pardonnez moi, mais je n'ai pas le choix de vous le prendre de force.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo1', 3,"Eh ? ! Mais pourquoi ferais-tu cela grand frère ?",kind_info=[['KM', 'no_weapon'],['SM', 'no_weapon'], ['JM', 'no_weapon'], 1, True])
                self.cinematic_frame(screen, 'bamboo1', 3,"Je ne vais pas dépenser mon argent sur une arme qui pourrait être une arnaque.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'], 1, True])
                self.cinematic_frame(screen, 'bamboo1', 3,"Mais dans ce cas là refuse alors ? Cela ne te correspond pas !",kind_info=[['KM', 'no_weapon'],['SM', 'no_weapon'], ['JM', 'no_weapon'], 1, True])
                self.cinematic_frame(screen, 'bamboo1', 3,"Es-tu si sûr de ça mon garçon? Je te déconseille fortement de me sous-estimer.",kind_info=[['KM', 'no_weapon'],['SM', 'no_weapon'], ['JM', 'no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo1', 3,"Je vous retourne la même réponse. Si vous me passez gentiment cette arme,","je ne vous tuerai pas.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'], 1, True])
                self.cinematic_frame(screen, 'bamboo1', 3,"Que deviens-tu grand frère...",kind_info=[['KM', 'no_weapon'],['SM', 'no_weapon'], ['JM', 'no_weapon'], 1, True])
                self.cinematic_frame(screen, 'bamboo1', 3,"Essaie encore, jeune homme. Tu vas regretter d'avoir dit de tels propos.",kind_info=[['KM', 'no_weapon'],['SM', 'no_weapon'], ['JM', 'no_weapon'], 3])
        elif saved == 'KT':
            if choose == 1:
                self.cinematic_frame(screen, 'bamboo1', 3, "Marché conclu. J'achète votre arme.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo1', 3, "Génial Musashi ! Tu vas devenir extrêmement puissant !",kind_info=[['KT', 'no_weapon'],['SM', 'no_weapon'], ['JM', 'no_weapon'], 1, True])
                self.cinematic_frame(screen, 'bamboo1', 3, "Ravi de faire affaire avec vous.",kind_info=[['KT', 'no_weapon'],['SM', 'no_weapon'], ['JM', 'no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo1', 3, "Le “Tengoku no Ikari”... J'en prendrai bien soin.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'], 1, True])
                self.cinematic_frame(screen, 'bamboo1', 3, "Faîtes en bon usage. Vous ne le regretterez pas.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo1', 3, "Je vous en remercie ! Faîtes attention à vous !",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo1', 3, "Merci de votre offre ! A la prochaine !",kind_info=[['KT', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'], 1, True])
                self.cinematic_frame(screen, 'bamboo1', 3, "Merci à vous ! N'hésite pas à revenir me voir !",kind_info=[['KT', 'no_weapon'],['SM', 'no_weapon'], ['JM', 'no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo1', 0,"Musashi obtient l'une des 7 épées légendaires: Le“Tengoku no Ikari”et","poursuit son voyage pour venger son village natal. Sera-t-elle conforme","aux attentes de notre samouraï? A suivre dans le prochain épisode.")
            elif choose == 2:
                self.cinematic_frame(screen, 'bamboo1', 3, "Je vous remercie de votre offre, mais je vais devoir refuser.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo1', 3,"C'était une occasion gâchée. Cela n'est pas grave, on pourra acheter d'autres","armes dans le village.",kind_info=[['KT', 'no_weapon'],['SM', 'no_weapon'], ['JM', 'no_weapon'], 1, True])
                self.cinematic_frame(screen, 'bamboo1', 3, "Ah bon ? Dommage. Peut-être une prochaine fois.",kind_info=[['KT', 'no_weapon'],['SM', 'no_weapon'], ['JM', 'no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo1', 3, "En effet, peut-être une prochaine fois.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'], 1, True])
                self.cinematic_frame(screen, 'bamboo1', 3,"Si on se retrouve, n'hésitez pas à me faire part de ce que vous recherchez.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo1', 3, "Compris ! On se retrouvera lorsque le moment viendra.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo1', 3, "Sur ce, à la prochaine jeune homme !",kind_info=[['KT', 'no_weapon'],['SM', 'no_weapon'], ['JM', 'no_weapon'], 1, True])
                self.cinematic_frame(screen, 'bamboo1', 3,"A la prochaine marchand Juzo! Faîtes très attention lors de votre voyage !",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'], 1, True])
                self.cinematic_frame(screen, 'bamboo1', 0,"Musashi poursuit son voyage pour venger son village natal. Arrivera-t-il à","atteindre sa destination? A suivre dans le prochain épisode.")
            elif choose == 3:
                self.cinematic_frame(screen, 'bamboo1', 3,"J'aimerais bien vous prendre cette arme, en échange d'un service que vous","pourriez me proposer.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo1', 3,"Un service tu dis ? Je vois, tu me dois donc un service si jamais tu prends","cette lame.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo1', 3,"En effet. Je dois venger mon village natal qui a été détruit par le clan","Takahiro.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo1', 3,"C'est un cas assez urgent pour moi. Je vous en fais la promesse.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo1', 3,"Hmm...D'accord, j'accepte ton offre. Actuellement, je n'ai pas de service","à te demander pour mon travail mais je t'en ferai part lorsqu'on se", "retrouvera.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo1', 3,"Voici le“Tengoku no Ikari”. Fais-en bon usage et fais très attention,","notamment aux ennemis que tu rencontreras.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo1', 3, "Continuons de rester sur nos gardes. On ne sait jamais.",kind_info=[['KT', 'no_weapon'],['SM', 'no_weapon'], ['JM', 'no_weapon'], 1, True])
                self.cinematic_frame(screen, 'bamboo1', 3,"C'est noté. Je resterai prudent lors de mon voyage. Encore une fois, je vous","remercie de votre bienveillance.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'], 1, True])
                self.cinematic_frame(screen, 'bamboo1', 3,"Aucun problème, on peut dire que c'est un cadeau en premier lieu. N'oublie","pas ta promesse et on se reverra aussitôt !",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo1', 3, "Bon courage pour ta quête Musashi !",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo1', 3, "Entendu ! Bon courage à vous aussi marchand Juzo !",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo1', 3, "Oui, au revoir marchand Juzo !",kind_info=[['KT', 'no_weapon'],['SM', 'no_weapon'], ['JM', 'no_weapon'], 1, True])
                self.cinematic_frame(screen, 'bamboo1', 0,"Musashi poursuit son voyage pour venger son village natal. Arrivera-t-il","à atteindre sa destination? A suivre dans le prochain épisode.")
            elif choose ==4:
                self.cinematic_frame(screen, 'bamboo1', 3,"Pardonnez moi, mais je n'ai pas le choix de vous le prendre de force.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo1', 3,"Que fais-tu Musashi !?",kind_info=[['KT', 'no_weapon'],['SM', 'no_weapon'],['JM', 'no_weapon'], 1, True])
                self.cinematic_frame(screen, 'bamboo1', 3,"Je ne vais pas dépenser mon argent sur une arme qui pourrait être une arnaque.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'], 1, True])
                self.cinematic_frame(screen, 'bamboo1', 3,"Es-tu si sûr de ça mon garçon? Je te déconseille fortement de me sous-estimer.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo1', 3,"Je vous retourne la même réponse. Si vous me passez gentiment cette arme,","je ne vous tuerai pas.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo1', 3,"Tu t'opposes au code Bushido, cesse tes singeries !",kind_info=[['KT', 'no_weapon'],['SM', 'no_weapon'], ['JM', 'no_weapon'],1, True])
                self.cinematic_frame(screen, 'bamboo1', 3,"Essaie encore, jeune homme. Tu vas regretter d'avoir dit de tels propos. ",kind_info=[['KT', 'no_weapon'],['SM', 'no_weapon'], ['JM', 'no_weapon'], 3])
        self.ecran_noir(screen)

    def cinematic_12(self,screen,saved):
        #cinématique vérifiée
        if saved=='none':
            self.cinematic_frame(screen, "azw2", 1, "L'heure est-elle venue pour affronter le clan ?",kind_info=["SM", "SM", "no_weapon", "right"])
            output1, output2 = self.choice_frame(screen, "azw2", [0, 2], ["OUI", "NON"])
            if output1=='choice':
                if output2==1:
                    self.cinematic_frame(screen, "azw2", 1, "C'est l'heure. Vengeons Magome.",kind_info=["SM", "SM", "no_weapon", "right"])
                elif output2==2:
                    self.cinematic_frame(screen, "azw2", 1, "Il me reste des choses plus importantes à faire.",kind_info=["SM", "SM", "no_weapon", "right"])
        elif saved=='KM':
            self.cinematic_frame(screen, "azw2", 2, "L'heure est-elle venue pour affronter le clan ?",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], 1])
            output1, output2 = self.choice_frame(screen, "azw2", [0, 2], ["OUI", "NON"])
            if output1=='choice':
                if output2==1:
                    self.cinematic_frame(screen, "azw2", 2, "C'est l'heure. Vengeons Magome.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'],1])
                elif output2 == 2:
                    self.cinematic_frame(screen, "azw2", 2, "Il me reste des choses plus importantes à faire.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], 1])

        elif saved=='KT':
            self.cinematic_frame(screen, "azw2", 2, "L'heure est-elle venue pour affronter le clan ?",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])
            output1, output2 = self.choice_frame(screen, "azw2", [0, 2], ["OUI", "NON"])
            if output1=='choice':
                if output2==1:
                    self.cinematic_frame(screen, "azw2", 2, "C'est l'heure. Vengeons Magome.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])
                elif output2==2:
                    self.cinematic_frame(screen, "azw2", 2, "Il me reste des choses plus importantes à faire.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])

        self.ecran_noir(screen)

    def cinematic_13(self,screen,saved):
        #cinématique vérifiée
        if saved=='none':
            self.cinematic_frame(screen, "mgm8", 1," …Magome…Mon village natal.",kind_info=["SM", "SM", "no_weapon", "right"])
            self.cinematic_frame(screen, "mgm8", 1,"Cela fait un petit moment que je ne l'ai pas visité.",kind_info=["SM", "SM", "no_weapon", "right"])
            self.cinematic_frame(screen, "mgm8", 1,"Qu'est qu'il est devenu depuis mon départ ? Ah, le bon vieux temps.",kind_info=["SM", "SM", "no_weapon", "right"])
            self.cinematic_frame(screen, "mgm8", 1,"J'avais eu plein de souvenirs de mon enfance.. J'aurai bien aimé", "rester enfant.",kind_info=["SM", "SM", "no_weapon", "right"])
            self.cinematic_frame(screen, "mgm8", 1,"Je me souvenais du moment où j'ai joué avec Takeshi dans les ruelles du", "village..",kind_info=["SM", "SM", "no_weapon", "right"])
            self.cinematic_frame(screen, "mgm8", 1,"Ou avec Keiko lorsqu'on a joué à cache-cache..",kind_info=["SM", "SM", "no_weapon", "right"])
            self.cinematic_frame(screen, "mgm8", 1,"Le bon vieux temps, quelle nostalgie..",kind_info=["SM", "SM", "no_weapon", "right"])
            self.cinematic_frame(screen, "mgm8", 1,"C'est comme si je revivais ces moments d'enfance..",kind_info=["SM", "SM", "no_weapon", "right"])
        elif saved=='KM':
            self.cinematic_frame(screen, "mgm8", 2, "…Magome…Mon village natal.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], 1])
            self.cinematic_frame(screen, "mgm8", 2, "Cela fait longtemps qu'on ne l'a pas visité.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], 2])
            self.cinematic_frame(screen, "mgm8", 2, "C'est vrai. Qu'est qu'il est devenu depuis nôtre départ ? Ah, le bon vieux", "temps.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], 1])
            self.cinematic_frame(screen, "mgm8", 2, "Nous avions eu plein de souvenirs de mon enfance.. J'aurai bien aimé", "rester enfant.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], 1])
            self.cinematic_frame(screen, "mgm8", 2, "Tout à fait. Malheureusement on est obligé de grandir.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], 2])
            self.cinematic_frame(screen, "mgm8", 2, "Je me souvenais du moment où j'ai joué avec Takeshi dans les ruelles du", "village..",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], 1])
            self.cinematic_frame(screen, "mgm8", 2, "Ou avec toi lorsqu'on a joué à cache-cache..",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], 1])
            self.cinematic_frame(screen, "mgm8", 2, "Le bon vieux temps, quelle nostalgie..",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], 1])
            self.cinematic_frame(screen, "mgm8", 2, "J'aurai bien aimé revoir nos parents. Malheureusement ils ont péri lors de", "l'incident..",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], 2])
            self.cinematic_frame(screen, "mgm8", 2, "Oui, c'est fort dommage. J'aimerai bien revivre mon enfance..",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], 1])
        elif saved == 'KT':
            self.cinematic_frame(screen, "mgm8", 2, "…Magome…Nôtre village natal.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])
            self.cinematic_frame(screen, "mgm8", 2, "On est parti il y a 1 mois. En 1 mois, nous sommes devenus des samouraïs.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 2])
            self.cinematic_frame(screen, "mgm8", 2, "Oui, cela fait un petit moment qu'on ne l'a pas visité.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])
            self.cinematic_frame(screen, "mgm8", 2, "Qu'est qu'il est devenu depuis nôtre départ ? Ah, le bon vieux temps.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])
            self.cinematic_frame(screen, "mgm8", 2, "J'avais eu plein de souvenirs de mon enfance.. J'aurai bien aimé", "rester enfant.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])
            self.cinematic_frame(screen, "mgm8", 2, "Pareil Shikisha. J'aurai bien aimé rester enfant aussi. Franchement, on a", "très vite grandi.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 2])
            self.cinematic_frame(screen, "mgm8", 2, "Je me souvenais du moment où j'ai joué avec toi dans les ruelles du village..",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])
            self.cinematic_frame(screen, "mgm8", 2, "Ou avec Keiko lorsqu'on a joué à cache-cache..",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])
            self.cinematic_frame(screen, "mgm8", 2, "Ce sont des moments inoubliables. Le temps passe vite, il faut bien en", "profiter, tout comme notre voyage.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 2])
            self.cinematic_frame(screen, "mgm8", 2, "Le bon vieux temps, quelle nostalgie..",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])
            self.cinematic_frame(screen, "mgm8", 2, "C'est comme si je revivais ces moments d'enfance..",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])
        self.ecran_noir(screen)

    def cinematic_14(self,screen,saved):
        #cinématique vérifiée
        if saved =='none':
            self.cinematic_frame(screen, "mgm8", 1," ! ! !",kind_info=["SM", "SM", "no_weapon", "right"])
            self.cinematic_frame(screen, "mgm8", 1,"Attends une minute..ce lieu…",kind_info=["SM", "SM", "no_weapon", "right"])
            self.cinematic_frame(screen, "mgm8", 1,"Je m'en souviens..C'est là où se situe la planque de l'ennemi !",kind_info=["SM", "SM", "no_weapon", "right"])
            self.cinematic_frame(screen, "mgm8", 1,"Mais oui! La planque se situait près du village de Magome depuis tout ce","temps !",kind_info=["SM", "SM", "no_weapon", "right"])
            self.cinematic_frame(screen, "mgm8", 1,"(Tout s'explique ! Je sais désormais où aller !)",kind_info=["SM", "SM", "no_weapon", "right"])
            self.cinematic_frame(screen, "mgm8", 1,"On n'a pas de temps à perdre ! Je vais battre le chef du clan lui-même, on y", "va ! ",kind_info=["SM", "SM", "no_weapon", "right"])
        elif saved=='KM':
            self.cinematic_frame(screen, "mgm8", 2, "..grand frère ?",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], 2])
            self.cinematic_frame(screen, "mgm8", 2," ! ! !",kind_info=[["SM", "no_weapon"], ['KM', 'no_weapon'], 2])
            self.cinematic_frame(screen, "mgm8", 2, "Attends une minute..ce lieu…",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], 1])
            self.cinematic_frame(screen, "mgm8", 2, "Je m'en souviens..C'est là où se situe la planque de l'ennemi !",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], 1])
            self.cinematic_frame(screen, "mgm8", 2, "Mais oui ! La planque se situait près de Magome depuis tout ce temps !",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], 1])
            self.cinematic_frame(screen, "mgm8", 2, "(Tout s'explique ! Je sais désormais où aller !)",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], 1])
            self.cinematic_frame(screen, "mgm8", 2, "On n'a pas de temps à perdre ! Je vais battre le chef du clan lui-même, on y ","va ! ",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], 1])
            self.cinematic_frame(screen, "mgm8", 2, "Attends tu sais où se trouve la base du clan Takahiro…?",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], 2])
            self.cinematic_frame(screen, "mgm8", 2, "Oui ! On doit faire vite !",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], 1])
        elif saved=='KT':
            self.cinematic_frame(screen, "mgm8", 2," ! ! !",kind_info=[["SM", "no_weapon"], ['KT', 'no_weapon'], 2])
            self.cinematic_frame(screen, "mgm8", 2, "Musashi ? Quelque chose te tracasse ? ",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 2])
            self.cinematic_frame(screen, "mgm8", 2, "Attends une minute..ce lieu…",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])
            self.cinematic_frame(screen, "mgm8", 2, "Je m'en souviens..C'est là où se situe la planque de l'ennemi !",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])
            self.cinematic_frame(screen, "mgm8", 2, "??? Tu sais où se situe la base de l'ennemi ?",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 2])
            self.cinematic_frame(screen, "mgm8", 2, "Mais oui ! La planque se situait près de Magome depuis tout ce temps !",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])
            self.cinematic_frame(screen, "mgm8", 2, "(Tout s'explique ! Je sais désormais où aller !)",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])
            self.cinematic_frame(screen, "mgm8", 2, "On n'a pas de temps à perdre ! Je vais battre le chef du clan lui-même, on y","va ! ",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])
            self.cinematic_frame(screen, "mgm8", 2, "Si tu le dis, alors je te fais confiance. Allons-y !",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 2])
        self.ecran_noir(screen)


    def cinematic_15(self,screen,saved,juzo,in_genocide_route):
        #cinématique vérifiée
        if saved =='none':
            if juzo==True:
                self.cinematic_frame(screen, 'bamboo5', 2, " ! Ce chariot..ce sac..ces vêtements, ce ne serait pas.. ?", kind_info=[['SM','no_weapon'], ['JM','no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo5', 2, "Musashi ! C'est urgent ! !", kind_info=[['SM','no_weapon'], ['JM','no_weapon'], 2])
                self.cinematic_frame(screen, 'bamboo5', 2, "Quoi donc ?", kind_info=[['SM','no_weapon'], ['JM','no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo5', 2, "Je suis désolé de te dire cela, mais il va falloir que tu me rendes service", "ici et maintenant. ", kind_info=[['SM','no_weapon'], ['JM','no_weapon'], 2])
                self.cinematic_frame(screen, 'bamboo5', 2, "Ici et maintenant ? Pourquoi ? Est-ce très urgent ?", kind_info=[['SM','no_weapon'], ['JM','no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo5', 2, "Oui... Malheureusement je ne t'avais pas prévenu auparavant lors de notre", "rencontre dans la forêt..", kind_info=[['SM','no_weapon'], ['JM','no_weapon'], 2])
                self.cinematic_frame(screen, 'bamboo5', 2, "Le“Tengoku no Ikari”... est une arme maudite.", kind_info=[['SM','no_weapon'], ['JM','no_weapon'], 2])
                self.cinematic_frame(screen, 'bamboo5', 2, "Une arme maudite ? Alors que c'est l'une des 7 épées légendaires ?", kind_info=[['SM','no_weapon'], ['JM','no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo5', 2, "Oui..Sache que les 7 épées légendaires sont toutes maudites. ", kind_info=[['SM','no_weapon'], ['JM','no_weapon'], 2])
                self.cinematic_frame(screen, 'bamboo5', 2, "Le seul moyen de lever la malédiction, c'est de battre une autre personne qui", "possède une autre arme légendaire.", kind_info=[['SM','no_weapon'], ['JM','no_weapon'], 2])
                self.cinematic_frame(screen, 'bamboo5', 2, "Hmmmm. Si j'ai compris, je vais devoir affronter un autre guerrier avec cette", "même arme..", kind_info=[['SM','no_weapon'], ['JM','no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo5', 2, "Dans ce cas là, où devrais-je donc l'affronter ?", kind_info=[['SM','no_weapon'], ['JM','no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo5', 2, "Eh bien. Justement, il ne devrait pas tarder à arriver..", kind_info=[['SM','no_weapon'], ['JM','no_weapon'], 2])
                self.cinematic_frame(screen, 'bamboo5', 0, "Un guerrier sort de son cheval, rempli de détermination et de sérieux.")
                self.cinematic_frame(screen, "bamboo5", 3, "...",kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], ['SA', 'no_weapon'], 3, None,['SA']])
                self.cinematic_frame(screen, "bamboo5", 3, "Par ailleurs, sache que ceux qui possèdent l'une de ces épées sont destinées", "à forcément se rencontrer un jour.",kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], ['SA', 'no_weapon'],2])
                self.cinematic_frame(screen, "bamboo5", 3, "Lors du moment venu, un combat à mort se produit. Il ne peut y avoir qu'un", "seul vainqueur.",kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], ['SA', 'no_weapon'],2])
                self.cinematic_frame(screen, "bamboo5", 3, "Celui qui remporte la victoire aura la possibilité d'utiliser l'autre arme,", "mais restera à nouveau maudit.",kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], ['SA', 'no_weapon'], 2])
                self.cinematic_frame(screen, "bamboo5", 3, "Je suis très navré de ne t'avoir pas prévenu auparavant.",kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], ['SA', 'no_weapon'], 2])
                self.cinematic_frame(screen, "bamboo5", 3, "...Non tu ne devrais pas t'excuser.",kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], ['SA', 'no_weapon'], 1])
                self.cinematic_frame(screen, "bamboo5", 3, "Si toi aussi, tu as été maudit par cette arme..",kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], ['SA', 'no_weapon'], 1])
                self.cinematic_frame(screen, "bamboo5", 3, "Alors je suis prêt à lever non seulement ma malédiction, mais aussi la tienne.",kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], ['SA', 'no_weapon'], 1])
                self.cinematic_frame(screen, "bamboo5", 3, "Musashi...",kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], ['SA', 'no_weapon'], 2])
                self.cinematic_frame(screen, "bamboo5", 3, "Que l'arme soit maudite ou non, le principe reste le même. Ce n'est pas nous", "qui choisissons notre épée, c'est l'épée qui nous choisit.",kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], ['SA', 'no_weapon'], 1])
                self.cinematic_frame(screen, "bamboo5", 3, "Ainsi, je suis prêt à parier sur ma vie pour être l'élu de ce katana.",kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], ['SA', 'no_weapon'], 1])
                self.cinematic_frame(screen, "bamboo5", 3, "Assez parler. Passons aux introductions.",kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], ['SA', 'no_weapon'], 1])
                self.cinematic_frame(screen, "bamboo5", 3, "Je suis Shikisha Musashi. Je suis récemment devenu samouraï et je viens du", "village de Magome.",kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], ['SA', 'no_weapon'], 1])
                self.cinematic_frame(screen, "bamboo5", 3, "...Je suis Senshi Akuma, samouraï d'Aizuwakamatsu. J'appartiens au clan", "Yoshioka, un clan qui deviendra l'un des clans les plus puissants", "de l'histoire du Japon.",kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], ['SA', 'no_weapon'], 3])
                self.cinematic_frame(screen, "bamboo5", 3, "Si j'ai bien compris, ton épée légendaire serait le“Tengoku no Ikari”.", "Pour mon cas, c'est le “Jigoku no Shizuka”. Il se trouve que ces", "deux armes font une paire très puissante.",kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], ['SA', 'no_weapon'], 3])
                self.cinematic_frame(screen, "bamboo5", 3, "Celui qui remporte ce duel sera celui qui régnera en tant que le plus", "puissant samouraï de l'histoire.",kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], ['SA', 'no_weapon'], 3])
                self.cinematic_frame(screen, "bamboo5", 3, "Qui restera en vie ? Le paradis ? ou l'Enfer ?",kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], ['SA', 'no_weapon'], 3])
                self.cinematic_frame(screen, "bamboo5", 3, "En tout cas, je ne compte pas baisser les bras. Prépare toi jeune samouraï, je", "vais gagner ce duel..",kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], ['SA', 'no_weapon'], 3])
                self.cinematic_frame(screen, "bamboo5", 3, "Et être reconnu en tant que le meilleur samouraï de l'histoire dans le clan", "Yoshioka !",kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], ['SA', 'no_weapon'], 3])
                self.cinematic_frame(screen, "bamboo5", 3, "Sache que tu n'es pas le seul à avoir gagné en puissance grâce à ton clan. ",kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], ['SA', 'no_weapon'], 1])
                self.cinematic_frame(screen, "bamboo5", 3, "Nos destins vont s'entrechoquer..Ici et maintenant !",kind_info=[['SM', 'no_weapon'], ['JM', 'no_weapon'], ['SA', 'no_weapon'], 1])
                self.ecran_noir(screen)
            if in_genocide_route==True:
                self.ecran_noir(screen)
                self.cinematic_frame(screen, 'bamboo2', 2, "..Musashi.", kind_info=[['SM','no_weapon'], ['SH','no_weapon'], 2])
                self.cinematic_frame(screen, 'bamboo2', 2, "Sensei Hoshida ? Que faîtes vous ici ?", kind_info=[['SM','no_weapon'], ['SH','no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo2', 2, "Tu sais très bien pourquoi je suis ici.", kind_info=[['SM','no_weapon'], ['SH','no_weapon'], 2])
                self.cinematic_frame(screen, 'bamboo2', 2, " ? ? ? Je n'ai pas la moindre idée de votre présence.", kind_info=[['SM','no_weapon'], ['SH','no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo2', 2, "Dans ce cas là..J'aimerai bien que tu m'expliques..", kind_info=[['SM','no_weapon'], ['SH','no_weapon'], 2])
                self.cinematic_frame(screen, 'bamboo2', 2, "La présence de sang qui couvre tes vêtements..", kind_info=[['SM','no_weapon'], ['SH','no_weapon'], 2])
                self.cinematic_frame(screen, 'bamboo2', 2, "Du sang ? Pff, franchement c'est juste le sang de certains membres du clan", "Takahiro.", kind_info=[['SM','no_weapon'], ['SH','no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo2', 2, "Ne vous inquiétez pas, c'est pour le bien de chacun.", kind_info=[['SM','no_weapon'], ['SH','no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo2', 2, "S'ils ont tué, je ne devrais pas pour autant me restreindre à me défendre pour", "les tuer aussi.", kind_info=[['SM','no_weapon'], ['SH','no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo2', 2, "C'est justement le problème Musashi. Tu ne fais que de tuer.", kind_info=[['SM','no_weapon'], ['SH','no_weapon'], 2])
                self.cinematic_frame(screen, 'bamboo2', 2, "Si tu poursuis ce chemin, tu vas fortement le regretter. ", kind_info=[['SM','no_weapon'], ['SH','no_weapon'], 2])
                self.cinematic_frame(screen, 'bamboo2', 2, "Tu vas t'apercevoir au final que tu seras devenu ce que tu détestais", "auparavant.", kind_info=[['SM','no_weapon'], ['SH','no_weapon'], 2])
                self.cinematic_frame(screen, 'bamboo2', 2, "La raison pour laquelle je bloque ton passage, c'est de te faire comprendre", "cela.", kind_info=[['SM','no_weapon'], ['SH','no_weapon'], 2])
                self.cinematic_frame(screen, 'bamboo2', 2, "Et pourtant, tu aurais dit la même chose à ces tueurs non ?", kind_info=[['SM','no_weapon'], ['SH','no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo2', 2, "Si la violence est le seul moyen de faire changer le monde à ta guise, alors", "j'en ferai bon usage.", kind_info=[['SM','no_weapon'], ['SH','no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo2', 2, "Pas forcément Musashi, pas forcément. ", kind_info=[['SM','no_weapon'], ['SH','no_weapon'], 2])
                self.cinematic_frame(screen, 'bamboo2', 2, "Prendre une décision pacifiste est l'une des meilleures décisions qu'on puisse", "prendre moralement.", kind_info=[['SM','no_weapon'], ['SH','no_weapon'], 2])
                self.cinematic_frame(screen, 'bamboo2', 2, "Le but d'être pacifiste, c'est de faire comprendre aux autres de ne pas avoir", "toujours recours à la violence.", kind_info=[['SM','no_weapon'], ['SH','no_weapon'], 2])
                self.cinematic_frame(screen, 'bamboo2', 2, "Donc Musashi...Mon cher élève..Quel chemin vas-tu prendre ?", kind_info=[['SM','no_weapon'], ['SH','no_weapon'], 2])
                self.cinematic_frame(screen, 'bamboo2', 2, "Le chemin des regrets ? Ou le chemin du succès ?", kind_info=[['SM','no_weapon'], ['SH','no_weapon'], 2])
                output1, output2 = self.choice_frame(screen, "bamboo2", [0, 2], ["ECOUTER SENSEI", "NE PAS L'ECOUTER"])
                if output1=='choice':
                    if output2==1:
                        self.cinematic_frame(screen, "bamboo2", 2, "..Oui vous avez certainement raison Sensei Hoshida.",kind_info=[['SM', 'no_weapon'], ['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 2, "J'ai été beaucoup aveuglé par la violence. Je ne faisais que d'en vouloir au", "clan Takahiro.",kind_info=[['SM', 'no_weapon'], ['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 2, "J'avais un très grand désir de vengeance..Mais je souhaite me repentir.",kind_info=[['SM', 'no_weapon'], ['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 2, "Même si on a accumulé des regrets jusqu'ici, alors je suis prêt à accumuler", "des succès à partir d'aujourd'hui.",kind_info=[['SM', 'no_weapon'], ['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 2, "Je suis fier de toi, mon cher élève. Poursuis le chemin de rédemption, et", "deviens un véritable samouraï.",kind_info=[['SM', 'no_weapon'], ['SH', 'no_weapon'], 2])
                        self.cinematic_frame(screen, "bamboo2", 2, "Cesse les massacres, laisse ton esprit se ressaisir et tu t'offriras une", "meilleure voie.",kind_info=[['SM', 'no_weapon'], ['SH', 'no_weapon'], 2])
                        self.cinematic_frame(screen, "bamboo2", 2, "Oui Sensei Hoshida. Veuillez me pardonner de tout ce qu'ai pu faire d'atroce.",kind_info=[['SM', 'no_weapon'], ['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 2, "Tant que tu gardes ta parole, alors je suis prêt à te pardonner Musashi.",kind_info=[['SM', 'no_weapon'], ['SH', 'no_weapon'], 2])
                        self.cinematic_frame(screen, "bamboo2", 2, "La fin du voyage approche, alors je t'en prie, viens à bout du clan Takahiro,", "pour tout le Japon.",kind_info=[['SM', 'no_weapon'], ['SH', 'no_weapon'], 2])
                        self.cinematic_frame(screen, "bamboo2", 2, "Oui Sensei Hoshida, je ne compte pas vous décevoir ! ",kind_info=[['SM', 'no_weapon'], ['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 0, "Musashi s'approche de plus en plus à son plus grand affrontement.")
                        self.cinematic_frame(screen, "bamboo2", 0, "Le chef du clan Takahiro, l'attend dans son domaine avec impatience, pour","pouvoir en finir.")
                        self.cinematic_frame(screen, "bamboo2", 0, "Qui en sortira vainqueur ? A suivre dans le prochain épisode..")
                        self.ecran_noir(screen)
                    elif output2==2:
                        self.cinematic_frame(screen, "bamboo2", 2, "...",kind_info=[['SM', 'no_weapon'], ['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 2, "Alors Musashi ? Ta décision ?",kind_info=[['SM', 'no_weapon'], ['SH', 'no_weapon'], 2])
                        self.cinematic_frame(screen, "bamboo2", 2, "Eh bien Sensei Hoshida, je pense que vous connaissez déjà la réponse.",kind_info=[['SM', 'no_weapon'], ['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 2, "Ah ! Tu me rassures alors Musashi. Je suis fier de ton choi-",kind_info=[['SM', 'no_weapon'], ['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 0, "(SCHIOU) (Sensei Hoshida se fait transpercer le coeur par Musashi)")
                        self.cinematic_frame(screen, "bamboo2", 2, " ! ! ! Guah..",kind_info=[['SM', 'no_weapon'], ['SH', 'no_weapon'], 2])
                        self.cinematic_frame(screen, "bamboo2", 2, "Mais...Pourquoi...Fais...Tu...Cela…",kind_info=[['SM', 'no_weapon'], ['SH', 'no_weapon'], 2])
                        self.cinematic_frame(screen, "bamboo2", 2, "Heh, vieux schnock. Tu n'as pas du tout compris on dirait.",kind_info=[['SM', 'no_weapon'], ['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 2, "Comme je l'ai déjà dit, la violence est l'outil le plus pratique pour pouvoir", "faire changer le monde à sa guise.",kind_info=[['SM', 'no_weapon'], ['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 2, "Sans la violence, on cesse d'évoluer. C'est grâce aux combats, aux duels,", "guerres qu'on n'arrive à avoir dans de nouvelles avancées technologiques.",kind_info=[['SM', 'no_weapon'], ['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 2, "Vous vous trompez fortement sur la distinction de ces deux chemins.",kind_info=[['SM', 'no_weapon'], ['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 2, "..Tu me déçois fortement mon cher élève..",kind_info=[['SM', 'no_weapon'], ['SH', 'no_weapon'], 2])
                        self.cinematic_frame(screen, "bamboo2", 2, "Je vous retourne le compliment. Je vais tous les massacrer, vous verrez..",kind_info=[['SM', 'no_weapon'], ['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 2, "..Tu.. es.. renvoyé..",kind_info=[['SM', 'no_weapon'], ['SH', 'no_weapon'], 2])
                        self.cinematic_frame(screen, "bamboo2", 0, "(Sensei Hoshida tombe par terre)")
                        self.cinematic_frame(screen, "bamboo2", 1, "Hmph. Il n'en avait pas pour longtemps ce vieillard.",kind_info=['SM','SM', 'no_weapon','right'])
                        self.cinematic_frame(screen, "bamboo2", 0, "Musashi s'approche de plus en plus de son plus grand affrontement.")
                        self.cinematic_frame(screen, "bamboo2", 0, "Le chef du clan Takahiro, l'attend dans son domaine avec impatience, pour", "pouvoir en finir.")
                        self.cinematic_frame(screen, "bamboo2", 0, "Qui en sortira vainqueur ? A suivre dans le prochain épisode..")
                        self.ecran_noir(screen)
        elif saved =='KM':
            if juzo==True:
                self.cinematic_frame(screen, "bamboo5", 3, " ! Ce chariot..ce sac..ces vêtements, ce ne serait pas.. ?",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'],1])
                self.cinematic_frame(screen, "bamboo5", 3, "C'est marchand Juzo !",kind_info=[['KM', 'no_weapon'],['SM', 'no_weapon'], ['JM', 'no_weapon'],1, True])
                self.cinematic_frame(screen, "bamboo5", 3, "Musashi ! C'est urgent ! !",kind_info=[['KM', 'no_weapon'],['SM', 'no_weapon'], ['JM', 'no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 3, "Quoi donc ?",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'],1, True])
                self.cinematic_frame(screen, "bamboo5", 3, "Je suis désolé de te dire cela, mais il va falloir que tu me rendes service", "ici et maintenant. ",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 3, "Ici et maintenant ? Pourquoi ???",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'],1])
                self.cinematic_frame(screen, "bamboo5", 3, "Oui..Malheureusement je ne t'avais pas prévenu auparavant lors de notre", "rencontre dans la forêt..",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 3, "Le “Tengoku no Ikari”..est une arme maudite.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 3, "Quoi ?! Vous avez donné une arme maudite à mon frère ?!!",kind_info=[['KM', 'no_weapon'],['SM', 'no_weapon'],['JM', 'no_weapon'],1, True])
                self.cinematic_frame(screen, "bamboo5", 3, "Alors que c'est l'une des 7 épées légendaires ?",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'],1, True])
                self.cinematic_frame(screen, "bamboo5", 3, "Oui..Sache que les 7 épées légendaires sont toutes maudites.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 3, "Le seul moyen de lever la malédiction, c'est de battre une autre personne qui", "possède une autre arme légendaire.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 3, "Hm. Si j'ai compris, je vais devoir affronter un autre guerrier avec cette", "même arme..",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'],1])
                self.cinematic_frame(screen, "bamboo5", 3, "Dans ce cas là, où devrais-je donc l'affronter ?",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'],1])
                self.cinematic_frame(screen, "bamboo5", 3, "Eh bien. Justement, il ne devrait pas tarder à arriver..",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 0, "Un guerrier sort de son cheval, rempli de détermination et de sérieux.")
                self.cinematic_frame(screen, "bamboo5", 3, "...",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'],['SA','no_weapon'],3,None,['SA']])
                self.cinematic_frame(screen, "bamboo5", 3, "Par ailleurs, sache que ceux qui possèdent l'une de ces épées sont destinées","à forcément se rencontrer un jour.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 3, "Lors du moment venu, un combat à mort se produit. Il ne peut y avoir qu'un", "seul vainqueur.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 3, "Celui qui remporte la victoire aura la possibilité d'utiliser l'autre arme,", "mais restera à nouveau maudit.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 3, "Je suis très navré de ne t'avoir pas prévenu auparavant.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 3, "...Non tu ne devrais pas t'excuser.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'],1])
                self.cinematic_frame(screen, "bamboo5", 3, "Si toi aussi, tu as été maudit par cette arme..",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'],1])
                self.cinematic_frame(screen, "bamboo5", 3, "Alors... Je suis prêt à lever non seulement ma malédiction, mais aussi la", "tienne.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'],1])
                self.cinematic_frame(screen, "bamboo5", 3, "Musashi...",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 3, "Que l'arme soit maudite ou non, le principe reste le même. Ce n'est pas nous", "qui choisissons notre épée, c'est l'épée qui nous choisit.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'],1])
                self.cinematic_frame(screen, "bamboo5", 3, "Ainsi, je suis prêt à parier sur ma vie pour être l'élu de ce katana.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'],1])
                self.cinematic_frame(screen, "bamboo5", 3, "Musashi, es-tu sûr de toi ??",kind_info=[['KM', 'no_weapon'],['SM', 'no_weapon'], ['JM', 'no_weapon'],1, True])
                self.cinematic_frame(screen, "bamboo5", 3, "Merci de t'inquiéter Keiko.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'],1, True])
                self.cinematic_frame(screen, "bamboo5", 3, "Mais, je sais ce que je fais. Ne t'en fais pas.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['JM', 'no_weapon'],1])
                self.cinematic_frame(screen, "bamboo5", 3, "Assez parler. Passons aux introductions.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'],['SA','no_weapon'],1])
                self.cinematic_frame(screen, "bamboo5", 3, "Je suis Shikisha Musashi. Je suis récemment devenu samouraï et je viens du", "village de Magome",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'],['SA','no_weapon'],1])
                self.cinematic_frame(screen, "bamboo5", 3, "...Je suis Senshi Akuma, un samouraï d'Aizuwakamatsu. J'appartiens au clan", "Yoshioka, un clan qui deviendra l'un des clans les plus puissants de toute", "l'histoire du Japon.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'],['SA','no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 3, "Si j'ai bien compris, ton épée légendaire serait le “Tengoku no Ikari”. Pour", "mon cas, c'est le “Jigoku no Shizuka”. Il se trouve que ces deux armes font", "une paire très puissante.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['SA','no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 3, "Celui qui remporte ce duel sera celui qui régnera en tant que le plus", "puissant samouraï de l'histoire.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'],['SA','no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 3, "Qui restera en vie ? Le paradis ? ou l'Enfer ?",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['SA','no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 3, "En tout cas, je ne compte pas baisser les bras. Prépare toi jeune samouraï,", "je vais gagner ce duel..",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'],['SA','no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 3, "Et être reconnu en tant que le meilleur samouraï de l'histoire dans le clan", "Yoshioka !",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['SA','no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 3, "Sache que tu n'es pas le seul à avoir gagné en puissance grâce à ton clan. ",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], ['SA','no_weapon'],1])
                self.cinematic_frame(screen, "bamboo5", 3, "Nos destins vont s'entrechoquer..Ici et maintenant !",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'],['SA','no_weapon'],1])
                self.ecran_noir(screen)
            if in_genocide_route==True:
                self.cinematic_frame(screen, 'bamboo2', 3, "..Musashi.", kind_info=[['SM','no_weapon'], ['KM','no_weapon'], ['SH','no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo2', 3, "Sensei Hoshida ? Que faîtes vous ici ?", kind_info=[['SM','no_weapon'], ['KM','no_weapon'],['SH','no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo2', 3, "Tu sais très bien pourquoi je suis ici.", kind_info=[['SM','no_weapon'],['KM','no_weapon'], ['SH','no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo2', 3, " ? ? ? Je n'ai pas la moindre idée de votre présence.", kind_info=[['SM','no_weapon'],['KM','no_weapon'], ['SH','no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo2', 3, "Dans ce cas là..J'aimerai bien que tu m'expliques..", kind_info=[['SM','no_weapon'],['KM','no_weapon'], ['SH','no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo2', 3, "La présence de sang qui couvre tes vêtements..", kind_info=[['SM','no_weapon'],['KM','no_weapon'], ['SH','no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo2', 3, "Du sang ? Pff, franchement c'est juste le sang de certains membres du", "clan Takahiro.", kind_info=[['SM','no_weapon'],['KM','no_weapon'], ['SH','no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo2', 3, "Ne vous inquiétez pas, c'est pour le bien de chacun.", kind_info=[['SM','no_weapon'],['KM','no_weapon'], ['SH','no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo2', 3, "S'ils ont tué, je ne devrais pas pour autant me restreindre à me défendre pour", "les tuer aussi.", kind_info=[['SM','no_weapon'],['KM','no_weapon'], ['SH','no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo2', 3, "Musashi... ne dis quand même pas cela..", kind_info=[['KM', 'no_weapon'],['SM','no_weapon'], ['SH','no_weapon'], 1, True])
                self.cinematic_frame(screen, 'bamboo2', 3, "C'est justement le problème Musashi. Tu ne fais que de tuer.", kind_info=[['KM', 'no_weapon'],['SM','no_weapon'],['SH','no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo2', 3, "Si tu poursuis ce chemin, tu vas fortement le regretter. ", kind_info=[['KM', 'no_weapon'],['SM','no_weapon'],['SH','no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo2', 3, "Tu vas t'apercevoir au final que tu seras devenu ce que tu détestais", "auparavant.", kind_info=[['KM', 'no_weapon'],['SM','no_weapon'],['SH','no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo2', 3, "La raison pour laquelle je bloque ton passage, c'est de te faire comprendre", "cela.", kind_info=[['KM', 'no_weapon'],['SM','no_weapon'],['SH','no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo2', 3, "Et pourtant, tu aurais dit la même chose à ces tueurs non ?", kind_info=[['SM','no_weapon'],['KM','no_weapon'], ['SH','no_weapon'], 1, True])
                self.cinematic_frame(screen, 'bamboo2', 3, "Si la violence est le seul moyen de faire changer le monde à ta guise, alors", "j'en ferai bon usage.", kind_info=[['SM','no_weapon'],['KM','no_weapon'], ['SH','no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo2', 3, "Pas forcément Musashi, pas forcément. ", kind_info=[['SM','no_weapon'],['KM','no_weapon'], ['SH','no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo2', 3, "Prendre une décision pacifiste est l'une des meilleures décisions qu'on puisse", "prendre moralement.", kind_info=[['SM','no_weapon'],['KM','no_weapon'], ['SH','no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo2', 3, "Le but d'être pacifiste, c'est de faire comprendre aux autres de ne pas avoir", "toujours recours à la violence.", kind_info=[['SM','no_weapon'], ['KM','no_weapon'],['SH','no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo2', 3, "Donc Musashi...Mon cher élève..Quel chemin vas-tu prendre ?", kind_info=[['SM','no_weapon'], ['KM','no_weapon'],['SH','no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo2', 3, "Le chemin des regrets ? Ou le chemin du succès ?", kind_info=[['SM','no_weapon'],['KM','no_weapon'], ['SH','no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo2', 3, "Musashi, je t'en supplie. Ecoute ton sensei !", kind_info=[['KM', 'no_weapon'],['SM','no_weapon'],['SH','no_weapon'], 1, True])
                output1, output2 = self.choice_frame(screen, "bamboo2", [0, 2], ["ECOUTER SENSEI", "NE PAS L'ECOUTER"])
                if output1=='choice':
                    if output2==1:
                        self.cinematic_frame(screen, "bamboo2", 3, "..Oui vous avez certainement raison Sensei Hoshida.",kind_info=[['SM', 'no_weapon'],['KM','no_weapon'], ['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 3, "J'ai été beaucoup aveuglé par la violence. Je ne faisais que d'en vouloir au", "clan Takahiro.",kind_info=[['SM', 'no_weapon'],['KM','no_weapon'], ['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 3, "J'avais un très grand désir de vengeance..Mais je souhaite me repentir.",kind_info=[['SM', 'no_weapon'],['KM','no_weapon'], ['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 3, "Même si on a accumulé des regrets jusqu'ici, alors je suis prêt à accumuler", "des succès à partir d'aujourd'hui.",kind_info=[['SM', 'no_weapon'],['KM','no_weapon'], ['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 3, "Je suis fier de toi, mon cher élève.  Poursuis le chemin de rédemption, et", "deviens un véritable samouraï.",kind_info=[['SM', 'no_weapon'],['KM','no_weapon'], ['SH', 'no_weapon'], 3])
                        self.cinematic_frame(screen, "bamboo2", 3, "Cesse les massacres, laisse ton esprit se ressaisir et tu t'offriras une", "meilleure voie.",kind_info=[['SM', 'no_weapon'],['KM','no_weapon'], ['SH', 'no_weapon'], 3])
                        self.cinematic_frame(screen, "bamboo2", 3, "Oui Sensei Hoshida. Veuillez me pardonner de tout ce qu'ai pu faire d'atroce.",kind_info=[['SM', 'no_weapon'], ['KM','no_weapon'],['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 3, "Tant que tu gardes ta parole, alors je suis prêt à te pardonner Musashi.",kind_info=[['SM', 'no_weapon'],['KM','no_weapon'], ['SH', 'no_weapon'], 3])
                        self.cinematic_frame(screen, 'bamboo2', 3, "Tu es enfin redevenu toi-même Musashi !!",kind_info=[['KM', 'no_weapon'],['SM', 'no_weapon'], ['SH', 'no_weapon'],1, True])
                        self.cinematic_frame(screen, "bamboo2", 3, "La fin du voyage approche, alors je t'en prie, viens à bout du clan Takahiro,", "pour tout le Japon.",kind_info=[['KM', 'no_weapon'],['SM', 'no_weapon'],['SH', 'no_weapon'], 3])
                        self.cinematic_frame(screen, "bamboo2", 3, "Oui Sensei Hoshida, je ne compte pas vous décevoir ! ",kind_info=[['SM', 'no_weapon'],['KM','no_weapon'], ['SH', 'no_weapon'], 1, True])
                        self.cinematic_frame(screen, "bamboo2", 0, "Musashi s'approche de plus en plus à son plus grand affrontement.")
                        self.cinematic_frame(screen, "bamboo2", 0, "Le chef du clan Takahiro, l'attend dans son domaine avec impatience, pour","pouvoir en finir.")
                        self.cinematic_frame(screen, "bamboo2", 0, "Qui en sortira vainqueur ? A suivre dans le prochain épisode..")
                        self.ecran_noir(screen)
                    elif output2==2:
                        self.cinematic_frame(screen, "bamboo2", 3, "...",kind_info=[['SM', 'no_weapon'],['KM','no_weapon'], ['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 3, "Alors Musashi ? Ta décision ?",kind_info=[['SM', 'no_weapon'],['KM','no_weapon'], ['SH', 'no_weapon'], 3])
                        self.cinematic_frame(screen, "bamboo2", 3, "Eh bien Sensei Hoshida, je pense que vous connaissez déjà la réponse.",kind_info=[['SM', 'no_weapon'],['KM','no_weapon'], ['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 3, "Ah ! Tu me rassures alors Musashi. Je suis fier de ton choi-",kind_info=[['SM', 'no_weapon'],['KM','no_weapon'], ['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 0, "(SCHIOU) (Sensei Hoshida se fait transpercer le coeur par Musashi)")
                        self.cinematic_frame(screen, "bamboo2", 3, " ! ! ! Guah..",kind_info=[['SM', 'no_weapon'],['KM','no_weapon'], ['SH', 'no_weapon'], 3])
                        self.cinematic_frame(screen, "bamboo2", 3, "Mais...Pourquoi...Fais...Tu...Cela…",kind_info=[['SM', 'no_weapon'],['KM','no_weapon'], ['SH', 'no_weapon'], 3])
                        self.cinematic_frame(screen, 'bamboo2', 3, "Mais, tu es devenu totalement fou Musashi !!!",kind_info=[['KM', 'no_weapon'], ['SM', 'no_weapon'], ['SH', 'no_weapon'],1, True])
                        self.cinematic_frame(screen, "bamboo2", 3, "Heh, vieux schnock. Tu n'as pas du tout compris on dirait.",kind_info=[['SM', 'no_weapon'],['KM','no_weapon'], ['SH', 'no_weapon'], 1, True])
                        self.cinematic_frame(screen, "bamboo2", 3, "Comme je l'ai déjà dit, la violence est l'outil le plus pratique pour pouvoir", "faire changer le monde à sa guise.",kind_info=[['SM', 'no_weapon'],['KM','no_weapon'], ['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 3, "Sans la violence, on cesse d'évoluer. C'est grâce aux combats, aux duels,", "guerres qu'on n'arrive à avoir dans de nouvelles avancées technologiques.",kind_info=[['SM', 'no_weapon'],['KM','no_weapon'], ['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 3, "Vous vous trompez fortement sur la distinction de ces deux chemins.",kind_info=[['SM', 'no_weapon'],['KM','no_weapon'], ['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 3, "..Tu me déçois fortement mon cher élève..",kind_info=[['SM', 'no_weapon'],['KM','no_weapon'], ['SH', 'no_weapon'], 3])
                        self.cinematic_frame(screen, "bamboo2", 3, "Je vous retourne le compliment. Je vais tous les massacrer, vous verrez..",kind_info=[['SM', 'no_weapon'], ['KM','no_weapon'],['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 3, "..Tu.. es.. renvoyé..",kind_info=[['SM', 'no_weapon'],['KM','no_weapon'], ['SH', 'no_weapon'], 3])
                        self.cinematic_frame(screen, "bamboo2", 0, "(Sensei Hoshida tombe par terre)")
                        self.cinematic_frame(screen, 'bamboo2', 2, "Je ne te reconnais plus, je ne reconnais plus mon grand-frère Musashi...", "Qu'es-tu devenu... ",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'],2])
                        self.cinematic_frame(screen, "bamboo2", 2, "Hmph. Il n'en avait pas pour longtemps ce vieillard.",kind_info=[['SM', 'no_weapon'],['KM','no_weapon'],1])
                        self.cinematic_frame(screen, "bamboo2", 0, "Musashi s'approche de plus en plus de son plus grand affrontement.")
                        self.cinematic_frame(screen, "bamboo2", 0, "Le chef du clan Takahiro, l'attend dans son domaine avec impatience, pour", "pouvoir en finir.")
                        self.cinematic_frame(screen, "bamboo2", 0, "Qui en sortira vainqueur ? A suivre dans le prochain épisode..")
                        self.ecran_noir(screen)
        elif saved =='KT':
            if juzo==True:
                self.cinematic_frame(screen, "bamboo5", 3, " ! Ce chariot..ce sac..ces vêtements, ce ne serait pas.. ?",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'],1])
                self.cinematic_frame(screen, "bamboo5", 3, "C'est marchand Juzo !",kind_info=[['KT','no_weapon'],['SM', 'no_weapon'], ['JM', 'no_weapon'],1, True])
                self.cinematic_frame(screen, "bamboo5", 3, "Musashi ! C'est urgent ! !",kind_info=[['KT', 'no_weapon'],['SM', 'no_weapon'], ['JM', 'no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 3, "Quoi donc ?",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'],1,True])
                self.cinematic_frame(screen, "bamboo5", 3, "Je suis désolé de te dire cela, mais il va falloir que tu me rendes service", "ici et maintenant. ",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 3, "Ici et maintenant ? Pourquoi ???",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'],1])
                self.cinematic_frame(screen, "bamboo5", 3, "Oui..Malheureusement je ne t'avais pas prévenu auparavant lors de notre", "rencontre dans la forêt..",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 3, "Le “Tengoku no Ikari”..est une arme maudite.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 3, " ! ! Une arme maudite ?",kind_info=[['KT', 'no_weapon'],['SM', 'no_weapon'], ['JM', 'no_weapon'],1, True])
                self.cinematic_frame(screen, "bamboo5", 3, "Alors que c'est l'une des 7 épées légendaires ?",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'],1, True])
                self.cinematic_frame(screen, "bamboo5", 3, "Oui..Sache que les 7 épées légendaires sont toutes maudites.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 3, "Le seul moyen de lever la malédiction, c'est de battre une autre personne qui", "possède une autre arme légendaire.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 3, "Hm. Si j'ai compris, je vais devoir affronter un autre guerrier avec cette", "même arme..",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'],1])
                self.cinematic_frame(screen, "bamboo5", 3, "Dans ce cas là, où devrais-je donc l'affronter ?",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'],1])
                self.cinematic_frame(screen, "bamboo5", 3, "Eh bien. Justement, il ne devrait pas tarder à arriver..",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 0, "Un guerrier sort de son cheval, rempli de détermination et de sérieux.")
                self.cinematic_frame(screen, "bamboo5", 3, "...",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['SA','no_weapon'],3,None,['SH']])
                self.cinematic_frame(screen, "bamboo5", 3, "Par ailleurs, sache que ceux qui possèdent l'une de ces épées sont destinées","à forcément se rencontrer un jour.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 3, "Lors du moment venu, un combat à mort se produit. Il ne peut y avoir qu'un", "seul vainqueur.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 3, "Celui qui remporte la victoire aura la possibilité d'utiliser l'autre arme,", "mais restera à nouveau maudit.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 3, "Je suis très navré de ne t'avoir pas prévenu auparavant.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 3, "...Non tu ne devrais pas t'excuser.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'],1])
                self.cinematic_frame(screen, "bamboo5", 3, "Si toi aussi, tu as été maudit par cette arme..",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'],1])
                self.cinematic_frame(screen, "bamboo5", 3, "Alors... Je suis prêt à lever non seulement ma malédiction, mais aussi la", "tienne.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'],1])
                self.cinematic_frame(screen, "bamboo5", 3, "Musashi...",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 3, "Que l'arme soit maudite ou non, le principe reste le même. Ce n'est pas nous", "qui choisissons notre épée, c'est l'épée qui nous choisit.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'],1])
                self.cinematic_frame(screen, "bamboo5", 3, "Ainsi, je suis prêt à parier sur ma vie pour être l'élu de ce katana.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'],1])
                self.cinematic_frame(screen, "bamboo5", 3, "Musashi, je vais t'aider dans ton duel.",kind_info=[['KT', 'no_weapon'],['SM', 'no_weapon'],['JM', 'no_weapon'],1, True])
                self.cinematic_frame(screen, "bamboo5", 3, "Je te remercie Takeshi, mais puisque c'est un duel, ce n'est qu'entre mon", "adversaire et moi.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'],1, True])
                self.cinematic_frame(screen, "bamboo5", 3, "Désolé, mais exceptionnellement je ne vais pas demander ton aide.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['JM', 'no_weapon'],1])
                self.cinematic_frame(screen, "bamboo5", 3, "Assez parler. Passons aux introductions.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'],['SA','no_weapon'],1])
                self.cinematic_frame(screen, "bamboo5", 3, "Je suis Shikisha Musashi. Je suis récemment devenu samouraï et je viens du", "village de Magome",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'],['SA','no_weapon'],1])
                self.cinematic_frame(screen, "bamboo5", 3, "...Je suis Senshi Akuma, un samouraï d'Aizuwakamatsu. J'appartiens au clan", "Yoshioka, un clan qui deviendra l'un des clans les plus puissants de toute", "l'histoire du Japon.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'],['SA','no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 3, "Si j'ai bien compris, ton épée légendaire serait le “Tengoku no Ikari”. Pour", "mon cas, c'est le “Jigoku no Shizuka”. Il se trouve que ces deux armes font", "une paire très puissante.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'],['SA','no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 3, "Celui qui remporte ce duel sera celui qui régnera en tant que le plus", "puissant samouraï de l'histoire.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'],['SA','no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 3, "Qui restera en vie ? Le paradis ? ou l'Enfer ?",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['SA','no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 3, "En tout cas, je ne compte pas baisser les bras. Prépare toi jeune samouraï,", "je vais gagner ce duel..",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['SA','no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 3, "Et être reconnu en tant que le meilleur samouraï de l'histoire dans le clan", "Yoshioka !",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['SA','no_weapon'],3])
                self.cinematic_frame(screen, "bamboo5", 3, "Sache que tu n'es pas le seul à avoir gagné en puissance grâce à ton clan. ",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['SA','no_weapon'],1])
                self.cinematic_frame(screen, "bamboo5", 3, "Nos destins vont s'entrechoquer..Ici et maintenant !",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], ['SA','no_weapon'],1])
                self.ecran_noir(screen)
            if in_genocide_route==True:
                self.cinematic_frame(screen, 'bamboo2', 3, "..Musashi.", kind_info=[['SM','no_weapon'], ['KT','no_weapon'], ['SH','no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo2', 3, "Sensei Hoshida ? Que faîtes vous ici ?", kind_info=[['SM','no_weapon'], ['KT','no_weapon'],['SH','no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo2', 3, "Tu sais très bien pourquoi je suis ici.", kind_info=[['SM','no_weapon'],['KT','no_weapon'], ['SH','no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo2', 3, " ? ? ? Je n'ai pas la moindre idée de votre présence.", kind_info=[['SM','no_weapon'],['KT','no_weapon'], ['SH','no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo2', 3, "Dans ce cas là..J'aimerai bien que tu m'expliques..", kind_info=[['SM','no_weapon'],['KT','no_weapon'], ['SH','no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo2', 3, "La présence de sang qui couvre tes vêtements..", kind_info=[['SM','no_weapon'],['KT','no_weapon'], ['SH','no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo2', 3, "Du sang ? Pff, franchement c'est juste le sang de certains membres du", "clan Takahiro.", kind_info=[['SM','no_weapon'],['KT','no_weapon'], ['SH','no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo2', 3, "Ne vous inquiétez pas, c'est pour le bien de chacun.", kind_info=[['SM','no_weapon'],['KT','no_weapon'], ['SH','no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo2', 3, "S'ils ont tué, je ne devrais pas pour autant me restreindre à me défendre pour", "les tuer aussi.", kind_info=[['SM','no_weapon'],['KT','no_weapon'], ['SH','no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo2', 3, "Musashi... ne dis quand même pas ça", kind_info=[['KT','no_weapon'],['SM','no_weapon'], ['SH','no_weapon'], 1, True])
                self.cinematic_frame(screen, 'bamboo2', 3, "C'est justement le problème Musashi. Tu ne fais que de tuer.", kind_info=[['KT','no_weapon'],['SM','no_weapon'],['SH','no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo2', 3, "Si tu poursuis ce chemin, tu vas fortement le regretter. ", kind_info=[['KT','no_weapon'],['SM','no_weapon'],['SH','no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo2', 3, "Tu vas t'apercevoir au final que tu seras devenu ce que tu détestais", "auparavant.", kind_info=[['KT','no_weapon'],['SM','no_weapon'], ['SH','no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo2', 3, "La raison pour laquelle je bloque ton passage, c'est de te faire comprendre", "cela.", kind_info=[['KT','no_weapon'],['SM','no_weapon'], ['SH','no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo2', 3, "Et pourtant, tu aurais dit la même chose à ces tueurs non ?", kind_info=[['SM','no_weapon'],['KT','no_weapon'], ['SH','no_weapon'], 1,True])
                self.cinematic_frame(screen, 'bamboo2', 3, "Si la violence est le seul moyen de faire changer le monde à ta guise, alors", "j'en ferai bon usage.", kind_info=[['SM','no_weapon'],['KT','no_weapon'], ['SH','no_weapon'], 1])
                self.cinematic_frame(screen, 'bamboo2', 3, "Pas forcément Musashi, pas forcément. ", kind_info=[['SM','no_weapon'],['KT','no_weapon'], ['SH','no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo2', 3, "Prendre une décision pacifiste est l'une des meilleures décisions qu'on puisse", "prendre moralement.", kind_info=[['SM','no_weapon'],['KT','no_weapon'], ['SH','no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo2', 3, "Le but d'être pacifiste, c'est de faire comprendre aux autres de ne pas avoir", "toujours recours à la violence.", kind_info=[['SM','no_weapon'], ['KT','no_weapon'],['SH','no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo2', 3, "Donc Musashi...Mon cher élève..Quel chemin vas-tu prendre ?", kind_info=[['SM','no_weapon'], ['KT','no_weapon'],['SH','no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo2', 3, "Le chemin des regrets ? Ou le chemin du succès ?", kind_info=[['SM','no_weapon'],['KT','no_weapon'], ['SH','no_weapon'], 3])
                self.cinematic_frame(screen, 'bamboo2', 3, "Musashi, je t'en supplie. Ecoute notre sensei !", kind_info=[['KT','no_weapon'],['SM','no_weapon'], ['SH','no_weapon'], 1, True])
                output1, output2 = self.choice_frame(screen, "bamboo2", [0, 2], ["ECOUTER SENSEI", "NE PAS L'ECOUTER"])
                if output1=='choice':
                    if output2==1:
                        self.cinematic_frame(screen, "bamboo2", 3, "..Oui vous avez certainement raison Sensei Hoshida.",kind_info=[['SM', 'no_weapon'],['KT','no_weapon'], ['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 3, "J'ai été beaucoup aveuglé par la violence. Je ne faisais que d'en vouloir au", "clan Takahiro.",kind_info=[['SM', 'no_weapon'],['KT','no_weapon'], ['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 3, "J'avais un très grand désir de vengeance..Mais je souhaite me repentir.",kind_info=[['SM', 'no_weapon'],['KT','no_weapon'], ['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 3, "Même si on a accumulé des regrets jusqu'ici, alors je suis prêt à accumuler", "des succès à partir d'aujourd'hui.",kind_info=[['SM', 'no_weapon'],['KT','no_weapon'], ['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 3, "Je suis fier de toi, mon cher élève.  Poursuis le chemin de rédemption, et", "deviens un véritable samouraï.",kind_info=[['SM', 'no_weapon'],['KT','no_weapon'], ['SH', 'no_weapon'], 3])
                        self.cinematic_frame(screen, "bamboo2", 3, "Cesse les massacres, laisse ton esprit se ressaisir et tu t'offriras une", "meilleure voie.",kind_info=[['SM', 'no_weapon'],['KT','no_weapon'], ['SH', 'no_weapon'], 3])
                        self.cinematic_frame(screen, "bamboo2", 3, "Oui Sensei Hoshida. Veuillez me pardonner de tout ce qu'ai pu faire d'atroce.",kind_info=[['SM', 'no_weapon'], ['KT','no_weapon'],['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 3, "Tant que tu gardes ta parole, alors je suis prêt à te pardonner Musashi.",kind_info=[['SM', 'no_weapon'],['KT','no_weapon'], ['SH', 'no_weapon'], 3])
                        self.cinematic_frame(screen, 'bamboo2', 3, "Tu es enfin redevenu toi-même Musashi !!",kind_info=[['KT','no_weapon'],['SM', 'no_weapon'],['SH', 'no_weapon'],1,True])
                        self.cinematic_frame(screen, "bamboo2", 3, "La fin du voyage approche, alors je t'en prie, viens à bout du clan Takahiro,", "pour tout le Japon.",kind_info=[['KT','no_weapon'],['SM', 'no_weapon'],['SH', 'no_weapon'], 3])
                        self.cinematic_frame(screen, "bamboo2", 3, "Oui Sensei Hoshida, je ne compte pas vous décevoir ! ",kind_info=[['SM', 'no_weapon'],['KT','no_weapon'], ['SH', 'no_weapon'], 1, True])
                        self.cinematic_frame(screen, "bamboo2", 0, "Musashi s'approche de plus en plus à son plus grand affrontement.")
                        self.cinematic_frame(screen, "bamboo2", 0, "Le chef du clan Takahiro, l'attend dans son domaine avec impatience, pour","pouvoir en finir.")
                        self.cinematic_frame(screen, "bamboo2", 0, "Qui en sortira vainqueur ? A suivre dans le prochain épisode..")
                        self.ecran_noir(screen)
                    elif output2==2:
                        self.cinematic_frame(screen, "bamboo2", 3, "...",kind_info=[['SM', 'no_weapon'],['KT','no_weapon'], ['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 3, "Alors Musashi ? Ta décision ?",kind_info=[['SM', 'no_weapon'],['KT','no_weapon'], ['SH', 'no_weapon'], 3])
                        self.cinematic_frame(screen, "bamboo2", 3, "Eh bien Sensei Hoshida, je pense que vous connaissez déjà la réponse.",kind_info=[['SM', 'no_weapon'],['KT','no_weapon'], ['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 3, "Ah ! Tu me rassures alors Musashi. Je suis fier de ton choi-",kind_info=[['SM', 'no_weapon'],['KT','no_weapon'], ['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 0, "(SCHIOU) (Sensei Hoshida se fait transpercer le coeur par Musashi)")
                        self.cinematic_frame(screen, "bamboo2", 3, " ! ! ! Guah..",kind_info=[['SM', 'no_weapon'],['KT','no_weapon'], ['SH', 'no_weapon'], 3])
                        self.cinematic_frame(screen, "bamboo2", 3, "Mais...Pourquoi...Fais...Tu...Cela…",kind_info=[['SM', 'no_weapon'],['KT','no_weapon'], ['SH', 'no_weapon'], 3])
                        self.cinematic_frame(screen, 'bamboo2', 3, "Mais, tu es devenu totalement fou Musashi !!!",kind_info=[['KT','no_weapon'],['SM', 'no_weapon'],['SH', 'no_weapon'],1,True])
                        self.cinematic_frame(screen, "bamboo2", 3, "Heh, vieux schnock. Tu n'as pas du tout compris on dirait.",kind_info=[['SM', 'no_weapon'],['KT','no_weapon'], ['SH', 'no_weapon'], 1, True])
                        self.cinematic_frame(screen, "bamboo2", 3, "Comme je l'ai déjà dit, la violence est l'outil le plus pratique pour pouvoir", "faire changer le monde à sa guise.",kind_info=[['SM', 'no_weapon'],['KT','no_weapon'], ['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 3, "Sans la violence, on cesse d'évoluer. C'est grâce aux combats, aux duels,", "guerres qu'on n'arrive à avoir dans de nouvelles avancées technologiques.",kind_info=[['SM', 'no_weapon'],['KT','no_weapon'], ['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 3, "Vous vous trompez fortement sur la distinction de ces deux chemins.",kind_info=[['SM', 'no_weapon'],['KT','no_weapon'], ['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 3, "..Tu me déçois fortement mon cher élève..",kind_info=[['SM', 'no_weapon'],['KT','no_weapon'], ['SH', 'no_weapon'], 3])
                        self.cinematic_frame(screen, "bamboo2", 3, "Je vous retourne le compliment. Je vais tous les massacrer, vous verrez..",kind_info=[['SM', 'no_weapon'], ['KT','no_weapon'],['SH', 'no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 3, "..Tu.. es.. renvoyé..",kind_info=[['SM', 'no_weapon'],['KT','no_weapon'], ['SH', 'no_weapon'], 3])
                        self.cinematic_frame(screen, "bamboo2", 0, "(Sensei Hoshida tombe par terre)")
                        self.cinematic_frame(screen, 'bamboo2', 2, "Je ne te reconnais plus, je ne reconnais plus mon ami Musashi...", "Qu'es-tu devenu... ",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'],2])
                        self.cinematic_frame(screen, "bamboo2", 2, "Hmph. Il n'en avait pas pour longtemps ce vieillard.",kind_info=[['SM', 'no_weapon'],['KT','no_weapon'], 1])
                        self.cinematic_frame(screen, "bamboo2", 0, "Musashi s'approche de plus en plus de son plus grand affrontement.")
                        self.cinematic_frame(screen, "bamboo2", 0, "Le chef du clan Takahiro, l'attend dans son domaine avec impatience, pour", "pouvoir en finir.")
                        self.cinematic_frame(screen, "bamboo2", 0, "Qui en sortira vainqueur ? A suivre dans le prochain épisode..")
                        self.ecran_noir(screen)

    def cinematic_16(self,screen,saved):
        #cinématique vérifiée
        if saved=='none':
            self.cinematic_frame(screen, "black",0,"Le combat tant attendu est arrivé.")
            self.cinematic_frame(screen, "black",0,"Musashi avec son visage coriace reprend sa respiration avant la bataille", "finale.")
            self.cinematic_frame(screen, "black",0,"Ces deux destins s'entrechoqueront très bientôt.")
            self.cinematic_frame(screen, "black",0,"Un loup blanc solitaire...contre une armée de chasseurs impitoyables..")
            self.cinematic_frame(screen, "black",0,"Saurez-vous guider vos compétences vers la victoire?")
            self.cinematic_frame(screen, "black",0,"Nous le saurons...dès maintenant.")
            self.ecran_noir(screen)
            self.cinematic_frame(screen, "tkh2",0,"Une brise passe à travers les vêtements du samouraï rempli de conviction.")
            self.cinematic_frame(screen, "tkh2",0,"Il se sent tendu, son coeur bat rapidement, mais sa volonté, son objectif","reste le même...")
            self.cinematic_frame(screen, "tkh2",0,"Terrasser le clan Takahiro de sa destruction et de son totalitarisme.")
            self.cinematic_frame(screen, "tkh2", 1, "...",kind_info=["SM", "SM", "no_weapon", "right"])
            self.cinematic_frame(screen, "tkh2", 1, "Le moment est enfin venu.",kind_info=["SM", "SM", "no_weapon", "right"])
            self.cinematic_frame(screen, "tkh2", 1, "Le domaine du clan Takahiro..",kind_info=["SM", "SM", "no_weapon", "right"])
            self.cinematic_frame(screen, "tkh2", 1, "Le nombre d'entraînements, d'ennemis..de succès et d'échecs...",kind_info=["SM", "SM", "no_weapon", "right"])
            self.cinematic_frame(screen, "tkh2", 1, "J'ai pu faire mes preuves..et je vais enfin mettre un terme à ce cauchemar !",kind_info=["SM", "SM", "no_weapon", "right"])
            self.cinematic_frame(screen, "tkh2", 1, "Qu'ils soient 10, 100, 1000, 10000 ou 100000..Je vais tous les battre ! ",kind_info=["SM", "SM", "no_weapon", "right"])
            self.cinematic_frame(screen, "tkh2", 1, "Je forgerai..ma propre Voie ! ",kind_info=["SM", "SM", "no_weapon", "right"])
            self.cinematic_frame(screen, "tkh2",0,"Musashi entre enfin dans le domaine des Takahiro. De nombreuses épreuves", "seront face à notre samouraï.")
            self.cinematic_frame(screen, "tkh2",0,"La fin approche de plus en plus.")

        elif saved =='KM':
            self.cinematic_frame(screen, "black",0,"Le combat tant attendu est arrivé.")
            self.cinematic_frame(screen, "black",0,"Musashi avec son visage coriace reprend sa respiration avant la bataille", "finale.")
            self.cinematic_frame(screen, "black",0,"Ces deux destins s'entrechoqueront très bientôt.")
            self.cinematic_frame(screen, "black",0,"Un loup blanc solitaire...contre une armée de chasseurs impitoyables..")
            self.cinematic_frame(screen, "black",0,"Saurez-vous guider vos compétences vers la victoire?")
            self.cinematic_frame(screen, "black",0,"Nous le saurons...dès maintenant.")
            self.ecran_noir(screen)
            self.cinematic_frame(screen, "tkh2",0,"Une brise passe à travers les vêtements du samouraï rempli de conviction.")
            self.cinematic_frame(screen, "tkh2",0,"Il se sent tendu, son coeur bat rapidement, mais sa volonté, son objectif","reste le même...")
            self.cinematic_frame(screen, "tkh2",0,"Terrasser le clan Takahiro de sa destruction et de son totalitarisme.")
            self.cinematic_frame(screen, "tkh2", 2, "...",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh2", 2, "Le moment est enfin venu.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh2", 2, "...Oui..Cela m'attriste tellement de voir le bout de ce voyage.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], 2])
            self.cinematic_frame(screen, "tkh2", 2, "Le domaine du clan Takahiro..",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh2", 2, "Le nombre d'entraînements, d'ennemis..de succès et d'échecs...",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh2", 2, "J'ai pu faire mes preuves..et je vais enfin mettre un terme à ce cauchemar !",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh2", 2, "Qu'ils soient 10, 100, 1000, 10000 ou 100000..Je vais tous les battre ! ",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh2", 2, "Je forgerai..ma propre Voie ! ",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh2", 2, "Je te souhaite très bonne chance grand frère, ne meurs pas ! ",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'], 2])
            self.cinematic_frame(screen, "tkh2",0,"Musashi entre enfin dans le domaine des Takahiro. De nombreuses épreuves", "seront face à notre samouraï.")
            self.cinematic_frame(screen, "tkh2",0,"La fin approche de plus en plus.")
        elif saved =='KT':
            self.cinematic_frame(screen, "black",0,"Le combat tant attendu est arrivé.")
            self.cinematic_frame(screen, "black",0,"Musashi avec son visage coriace reprend sa respiration avant la bataille", "finale.")
            self.cinematic_frame(screen, "black",0,"Ces deux destins s'entrechoqueront très bientôt.")
            self.cinematic_frame(screen, "black",0,"Un loup blanc solitaire...contre une armée de chasseurs impitoyables..")
            self.cinematic_frame(screen, "black",0,"Saurez-vous guider vos compétences vers la victoire?")
            self.cinematic_frame(screen, "black",0,"Nous le saurons...dès maintenant.")
            self.ecran_noir(screen)
            self.cinematic_frame(screen, "tkh2",0,"Une brise passe à travers les vêtements du samouraï rempli de conviction.")
            self.cinematic_frame(screen, "tkh2",0,"Il se sent tendu, son coeur bat rapidement, mais sa volonté, son objectif","reste le même...")
            self.cinematic_frame(screen, "tkh2",0,"Terrasser le clan Takahiro de sa destruction et de son totalitarisme.")
            self.cinematic_frame(screen, "tkh2", 2, "...",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh2", 2, "...",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 2])
            self.cinematic_frame(screen, "tkh2", 2, "Le moment est enfin venu.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh2", 2, "Oui. On est enfin arrivé..",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 2])
            self.cinematic_frame(screen, "tkh2", 2, "Le domaine du clan Takahiro..",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh2", 2, "Le nombre d'entraînements, d'ennemis..de succès et d'échecs...",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh2", 2, "J'ai pu faire mes preuves..et je vais enfin mettre un terme à ce cauchemar !",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh2", 2, "Qu'ils soient 10, 100, 1000, 10000 ou 100000..Je vais tous les battre ! ",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh2", 2, "Je forgerai..ma propre Voie ! ",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh2",0,"Musashi entre enfin dans le domaine des Takahiro. De nombreuses épreuves", "seront face à notre samouraï.")
            self.cinematic_frame(screen, "tkh2",0,"La fin approche de plus en plus.")
        self.ecran_noir(screen)

    def cinematic_17(self,screen,saved):

        if saved=='none' or saved=='KM':
            self.switch_lowercase(True)
            self.cinematic_frame(screen, "tkh2", 1, "Sigh...",kind_info=["SM", "SM", "no_weapon", "right"])
            self.switch_lowercase(False)
            self.cinematic_frame(screen, "tkh2", 1, "Qu'ils sont coriaces ceux-là.",kind_info=["SM", "SM", "no_weapon", "right"])
            self.cinematic_frame(screen, "tkh2", 1, "Ils auront beau être plusieurs, ils auront beau avoir toutes les armes qui", "existent dans notre monde..",kind_info=["SM", "SM", "no_weapon", "right"])
            self.cinematic_frame(screen, "tkh2", 1, "Ils ne surpasseront jamais mes propres tactiques, mes propres stratégies..",kind_info=["SM", "SM", "no_weapon", "right"])
            self.cinematic_frame(screen, "tkh2", 1, "Oui..Tout cela tourne autour de ce qu'on appelle cette“Voie”.",kind_info=["SM", "SM", "no_weapon", "right"])
            self.cinematic_frame(screen, "tkh2", 1, "La“Voie”..à deux sabres !",kind_info=["SM", "SM", "no_weapon", "right"])
            self.cinematic_frame(screen, "tkh2", 1, "Hmm..non pas encore. Je n'ai pas encore maîtrisé le double maniement des", "sabres.",kind_info=["SM", "SM", "no_weapon", "right"])
            self.cinematic_frame(screen, "tkh2", 1, "Cela pourrait m'être intéressant par la suite..Mais j'apprendrai à utiliser", "deux katanas une autre fois.",kind_info=["SM", "SM", "no_weapon", "right"])
            self.cinematic_frame(screen, "tkh2", 1, "Rejoignons le chef du clan..Il doit m'attendre pendant un bon moment.",kind_info=["SM", "SM", "no_weapon", "right"])
            self.cinematic_frame(screen, "tkh2",0, "Musashi contre le chef du clan Takahiro, Kojiro Takahiro. Le duel des", "meilleurs samouraïs de l'époque.")
            self.cinematic_frame(screen, "tkh2",0, "Le samouraï le plus fort d'aujourd'hui contre le samouraï le plus fort de", "l'histoire.")
            self.cinematic_frame(screen, "tkh2",0, "Qui le remportera ? A suivre dans ce dernier épisode.")

        elif saved=='KT':
            self.switch_lowercase(True)
            self.cinematic_frame(screen, "tkh2", 2, "Sigh...",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])
            self.switch_lowercase(False)
            self.cinematic_frame(screen, "tkh2", 2, "Qu'ils sont coriaces ceux-là.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh2", 2, "Oui, je dois l'avouer, ils sont très forts.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 2])
            self.cinematic_frame(screen, "tkh2", 2, "Ils auront beau être plusieurs, ils auront beau avoir toutes les armes qui", "existent dans notre monde..",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh2", 2, "Ils ne surpasseront jamais mes propres tactiques, mes propres stratégies..",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh2", 2, "Oui..Tout cela tourne autour de ce qu'on appelle cette “Voie”.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh2", 2, "La “Voie”..à deux sabres !",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh2", 2, "La “Voie” à deux sabres ? Qu'est-ce tu racontes ? ",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 2])
            self.cinematic_frame(screen, "tkh2", 2, "C'est un concept que j'ai voulu implémenter depuis un bon bout de temps.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh2", 2, "Cependant, je ne compte pas encore le faire puisque je n'ai pas encore", "maîtrisé le double maniement des sabres.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh2", 2, "Cela pourrait m'être intéressant par la suite..Mais j'apprendrai à utiliser", "deux katanas une autre fois.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh2", 2, "Intéressant, je suis curieux de voir comment ta théorie va aboutir.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 2])
            self.cinematic_frame(screen, "tkh2", 2, "Takeshi, laisse-moi affronter moi-même le chef du clan..Il doit m'attendre", "pendant un bon moment..",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh2", 2, "Ce sera un duel entre lui et moi. Attends-moi à la sortie.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh2", 2, "D'accord Musashi..Tu as intérêt à rester en vie.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 2])
            self.cinematic_frame(screen, "tkh2", 2, "Ne t'inquiètes pas, je gagnerai ce duel.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh2",0, "Musashi contre le chef du clan Takahiro, Kojiro Takahiro. Le duel des", "meilleurs samouraïs de l'époque.")
            self.cinematic_frame(screen, "tkh2",0, "Le samouraï le plus fort d'aujourd'hui contre le samouraï le plus fort de", "l'histoire.")
            self.cinematic_frame(screen, "tkh2",0, "Qui le remportera ? A suivre dans ce dernier épisode.")
        self.ecran_noir(screen)

    def cinematic_18(self,screen):
        #cinématique vérifiée
        self.cinematic_frame(screen, "tkh1", 2, "..Takhiro Kojiro, chef du clan Takahiro..",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
        self.cinematic_frame(screen, "tkh1", 2, "Shikisha Musashi..tu es donc vivant..",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
        self.cinematic_frame(screen, "tkh1", 2, "Je te félicite d'avoir vaincu mes très puissants subordonnées..Tu es bien", "l'élève de Sensei Hoshida.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
        self.cinematic_frame(screen, "tkh1", 2, "Vous allez le payer fortement ! Pourquoi toute cette destruction ? Cette", "torture ? Pourquoi ?",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
        self.cinematic_frame(screen, "tkh1", 2, "Ce n'est pas la question que tu devrais te poser mon garçon.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
        self.cinematic_frame(screen, "tkh1", 2, "Tous ces villages, ces habitants, ces personnes ont tout simplement eu ce", "qu'ils devaient avoir.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
        self.cinematic_frame(screen, "tkh1", 2, "De toute façon tu dois bien savoir que c'est moi qui orchestre ces actions", "pour le bien du Japon.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
        self.cinematic_frame(screen, "tkh1", 2, "Je prendrai le contrôle de ce pays pour pouvoir mener à bien une nouvelle ère,", "une nouvelle époque, une nouvelle évolution.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
        self.cinematic_frame(screen, "tkh1", 2, "Tu n'es pas la première personne qui a tenté de mettre fin à mes projets, et", "tu es loin d'être le dernier.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
        self.cinematic_frame(screen, "tkh1", 2, "25 ans..Cela fait depuis 25 ans que j'ai fait du clan Takahiro l'un des", "meilleurs clans du Japon.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
        self.cinematic_frame(screen, "tkh1", 2, "Et je suis l'un des meilleurs samouraïs que le Japon n'a jamais connu.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
        self.cinematic_frame(screen, "tkh1", 2, "Certains diront que je suis une bonne personne qui agit pour le mal..",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
        self.cinematic_frame(screen, "tkh1", 2, "Je dirai que c'est le contraire, puisque mon cœur et mes actions se tournent", "très certainement vers la justice.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
        self.cinematic_frame(screen, "tkh1", 2, "De plus, tu devrais savoir à quel point nous vivons dans un monde corrompu.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
        self.cinematic_frame(screen, "tkh1", 2, "Ainsi, je te conseille fortement de ne pas lever un seul doigt contre moi.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
        self.cinematic_frame(screen, "tkh1", 2, "...un monde corrompu ?",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
        self.cinematic_frame(screen, "tkh1", 2, "Vous dîtes que vos actions..et votre coeur se tournent vers le chemin de la", "justice ?",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
        self.cinematic_frame(screen, "tkh1", 2, "Ne me faîtes pas rire !",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
        self.cinematic_frame(screen, "tkh1", 2, "Vous avez ruiné énormément de personnes.. énormément de familles..", "énormément de vies..",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
        self.cinematic_frame(screen, "tkh1", 2, "Et vous pensez vraiment agir pour le bien ?",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
        self.cinematic_frame(screen, "tkh1", 2, "Dans ce cas là, vous vous trompez fortement ! ",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
        self.cinematic_frame(screen, "tkh1", 2, "Que mon adversaire soit faible ou fort.., je donnerai toujours mon maximum.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
        self.cinematic_frame(screen, "tkh1", 2, "Et vous Takahiro Kojiro..Je renverserai votre clan de sorte à ce que la paix", "soit amenée à la lumière du jour !",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
        self.cinematic_frame(screen, "tkh1", 2, "Préparez-vous, je ne serai d'aucune pitié !",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
        self.cinematic_frame(screen, "tkh1", 2, "Tu me fatigues...",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
        self.cinematic_frame(screen, "tkh1", 2, "Très bien, tu vas payer pour tout ce que tu as fait à mon clan. Je vais te", "mettre à terre et te torture jusqu'à la fin de ma vie.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
        self.cinematic_frame(screen, "tkh1", 2, "Amenez-vous, je vous attends !",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
        self.ecran_noir(screen)

    def cinematic_19(self,screen,chef_tkh_battu):
        #cinématique vérifiée
        if chef_tkh_battu==False:
            self.cinematic_frame(screen, "tkh1", 2, "Je te l'avais dit. Tu n'avais aucune chance de me battre.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
        elif chef_tkh_battu==True:
            self.cinematic_frame(screen, "tkh1", 2, "...Comment..cela..se fait-il..?",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
            self.cinematic_frame(screen, "tkh1", 2, "Moi ? Me faire battre par un gamin.. comme lui ?",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
            self.cinematic_frame(screen, "tkh1", 2, "Impossible..C'est impossible ! !",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
            self.cinematic_frame(screen, "tkh1", 2, "Le moment où vous vous êtes dit qu'il était impossible de vous battre..",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh1", 2, "C'était le moment où vous aviez déjà perdu. ",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh1", 2, "Je n'ai pas envie de l'avouer..mais tu es un très puissant samouraï.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
            self.switch_lowercase(True)
            self.cinematic_frame(screen, "tkh1", 2, "Sigh...",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
            self.switch_lowercase(False)
            self.cinematic_frame(screen, "tkh1", 2, "Je vais bientôt y passer...",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
            self.cinematic_frame(screen, "tkh1", 2, "Toi, Shikisha Musashi..Tu as intérêt à réussir ta carrière de samouraï.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
            self.cinematic_frame(screen, "tkh1", 2, "Je reconnais mes erreurs...J'ai perdu mon duel...La mort ne fait que de", "m'attendre.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
        self.ecran_noir(screen)

    def cinematic_20(self,screen,route):
        #cinématique vérifiée
        if route=='pacifist':
            self.cinematic_frame(screen, "tkh1", 2, "M.Takahiro...Je suis ravi d'avoir fait ce duel avec vous. Malgré vos actions", "passées...",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh1", 2, "Je vous pardonne. Tout le monde mérite une seconde chance.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh1", 2, "Musashi...",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
            self.cinematic_frame(screen, "tkh1", 2, "Depuis la destruction de mon village natal, Magome..",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh1", 2, "J'avais  de nombreuses rancunes. Une colère bouillait au fond de moi.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh1", 2, "Cependant..Grâce à mon entraînement avec Sensei Hoshida..",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh1", 2, "J'ai pu assimiler en moi une paix intérieure, une paix manichéenne.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh1", 2, "Tout ce que je recherche n'est rien d'autre que le bien de chacun, que tout", "le monde soit satisfait.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh1", 2, "M.Takahiro, votre désir de lever la corruption de ce monde...est vraiment", "très admirable.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh1", 2, "Sachez cependant, qu'il existe d'autres solutions pour accomplir ses buts,", "sans avoir forcément recours à la violence.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh1", 2, "Même si on regrette d'avoir commis de tels actes, de telles erreurs, de tels", "pêchés..On a toujours l'opportunité de changer..",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh1", 2, " L'opportunité de devenir une meilleure personne.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh1", 2, "...",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
            self.cinematic_frame(screen, "tkh1", 2, "Tu es si sage pour un jeune homme de ton âge.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
            self.cinematic_frame(screen, "tkh1", 2, "Je suis ravi d'avoir péri de tes propres mains..",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
            self.cinematic_frame(screen, "tkh1", 0, "(Takahiro faint, inconscient, a perdu la vie.)")
            self.cinematic_frame(screen, "tkh1", 1, "Magome..M.Takahiro..Takeshi et Keiko..Regardez moi.",kind_info=['SM','SM','no_weapon','right'])
            self.cinematic_frame(screen, "tkh1", 1, "J'ai réussi à rétablir la paix au sein du Japon, je vais pouvoir sauver de", "nombreuses vies.",kind_info=['SM','SM','no_weapon','right'])
            self.cinematic_frame(screen, "tkh1", 1, "Ainsi, on peut toujours évoluer, toujours se remettre dans le droit chemin.",kind_info=['SM','SM','no_weapon','right'])
            self.cinematic_frame(screen, "tkh1", 1, "Et je suis ravi d'avoir l'avoir pris.",kind_info=['SM','SM','no_weapon','right'])
            self.cinematic_frame(screen, "tkh1", 1, "A toutes les personnes qui ont perdu la vie durant ces dernières années..","Veuillez reposer en paix.",kind_info=['SM','SM','no_weapon','right'])
            self.cinematic_frame(screen, "tkh1", 1, "Il vaut mieux subir le pardon de son ennemi plutôt que la vengeance de son", "ami.",kind_info=['SM','SM','no_weapon','right'])
            self.cinematic_frame(screen, "tkh1", 1, "Bon ! Je vais me remettre à l'entraînement ! ",kind_info=['SM','SM','no_weapon','right'])
            self.cinematic_frame(screen, "tkh1", 0, "FIN")

        elif route=='neutral':
            self.cinematic_frame(screen, "tkh1", 2, "M.Takahiro. Je vais être honnête, je ne suis pas le mieux placé pour vous", "dire cela..",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh1", 2, "Mais je comprends définitivement ce que vous ressentez.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh1", 2, "Moi-même j'ai fait des actes qui étaient considérés comme acceptables voire", "inacceptables.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh1", 2, "J'ai rempli le bonheur de nombreuses personnes tout comme leur douleur. Je", "commençais à ne plus me reconnaître.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh1", 2, "Malgré cela, j'ai pu me reprendre, et c'est ce qui comptait vraiment pour moi.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh1", 2, "Hmm je vois. Tu es donc toi aussi coupable de tes crimes tout comme moi ?",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
            self.cinematic_frame(screen, "tkh1", 2, "Oui..Et ce que j'aimerai vous dire, c'est qu'il existe toujours la", "possibilité de changer.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh1", 2, "Le passé de chacun donne une première image de ce qu'on est actuellement..",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh1", 2, "Ce qui compte vraiment au final, c'est maintenant. C'est le présent.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh1", 2, "Et lorsqu'on prend l'opportunité de devenir quelqu'un de bien, quelqu'un de", "bon, on façonne notre futur.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh1", 2, "C'est pour cela M.Takahiro, que je suis conscient des actes que vous avez", "commis auparavant..",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh1", 2, "Mais que cela importait peu si tout le monde avait la possibilité de changer.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh1", 2, "...Hm..Oui je pense que tu as définitivement raison.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
            self.cinematic_frame(screen, "tkh1", 2, "Heh..Peut-être que dans une autre vie, je pourrai devenir quelqu'un de bien,", "quelqu'un qui se tourne vers un bel avenir.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
            self.cinematic_frame(screen, "tkh1", 2, "La prochaine fois qu'on se voit..Je t'en ferai la promesse.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
            self.cinematic_frame(screen, "tkh1", 2, "Oui M.Takahiro, vivement cela, qu'à tous ceux qui ont péri ainsi que vous", "puissiez reposer en paix. ",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh1", 2, "Je te remercie jeune samouraï. Ne perds pas cette flamme qui est en toi.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
            self.cinematic_frame(screen,'tkh1',0, "(Takahiro faint, inconscient, a perdu la vie.)")
            self.cinematic_frame(screen, "tkh1", 1, "Magome..M.Takahiro..Takeshi et Keiko..Regardez moi.",kind_info=['SM','SM','no_weapon','right'])
            self.cinematic_frame(screen, "tkh1", 1, "J'ai réussi à rétablir la paix au sein du Japon, je vais pouvoir sauver de", "nombreuses vies.",kind_info=['SM','SM','no_weapon','right'])
            self.cinematic_frame(screen, "tkh1", 1, "J'ai beau commettre des horreurs, j'ai toujours la possibilité de me repentir.",kind_info=['SM','SM','no_weapon','right'])
            self.cinematic_frame(screen, "tkh1", 1, "Regardez mes progrès au fur et à mesure que j'évolue dans ma carrière de", "samouraï..",kind_info=['SM','SM','no_weapon','right'])
            self.cinematic_frame(screen, "tkh1", 1, "Je fonderai ma propre voie, une voie qui assure le bonheur de chacun, mais", "aussi de moi.",kind_info=['SM','SM','no_weapon','right'])
            self.cinematic_frame(screen, "tkh1", 1, "Une nouvelle journée, un nouvel espoir.",kind_info=['SM','SM','no_weapon','right'])
            self.cinematic_frame(screen, "tkh1", 1, "Mettez vos passés de côté, et fondez vos propres histoires.",kind_info=['SM','SM','no_weapon','right'])
            self.cinematic_frame(screen, "tkh1", 1, "Maintenant..Retour à l'entraînement ! ",kind_info=['SM','SM','no_weapon','right'])
            self.cinematic_frame(screen,'tkh1',0,"FIN")

        elif route == 'genocide':
            self.cinematic_frame(screen, "tkh1", 2, "Kh !",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
            self.cinematic_frame(screen, "tkh1", 0, "(Une lame transperce la tête de Takahiro)")
            self.cinematic_frame(screen, "tkh1", 2, "Comment ???",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
            self.cinematic_frame(screen, "tkh1", 2, "...",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh1", 2, "Hm ? Alors M.Takahiro ? Pouvez vous me dire un mot ?",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh1", 2, "Décidément..tu..n'es..vraiment..qu'un..véritable..prétentieux..",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
            self.cinematic_frame(screen, "tkh1", 2, "Tu oses accuser mes actes comme étant maléfiques..",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
            self.cinematic_frame(screen, "tkh1", 2, "Or, tu es tout simplement l'incarnation du mal !",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
            self.cinematic_frame(screen, "tkh1", 2, "Franchement tu devrais avoir honte !",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
            self.cinematic_frame(screen, "tkh1", 2, "Ha ! Ha ! Ha ! Ha ! Ha ! Ha ! Ha ! Ha ! Ha ! Ha ! Ha ! Ha ! Ha ! Ha ! Ha !",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh1", 2, "Non mais c'est une blague ? “L'incarnation du mal “ ?",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh1", 2, "Tout réside pour le bien de l'humanité ! Ils ont tout simplement mérité de ce", "qu'il devait subir !",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 1])
            self.cinematic_frame(screen, "tkh1", 2, "Bien sûr...On dirait que tu avais très soif de vengeance.",kind_info=[['SM', 'no_weapon'], ['TK', 'no_weapon'], 2])
            self.cinematic_frame(screen, "tkh1", 0, "(Takahiro faint, inconscient, a perdu la vie.)")
            self.cinematic_frame(screen, "tkh1", 1, "Huh. Il n'avait qu'à pas mourir celui-là.",kind_info=['SM','SM','no_weapon','right'])
            self.cinematic_frame(screen, "tkh1", 1, "Bon, j'ai enfin pu tuer cette bête..Que faire maintenant ?",kind_info=['SM','SM','no_weapon','right'])
            self.cinematic_frame(screen, "tkh1", 1, "D'ailleurs, est-ce que finalement tout cela a valu le coup..?",kind_info=['SM','SM','no_weapon','right'])
            self.cinematic_frame(screen, "tkh1", 1, "!!!", kind_info=['SM','SM','no_weapon','right'])
            self.cinematic_frame(screen, "tkh1", 1, "Musashi se retourne et voit la pile de cadavres qu'il a créée suite à son", "massacre.",kind_info=['SM','SM','no_weapon','right'])
            self.cinematic_frame(screen, "tkh1", 1, "Gh..! Hein..? ? ?",kind_info=['SM','SM','no_weapon','right'])
            self.cinematic_frame(screen, "tkh1", 1, "J'ai...tué...autant...de...personnes...? ? ?",kind_info=['SM','SM','no_weapon','right'])
            self.cinematic_frame(screen, "tkh1", 1, "Hein..? Hein..? HEIN..? ? ?",kind_info=['SM','SM','no_weapon','right'])
            self.cinematic_frame(screen, "tkh1", 1, "Moi ? Moi ? MOI !!??",kind_info=['SM','SM','no_weapon','right'])
            self.cinematic_frame(screen, "tkh1", 1, "NON..NON...NON ! ! !",kind_info=['SM','SM','no_weapon','right'])
            self.cinematic_frame(screen, "tkh1", 1, "POURQUOI ? POURQUOI AI-JE DONC FAIT CELA ? ? ?",kind_info=['SM','SM','no_weapon','right'])
            self.cinematic_frame(screen, "tkh1", 1, "GUAH..GRHHAH..RAHHHHH….",kind_info=['SM','SM','no_weapon','right'])
            self.cinematic_frame(screen, "tkh1", 1, "….J'ai un démon en moi...c'est de sa faute..",kind_info=['SM','SM','no_weapon','right'])
            self.cinematic_frame(screen, "tkh1", 1, "C'est de sa faute...C'est de sa faute ! !",kind_info=['SM','SM','no_weapon','right'])
            self.cinematic_frame(screen, "tkh1", 1, "C'EST DE SA FAUTE ! ! ",kind_info=['SM','SM','no_weapon','right'])
            self.cinematic_frame(screen, "tkh1", 0, "La légende raconte que Musashi a fui son propre village, et a décidé de", "partir vers un autre pays pour débuter une nouvelle vie.")
            self.cinematic_frame(screen, "tkh1", 0, "Des enquêtes ont été mises en place pour la recherche de ce samouraï, où tout", "le monde parle de sa disparition. ")
            self.cinematic_frame(screen, "tkh1", 0, "La honte, le désespoir, la culpabilité de ce jeune homme restera gravé chez", "lui pour le reste de sa vie, voire de l'éternité.")
            self.cinematic_frame(screen, "tkh1", 0, "FIN")
        self.ecran_noir(screen)


    def cinematic_21(self,screen,saved):
        if saved=='none':
            self.music.play(self.music.exploration)
            self.cinematic_frame(screen, "forest2", 1, "Le temps presse. Il faut que j'atteigne la ville d'Aizuwakamatsu au plus vite!",kind_info=['SM','SM','no_weapon','left'])
            self.cinematic_frame(screen, "forest2", 1, "Mon objectif reste le même: Venger mon village natal. Alors, allons-y!",kind_info=['SM','SM','no_weapon','left'])
            self.cinematic_frame(screen, "forest2", 1, "La sortie.. Je la vois !",kind_info=['SM','SM','no_weapon','left'])
            self.cinematic_frame(screen, "forest2", 1, "Aizuwakamatsu.. Me voilà !",kind_info=['SM','SM','no_weapon','left'])
            self.sound.arbre.play()
            self.cinematic_frame(screen, "forest2", 0, "SCHLAC! (Deux arbres ont été coupées pour bloquer le passage)")
            self.cinematic_frame(screen, "forest2", 1, "! ! !",kind_info=['SM','SM','no_weapon','left'])
            self.cinematic_frame(screen, "forest2", 1, "Qui a bloqué ce passage ?!",kind_info=['SM','SM','no_weapon','left'])
            self.cinematic_frame(screen, "forest2", 0, "(L'escouade de Takahiro apparaît)")
            self.music.play(self.music.theme_tkh1)
            self.cinematic_frame(screen, 'forest2', 3, "Shikisha Musashi du village de Magome.. ",kind_info=[['TW', 'no_weapon'], ['TW_H', 'no_weapon'],['SM', 'no_weapon'],  1])
            self.cinematic_frame(screen, 'forest2', 3, "Vous avez osé chercher la tête de notre dirigeant..",kind_info=[['TW', 'no_weapon'], ['TW_H', 'no_weapon'],['SM', 'no_weapon'],  2])
            self.cinematic_frame(screen, 'forest2', 3, "L'heure est donc venue pour vous d'être puni pour vos crimes.",kind_info=[['TW', 'no_weapon'], ['TW_H', 'no_weapon'],['SM', 'no_weapon'], 1])
            self.cinematic_frame(screen, 'forest2', 3, "Puisque nous sommes l'escouade du clan Takahiro ! !",kind_info=[ ['TW', 'no_weapon'], ['TW_H', 'no_weapon'],['SM', 'no_weapon'], 1])
            self.cinematic_frame(screen, 'forest2', 3, "...",kind_info=[['TW', 'no_weapon'], ['TW_H', 'no_weapon'],['SM', 'no_weapon'], 3])
            self.cinematic_frame(screen, 'forest2', 3, "...",kind_info=[['TW', 'no_weapon'], ['TW_H', 'no_weapon'],['SM', 'no_weapon'], 1])
            self.cinematic_frame(screen, 'forest2', 3, "...",kind_info=[['TW', 'no_weapon'], ['TW_H', 'no_weapon'],['SM', 'no_weapon'],  2])
            self.cinematic_frame(screen, 'forest2', 3, "Vas-tu réagir, insolent ?",kind_info=[['TW', 'no_weapon'], ['TW_H', 'no_weapon'],['SM', 'no_weapon'],  1])
            self.cinematic_frame(screen, 'forest2', 3, "Eh ? C'est vous avec vos poses de fanfare ! Vous ne faîtes que d'embarrasser", "votre clan.",kind_info=[ ['TW', 'no_weapon'], ['TW_H', 'no_weapon'],['SM', 'no_weapon'], 3])
            self.cinematic_frame(screen, 'forest2', 3, "Embarrasser ? Hors de question ! La pose de la victoire est un atout", "extrêmement important pour un guerrier !",kind_info=[['TW', 'no_weapon'], ['TW_H', 'no_weapon'],['SM', 'no_weapon'], 2])
            self.cinematic_frame(screen, 'forest2', 3, "Evidemment mon cher ! Tout le monde le fait. Pourquoi ce ne serait pas le", "cas ?",kind_info=[['TW', 'no_weapon'], ['TW_H', 'no_weapon'],['SM', 'no_weapon'], 1])
            self.cinematic_frame(screen, 'forest2', 3, "A ce que je sache, les samouraïs ne font pas des poses de la victoire à la", "fin de leurs combats..",kind_info=[['TW', 'no_weapon'], ['TW_H', 'no_weapon'],['SM', 'no_weapon'], 3])
            self.cinematic_frame(screen, 'forest2', 3, "(Quel bande d'idiots ces deux-là..)",kind_info=[['TW', 'no_weapon'], ['TW_H', 'no_weapon'],['SM', 'no_weapon'], 3])
            self.cinematic_frame(screen, 'forest2', 3, "(Bref, revenons à nos moutons. Si ces personnes tentent de m'assassiner..)",kind_info=[['TW', 'no_weapon'], ['TW_H', 'no_weapon'],['SM', 'no_weapon'], 3])
            self.cinematic_frame(screen, 'forest2', 3, "(Il faut que je fasse le meilleur choix possible.)",kind_info=[['TW', 'no_weapon'], ['TW_H', 'no_weapon'],['SM', 'no_weapon'], 3])
            self.cinematic_frame(screen, 'forest2', 3, "(Dois-je plutôt fuir ? Ou peut-être les combattre ? Ou même encore se servir","de l'environnement, et donc du milieu alentour à mon avantage ? Que faire ?",kind_info=[['TW', 'no_weapon'], ['TW_H', 'no_weapon'],['SM', 'no_weapon'], 3])
            output1, output2 = self.choice_frame(screen, "forest2", [0, 3], ["FUIR", "COMBATTRE", "UTILISER MILIEU"])
        elif saved =='KM':
            self.music.play(self.music.exploration)
            self.cinematic_frame(screen, "forest2", 2, "Le temps presse. Il faut que j'atteigne la ville d'Aizuwakamatsu au plus vite!",kind_info=[['SM','no_weapon'],['KM','no_weapon'],1])
            self.cinematic_frame(screen, "forest2", 2, "Mon objectif reste le même : Venger mon village natal. Alors, allons-y!",kind_info=[['SM','no_weapon'],['KM','no_weapon'],1])
            self.cinematic_frame(screen, "forest2", 2, "Attends-moi grand-frère !",kind_info=[['SM','no_weapon'],['KM','no_weapon'],2])
            self.cinematic_frame(screen, "forest2", 2, "La sortie.. Je la vois !",kind_info=[['SM','no_weapon'],['KM','no_weapon'],1])
            self.cinematic_frame(screen, "forest2", 2, "Enfin ! Nous sommes enfin arrivés !",kind_info=[['SM','no_weapon'],['KM','no_weapon'],2])
            self.cinematic_frame(screen, "forest2", 2, "Aizuwakamatsu.. Me voilà !",kind_info=[['SM','no_weapon'],['KM','no_weapon'],1])
            self.sound.arbre.play()
            self.cinematic_frame(screen, "forest2", 0, "SCHLAC! (Deux arbres ont été coupées pour bloquer le passage)")
            self.cinematic_frame(screen, "forest2", 2, "! ! !",kind_info=[['SM','no_weapon'],['KM','no_weapon'],1])
            self.cinematic_frame(screen, "forest2", 2, "! ! !",kind_info=[['SM','no_weapon'],['KM','no_weapon'],2])
            self.cinematic_frame(screen, "forest2", 2, "Qui a bloqué ce passage ?!",kind_info=[['SM','no_weapon'],['KM','no_weapon'],1])
            self.cinematic_frame(screen, "forest2", 0, "(L'escouade de Takahiro apparaît)")
            self.music.play(self.music.theme_tkh1)
            self.cinematic_frame(screen, 'forest2', 3, "Shikisha Musashi du village de Magome.. ",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'],['TW', 'no_weapon'], 3])
            self.cinematic_frame(screen, 'forest2', 3, "Vous avez osé chercher la tête de notre dirigeant..",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'],['TW_H', 'no_weapon'], 3])
            self.cinematic_frame(screen, 'forest2', 3, "L'heure est donc venue pour vous d'être puni pour vos crimes.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'],['TW', 'no_weapon'], 3])
            self.cinematic_frame(screen, 'forest2', 3, "Puisque nous sommes l'escouade du clan Takahiro ! !",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'],['TW_H', 'no_weapon'], 3])
            self.cinematic_frame(screen, 'forest2', 3, "...",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'],['TW', 'no_weapon'], 1])
            self.cinematic_frame(screen, 'forest2', 3, "...",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'],['TW', 'no_weapon'], 2])
            self.cinematic_frame(screen, 'forest2', 3, "...",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'],['TW', 'no_weapon'], 3])
            self.cinematic_frame(screen, 'forest2', 3, "...",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'],['TW_H', 'no_weapon'], 3])
            self.cinematic_frame(screen, 'forest2', 3, "Allez-vous réagir, bande d'insolents?",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'],['TW', 'no_weapon'], 3])
            self.cinematic_frame(screen, 'forest2', 3, "Eh ? C'est vous avec vos poses de fanfare ! Vous ne faîtes que d'embarrasser", "votre clan.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'],['TW', 'no_weapon'], 1])
            self.cinematic_frame(screen, 'forest2', 3, "Je suis d'accord avec Shikisha. C'est tout simplement embarrassant.",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'],['TW', 'no_weapon'], 2])
            self.cinematic_frame(screen, 'forest2', 3, "Embarrasser ? Hors de question ! La pose de la victoire est un atout", "extrêmement important pour un guerrier !",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'],['TW_H', 'no_weapon'], 3])
            self.cinematic_frame(screen, 'forest2', 3, "Evidemment mon cher ! Tout le monde le fait. Pourquoi ce ne serait pas le", "cas ?",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'],['TW', 'no_weapon'], 3])
            self.cinematic_frame(screen, 'forest2', 3, "A ce que je sache, les samouraïs ne font pas des poses de la victoire à la", "fin de leurs combats..",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'],['TW', 'no_weapon'], 1])
            self.cinematic_frame(screen, 'forest2', 3, "(Quel bande d'idiots ces deux-là..)",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'],['TW', 'no_weapon'], 1])
            self.cinematic_frame(screen, 'forest2', 3, "Shikisha, il faut qu'on se sorte d'ici. Je ne pense pas qu'on devrait les", "affronter..",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'],['TW', 'no_weapon'], 2])
            self.cinematic_frame(screen, 'forest2', 3, "(C'est vrai. Cependant, il faut que je considère mes options..)",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'],['TW', 'no_weapon'], 1])
            self.cinematic_frame(screen, 'forest2', 3, "(et il faut que je fasse le meilleur choix possible.)",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'],['TW', 'no_weapon'], 1])
            self.cinematic_frame(screen, 'forest2', 3, "(Dois-je plutôt fuir? Ou peut-être les combattre ? Ou même encore se servir de", "l'environnement, et donc du milieu alentour à mon avantage ? Que faire ?",kind_info=[['SM', 'no_weapon'], ['KM', 'no_weapon'],['TW', 'no_weapon'], 1])
            output1, output2 = self.choice_frame(screen, "forest2", [0, 3], ["FUIR", "COMBATTRE", "UTILISER MILIEU"])
        elif saved =='KT':
            self.music.play(self.music.exploration)
            self.cinematic_frame(screen, "forest2", 2, "Le temps presse. Il faut que j'atteigne la ville d'Aizuwakamatsu au plus vite!",kind_info=[['SM','no_weapon'],['KT','no_weapon'],1])
            self.cinematic_frame(screen, "forest2", 2, "Oui. Nous devons y aller sans plus tarder. Allons-y !",kind_info=[['SM','no_weapon'],['KT','no_weapon'],2])
            self.cinematic_frame(screen, "forest2", 2, "La sortie.. Je la vois !",kind_info=[['SM','no_weapon'],['KT','no_weapon'],1])
            self.cinematic_frame(screen, "forest2", 2, "Nous sommes enfin arrivés à notre destination..",kind_info=[['SM','no_weapon'],['KT','no_weapon'],2])
            self.cinematic_frame(screen, "forest2", 2, "Aizuwakamatsu.. Nous voilà !",kind_info=[['SM','no_weapon'],['KT','no_weapon'],1])
            self.sound.arbre.play()
            self.cinematic_frame(screen, "forest2", 0, "SCHLAC! (Deux arbres ont été coupées pour bloquer le passage)")
            self.cinematic_frame(screen, "forest2", 2, "! ! !",kind_info=[['SM','no_weapon'],['KT','no_weapon'],1])
            self.cinematic_frame(screen, "forest2", 2, "! ! !",kind_info=[['SM','no_weapon'],['KT','no_weapon'],2])
            self.cinematic_frame(screen, "forest2", 2, "Qui a bloqué ce passage ?!",kind_info=[['SM','no_weapon'],['KT','no_weapon'],1])
            self.cinematic_frame(screen, "forest2", 0, "(L'escouade de Takahiro apparaît)")
            self.music.play(self.music.theme_tkh1)
            self.cinematic_frame(screen, 'forest2', 3, "Shikisha Musashi du village de Magome.. ",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'],['TW', 'no_weapon'], 3])
            self.cinematic_frame(screen, 'forest2', 3, "Vous avez osé chercher la tête de notre dirigeant..",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'],['TW_H', 'no_weapon'], 3])
            self.cinematic_frame(screen, 'forest2', 3, "L'heure est donc venue pour vous d'être puni pour vos crimes.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'],['TW', 'no_weapon'], 3])
            self.cinematic_frame(screen, 'forest2', 3, "Puisque nous sommes l'escouade du clan Takahiro ! !",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'],['TW_H', 'no_weapon'], 3])
            self.cinematic_frame(screen, 'forest2', 3, "...",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'],['TW', 'no_weapon'], 1])
            self.cinematic_frame(screen, 'forest2', 3, "...",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'],['TW', 'no_weapon'], 2])
            self.cinematic_frame(screen, 'forest2', 3, "...",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'],['TW', 'no_weapon'], 3])
            self.cinematic_frame(screen, 'forest2', 3, "...",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'],['TW_H', 'no_weapon'], 3])
            self.cinematic_frame(screen, 'forest2', 3, "Allez-vous réagir, bande d'insolents?",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'],['TW', 'no_weapon'], 3])
            self.cinematic_frame(screen, 'forest2', 3, "Eh ? C'est vous avec vos poses de fanfare ! Vous ne faîtes que d'embarrasser", "votre clan.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'],['TW', 'no_weapon'], 1])
            self.cinematic_frame(screen, 'forest2', 3, "Je suis du même avis. Vous devez avoir honte. ",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'],['TW', 'no_weapon'], 2])
            self.cinematic_frame(screen, 'forest2', 3, "Embarrasser ? Hors de question ! La pose de la victoire est un atout", "extrêmement important pour un guerrier !",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'],['TW_H', 'no_weapon'], 3])
            self.cinematic_frame(screen, 'forest2', 3, "Evidemment mon cher ! Tout le monde le fait. Pourquoi ce ne serait pas le", "cas ?",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'],['TW', 'no_weapon'], 3])
            self.cinematic_frame(screen, 'forest2', 3, "A ce que je sache, les samouraïs ne font pas des poses de la victoire à la", "fin de leurs combats..",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'],['TW', 'no_weapon'], 1])
            self.cinematic_frame(screen, 'forest2', 3, "(Quel bande d'idiots ces deux-là..)",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'],['TW', 'no_weapon'], 1])
            self.cinematic_frame(screen, 'forest2', 3, "C'est un 2v2... À forces égales, je pense qu'on peut les battre.",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'],['TW', 'no_weapon'], 2])
            self.cinematic_frame(screen, 'forest2', 3, "Qu'en penses-tu Musashi ?",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'],['TW', 'no_weapon'], 2])
            self.cinematic_frame(screen, 'forest2', 3, "(C'est vrai, nous sommes des samouraïs. Cependant, il faut que je considère", "mes options..)",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'],['TW', 'no_weapon'], 1])
            self.cinematic_frame(screen, 'forest2', 3, "(et il faut que je fasse le meilleur choix possible.)",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'],['TW', 'no_weapon'], 1])
            self.cinematic_frame(screen, 'forest2', 3, "(Dois-je plutôt fuir? Ou peut-être les combattre ? Ou même encore se servir de", "l'environnement, et donc du milieu alentour à mon avantage ? Que faire ?",kind_info=[['SM', 'no_weapon'], ['KT', 'no_weapon'],['TW', 'no_weapon'], 1])
            output1, output2 = self.choice_frame(screen, "forest2", [0, 3], ["FUIR", "COMBATTRE", "UTILISER MILIEU"])

    def cinematic_22(self,screen,saved):
        self.music.play(self.music.theme_tkh1)
        if saved == 'none':
            self.cinematic_frame(screen, 'forest2', 3, "(Très bien, je sais ce que je dois faire.)",kind_info=[['TW', 'no_weapon'], ['TW_H', 'no_weapon'],['SM', 'no_weapon'], 3])
            self.cinematic_frame(screen, 'forest2', 3, "J'aimerais bien vous affronter.. À condition que vous voyez ce qui se trouve", "derrière vous.",kind_info=[['TW', 'no_weapon'], ['TW_H', 'no_weapon'],['SM', 'no_weapon'], 3])
            self.cinematic_frame(screen, 'forest2', 3, "Hein ?",kind_info=[['TW', 'no_weapon'], ['TW_H', 'no_weapon'],['SM', 'no_weapon'], 1])
            self.cinematic_frame(screen, 'forest2', 3, "Quoi ?",kind_info=[['TW', 'no_weapon'], ['TW_H', 'no_weapon'],['SM', 'no_weapon'], 2])
            self.cinematic_frame(screen,'forest2',0,"Les deux soldats du clan Takahiro se retournent stupidement")
            self.cinematic_frame(screen, 'forest2', 3, "(Ma chance!)",kind_info=[['TW', 'no_weapon'], ['TW_H', 'no_weapon'],['SM', 'no_weapon'], 3])
            self.cinematic_frame(screen, 'forest2', 3, "Une autre fois peut-être ! On se reverra plus tard !",kind_info=[['TW', 'no_weapon'], ['TW_H', 'no_weapon'],['SM', 'no_weapon'], 3])
            self.cinematic_frame(screen, 'forest2', 3, "Comment ?",kind_info=[['TW', 'no_weapon'], ['TW_H', 'no_weapon'],['SM', 'no_weapon'], 1])
            self.cinematic_frame(screen, 'forest2', 3, "Il nous a bien eu !",kind_info=[['TW', 'no_weapon'], ['TW_H', 'no_weapon'],['SM', 'no_weapon'], 2])
            self.cinematic_frame(screen,'forest2',0,"(Musashi tente de s'enfuir avec le plus de force possible)")
            self.ecran_noir(screen)
            self.sound.H_essoufle.play()
            self.cinematic_frame(screen, "bamboo4", 1, "*sigh*, *sigh*, *sigh*",kind_info=['SM','SM','no_weapon','left'])
            self.cinematic_frame(screen, "bamboo4", 1, "Phew.. Heureusement qu'ils sont tombés dans ma ruse, c'était moins d'une.",kind_info=['SM','SM','no_weapon','left'])
            self.cinematic_frame(screen, "bamboo4", 1, "Trouvons maintenant un autre chemin pour aller dans la ville sans se faire", "repérer.",kind_info=['SM','SM','no_weapon','left'])
        elif saved == 'KM':
            self.cinematic_frame(screen,'forest2',3,"(Très bien, je sais ce que je dois faire.)",kind_info=[['SM','no_weapon'],['KM','no_weapon'],['TW','no_weapon'],1])
            self.cinematic_frame(screen,'forest2',3,"J'aimerais bien vous affronter.. À condition que vous voyez ce qui se trouve", "derrière vous.",kind_info=[['SM','no_weapon'],['KM','no_weapon'],['TW','no_weapon'],1])
            self.cinematic_frame(screen,'forest2',3,"Hein ?",kind_info=[['SM','no_weapon'],['KM','no_weapon'],['TW','no_weapon'],3])
            self.cinematic_frame(screen,'forest2',3,"Quoi ?",kind_info=[['SM','no_weapon'],['KM','no_weapon'],['TW_H','no_weapon'],3])
            self.cinematic_frame(screen,'forest2',0,"Les deux soldats du clan Takahiro se retournent stupidement")
            self.cinematic_frame(screen,'forest2',3,"(Maintenant !)",kind_info=[['SM','no_weapon'],['KM','no_weapon'],['TW','no_weapon'],1])
            self.cinematic_frame(screen,'forest2',3,"Fuyons Keiko ! Une autre fois peut-être ! On se reverra plus tard !",kind_info=[['SM','no_weapon'],['KM','no_weapon'],['TW','no_weapon'],1])
            self.cinematic_frame(screen,'forest2',3,"Allez, on y va !",kind_info=[['SM','no_weapon'],['KM','no_weapon'],['TW','no_weapon'],2])
            self.cinematic_frame(screen,'forest2',3,"Comment ?",kind_info=[['SM','no_weapon'],['KM','no_weapon'],['TW','no_weapon'],3])
            self.cinematic_frame(screen,'forest2',3,"Il nous a bien eu !",kind_info=[['SM','no_weapon'],['KM','no_weapon'],['TW_H','no_weapon'],3])
            self.cinematic_frame(screen,'forest2',0,"(Musashi et Keiko tentent de s'enfuir avec le plus de force possible)")
            self.ecran_noir(screen)
            self.sound.H_essoufle.play()
            self.cinematic_frame(screen,'bamboo4',2,"*sigh*, *sigh*, *sigh*",kind_info=[['SM','no_weapon'],['KM','no_weapon'],1])
            self.sound.F_essoufle.play()
            self.cinematic_frame(screen,'bamboo4',2,"*sigh*, *sigh*, *sigh*",kind_info=[['SM','no_weapon'],['KM','no_weapon'],2])
            self.cinematic_frame(screen,'bamboo4',2,"Phew.. Heureusement qu'ils sont tombés dans ma ruse, c'était moins d'une.",kind_info=[['SM','no_weapon'],['KM','no_weapon'],1])
            self.cinematic_frame(screen,'bamboo4',2,"Oui. C'était moins d'une.",kind_info=[['SM','no_weapon'],['KM','no_weapon'],2])
            self.cinematic_frame(screen,'bamboo4',2,"Trouvons maintenant un autre chemin pour aller dans la ville sans se faire", "repérer.",kind_info=[['SM','no_weapon'],['KM','no_weapon'],1])
            self.cinematic_frame(screen,'bamboo4',2,"Dans ce cas, je sais où aller. Suis-moi grand frère !",kind_info=[['SM','no_weapon'],['KM','no_weapon'],2])
            self.cinematic_frame(screen,'bamboo4',2,"Je te suis !",kind_info=[['SM','no_weapon'],['KM','no_weapon'],1])
        elif saved == 'KT':
            self.cinematic_frame(screen,'forest2',3,"(Très bien, je sais ce que je dois faire.)",kind_info=[['SM','no_weapon'],['KT','no_weapon'],['TW','no_weapon'],1])
            self.cinematic_frame(screen,'forest2',3,"Même si on peut les battre Takeshi..Je pense qu'on devrait fuir.",kind_info=[['SM','no_weapon'],['KT','no_weapon'],['TW','no_weapon'],1])
            self.cinematic_frame(screen,'forest2',3,"Pardon ? Pourquoi fuir ? Nous sommes des samouraïs !",kind_info=[['SM','no_weapon'],['KT','no_weapon'],['TW','no_weapon'],2])
            self.cinematic_frame(screen,'forest2',3,"Nous ne sommes pas des lâches à ce que je sache..",kind_info=[['SM','no_weapon'],['KT','no_weapon'],['TW','no_weapon'],2])
            self.cinematic_frame(screen,'forest2',3,"Je le sais. Mais ne dépensons pas toute notre énergie contre cette escouade.",kind_info=[['SM','no_weapon'],['KT','no_weapon'],['TW','no_weapon'],1])
            self.cinematic_frame(screen,'forest2',3,"Il peut y avoir un ennemi beaucoup plus fort qu'on pourrait rencontrer", "bien plus tard.",kind_info=[['SM','no_weapon'],['KT','no_weapon'],['TW','no_weapon'],1])
            self.cinematic_frame(screen,'forest2',3,"..Dans ce cas là, je suis désolé de te le dire Musashi..",kind_info=[['SM','no_weapon'],['KT','no_weapon'],['TW','no_weapon'],2])
            self.cinematic_frame(screen,'forest2',3,"Mais je vais les affronter seul si tu ne souhaites pas venir m'aider dans ce", "combat.",kind_info=[['SM','no_weapon'],['KT','no_weapon'],['TW','no_weapon'],2])
            self.cinematic_frame(screen,'forest2',3,"! ! !",kind_info=[['SM','no_weapon'],['KT','no_weapon'],['TW','no_weapon'],1])
            self.cinematic_frame(screen,'forest2',3,"Mais pourtant Takeshi..Je pensais qu'on allait faire ce voyage ensemble..",kind_info=[['SM','no_weapon'],['KT','no_weapon'],['TW','no_weapon'],1])
            self.cinematic_frame(screen,'forest2',3,"Je le pensais aussi..Mais on dirait que nos chemins se séparent.",kind_info=[['SM','no_weapon'],['KT','no_weapon'],['TW','no_weapon'],2])
            self.cinematic_frame(screen,'forest2',3,"..Si jamais tu ressort de ce combat vivant, retrouvons nous à Aizuwakamatsu.",kind_info=[['SM','no_weapon'],['KT','no_weapon'],['TW','no_weapon'],1])
            self.cinematic_frame(screen,'forest2',3,"Si tu le souhaites, alors pourquoi pas.",kind_info=[['SM','no_weapon'],['KT','no_weapon'],['TW','no_weapon'],2])
            self.cinematic_frame(screen,'forest2',3,"Bonne chance Takeshi, ne meurs pas.",kind_info=[['SM','no_weapon'],['KT','no_weapon'],['TW','no_weapon'],1])
            self.cinematic_frame(screen,'forest2',3,"(Désolé Takeshi, mais c'est le choix le plus raisonnable que je puisse faire..","Je ne souhaite pas avoir recours à la violence.)",kind_info=[['SM','no_weapon'],['KT','no_weapon'],['TW','no_weapon'],1])
            self.ecran_noir(screen)
            self.cinematic_frame(screen,'forest2',3,"Sur ce, mettons nous au travail.",kind_info=[['TW_H','no_weapon'],['TW','no_weapon'],['KT','no_weapon'],3])
            self.cinematic_frame(screen,'forest2',3,"Ne meurs pas vite.",kind_info=[['TW_H','no_weapon'],['TW','no_weapon'],['KT','no_weapon'],2])
            self.cinematic_frame(screen,'forest2',3,"J'espère que tu ne fuiras pas à la fin du combat comme ton camarade.",kind_info=[['TW_H','no_weapon'],['TW','no_weapon'],['KT','no_weapon'],1])
            self.cinematic_frame(screen,'forest2',3,"Ne nous sous-estime pas si tu penses pouvoir gagner facilement ce combat.",kind_info=[['TW_H','no_weapon'],['TW','no_weapon'],['KT','no_weapon'],2])






if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    pygame.display.set_caption("Kage no Michi - Cinématiques")
    c = Cinematics()
    output = c.cinematic_15(screen, "KM", True, True)
    print(output)
    pygame.quit()
