#Projet : Kage no Michi
#Auteurs : Alptan Korkmaz, Maxime Rousseaux, Ahmed-Adam Rezkallah, Clément Roux--Bénabou, Cyril Zhao


# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 17:38:15 2025

@author: clementroux--benabou
"""


#############
"""Placer le fichier dans le même dossier que le reste des fichiers python"""
#############


import pygame
import math
from enum import Enum
from Cinematics import Cinematics
from Audio import Music,Sound
from map.src.game import Game_map

class minigm_follow :
    
    def __init__ (self,screen):
        ### Etats du mini-jeu ###
        
        #Si le jeu tourne
        self.running = True
        
        #Si le mini-jeu est entrain d'âtre joué
        self.playing = False
        
        #Si la phase de gameplay (entre l'intro et la fin) est active
        self.in_minigm = False
        
        ### Appel de la classe cinématique, on utilisera principalement self.cin.cinematic_frame() et self.cin.cinematics_bgs
        self.cin = Cinematics()
        self.map = Game_map(screen,load_only=[True,"mg5"])
        
        ### Appel des classes pour l'audio, on utilisera principalement la fonction play() et les variables (aller voir le fichier)
        self.music,self.sound = Music(),Sound()
        
        self.gp_phases = Enum("Phase","BEGIN ADVANCE GO WATCH FOUND WIN PERFECT_WIN LOOSE")
        self.current_gp_phase = self.gp_phases.BEGIN
        self.current_advance_phase = 0
        self.steps = 0
        self.guards_arrived = False
        self.win_timer = 0
        
        self.load_assets()
     
    ########## Démarrage du mini-jeu ##########
    def load (self,devmode):
        self.map.player.set_allow_sprint(devmode)
        self.display_filter = not devmode
        self.playing = True
        self.current_advance_phase=1
        self.steps = 0
        self.guards_arrived = devmode
        self.win_timer = 0
        self.map.map_manager.change_map("mg5")
        self.check_guards_front = not devmode
     
    def load_assets(self):
        # Importer les images, sons etc.. ici (depuis "../data/assets")
        
        
        self.arrow = pygame.image.load("../data/assets/minigm/Flèche_Directionnelle_Bas.png").convert_alpha()
        self.current_arrow_rect= pygame.Rect(0,0,99,99)
        
        self.exclamation_point = pygame.image.load("../data/assets/minigm/Point_Exclamation.png").convert_alpha()

        self.filter = pygame.surface.Surface((1280,720))
        self.filter.fill("black")
        self.filter.set_alpha(100)
        
        ### Importation de la police d'écriture (taille des textes des dialogues)
        self.font_MFMG30 = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf",30)
     
    ########## Intro/Fin ##########
    def intro(self,screen,saved):
        #Appeler ici la fonction self.cin.cinematic_frame()
        #Exemple d'utilisation que vous pouvez copier coller (attention, TOUJOURS finir l'appel par running=self.running):
        
        self.cin.cinematic_frame(screen,'doj2', 3,"Suivez les espions du clan Takahiro pour récupérer des infos.", "Soyez discret et cachez vous quand ils se retournent !", kind_info=[['TW','no_weapon'],['TW_H','cin07'],['SM','no_weapon'],0], running=self.running)
        
        #À la toute fin de la fonction
        self.in_minigm = True
        self.current_gp_phase = self.gp_phases.BEGIN
    
    def end(self,screen,saved,passcode):
        #Appeler ici la fonction self.cin.cinematic_frame()
        if self.current_gp_phase in [self.gp_phases.WIN,self.gp_phases.PERFECT_WIN]:
            if self.guards_arrived:
                self.cin.cinematic_frame(screen,"ine1", 3, "Hayato, tu sais que le chef a ouvert une planque à Aizuwakamatsu ?", "Il m'a dit qu'il nous y enverrait prochainement.",kind_info=[['TW','no_weapon'],['TW_H','cin07'],['SM','no_weapon'],1], running=self.running)
                self.cin.cinematic_frame(screen,"ine1", 3, "Pour y investiguer sur les samouraïs là-bas aussi ?", kind_info=[['TW','no_weapon'],['TW_H','cin07'],['SM','no_weapon'],2], running=self.running)
                self.cin.cinematic_frame(screen,"ine1", 3, f"Sûrement. En tous cas, le code secret là-bas est {passcode}.", kind_info=[['TW','no_weapon'],['TW_H','cin07'],['SM','no_weapon'],1], running=self.running)
                self.cin.cinematic_frame(screen,"ine1", 3, "D'accord, je tâcherai de m'en souvenir.", kind_info=[['TW','no_weapon'],['TW_H','cin07'],['SM','no_weapon'],2], running=self.running)
                if self.current_gp_phase == self.gp_phases.PERFECT_WIN:
                    self.cin.cinematic_frame(screen,"ine1", 3, "Ils sont en position de faiblesse, si j’en profite, ils n’ont aucune chance.", "J’y vais, ou je rentre ? J’ai déjà assez d’informations comme ça, non ?", kind_info=[['TW','no_weapon'],['TW_H','cin07'],['SM','no_weapon'],3], running=self.running)
                else:
                    self.cin.cinematic_frame(screen,"ine1", 3,"Parfait, c’est noté. Retournons voir Sensei pour expliquer la situation.", kind_info=[['TW','no_weapon'],['TW_H','cin07'],['SM','no_weapon'],3], running=self.running)
            else:
                print("Tricheur !")
            
        
        elif self.current_gp_phase == self.gp_phases.LOOSE:
            self.cin.cinematic_frame(screen, "ine1", 3, "Tiens donc, un petit fouineur.", kind_info=[["TW","no_weapon"],["TW_H","no_weapon"],["SM","no_weapon"],1])
            self.cin.cinematic_frame(screen, "ine1", 3, "On ne joue pas au plus malin avec le clan Takahiro.", "Tu aurais dû le savoir.",kind_info=[["TW_H","no_weapon"],["TW","no_weapon"],["SM","no_weapon"],1,True])
        
        #À la toute fin de la fonction
        self.map.player.set_allow_sprint(True)
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
        
        
        if self.current_gp_phase == self.gp_phases.GO:
            self.map.player.save_location()
            self.map.handle_input(self.running,from_game=True)

        
    
    
    ########## Partie 2 : Mise à jour ##########
    def minigm_update (self):
        self.map.update()
        current_active_events = self.map.map_manager.get_current_active_events()
        
        
        self.handle_zone_events(current_active_events)
        self.arrow_update("finish")
        
        
        
        if self.current_gp_phase == self.gp_phases.BEGIN:
            self.move_npcs("down")
            self.change_phase(self.gp_phases.ADVANCE)
        elif self.current_gp_phase == self.gp_phases.ADVANCE:
            self.move_npcs("down")
        elif self.current_gp_phase == self.gp_phases.GO:
            if self.current_advance_phase==5 and not self.guards_arrived:
                self.guards_arrived = True
                self.win_timer = pygame.time.get_ticks()
            if self.map.map_manager.get_pos()[1] >= self.map.map_manager.get_map().npcs[0].position[1] and self.check_guards_front:
                self.change_phase(self.gp_phases.FOUND)
            if pygame.time.get_ticks()-self.current_phase_timer_start >= 7000:
                self.change_phase(self.gp_phases.WATCH)
        elif self.current_gp_phase == self.gp_phases.WATCH:
            if self.steps < 5 and pygame.time.get_ticks()-self.current_phase_timer_start < 2000:
                self.move_npcs("up")
                self.steps +=1
            elif pygame.time.get_ticks()-self.current_phase_timer_start >= 2000:
                if self.current_advance_phase < 5:
                    self.current_advance_phase += 1
                    self.change_phase(self.gp_phases.ADVANCE)
                    self.steps = 0
                else:
                    if self.steps > 0:
                        self.move_npcs("down")
                        self.steps -=1
                    else:
                        self.win_timer += pygame.time.get_ticks()-self.current_phase_timer_start
                        self.change_phase(self.gp_phases.GO)
        elif self.current_gp_phase == self.gp_phases.FOUND:
            if pygame.time.get_ticks()-self.current_phase_timer_start >=2000:
                self.change_phase(self.gp_phases.LOOSE)
                self.in_minigm = False
        else:
            pass
    
    def change_phase (self,phase):
        self.current_gp_phase = phase
        self.current_phase_timer_start = pygame.time.get_ticks()
    
    def move_npcs (self,direction):
        for npc in self.map.map_manager.get_map().npcs:
            npc.move_dir(direction)
    
    def handle_zone_events (self,events):
        for i in range(len(events)):
            event = events[i]
            data = event.data
            
            if event.type == "mgm_stop_npc":
                if self.current_gp_phase == self.gp_phases.ADVANCE and self.current_advance_phase == data[0]:
                    self.change_phase(self.gp_phases.GO)
            
            if event.type == "mgm_in_sight":
                if self.current_gp_phase == self.gp_phases.WATCH and data[0] == self.current_advance_phase and self.steps >= 5:
                    self.change_phase(self.gp_phases.FOUND)
                    
            if event.type == "mgm_end":
                final_time = pygame.time.get_ticks()-self.win_timer
                if final_time <= 5000:
                    self.change_phase(self.gp_phases.PERFECT_WIN)
                else:
                    self.change_phase(self.gp_phases.WIN)
                self.in_minigm=False
    
    def arrow_update (self,point):
        screen_rect = self.map.map_manager.get_map().group._map_layer.view_rect
        target_point = self.map.map_manager.get_point_pos(point)
        player_pos = self.map.map_manager.player.rect
        
        diffs = [(target_point[0]-player_pos.centerx),(target_point[1]-player_pos.centery)]
        if diffs[0]==0 and diffs[1]==0:
            angle = 0
        else:
            hypotenuse = math.sqrt((diffs[0]**2)+(diffs[1]**2))
            angle = math.degrees(math.asin(diffs[0]/hypotenuse))
        if diffs[1]<0:
            angle=-angle+180
            
        self.current_arrow_surface = pygame.transform.rotate(self.arrow,angle)
        
        self.current_arrow_rect.top = (player_pos.bottom-screen_rect.top)*2+5
        self.current_arrow_rect.left = (player_pos.left-screen_rect.left)*2+5
    

        
        
        
    ########## Partie 3 : Affichage ##########
    def minigm_draw (self,screen):
        #Remplissage avec du noir (fond)
        screen.fill((0,0,0))
        
        self.map.map_manager.draw()
        #for npc in self.map.map_manager.get_map().npcs:
        #    screen.blit(npc.image,npc.rect)
        if self.current_gp_phase == self.gp_phases.GO:
            screen.blit(self.current_arrow_surface,self.current_arrow_rect)
        elif self.current_gp_phase == self.gp_phases.FOUND:
            rect1,rect2 = self.get_exclamation_point_rects()
            screen.blit(self.exclamation_point,rect1)
            screen.blit(self.exclamation_point,rect2)
        
        if self.display_filter:
            screen.blit(self.filter,pygame.Rect(0,0,1280,720))
        #Mise à jour de l'écran
        pygame.display.flip()
    
    def get_exclamation_point_rects(self):
        x1,x2 = 730.5,858.5
        
        screen_top = self.map.map_manager.get_map().group._map_layer.view_rect.top
        npcs_head_top = self.map.map_manager.get_map().npcs[0].position[1]
        y= (npcs_head_top-screen_top)*2 - 20
        
        rect1,rect2=pygame.Rect(x1,y,7,27),pygame.Rect(x2,y,7,27)
        
        return rect1,rect2
    
   
    ########## Boucle mini-jeu ##########
    def run (self,screen,saved,passcode,devmode=False):
        #L'argument saved permet de savoir quelle version de l'intro et de la fin afficher en fonction de qui a été sauvé. Il permet aussi d'afficher le bon sprite dans le mini-jeu le cas échéant 

        
        self.load(devmode)
        self.intro(screen,saved)
        
        pygame.mouse.set_visible(False)
        
        while self.playing and self.running and self.in_minigm:
            self.minigm_events()
            self.minigm_update()
            self.minigm_draw(screen)
            pygame.time.Clock().tick(60)
            
        pygame.mouse.set_visible(True)
        
        if self.playing and self.running:
            self.end(screen,saved,passcode)
        return self.running

#Lancement du mini-jeu
if __name__ == '__main__':
    pygame.init()
    
    icon = pygame.image.load("../data/assets/common/Icone_LOGO_V12.ico")
    pygame.display.set_icon(icon)
    cursor = pygame.image.load("../data/assets/common/Souris_V4.png")
    pygame.mouse.set_cursor((5,5),cursor)
    screen = pygame.display.set_mode((1280,720))
    pygame.display.set_caption("Kage no michi - Mini-jeu de filature")
    
    minigm = minigm_follow(screen)
    minigm.run(screen, 'KM',"jaimelecouscoustajine")
    pygame.quit()
    
