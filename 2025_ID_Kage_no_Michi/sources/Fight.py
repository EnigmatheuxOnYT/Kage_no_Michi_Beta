#Projet : Kage no Michi
#Auteurs : Alptan Korkmaz, Clément Roux--Bénabou, Maxime Rousseaux, Ahmed-Adam Rezkallah, Cyril Zhao


# -*- coding: utf-8 -*-
"""
Created on Fri Mar 07 23:18:22 2025

@author: clementroux--benabou
"""

import pygame
from Mini_jeu_TPT_Créateur import *

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
        self.fond = pygame.image.load("../data/assets/bgs/Fond_Ine_Dojo_Arene_1.png").convert_alpha()
        self.panel_affichage = pygame.image.load("../data/assets/minigm/Parchemin_Question.png").convert_alpha()

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
        self.attaque_frontale_hitbox = pygame.Rect(15, 350, 100, 100)
        self.attaque_special_hitbox = pygame.Rect(15, 470, 100, 100)
        self.potion_hitbox = pygame.Rect(500, 600, 80, 80)
        self.affichage_display = pygame.Rect(0,0,1280,50)

        self.continuer = True
        self.click_cooldown = False

        sprites_coordinates = [(400,350),(700, 350),(850, 350)]



    
    def draw_text(text, font, text_color, x, y):
        """
        Affiche du texte sur l'écran.
        """
        img = font.render(text, True, text_color)
        screen.blit(img, (x, y))

    def affichage_panel():
        """
        Affiche le panneau de dialogue et les points de vie des personnages.
        """
        screen.blit(panel_affichage, (0, 540))
        draw_text(f'Musashi PV: {Musashi.pv}', police_base, VERT, 100, 610)
        draw_text(f'Guerrier Takahiro PV: {guerrier_takahiro.pv}', police_base, PINK, 700, 610)
        draw_text(f'Guerrier Takahiro PV: {guerrier_takahiro2.pv}', police_base, PINK, 700, 660)

    def debounce(cooldown: float):
        """
        Hyp: la fonction debounce met en pause pendant une durée (en secondes) afin de ralentir l'exécution pour mieux visualiser l'action.
        """
        start_time = time.time()
        while time.time() - start_time < cooldown:
            pass

    def changer_orientation_sprite(sprite):return pygame.transform.flip(sprite,True,False)

    def load (self,perso_player:Perso,allies:List[Perso],persos_ennemy:List[Perso],potions:int):
        # Variables de Jeu
        self.perso_player=perso_player
        self.allies=allies
        self.persos_ennemy = persos_ennemy
        self.nombre_ennemi = len(persos_ennemy)
        self.attaque_frontale_compteur = 0
        self.action = 1
        self.potion = potions
        self.modifieur_degats = 5
        self.modifieur_degats_spe = 15

        # Dégâts aléatoires pour les attaques
        self.attaque_frontale = random.randint(perso_player.current_damage-self.modifieur_degats,perso_player.current_damage+self.modifieur_degats)
        self.attaque_special = random.randint(perso_player.current_damage+self.modifieur_degats,perso_player.current_damage+self.modifieur_degats+self.modifieur_degats_spe)

        self.display_damage=False
        self.damage_duration=2000
        self.in_atk=False
        self.atk_info = {'attacker':None,'atk_type':None,'defender':None}
        self.atk_index=0

        # Variables pour gérer le temps (pour le cooldown des attaques ennemies)
        self.cooldown_ennemi = 1000  # 1 seconde de cooldown
        self.dernier_temps_attaque = 0
        self.ennemi_peut_attaquer = False
        self.tour = 1

        self.click_cooldown = False

        barres_vie = {}
        self.perso_player_barrevie = BarreVie(100,640, self.perso_player.pv, self.perso_player.pv_max)

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


    def handle_imput (self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.continuer=False
                pygame.event.post(event)
            
            # Si le joueur peut agir
            if self.action == 1:
                if event.type == pygame.MOUSEBUTTONUP and self.click_cooldown == False:
                    self.click_cooldown = True

                    #Utilisation de la potion
                    if potion_hitbox.collidepoint(event.pos) and self.potion > 0:
                        self.potion -= 1
                        self.action = 0
                        if self.perso_player.pv < 80:
                            soins_necessaire = 30
                            Degats(self.perso_player.x + 30, self.perso_player.y+50, soins_necessaire, self.VERT_VIE) #Affichage des dégâts
                            self.perso_player_barrevie.draw(self.perso_player.pv)
                        else: #Si le pv du joueur est au-dessus des pv données par la potion
                            soins_necessaire = 100 - self.perso_player.pv
                            Degats(self.perso_player.x+30, self.perso_player.y+50, soins_necessaire, self.VERT_VIE) #Affichage des dégâts
                            self.perso_player_barrevie.draw(self.perso_player.pv)
                        self.perso_player.pv += soins_necessaire
                        self.ennemi_peut_attaquer = False

                    # Attaque frontale
                    if attaque_frontale_hitbox.collidepoint(event.pos) and self.ennemi_peut_attaquer:
                        attaque_effectuee = False
                        for ennemy in self.persos_ennemy:
                            if ennemy.pv >0 and not attaque_effectuee:
                                self.perso_player.draw_animations("Attaque_Frontale",(ennemy.x,ennemy.y),"droite")
                                attaque_frontale = random.randint(self.perso_player.current_damage-self.modifieur_dégats,self.perso_player.current_damage+self.modifieur_dégats)
                                Degats(ennemy.x+30, ennemy.y+50, attaque_frontale, ROUGE) #Affichage des dégâts
                                ennemy.pv -= attaque_frontale
                                self.ennemi_peut_attaquer[ennemy.name].draw(ennemy.pv)
                                self.attaque_frontale_compteur += 1
                                self.action = 0
                                attaque_effectuee=True
                        self.dernier_temps_attaque = pygame.time.get_ticks()
                        self.ennemi_peut_attaquer = False

                    # Attaque spéciale (se déclenche après 4 attaques de base)
                    if attaque_special_hitbox.collidepoint(event.pos) and self.attaque_frontale_compteur >= 4 and self.ennemi_peut_attaquer:
                        for ennemy in self.persos_ennemy:
                            if ennemy.pv >0 and not attaque_effectuee:
                                self.perso_player.draw_animations("Attaque_Speciale", (ennemy.x,ennemy.y),"droite")
                                attaque_special = random.randint(10, 30)
                                Degats(ennemy.x+30, ennemy.y+50, attaque_special, ROUGE)
                                ennemy.pv -= attaque_special
                                self.ennemies_barres_vie[ennemy.name].draw(ennemy.pv)
                                self.attaque_frontale_compteur = 0
                                self.action = 0
                        self.ennemi_peut_attaquer = False
    
    def update (self):
        # Fin du combat : victoire ou défaite
        compteur_ennemi_mort = 0
        for i in range(nombre_ennemi):
            ennemy=self.persos_ennemy[i]
            if ennemy.pv <= 0 :
                compteur_ennemi_mort+=1
        if compteur_ennemi_mort==nombre_ennemi:
            print('WIN')
            self.continuer = False
        elif self.perso_player.pv <= 0:
            print('LOSE')
            self.continuer = False


    def draw (self,screen):
        pygame.display.flip()
    
    def run(self,screen,perso_player:Perso,allies:List[Perso],persos_ennemy:List[Perso],potions:int):
        self.load(perso_player,allies,persos_ennemy,potions)

        while self.continuer:
            self.handle_imput()
            self.update()
            self.draw(screen)
            self.clock.tick(60)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    pygame.display.set_caption("Kage no Michi - Système de combat TPT")
    Fight().run()
    pygame.quit()
