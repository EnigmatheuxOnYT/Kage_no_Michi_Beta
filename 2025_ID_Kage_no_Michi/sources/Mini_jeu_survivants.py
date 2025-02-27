#Projet : Kage no Michi
#Auteurs : Alptan Korkmaz, Maxime Rousseaux, Ahmed-Adam Rezkallah, Clément Roux--Bénabou, Cyril Zhao


# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 17:38:15 2025

@author: clementroux--benabou
"""

import pygame
import random
from Cinematics import Cinematics
from Characters_sprites import Characters_sprites
from Audio import Music,Sound

class minigm_survivors :
    
    def __init__ (self):
        self.sprites = Characters_sprites().for_cinematics
        self.villagers_sprites = Characters_sprites().for_mgm
        self.cin = Cinematics()
        self.music,self.sound = Music(),Sound()
        self.mouse_on_button = {'Reconstruction': False, 'Ravitaillement': False, 'Défense': False}
        self.menu_save_delete_file_bg = pygame.image.load("../data/assets/menu/Interface_Suppression_Sauvegarde_V1.png")
        self.rect_save_delete_file = pygame.Rect(640,110,400,300)
        self.rect_villager = pygame.Rect(400,110,238,593)
        self.button_green_bg = pygame.image.load("../data/assets/buttons/Fond_Bouton_VERT_330p.png")
        self.button_dgreen_bg = pygame.image.load("../data/assets/buttons/Fond_Bouton_VERTF_330p.png")
        self.rects_buttons = [pygame.Rect((72.5+(402.5*n)),550,330,120) for n in range (3)]
        self.rects_buttons_pushed = [pygame.Rect((74+(402.5*n)),551.5,330,120) for n in range (3)]
        self.font_MFMG35 = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf",35)
        self.font_MFMG20 = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf",20)
        self.text_button_rb = self.font_MFMG35.render("Reconstruction",False,(0,0,0))
        self.text_button_rv = self.font_MFMG35.render("Ravitaillement",False,(0,0,0))
        self.text_button_df = self.font_MFMG35.render("Défense",False,(0,0,0))
        self.rect_text_rb = pygame.Rect(115,590,200,50)
        self.rect_text_rv = pygame.Rect(522,590,200,50)
        self.rect_text_df = pygame.Rect(984,590,200,50)
        self.text_name = self.font_MFMG20.render("Nom :",False,(0,0,0))
        self.text_age = self.font_MFMG20.render("Âge :",False,(0,0,0))
        self.text_job = self.font_MFMG20.render("Métier :",False,(0,0,0))
        self.text_infos = self.font_MFMG20.render("Infos :",False,(0,0,0))
        self.rect_text_name = pygame.Rect(680,140,100,50)
        self.rect_text_age = pygame.Rect(680,190,100,50)
        self.rect_text_job = pygame.Rect(680,240,100,50)
        self.rect_text_infos = pygame.Rect(680,290,100,50)
        self.rect_name = pygame.Rect(680,165,100,50)
        self.rect_age = pygame.Rect(680,215,100,50)
        self.rect_job = pygame.Rect(680,265,100,50)
        self.rect_infos1 = pygame.Rect(680,315,100,50)
        self.rect_infos2 = pygame.Rect(680,340,100,50)
        self.rect_infos3 = pygame.Rect(680,365,100,50)
        self.villagers = {"villager1": {'correct':"Reconstruction",'name':'Taro','age':"32 ans","job":"Artisan","infos":["Son atelier n'a pas été détruit.","Il construit des structures","en bois et bambou."]},
                          "villager2": {'correct':"Ravitaillement",'name':'Hana','age':"25 ans","job":"Experte des eaux","infos":["Sait si une eau est potable.","Connaît les sources d'eau","cachées près du village."]},
                          "villager3": {'correct':"Défense",'name':'Yuki','age':"19 ans","job":"Combattante","infos":["Fait du karaté depuis 8 ans.","Sait se servir d'armes","blanches."]},
                          "villager4": {'correct':"Ravitaillement",'name':"Daisuke",'age':"59 ans","job":"Mushoku (sans profession)","infos":["Aime bien se promener en forêt","pour ramasser des fruits.","Connaît les plantes comestibles."]},
                          "villager5": {'correct':"Reconstruction",'name':"Yukina",'age':"42 ans","job":"Boulangère","infos":["Aime la géométrie.","Expérimente avec des pâtisseries","en mosaïque."]},
                          "villager6": {'correct':"Ravitaillement",'name':"Sora",'age':"14 ans","job":"Étudiante","infos":["Étudie dans un village voisin.","Fait la route quotidiennement.",""]},
                          "villager7": {'correct':"Défense",'name':"Shizuka",'age':"23 ans","job":"Potier","infos":["Jette ses pots cassés","avec précision.",""]},
                          "villager8": {'correct':"Défense",'name':"Kata",'age':"37 ans","job":"Pécheur","infos":["A survécu à nombre de tempêtes.","Manie les bouts parfaitement.","Remonte une ancre à main nues."]},
                          "villager9": {'correct':"Reconstruction",'name':"Haiko",'age':"28","job":"Charbonnier","infos":["Est le seul à comprendre","comment ses fours fonctionnent.","Est un peu renfermé."]},
                          "villager10": {'correct':"Ravitaillement",'name':"Aki",'age':"34","job":"Poètesse","infos":["Aime écrire des haïkus","sur l'automne.","Dort beaucoup.","Ne gagne pas beaucoup."]},
                          "villager11": {'correct':"Défense",'name':"Shojiro",'age':"20","job":"Saltimbanque","infos":["Sait sauter très haut.","Sait jongler avec des torches.","Manie les rubans de gymnasique."]},
                          "villager12": {'correct':"Reconstruction",'name':"Bomboclat",'age':"46","job":"Mineuse","infos":["Exploite sa propre mine.","",""]}
                          }
        self.rect_villager = pygame.Rect(300,20,150,476)
    
    def list_creator(self):
        self.villager_list = [f'villager{i}' for i in range (1,13)]
        self.villager_list_output = []
        for i in range(3):
            used_list = self.villager_list[i*4:i*4+4]
            villagers = random.sample(used_list,3)
            for villager in villagers:
                self.villager_list_output.append(villager)
            
        
    ########## Partie 1 : évènements ##########
    def events (self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.event.post(event)
                return None
            pygame.event.post(event)
        
        
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_F11]:
            pygame.display.toggle_fullscreen()
            pygame.time.Clock().tick(5)
        
        
        if self.in_intro or self.in_end:
            self.intro_end_events()
        elif self.in_minigm:
            self.minigm_events()
        else:
            print("erreur d'état")
        pygame.event.clear()
    
    def intro_end_events (self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                ##### Son #####
                self.sound.play(self.sound.click)
                ##### Changement d'image ou affichage de toutes les lettres #####
                if self.current_last_letter == [len(self.line1),len(self.line2),len(self.line3)]:
                    self.frame += 1
                    self.next_frame = True
                elif not self.written:
                    self.current_last_letter = [len(self.line1),len(self.line2),len(self.line3)]
                    
        
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_F11]: 
            pygame.display.toggle_fullscreen()
            pygame.time.Clock().tick(5)
            
        elif pressed_keys[pygame.K_SPACE] or pressed_keys[pygame.K_RETURN] or pressed_keys[pygame.K_RIGHT]:
            ##### Passage à la prochaine image si toutes les lettres sont affichées et que le cooldonw est terminé #####
            if not self.keys_cooldown:
                if self.current_last_letter == [len(self.line1),len(self.line2),len(self.line3)]:
                    self.frame += 1
                    self.next_frame = True
                elif not self.written:
                    self.current_last_letter = [len(self.line1),len(self.line2),len(self.line3)]
                self.keys_cooldown = True
        elif self.keys_cooldown:
            self.keys_cooldown = False
    
    def minigm_events (self):
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                ##### Son #####
                self.sound.play(self.sound.click)
                ##### Détection du bouton appuyé #####
                pos = pygame.mouse.get_pos()
                if self.rects_buttons[0].collidepoint(pos):
                    self.change_villager("Reconstruction")
                    
                elif self.rects_buttons[1].collidepoint(pos):
                    self.change_villager("Ravitaillement")
                    
                elif self.rects_buttons[2].collidepoint(pos):
                    self.change_villager("Défense")
        
                    
    def change_villager(self,choice):
        if choice == self.villagers[self.villager_list_output[self.current_villager]]['correct']:
            self.correct_choices += 1
        if self.current_villager < 8:
            self.current_villager += 1
            if self.devmode:
                print("Bonne réponse :", self.villagers[self.villager_list_output[self.current_villager]]['correct'])
        else:
            self.go_end = True
    
    ########## Partie 2 : Mise à jour ##########
    def update (self):
        if self.in_intro or self.in_end:
            self.intro_end_update()
        elif self.in_minigm:
            self.minigm_update()
        else:
            print("erreur d'état")
    
    def intro_end_update (self):
        
        if self.written:
            
            if self.next_indicator_frame == 60:
                self.next_indicator_frame = 1
            else:
                self.next_indicator_frame += 1
        
        else:
            if self.current_last_letter[0] < len(self.line1):
                self.current_last_letter[0] += 1
            elif self.current_last_letter[1] < len(self.line2):
                self.current_last_letter[1] += 1
            elif self.current_last_letter[2] < len(self.line3):
                self.current_last_letter[2] += 1
            else:
                self.written = True
    
    def minigm_update (self):
        
        self.mouse_on_button['Reconstruction'] = self.rects_buttons[0].collidepoint(pygame.mouse.get_pos())
        self.mouse_on_button['Ravitaillement'] = self.rects_buttons[1].collidepoint(pygame.mouse.get_pos())
        self.mouse_on_button['Défense'] = self.rects_buttons[2].collidepoint(pygame.mouse.get_pos())
        
        if self.go_end:
            self.in_minigm = False
            self.in_end = True
            
    
    ########## Partie 3 : Affichage ##########
    
    ####################
    
    #line1 = ""
    #line2 = ""
    #line3 = ""
    
    ####################
    
    def draw (self, screen, choice):
        
        if self.next_frame:
            self.current_last_letter = [0,0,0]
            pygame.event.clear()
            self.written = False
            self.next_frame = False
        
        if self.in_intro :
            self.intro_draw(screen)
        elif self.in_minigm:
            self.minigm_draw(screen)
        elif self.in_end:
            self.end_draw(screen, choice)
        else:
            print("erreur d'état")
        
        pygame.display.flip()
    
    def intro_draw (self, screen):
        
        if self.frame == 1:
                        
            self.line1 = "Yoshirō confie à Musashi la tâche de réorganiser les villageois."
            self.line2 = "Les ressources sont rares,"
            self.line3 = "et chaque décision peut faire la différence entre la vie et la mort."
            
        
        elif self.frame == 2:
            
            self.line1 = "Répartissez les survivants en groupes pour maximiser vos chances :"
            self.line2 = "Il faut reconstruire, chercher de la nourriture et renforcer les défenses."
            self.line3 = "Choisissez judicieusement."
        
        elif self.frame > 2:
            self.list_creator()
            self.current_villager = 0
            self.frame = 1
            self.in_intro = False
            self.in_minigm = True
            print("Bonne réponse :", self.villagers[self.villager_list_output[self.current_villager]]['correct'])
            return None
        
        
        
        
        
        text_line1 = self.cin.font_MFMG30.render(self.line1[:self.current_last_letter[0]],False,(0,0,0))
        text_line2 = self.cin.font_MFMG30.render(self.line2[:self.current_last_letter[1]],False,(0,0,0))
        text_line3 = self.cin.font_MFMG30.render(self.line3[:self.current_last_letter[2]],False,(0,0,0))
        
        screen.blit(self.cin.cinematics_bgs["mgm6"], pygame.Rect(0,0,1280,720))
        screen.blit(self.sprites["SM"]['right']["no_weapon"]['secondary'],self.cin.rects_caracters['right'])
        screen.blit(self.sprites["Y?"]['left']["no_weapon"]['secondary'],self.cin.rects_caracters['left'])
        
        screen.blit(self.cin.text_bg,pygame.Rect(0,390,1280,330))
        screen.blit(self.cin.names["N"],self.cin.rect_names)
        screen.blit(text_line1,pygame.Rect(60,500,1180,50))
        screen.blit(text_line2,pygame.Rect(60,550,1180,50))
        screen.blit(text_line3,pygame.Rect(60,600,1180,50))
        
        if self.written:
            if self.next_indicator_frame > 30:
                screen.blit(self.cin.next_indicator[1],pygame.Rect(1200,640,50,50))
            else:
                screen.blit(self.cin.next_indicator[0],pygame.Rect(1200,640,50,50))
        
    def minigm_draw (self,screen):
        screen.blit(self.cin.cinematics_bgs["mgm7"], pygame.Rect(0,0,1280,720))
        screen.blit(self.menu_save_delete_file_bg,self.rect_save_delete_file)
        
        screen.blit(self.villagers_sprites[self.villager_list_output[self.current_villager]],self.rect_villager)
        
        if self.mouse_on_button['Reconstruction']:
            screen.blit(self.button_dgreen_bg,self.rects_buttons_pushed[0])
        else:
            screen.blit(self.button_green_bg,self.rects_buttons[0])
        if self.mouse_on_button['Ravitaillement']:
            screen.blit(self.button_dgreen_bg,self.rects_buttons_pushed[1])
        else:
            screen.blit(self.button_green_bg,self.rects_buttons[1])
        if self.mouse_on_button['Défense']:
            screen.blit(self.button_dgreen_bg,self.rects_buttons_pushed[2])
        else:
            screen.blit(self.button_green_bg,self.rects_buttons[2])
        
        screen.blit(self.text_button_rb,self.rect_text_rb)
        screen.blit(self.text_button_rv,self.rect_text_rv)
        screen.blit(self.text_button_df,self.rect_text_df)
        
        
        screen.blit(self.text_name,self.rect_text_name)
        screen.blit(self.font_MFMG20.render(self.villagers[self.villager_list_output[self.current_villager]]['name'],False,(0,0,0)),self.rect_name)
        screen.blit(self.text_age,self.rect_text_age)
        screen.blit(self.font_MFMG20.render(self.villagers[self.villager_list_output[self.current_villager]]['age'],False,(0,0,0)),self.rect_age)
        screen.blit(self.text_job,self.rect_text_job)
        screen.blit(self.font_MFMG20.render(self.villagers[self.villager_list_output[self.current_villager]]['job'],False,(0,0,0)),self.rect_job)
        screen.blit(self.text_infos,self.rect_text_infos)
        screen.blit(self.font_MFMG20.render(self.villagers[self.villager_list_output[self.current_villager]]['infos'][0],False,(0,0,0)),self.rect_infos1)
        screen.blit(self.font_MFMG20.render(self.villagers[self.villager_list_output[self.current_villager]]['infos'][1],False,(0,0,0)),self.rect_infos2)
        screen.blit(self.font_MFMG20.render(self.villagers[self.villager_list_output[self.current_villager]]['infos'][2],False,(0,0,0)),self.rect_infos3)

    
    def end_draw (self, screen, choice):
        
        screen.blit(self.cin.cinematics_bgs["mgm6"], pygame.Rect(0,0,1280,720))
        
        if self.correct_choices < 6:
            if self.frame in [0.5,1]:
                
                self.line1 = "Musashi, je crois que tu n'as pas encore l'esprit clair."
                self.line2 = "Il vaudrait mieux refaire la répartition, tu ne penses pas ?"
                self.line3 = "Réessaye, nous avons confiance en toi."
                
                screen.blit(self.sprites['Y?']['left']["no_weapon"]['main'],self.cin.rects_caracters['left'])
                char = 'Y?'
                m = "secondary"
            
            elif self.frame > 1:
                self.frame = 1
                self.list_creator()
                self.current_villager = 0
                self.correct_choices = 0
                self.go_end = False
                self.in_end = False
                self.in_minigm = True
                self.playing = True
                print("Mini-jeu relancé")
                print("Bonne réponse :", self.villagers[self.villager_list_output[self.current_villager]]['correct'])
                return None
            
            
        elif self.correct_choices >= 6:
            if self.frame == 1:
                
                self.line1 = "Après plusieurs heures d’efforts, le village commence à reprendre forme."
                self.line2 = "Les survivants, bien que blessés et épuisés,"
                self.line3 = "trouvent un semblant de réconfort dans l’organisation instaurée par Musashi."
    
                screen.blit(self.sprites[choice]['left']["no_weapon"]['secondary'],self.cin.rects_caracters['left'])
                char = 'N'
                m = "secondary"
                
            if choice == 'none':
                if self.frame == 2:
                    
                    self.line1 = "Shikisha marche seul dans les ruines, sous le regard des villageois."
                    self.line2 = "Ils l'observent, pleins de gratitude et de respect."
                    self.line3 = "Mais leur soutien ne parvient pas à combler le vide en lui."
                    
                    screen.blit(self.sprites["none"]['left']["no_weapon"]['secondary'],self.cin.rects_caracters['left'])
                    char = 'N'
                    m = "secondary"
                    
                elif self.frame == 3:
                    
                    self.line1 = "C’est trop tard... je les ai déjà perdus."
                    self.line2 = ""
                    self.line3 = ""
                    
                    screen.blit(self.sprites["none"]['left']["no_weapon"]['secondary'],self.cin.rects_caracters['left'])
                    char = 'SM'
                    m = "main"
                
            elif choice == 'KM':
                if self.frame == 2:
                    
                    self.line1 = "Tu vois ? Je savais que tu réussirais."
                    self.line2 = ""
                    self.line3 = ""
                    
                    screen.blit(self.sprites["KM"]['left']["no_weapon"]['main'],self.cin.rects_caracters['left'])
                    char = 'KM'
                    m = "secondary"
                
                elif self.frame == 3:
                    
                    self.line1 = "Je n’ai pas encore réussi, Keiko."
                    self.line2 = "Mais je te promets que je ferai tout pour que ça tienne."
                    self.line3 = ""
                    
                    screen.blit(self.sprites["KM"]['left']["no_weapon"]['secondary'],self.cin.rects_caracters['left'])
                    char = 'SM'
                    m = "main"
                
                
            elif choice == "KT":
                if self.frame == 2:
                    
                    self.line1 = "Tu t’en sors mieux que personne, comme toujours."
                    self.line2 = ""
                    self.line3 = ""
                    
                    screen.blit(self.sprites["KT"]['left']["no_weapon"]['main'],self.cin.rects_caracters['left'])
                    char = 'KT'
                    m = "secondary"
                
                elif self.frame == 3:
                    
                    self.line1 = "C’est toi qui dis ça, alors que tu m’as épaulé à chaque étape ?"
                    self.line2 = "Merci, Takeshi."
                    self.line3 = ""
                    
                    screen.blit(self.sprites["KT"]['left']["no_weapon"]['secondary'],self.cin.rects_caracters['left'])
                    char = 'SM'
                    m = "main"
            
            
        if self.correct_choices == 9:
            if self.frame == 4:
                
                self.line1 = "Yoshirō, le doyen du village, revient vers Shikisha."
                self.line2 = ""
                self.line3 = ""
                 
                screen.blit(self.sprites["Y?"]['left']["no_weapon"]['secondary'],self.cin.rects_caracters['left'])
                char = "Y?"
                m = "secondary"
            
            elif self.frame == 5:
                
                self.line1 = "Musashi, nous tenons à te remercier pour tout ce que tu as fait pour nous."
                self.line2 = "Les villageois se sont cotisés pout te donner cette récompense :"
                self.line3 = "Tiens, voici 20 pièces pour toi."
                 
                screen.blit(self.sprites["Y?"]['left']["no_weapon"]['main'],self.cin.rects_caracters['left'])
                char = "Y?"
                m = "secondary"
                
            elif self.frame > 5:
                self.frame = 0
                self.in_end =  False
                self.playing = False
                return None
        
        elif self.frame > 3:
            self.frame = 0
            self.in_end = False
            self.playing = False
            return None
        
        
        text_line1 = self.cin.font_MFMG30.render(self.line1[:self.current_last_letter[0]],False,(0,0,0))
        text_line2 = self.cin.font_MFMG30.render(self.line2[:self.current_last_letter[1]],False,(0,0,0))
        text_line3 = self.cin.font_MFMG30.render(self.line3[:self.current_last_letter[2]],False,(0,0,0))
        
        
        screen.blit(self.sprites["SM"]['right']["no_weapon"][m],self.cin.rects_caracters['right'])
        
        screen.blit(self.cin.text_bg,pygame.Rect(0,390,1280,330))
        screen.blit(self.cin.names[char],self.cin.rect_names)
        screen.blit(text_line1,pygame.Rect(60,500,1180,50))
        screen.blit(text_line2,pygame.Rect(60,550,1180,50))
        screen.blit(text_line3,pygame.Rect(60,600,1180,50))
        
        if self.written:
            if self.next_indicator_frame > 30:
                screen.blit(self.cin.next_indicator[1],pygame.Rect(1200,640,50,50))
            else:
                screen.blit(self.cin.next_indicator[0],pygame.Rect(1200,640,50,50))
        
    
    ########## Démarrage du mini-jeu ##########
    def load (self):
        self.running = True
        self.playing = True
        self.in_intro = True
        self.in_minigm = False
        self.go_end = False
        self.in_end = False
        self.frame = 1
        self.keys_cooldown = True
        self.next_frame = False
        self.next_indicator_frame = 0
        self.correct_choices = 0
        self.current_villager = 0
        self.current_last_letter = [0,0,0]
        self.written = False
        self.line1 = "Yoshirō confie à Musashi la tâche de réorganiser les villageois."
        self.line2 = "Les ressources sont rares,"
        self.line3 = "et chaque décision peut faire la différence entre la vie et la mort."
        
    ########## Boucle mini-jeu ##########
    def run (self, screen, choice,devmode=False):
        self.devmode = devmode
        self.load()
        while self.playing and self.running:
            self.events()
            self.update()
            self.draw(screen, choice)
            pygame.time.Clock().tick(60)
        
        return self.running


if __name__ == '__main__':
    pygame.init()
    
    icon = pygame.image.load("../data/assets/common/Icone_LOGO_V12.ico")
    pygame.display.set_icon(icon)
    cursor = pygame.image.load("../data/assets/common/Souris_V4.png")
    pygame.mouse.set_cursor((5,5),cursor)
    screen = pygame.display.set_mode((1280,720))
    pygame.display.set_caption("Kage no michi - Mini-jeu de répartition des survivants")
    
    minigm = minigm_survivors()
    minigm.run(screen, 'KM')
    pygame.quit()
