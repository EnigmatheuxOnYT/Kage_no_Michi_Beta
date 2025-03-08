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
from dataclasses import dataclass

@dataclass
class Weapon:
    name : str
    weapon_damage : int

class Perso:
    """
    Classe représentant un personnage du jeu.
    """
    def __init__(self, name, pv_max, weapon, nouvelle_taille: tuple,level=1,instance=0): #Toutes les variables nécessaires pour la création d'un personnage
        self.name = name+str(instance) #Son nom, ATTENTION LE NOM DEFINIT LE SPRITE CHOISI !!
        self.sprite_name = name
        self.pv_max = pv_max #Ses hp max
        self.pv = pv_max #Ses pv, qui vont prendre tout simplement la valeur de ses pvs
        self._base_damage = 5
        self.weapon = weapon
        self.level = level #niveau du personnage
        sprite = pygame.image.load(f"../data/assets/sprites/{self.sprite_name}_Idle.png") #Le spirte quand il reste immobile
        self.image = pygame.transform.scale(sprite, nouvelle_taille) #On redimensionne le sprite de sorte à ce que ça soit cohérent avec le fond
        self.atk_frame_lengh = 80
        self.debut_frame = 0
        self.orientation="gauche"
        self.pos=(0,0)
        self.attacking=False
        self.animations_combat = [
            pygame.image.load(f"../data/assets/sprites/{self.sprite_name}_Combat_1.png"),
            pygame.image.load(f"../data/assets/sprites/{self.sprite_name}_Combat_2.png"),
            pygame.image.load(f"../data/assets/sprites/{self.sprite_name}_Combat_3.png"),
            pygame.image.load(f"../data/assets/sprites/{self.sprite_name}_Combat_4.png"),
            pygame.image.load(f"../data/assets/sprites/{self.sprite_name}_Combat_5.png"),
            pygame.image.load(f"../data/assets/sprites/{self.sprite_name}_Combat_6.png"),
            pygame.image.load(f"../data/assets/sprites/{self.sprite_name}_Combat_7.png"),
            pygame.image.load(f"../data/assets/sprites/{self.sprite_name}_Combat_8.png"),
            pygame.image.load(f"../data/assets/sprites/{self.sprite_name}_Combat_9.png"),
            pygame.image.load(f"../data/assets/sprites/{self.sprite_name}_Combat_10.png"),
            sprite
        ] #Tous les sprites présents lors de l'animation d'attaque

        self.index = 0
        self.max_index = 10

    @property
    def current_damage(self):return self._base_damage+self.weapon.weapon_damage
    @property
    def is_ko (self):return False if self.pv>0 else True
    
    def level_up (self):
        self.level+=1
        self.pv_max=round(self.pv_max*1.1,0)
        self.base_damage=round(self._base_damage*1.1,0)
    
    def change_weapon (self,weapon):self.weapon=weapon
    
    def set_orientation(self,new_orientation):self.orientation=new_orientation

    def set_pos(self,pos):self.pos=pos

    def set_attacking(self,val):self.attacking=val

    def draw_static(self):
        """
        Affiche le personnage à une position donnée.
        """
        if self.orientation == 'gauche':
            image = pygame.transform.flip(self.image,True,False)
        else:
            image=self.image
        screen.blit(image, self.pos) #Affichage du personnage choisi
    
    def draw_atk(self,attaque_choisie:str,ennemi_position:tuple):
        self.animations_attaque = [
            pygame.image.load(f"../data/assets/sprites/{attaque_choisie}_1_V1.png"),
            pygame.image.load(f"../data/assets/sprites/{attaque_choisie}_2_V1.png"),
            pygame.image.load(f"../data/assets/sprites/{attaque_choisie}_3_V1.png"),
            pygame.image.load(f"../data/assets/sprites/{attaque_choisie}_4_V1.png"),
            pygame.image.load(f"../data/assets/sprites/{attaque_choisie}_5_V1.png"),
            pygame.image.load(f"../data/assets/sprites/{attaque_choisie}_6_V1.png"),
            pygame.image.load(f"../data/assets/sprites/{attaque_choisie}_7_V1.png"),
            pygame.image.load(f"../data/assets/sprites/{attaque_choisie}_8_V1.png"),
            pygame.image.load(f"../data/assets/sprites/{attaque_choisie}_9_V1.png")
        ]

        if self.index == 0 or self.atk_frame_lengh-pygame.time.get_ticks()+self.debut_frame<=0:
            self.index +=1
            if self.index>self.max_index:
                self.index=0
                self.attacking=False
            self.debut_frame = pygame.time.get_ticks()
        if self.index!=0:
            image = pygame.transform.scale(self.animations_combat[self.index], (200,200))
            if self.orientation == "gauche":
                self.image = pygame.transform.flip(image, True, False)
            screen.blit(image,(self.pos))
            if self.index >= 2:
                image_attaque = pygame.transform.scale(self.animations_attaque[self.index-2],(200,200))
                screen.blit(image_attaque, ennemi_position)
        else:
            self.draw_static()


class Fight:
    def __init__(self):
        #Couleurs
        self.VERT = (0, 140, 70)
        self.VERT_VIE = (90, 180, 130)
        self.PINK = (240, 120, 174)
        self.ROUGE = (255, 0, 0)
        self.BLANC = (255, 255, 255)

        #Utiles
        self.clock=pygame.time.Clock()

        #Chargement des Ressources Graphiques
        # Fond d'écran et panneau de dialogue
        self.bgs = Cinematics().cinematics_bgs
        self.panel_affichage = pygame.image.load("../data/assets/minigm/Parchemin_Question.png").convert_alpha()
        self.HAUTEUR_PANEL = self.panel_affichage.get_height()

        # Polices d'écriture
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
        self.potion_hitbox = pygame.Rect(500,790-self.HAUTEUR_PANEL, 80, 80)
        self.affichage_display = pygame.Rect(0,0,1280,50)

        #Zones des textes
        self.ennemy_turn_text = self.police_display.render("Au tour de l'ennemi!",False,self.BLANC)
        self.any_turn_text_pos = (190,0)
        self.player_turn_text = self.police_display.render("Au tour du joueur!",False,self.BLANC)

        self.characters_positions = {'main':(400,250),
                                     'ally1':(350,250),
                                     'ally2':(300,250),
                                     'ennemy1':(700, 250),
                                     'ennemy2':(850, 250),
                                     'ennemy3':(900, 250)
                                     }
        
        self.continuer = True
        self.click_cooldown = False


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
        self.actions = ["player","allies","ennemies"]
        self.action = "player"
        self.queuing_phase = None
        self.end_phase = False
        self.end_phase_timer = 0
        self.phase_cooldown = 3000
        self.potion = potions
        self.modifieur_degats = 5
        self.modifieur_degats_spe = 15
        self.bg=self.bgs[bg_name]

        # Dégâts aléatoires pour les attaques
        self.attaque_frontale = random.randint(perso_player.current_damage-self.modifieur_degats,perso_player.current_damage+self.modifieur_degats)
        self.attaque_special = random.randint(perso_player.current_damage+self.modifieur_degats,perso_player.current_damage+self.modifieur_degats+self.modifieur_degats_spe)

        self.display_number=False
        self.is_number_damage = None
        self.number_duration = 800
        self.start_drawing_number_timer = 0

        # Variables pour gérer le temps (pour le cooldown des attaques ennemies)
        self.cooldown_ennemi = 1000  # 1 seconde de cooldown
        self.tour = 1
        self.current_ennemy_attacking_index = 0
        self.current_ally_attacking_index = 0

        self.click_cooldown = False

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

        #barres_vie = {}
        #self.perso_player_barrevie = BarreVie(100,640, self.perso_player.pv, self.perso_player.pv_max)
        """
        y = 150
        self.allies_barres_vie = {}
        for ally in self.allies:
            self.allies_barres_vie[ally.name] = BarreVie(100, 540+y, ally.pv, ally.pv_max)
            y += 20

        y = 100
        self.ennemies_barres_vie = {}
        for ennemy in self.persos_ennemy:
            self.ennemies_barres_vie[ennemy.name] = BarreVie(700,540+y, ennemy.pv, ennemy.pv_max)
            y+20
        """
    
    def change_phase(self,new_phase):
        self.queuing_phase=new_phase
        self.end_phase = True
        self.end_phase_timer = pygame.time.get_ticks()
    
    def start_to_draw_number(self,damage:bool,char:Perso):
        self.display_number=True
        self.is_number_damage = damage
        self.start_drawing_number_timer = pygame.time.get_ticks()
        pos = char.pos
        self.number_pos = (pos[0]-20,pos[1]-30)

    def handle_imput (self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.continuer=False
                pygame.event.post(event)
            
            # Si le joueur peut agir
            if self.action == "player":
                if event.type == pygame.MOUSEBUTTONUP and self.click_cooldown == False:
                    self.click_cooldown = True

                    #Utilisation de la potion
                    if self.potion_hitbox.collidepoint(event.pos) and self.potion > 0:
                        self.potion -= 1
                        self.number = min(self.perso_player.pv_max,self.perso_player.pv+30) - self.perso_player.pv
                        self.perso_player.pv += self.number
                        self.start_to_draw_number(False,self.perso_player)
                        self.change_phase("allies")

                    # Attaque frontale
                    if self.attaque_frontale_hitbox.collidepoint(event.pos):
                        self.number = random.randint(self.perso_player.current_damage-self.modifieur_degats,self.perso_player.current_damage+self.modifieur_degats)
                        self.current_ennemy.pv-=self.number
                        self.attaque_frontale_compteur += 1
                        self.perso_player.attacking=True
                        self.start_to_draw_number(True,self.current_ennemy)
                        self.change_phase("allies")

                    # Attaque spéciale (se déclenche après 4 attaques de base)
                    if self.attaque_special_hitbox.collidepoint(event.pos) and self.attaque_frontale_compteur >= 4:
                        self.number = random.randint(self.perso_player.current_damage+self.modifieur_degats,self.perso_player.current_damage+self.modifieur_degats+self.modifieur_degats_spe)
                        self.current_ennemy.pv -= self.number
                        self.attaque_frontale_compteur = 0
                        self.perso_player.attacking=True
                        self.start_to_draw_number(True,self.current_ennemy)
                        self.change_phase("allies")
                else:
                    self.click_cooldown=False

    def allies_attack(self):
        if self.nombre_allies!=0:
            ally = self.allies[self.current_ally_attacking_index]
            attacked_ennemy = random.choice(self.alive_ennemies)
            self.number = random.randint(ally.current_damage-self.modifieur_degats,ally.current_damage+self.modifieur_degats)
            attacked_ennemy.pv-=self.number
            self.attaque_frontale_compteur += 1
            self.perso_player.attacking=True
            self.start_to_draw_number(True,attacked_ennemy)
            self.next_ally()
    
    def next_ally (self):pass

    def ennemies_attack(self):
        pass
    
    def update (self):

        if self.end_phase and self.phase_cooldown-pygame.time.get_ticks()+self.end_phase_timer<=0:
            self.end_phase = False
            self.action = self.queuing_phase
        
        if self.display_number and self.number_duration-pygame.time.get_ticks()+self.start_drawing_number_timer<=0:
            self.display_number = False
        
        if self.action == 'allies':
            self.allies_attack()
        elif self.action == 'ennemies':
            self.ennemies_attack()

        for ennemy in self.alive_ennemies:
            if ennemy.is_ko:
                self.alive_ennemies.remove(ennemy)
        for ally in self.allies:
            if ally.is_ko:
                self.not_ko_allies.remove(ally)


        # Fin du combat : victoire ou défaite
        if len(self.alive_ennemies)==0:
            print('WIN')
            self.continuer = False
        elif self.perso_player.is_ko and len(self.not_ko_allies)==0:
            print('LOSE')
            self.continuer = False

    def draw_panel(self,screen):
        """
        Affiche le panneau de dialogue et les points de vie des personnages.
        """
        screen.blit(self.panel_affichage, (0, 720 - self.HAUTEUR_PANEL))
        screen.blit(self.potion_image, (500,790-self.HAUTEUR_PANEL))
        text_potion = self.police_base.render(str(self.potion),False,"black")
        screen.blit(text_potion,(535,580))

        #Joueur
        text = self.police_base.render(self.perso_player.sprite_name+' PV : '+str(self.perso_player.pv),False,self.VERT)
        screen.blit(text,(100,790-self.HAUTEUR_PANEL))
        ratio = self.perso_player.pv / self.perso_player.pv_max #Différence entre les pvs actuel et les pv maxs
        pygame.draw.rect(screen, self.ROUGE, (100, 820-self.HAUTEUR_PANEL, 300, 30)) #Les pvs qui ont été enlevé dans la barre d'hp
        pygame.draw.rect(screen, self.VERT_VIE, (100, 820-self.HAUTEUR_PANEL, 300 * ratio, 30))

        #Alliés
        for i in range(len(self.allies)):
            ally = self.allies[i]
            text = self.police_base.render(ally.sprite_name+' PV : '+str(ally.pv),False,self.VERT)
            screen.blit(text,(100,790-self.HAUTEUR_PANEL+60*(i+1)))
            ratio = ally.pv / ally.pv_max #Différence entre les pvs actuel et les pv maxs
            pygame.draw.rect(screen, self.ROUGE, (100, 820-self.HAUTEUR_PANEL+60*(i+1), 300, 30)) #Les pvs qui ont été enlevé dans la barre d'hp
            pygame.draw.rect(screen, self.VERT_VIE, (100, 820-self.HAUTEUR_PANEL+60*(i+1), 300 * ratio, 30))
        
        #Ennemis
        for i in range(len(self.persos_ennemy)):
            ennemy = self.persos_ennemy[i]
            text = self.police_base.render(ennemy.sprite_name+' PV : '+str(ennemy.pv),False,self.PINK)
            screen.blit(text,(700,790-self.HAUTEUR_PANEL+60*(i)))
            ratio = ennemy.pv / ennemy.pv_max #Différence entre les pvs actuel et les pv maxs
            pygame.draw.rect(screen, self.ROUGE, (700, 820-self.HAUTEUR_PANEL+60*(i), 300, 30)) #Les pvs qui ont été enlevé dans la barre d'hp
            pygame.draw.rect(screen, self.VERT_VIE, (700, 820-self.HAUTEUR_PANEL+60*(i), 300 * ratio, 30))

    def draw_persos (self,screen):
        if self.perso_player.pv > 0:
            if not self.perso_player.attacking:
                self.perso_player.draw_static()
        for i in range(len(self.allies)):
            ally=self.allies[i]
            if ally.pv > 0:
                if not ally.attacking:
                    ally.draw_static()
        for i in range(len(self.persos_ennemy)):
            ennemy=self.persos_ennemy[i]
            if ennemy.pv > 0:
                if not ennemy.attacking:
                    ennemy.draw_static()
        if self.perso_player.pv > 0:
            if self.perso_player.attacking:
                self.perso_player.draw_atk("Attaque_Frontale",self.current_ennemy.pos)
        for i in range(len(self.allies)):
            ally=self.allies[i]
            if ally.pv > 0:
                if ally.attacking:
                    ally.draw_atk("Attaque_Frontale",self.current_ennemy.pos)
        for i in range(len(self.persos_ennemy)):
            ennemy=self.persos_ennemy[i]
            if ennemy.pv > 0:
                if ennemy.attacking:
                    ennemy.draw_atk("Attaque_Frontale",self.perso_player.pos)

    def draw_number(self,screen):
        if self.is_number_damage:
            col = self.ROUGE
        else:
            col = self.VERT_VIE
        text = self.police_degats.render(str(self.number),False,col)
        screen.blit(text,self.number_pos)



    def draw (self,screen):
        screen.blit(self.bg,(0,0))
        text_tour = self.police_display.render(f'Tour {self.tour}',False,self.BLANC)
        screen.blit(text_tour,(790,0))
        if self.action == "ennemies":
            screen.blit(self.ennemy_turn_text,self.any_turn_text_pos)
        else:
            screen.blit(self.player_turn_text,self.any_turn_text_pos)
        self.draw_persos(screen)
        if self.display_number:
            self.draw_number(screen)
        self.draw_panel(screen)

        screen.blit(self.attaque_frontale_box, (15, 200))
        screen.blit(self.attaque_special_box, (15, 320))
        
        pygame.display.flip()
    
    def run(self,screen,bg_name,perso_player:Perso,allies:List[Perso],persos_ennemy:List[Perso],potions:int):
        self.load(bg_name,perso_player,allies,persos_ennemy,potions)

        while self.continuer:
            self.handle_imput()
            self.update()
            self.draw(screen)
            self.clock.tick(60)

if __name__ == "__main__":
    no_weapon = Weapon(name="no_weapon",weapon_damage=0)
    op_weapon = Weapon(name='op_weapon',weapon_damage=10)
    Musashi = Perso("Musashi",100,op_weapon,(200,200))
    guerrier_takahiro = Perso('Musashi',70,no_weapon,(200, 200))
    guerrier_takahiro2 = Perso('Musashi', 70,no_weapon,(200, 200))
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    pygame.display.set_caption("Kage no Michi - Système de combat TPT")
    Fight().run(screen,'ine1',Musashi,[],[guerrier_takahiro,guerrier_takahiro2],3)
    pygame.quit()
