#Projet : Kage no Michi
#Auteurs : Alptan Korkmaz, Clément Roux--Bénabou, Maxime Rousseaux, Ahmed-Adam Rezkallah, Cyril Zhao


# -*- coding: utf-8 -*-
"""
Created on Fri Mar 07 23:18:22 2025

@author: clementroux--benabou
"""

import pygame
import random
from typing import List
from Cinematics import Cinematics
from Fight_assets import Perso,Weapon,Fight_assets
from dataclasses import dataclass

class Fight:
    def __init__(self):
        #Couleurs
        self.VERT = (0, 140, 70)
        self.VERT_VIE = (90, 180, 130)
        self.PINK = (240, 120, 174)
        self.ROUGE = (255, 0, 0)
        self.BLANC = (255, 255, 255)
        self.GRIS = (150,150,150)

        #Utiles
        self.clock=pygame.time.Clock()

        #Chargement des Ressources Graphiques
        # Fond d'écran et panneau de dialogue
        self.bgs = Cinematics().cinematics_bgs
        self.panel_affichage = pygame.image.load("../data/assets/minigm/Parchemin_Question.png").convert_alpha()
        self.HAUTEUR_PANEL = self.panel_affichage.get_height()

        self.red_arrow = pygame.image.load("../data/assets/tpt/Flèche_Directionnelle_Bas_ROUGE.png").convert_alpha()
        self.is_target_choosen = False

        # Polices d'écriture
        self.police_hint = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf", 20)
        self.police_base = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf", 30)
        self.police_display = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf", 49)
        self.police_degats = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf", 40)

        # Images des objets (ex : potion de soin)
        self.potion_image = pygame.image.load("../data/assets/minigm/potion_de_soin.png").convert_alpha()
        self.potion_image = pygame.transform.scale(self.potion_image, (80, 80))

        # Images des boutons d'attaque (interface utilisateur)
        self.attaque_frontale_box = pygame.image.load("../data/assets/minigm/Attaque_Frontale_V1.png").convert_alpha()
        self.attaque_special_box = pygame.image.load("../data/assets/minigm/Attaque_Speciale_V1.png").convert_alpha()

        # Définition des zones cliquables (hitboxes)
        self.attaque_frontale_hitbox = pygame.Rect(15, 200, 100, 100)
        self.attaque_special_hitbox = pygame.Rect(15, 320, 100, 100)
        self.potion_hitbox = pygame.Rect(550,790-self.HAUTEUR_PANEL, 80, 80)
        self.affichage_display = pygame.Rect(0,0,1280,50)

        #Zones des textes
        self.ennemy_turn_text = self.police_display.render("Au tour de l'ennemi !",False,self.BLANC)
        self.player_turn_text = self.police_display.render("Au tour du joueur !",False,self.BLANC)
        self.victory_text = self.police_display.render("Victoire !",False,self.BLANC)
        self.defeat_text = self.police_display.render("Défaite...",False,self.BLANC)
        self.any_turn_text_pos = (190,0)

        self.pop_text_timer_lengh = 4000
        self.hint_timer = 0
        self.pop_text_choose_ennemy = self.police_hint.render("Choisissez l'adversaire à attaquer !",False,"black")
        self.pop_text_no_potion = self.police_hint.render("Vous n'avez plus de potion !",False,"black")
        self.attaque_frontale_compteur = 0
        self.pop_text_choose_ennemy_rect = self.pop_text_choose_ennemy.get_rect()
        self.pop_text_spe_not_ready_rect = self.pop_text_spe_not_ready.get_rect()
        self.pop_text_no_potion_rect = self.pop_text_no_potion.get_rect()
        midtop = (640,100)
        self.pop_text_spe_not_ready_rect.midtop = midtop
        self.pop_text_choose_ennemy_rect.midtop = midtop
        self.pop_text_no_potion_rect.midtop = midtop

        self.characters_positions = {'main':(400,250),
                                     'ally1':(350,250),
                                     'ally2':(300,250),
                                     'ennemy1':(700, 250),
                                     'ennemy2':(850, 250),
                                     'ennemy3':(900, 250)
                                     }
        
        self.continuer = True
        self.attack_cooldown = False
        self.attack_cooldown_stating_timer = 0
        self.attack_cooldown_timer = 1000
        self.end_cooldown_timer_lengh = 5000
        self.in_end_cooldown=False
        self.end_timer = 0


    def changer_orientation_sprite(sprite):return pygame.transform.flip(sprite,True,False)

    def load (self,bg_name,perso_player:Perso,allies:List[Perso],persos_ennemy:List[Perso],potions:int):
        # Variables de Jeu
        self.perso_player=perso_player
        self.allies=allies
        self.not_ko_allies = self.allies
        self.persos_ennemy = persos_ennemy
        self.alive_ennemies = self.persos_ennemy
        self.current_ennemy = persos_ennemy[0]
        self.nombre_ennemi = len(persos_ennemy)
        self.nombre_allies = len(allies)
        self.attaque_frontale_compteur = 0
        self.actions = ["player","allies","ennemies","victory","defeat"]
        self.action = "player"
        self.queuing_phase = None
        self.end_phase = False
        self.end_phase_timer = 0
        self.phase_cooldown = 1500
        self.potion = potions
        self.modifieur_degats = 5
        self.modifieur_degats_spe = 15
        self.bg=self.bgs[bg_name]

        self.display_number=False
        self.is_number_damage = None
        self.number_duration = 1000
        self.start_drawing_number_timer = 0
        self.draw_spe = False
        self.is_crit = False
        self.crit_text = self.police_hint.render("Coup critique !", False,"orange")

        self.allow_normal = True
        self.allow_spe = True
        self.allow_potion = True

        # Variables pour gérer le temps (pour le cooldown des attaques ennemies)
        self.tour = 1
        self.current_ennemy_attacking_index = 0
        self.current_ally_attacking_index = 0
        self.to_draw_hint = 'none'

        self.in_end_cooldown=False

        self.perso_player.set_pos(self.characters_positions["main"])
        self.perso_player.set_orientation("droite")
        for i in range(len(self.allies)):
            ally=self.allies[i]
            ally.set_pos(self.characters_positions[f'ally{i+1}'])
            ally.set_orientation("droite")
        for i in range(len(self.persos_ennemy)):
            ennemy = self.persos_ennemy[i]
            ennemy.set_pos(self.characters_positions[f'ennemy{i+1}'])
            ennemy.set_orientation('gauche')
    
    @property
    def nombre_alive_allies(self):return len(self.not_ko_allies)
    @property
    def nombre_alive_ennemies (self):return len(self.alive_ennemies)
    @property
    def pop_text_spe_not_ready (self):return self.police_hint.render(f"L'attaque spéciale n'est pas chargée ({4-self.attaque_frontale_compteur} attaque(s) normale(s) restante(s)) !",False,"black")

    def set_allowed_action (self,normal=True,spe=True,potion=True):
        self.allow_normal = normal
        self.allow_spe = spe
        self.allow_potion = potion
    
    def change_phase(self,new_phase):
        self.queuing_phase=new_phase
        self.end_phase = True
        self.end_phase_timer = pygame.time.get_ticks()
        self.is_target_choosen = False
    
    def start_to_draw_number(self,damage:bool,char:Perso):
        self.display_number=True
        self.is_number_damage = damage
        self.start_drawing_number_timer = pygame.time.get_ticks()
        pos = char.pos
        self.number_pos = (pos[0],pos[1]-30)

    def start_draw_hint(self,hint):
        self.to_draw_hint = hint
        self.hint_timer = pygame.time.get_ticks()

    def get_damage (self,char:Perso,is_spe:bool=False):
        base_damage = char.current_damage
        if is_spe :
            base_damage+=char.weapon.special_damage
        self.is_crit = random.random()<=char.weapon.crit_chance
        if self.is_crit:
            mult = (random.random()*3/4)+1.5
            base_damage=int(base_damage*mult)
        damage = random.randint(base_damage-char.level,base_damage+char.level)
        return max(damage,0)

    def handle_imput (self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.continuer=False
                pygame.event.post(event)
            
            # Si le joueur peut agir
            if self.action == "player" and not self.end_phase:
                if event.type == pygame.MOUSEBUTTONUP:
                    
                    for ennemy in self.alive_ennemies:
                        if ennemy.rect.collidepoint(event.pos):
                            self.is_target_choosen = True
                            self.current_ennemy = ennemy


                    #Utilisation de la potion
                    if self.potion_hitbox.collidepoint(event.pos) and self.allow_potion:
                        if self.potion >=1:
                            self.potion -= 1
                            self.number = min(self.perso_player.pv_max,self.perso_player.pv+30) - self.perso_player.pv
                            self.perso_player.pv += self.number
                            self.start_to_draw_number(False,self.perso_player)
                            self.change_phase("allies")
                        elif self.potion < 1:
                            self.start_draw_hint('potion')

                    elif self.is_target_choosen:
                        # Attaque frontale
                        if self.attaque_frontale_hitbox.collidepoint(event.pos) and self.allow_normal:
                            self.number = self.get_damage(self.perso_player)
                            self.current_ennemy.hit(self.number)
                            self.attaque_frontale_compteur += 1
                            self.perso_player.attacking=True
                            self.start_to_draw_number(True,self.current_ennemy)
                            self.change_phase("allies")
                            self.draw_spe = False

                        # Attaque spéciale (se déclenche après 4 attaques de base)
                        if self.attaque_special_hitbox.collidepoint(event.pos) and self.attaque_frontale_compteur >= 4 and self.allow_spe:
                            self.number = self.get_damage(self.perso_player,is_spe=True)
                            self.current_ennemy.hit(self.number)
                            self.attaque_frontale_compteur = 0
                            self.perso_player.attacking=True
                            self.start_to_draw_number(True,self.current_ennemy)
                            self.change_phase("allies")
                            self.draw_spe = True
                        elif self.attaque_special_hitbox.collidepoint(event.pos) and self.allow_spe:
                            self.start_draw_hint("spe")
                    elif not self.is_target_choosen and ((self.attaque_frontale_hitbox.collidepoint(event.pos) and self.allow_normal) or (self.attaque_special_hitbox.collidepoint(event.pos) and self.allow_spe)):
                        self.start_draw_hint("choose")
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()



    def allies_attack(self):
        if self.nombre_alive_allies == 0:
            self.action='ennemies'
        elif not self.attack_cooldown:
            ally = self.not_ko_allies[self.current_ally_attacking_index]
            attacked_ennemy = random.choice(self.alive_ennemies)
            self.number = self.get_damage(ally)
            attacked_ennemy.hit(self.number)
            ally.attacking=True
            self.start_to_draw_number(True,attacked_ennemy)
            self.next_ally()
        elif self.attack_cooldown_timer-pygame.time.get_ticks()+self.attack_cooldown_stating_timer<=0:
            self.attack_cooldown = False
    
    def next_ally (self):
        if self.current_ally_attacking_index >= self.nombre_alive_allies-1:
            self.current_ally_attacking_index = 0
            self.change_phase("ennemies")
        else:
            self.attack_cooldown = True
            self.attack_cooldown_stating_timer = pygame.time.get_ticks()
            self.current_ally_attacking_index+=1

    def ennemies_attack(self):
        if self.nombre_alive_ennemies != 0 and not self.attack_cooldown:
            ennemy = self.alive_ennemies[self.current_ennemy_attacking_index]
            if ennemy.do_attacks:
                attacked_ally = random.choice(self.not_ko_allies+[self.perso_player])
                self.number = self.get_damage(ennemy)
                attacked_ally.hit(self.number)
                ennemy.attacking=True
                self.start_to_draw_number(True,attacked_ally)
            self.next_ennemy()
        elif self.attack_cooldown_timer-pygame.time.get_ticks()+self.attack_cooldown_stating_timer<=0:
            self.attack_cooldown = False
    
    def next_ennemy (self):
        if self.current_ennemy_attacking_index >= self.nombre_alive_ennemies-1:
            self.current_ennemy_attacking_index = 0
            self.change_phase("player")
        else:
            self.attack_cooldown = True
            self.attack_cooldown_stating_timer = pygame.time.get_ticks()
            self.current_ennemy_attacking_index +=1
    
    def update (self):

        if self.end_phase and not self.in_end_cooldown and self.phase_cooldown-pygame.time.get_ticks()+self.end_phase_timer<=0:
            self.end_phase = False
            self.action = self.queuing_phase
            if self.action == 'player':
                self.tour+=1
                self.current_ennemy = self.alive_ennemies[0]
        
        if self.display_number and self.number_duration-pygame.time.get_ticks()+self.start_drawing_number_timer<=0:
            self.display_number = False
        
        if self.action == 'allies' and not self.end_phase:
            self.allies_attack()
        elif self.action == 'ennemies' and not self.end_phase:
            self.ennemies_attack()

        for ennemy in self.alive_ennemies:
            if ennemy.is_ko:
                self.alive_ennemies.remove(ennemy)
        for ally in self.allies:
            if ally.is_ko:
                self.not_ko_allies.remove(ally)


        # Fin du combat : victoire ou défaite
        if self.nombre_alive_ennemies==0 and not self.in_end_cooldown:
            self.action='victory'
            self.end_timer = pygame.time.get_ticks()
            self.in_end_cooldown = True
        elif self.perso_player.is_ko and self.nombre_alive_allies==0 and not self.in_end_cooldown:
            self.action='defeat'
            self.end_timer = pygame.time.get_ticks()
            self.in_end_cooldown = True
        
        if self.in_end_cooldown and self.end_cooldown_timer_lengh-pygame.time.get_ticks()+self.end_timer<=0:
            self.continuer = False

    def draw_panel(self,screen):
        """
        Affiche le panneau de dialogue et les points de vie des personnages.
        """
        screen.blit(self.panel_affichage, (0, 720 - self.HAUTEUR_PANEL))
        if self.allow_potion :
            screen.blit(self.potion_image, (550,790-self.HAUTEUR_PANEL))
            text_potion = self.police_base.render(str(self.potion),False,"black")
            rect_potion = text_potion.get_rect()
            rect_potion.midtop = (self.potion_image.get_width()/2+550,580)
            screen.blit(text_potion,rect_potion)

        #Joueur
        text = self.police_base.render(self.perso_player.sprite_name+ ' LVL:'+str(self.perso_player.level)+' PV : '+str(self.perso_player.pv),False,self.VERT)
        screen.blit(text,(100,790-self.HAUTEUR_PANEL))
        ratio = self.perso_player.pv / self.perso_player.pv_max #Différence entre les pvs actuel et les pv maxs
        pygame.draw.rect(screen, self.ROUGE, (100, 820-self.HAUTEUR_PANEL, 400, 30)) #Les pvs qui ont été enlevé dans la barre d'hp
        pygame.draw.rect(screen, self.VERT_VIE, (100, 820-self.HAUTEUR_PANEL, 400 * ratio, 30))

        #Alliés
        for i in range(len(self.allies)):
            ally = self.allies[i]
            text = self.police_base.render(ally.sprite_name+' LVL:'+str(ally.level)+' PV : '+str(ally.pv),False,self.VERT)
            screen.blit(text,(100,790-self.HAUTEUR_PANEL+60*(i+1)))
            ratio = ally.pv / ally.pv_max #Différence entre les pvs actuel et les pv maxs
            pygame.draw.rect(screen, self.ROUGE, (100, 820-self.HAUTEUR_PANEL+60*(i+1), 400, 30)) #Les pvs qui ont été enlevé dans la barre d'hp
            pygame.draw.rect(screen, self.VERT_VIE, (100, 820-self.HAUTEUR_PANEL+60*(i+1), 400 * ratio, 30))
        
        #Ennemis
        for i in range(len(self.persos_ennemy)):
            ennemy = self.persos_ennemy[i]
            text = self.police_base.render(ennemy.sprite_name+' LVL:'+str(ennemy.level)+' PV : '+str(ennemy.pv),False,self.PINK)
            screen.blit(text,(700,790-self.HAUTEUR_PANEL+60*(i)))
            ratio = ennemy.pv / ennemy.pv_max #Différence entre les pvs actuel et les pv maxs
            pygame.draw.rect(screen, self.ROUGE, (700, 820-self.HAUTEUR_PANEL+60*(i), 400, 30)) #Les pvs qui ont été enlevé dans la barre d'hp
            pygame.draw.rect(screen, self.VERT_VIE, (700, 820-self.HAUTEUR_PANEL+60*(i), 400 * ratio, 30))

    def draw_persos (self,screen):
        if self.perso_player.pv > 0:
            if not self.perso_player.attacking:
                self.perso_player.draw_static(screen)
        for i in range(len(self.allies)):
            ally=self.allies[i]
            if ally.pv > 0:
                if not ally.attacking:
                    ally.draw_static(screen)
        for i in range(len(self.persos_ennemy)):
            ennemy=self.persos_ennemy[i]
            if ennemy.pv > 0:
                if not ennemy.attacking:
                    ennemy.draw_static(screen)
        if self.perso_player.pv > 0:
            if self.perso_player.attacking:
                self.perso_player.draw_atk(screen,"Attaque_Speciale" if self.draw_spe else "Attaque_Frontale",self.current_ennemy.pos)
        for i in range(len(self.allies)):
            ally=self.allies[i]
            if ally.pv > 0:
                if ally.attacking:
                    ally.draw_atk(screen,"Attaque_Frontale",self.current_ennemy.pos)
        for i in range(len(self.persos_ennemy)):
            ennemy=self.persos_ennemy[i]
            if ennemy.pv > 0:
                if ennemy.attacking:
                    ennemy.draw_atk(screen,"Attaque_Frontale",self.perso_player.pos)

    def draw_number(self,screen):
        if self.number == 0:
            col = self.GRIS
        elif self.is_number_damage:
            col = self.ROUGE
        else:
            col = self.VERT_VIE
        if self.number==0 and self.is_number_damage:
            text = self.police_degats.render("Raté !",False,col)
        else:
            text = self.police_degats.render(str(self.number),False,col)
        screen.blit(text,self.number_pos)
        if self.is_crit:
            crit_pos = (self.number_pos[0],self.number_pos[1]-25)
            screen.blit(self.crit_text,crit_pos)

    def draw_arrow (self,screen):
        pos = self.current_ennemy.pos
        pos = pos[0]+73,pos[1]-70
        screen.blit(self.red_arrow,pos)

    def draw_overlay (self,screen):
        screen.blit(self.bg,(0,0))
        text_tour = self.police_display.render(f'Tour {self.tour}',False,self.BLANC)
        screen.blit(text_tour,(790,0))
        if self.action == "victory":
            screen.blit(self.victory_text,self.any_turn_text_pos)
        elif self.action == 'defeat':
            screen.blit(self.defeat_text,self.any_turn_text_pos)
        elif self.action == "ennemies":
            screen.blit(self.ennemy_turn_text,self.any_turn_text_pos)
        else:
            screen.blit(self.player_turn_text,self.any_turn_text_pos)

        if self.allow_normal:
            screen.blit(self.attaque_frontale_box, (15, 200))
        if self.allow_spe:

            if self.attaque_frontale_compteur >= 4:
                self.attaque_special_box =  pygame.image.load("../data/assets/minigm/Attaque_Speciale_V1.png").convert_alpha()
                screen.blit(self.attaque_special_box, (15, 320))
            else:
                self.attaque_special_box = pygame.image.load("../data/assets/minigm/Attaque_Speciale_Sombre_V1.png").convert_alpha()
                screen.blit(self.attaque_special_box, (15,320))
    
    def draw_hint(self,screen):
        if self.pop_text_timer_lengh-pygame.time.get_ticks()+self.hint_timer<=0:
            self.to_draw_hint='none'
        if self.to_draw_hint == "spe":
            screen.blit(self.pop_text_spe_not_ready,self.pop_text_spe_not_ready_rect)
        elif self.to_draw_hint == "choose":
            screen.blit(self.pop_text_choose_ennemy,self.pop_text_choose_ennemy_rect)
        elif  self.to_draw_hint == 'potion':
            screen.blit(self.pop_text_no_potion,self.pop_text_no_potion_rect)

    def draw (self,screen,do_refresh=True):
        self.draw_overlay(screen)
        self.draw_hint(screen)
        self.draw_persos(screen)
        if self.is_target_choosen:
            self.draw_arrow(screen)
        if self.display_number:
            self.draw_number(screen)
        self.draw_panel(screen)
        if do_refresh:
            pygame.display.flip()
    
    def run(self,screen:pygame.surface.Surface,bg_name:str,perso_player:Perso,allies:List[Perso],persos_ennemy:List[Perso],potions:int):
        self.load(bg_name,perso_player,allies,persos_ennemy,potions)

        while self.continuer:
            self.handle_imput()
            self.update()
            self.draw(screen)
            self.clock.tick(60)
        return self.action,self.potion

if __name__ == "__main__":
    fight_assets = Fight_assets()
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    pygame.display.set_caption("Kage no Michi - Système de combat TPT")
    Fight().run(screen,'ine1',fight_assets.Musashi_Tengoku,[],[fight_assets.Senshi],100)
    pygame.quit()