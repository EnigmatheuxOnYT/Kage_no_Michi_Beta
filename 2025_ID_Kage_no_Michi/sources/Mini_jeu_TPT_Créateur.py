#############################################
# Combat TPT - Jeu de Combat Tour par Tour  #
#############################################
# test commit
# -----------------------------
# 1. Importation et Initialisation
# -----------------------------
import pygame
import random
import time
from dataclasses import dataclass
from typing import List
import Combat_TPT_Persos_Data_Module

pygame.init()

# -----------------------------
# 2. Configuration et Constantes
# -----------------------------
# Dimensions de la fenêtre
LONGUEUR_ECRAN = 1280              # Largeur de la fenêtre
PANEL_HEIGHT = 180                 # Hauteur du panneau (zone d'infos en bas)
HAUTEUR_TOTALE = 540 + PANEL_HEIGHT  # Hauteur totale de la fenêtre

FPS = 60                           # Images par seconde

# Définition des couleurs (R, G, B)
VERT = (0, 140, 70)
VERT_VIE = (90, 180, 130)
PINK = (240, 120, 174)
ROUGE = (255, 0, 0)
BLANC = (255, 255, 255)

# -----------------------------
# 3. Création de la Fenêtre et Horloge
# -----------------------------
screen = pygame.display.set_mode((LONGUEUR_ECRAN, HAUTEUR_TOTALE))
pygame.display.set_caption("Mini-Jeu Combat Tour par Tour")
clock = pygame.time.Clock()

# -----------------------------
# 4. Chargement des Ressources Graphiques
# -----------------------------
# Fond d'écran et panneau de dialogue
fond = pygame.image.load("../data/assets/bgs/Fond_Ine_Dojo_Arene_1.png").convert_alpha()
panel_affichage = pygame.image.load("../data/assets/minigm/Parchemin_Question.png").convert_alpha()

# Polices d'écriture
police_base = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf", 30)
police_display = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf", 49)
police_degats = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf", 40)

# Images des objets (ex : potion de soin)
potion_image = pygame.image.load("../data/assets/minigm/potion_de_soin.png").convert_alpha()
potion_image = pygame.transform.scale(potion_image, (80, 80))

# Images des boutons d'attaque (interface utilisateur)
attaque_frontale_box = pygame.image.load("../data/assets/minigm/Attaque_Frontale_V1.png").convert_alpha()
attaque_special_box = pygame.image.load("../data/assets/minigm/Attaque_Speciale_V1.png").convert_alpha()

# Définition des zones cliquables (hitboxes)
attaque_frontale_hitbox = pygame.Rect(15, 350, 100, 100)
attaque_special_hitbox = pygame.Rect(15, 470, 100, 100)
potion_hitbox = pygame.Rect(500, 600, 80, 80)
affichage_display = pygame.Rect(0,0,LONGUEUR_ECRAN,50)

# -----------------------------
# 5. Variables de Jeu
# -----------------------------
nombre_ennemi = 2                   # Nombre d'ennemis
attaque_frontale_compteur = 0       # Compteur d'attaques de base (pour débloquer l'attaque spéciale)
action = 1                          # Indique si le joueur peut agir (1 = oui, 0 = non)
potion = 3                          # Nombre de potions disponibles

# Dégâts aléatoires pour les attaques
attaque_frontale = random.randint(5, 10)
attaque_special = random.randint(10, 30)

# Variables pour gérer le temps (pour le cooldown des attaques ennemies)
cooldown_ennemi = 1000  # 1 seconde de cooldown
dernier_temps_attaque = 0
ennemi_peut_attaquer = False
tour = 1

# -----------------------------
# 6. Fonctions Utilitaires
# -----------------------------
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
    screen.blit(panel_affichage, (0, HAUTEUR_TOTALE - PANEL_HEIGHT))
    draw_text(f'Musashi PV: {Musashi.pv}', police_base, VERT, 100, HAUTEUR_TOTALE - PANEL_HEIGHT + 70)
    draw_text(f'Guerrier Takahiro PV: {guerrier_takahiro.pv}', police_base, PINK, 700, HAUTEUR_TOTALE - PANEL_HEIGHT + 70)
    draw_text(f'Guerrier Takahiro PV: {guerrier_takahiro2.pv}', police_base, PINK, 700, HAUTEUR_TOTALE - PANEL_HEIGHT + 120)

def debounce(cooldown: float):
    """
    Hyp: la fonction debounce met en pause pendant une durée (en secondes) afin de ralentir l'exécution pour mieux visualiser l'action.
    """
    start_time = time.time()
    while time.time() - start_time < cooldown:
        pass

def changer_orientation_sprite(sprite):

    return pygame.transform.flip(sprite,True,False)

# -----------------------------
# 7. Définition des Classes
# -----------------------------
class BaseGameDisplay:
    """
    Classe qui gère l'affichage de base du jeu (fond, panneaux, boutons, etc.).
    """
    def __init__(self, screen, fond, attaque_frontale_box, attaque_special_box, potion_image, hauteur_totale, panel, barres_vie, persos_combat,affichage_display,tour:int):
        self.screen = screen #L'écran tout simplement
        self.fond = fond #Le fond actuel
        self.attaque_frontale_box = attaque_frontale_box
        self.attaque_special_box = attaque_special_box
        self.potion_image = potion_image
        self.hauteur_totale = hauteur_totale
        self.panel = panel
        self.barres_vie = barres_vie
        self.persos_combat = persos_combat
        self.affichage_display = affichage_display
        self.tour = tour

    def draw_normal(self,action):
        """
        Redessine tous les éléments statiques du jeu.
        """
        self.screen.blit(self.fond, (0, 0))
        affichage_panel()
        
        self.screen.blit(self.attaque_frontale_box, (15, 350))
        self.screen.blit(self.attaque_special_box, (15, 470))
        self.screen.blit(self.potion_image, (500, 600))
        for perso in self.persos_combat:
            if perso.pv > 0:
                perso.image = pygame.transform.scale(perso.image, (200,200))
                screen.blit(perso.image, (perso.x, perso.y))
            for barre in barres_vie:
                barre.draw(barre.pv)
        
        self.screen.blit(potion_image, (500, 600))
        pygame.draw.rect(self.screen, (0,0,0), affichage_display)
        draw_text(str(potion),police_base, (0,0,0),535,680)
        draw_text(f'Tour {tour}',police_display, (255,255,255), LONGUEUR_ECRAN/2+250,0)
        if action == 0:
            draw_text("Au tour de l'ennemi!", police_display, (255,255,255),LONGUEUR_ECRAN/2-450,0)
        else:
            draw_text("Au tour du joueur!", police_display, (255,255,255),LONGUEUR_ECRAN/2-450,0)
        
        pygame.display.update()

    def draw_prepare_animations(self,perso_choisi,action):

        '''
        Permet l'affichage des aniamtions dans le jeu, où on redesinne l'écran 
        '''

        self.screen.blit(self.fond, (0, 0))
        affichage_panel()
        self.screen.blit(self.attaque_frontale_box, (15, 350))
        self.screen.blit(self.attaque_special_box, (15, 470))
        self.screen.blit(self.potion_image, (500, 600))
        for perso in self.persos_combat:
            if perso != perso_choisi and perso.pv > 0 :
                perso.image = pygame.transform.scale(perso.image, (200,200))
                screen.blit(perso.image, (perso.x, perso.y))
                for barre in barres_vie:
                    barre.draw(barre.pv)
        
        self.screen.blit(potion_image, (500, 600))
        pygame.draw.rect(self.screen, (0,0,0), affichage_display)
        draw_text(str(potion),police_base, (0,0,0),535,680)
        draw_text(f'Tour {tour}',police_display, (255,255,255), LONGUEUR_ECRAN/2+250,0)
        if action == 0:
            draw_text("Au tour de l'ennemi!", police_display, (255,255,255),LONGUEUR_ECRAN/2-450,0)
        else:
            draw_text("Au tour du joueur!", police_display, (255,255,255),LONGUEUR_ECRAN/2-450,0)

@dataclass
class Weapon:
    name : str
    weapon_damage : int


class Perso:
    """
    Classe représentant un personnage du jeu.
    """
    def __init__(self, name, x, y, pv_max, weapon, nouvelle_taille: tuple,level=1): #Toutes les variables nécessaires pour la création d'un personnage
        self.name = name #Son nom
        self.x = x #La position x du sprite
        self.y = y #La position y du sprite
        self.pv_max = pv_max #Ses hp max
        self.pv = pv_max #Ses pv, qui vont prendre tout simplement la valeur de ses pvs
        self._base_damage = 5
        self.weapon = weapon
        self.level = level #niveau du personnage
        sprite = pygame.image.load(f"../data/assets/sprites/{self.name}_Idle.png") #Le spirte quand il reste immobile
        self.image = pygame.transform.scale(sprite, nouvelle_taille) #On redimensionne le sprite de sorte à ce que ça soit cohérent avec le fond
        self.animations_combat = [
            pygame.image.load(f"../data/assets/sprites/{self.name}_Combat_1.png"),
            pygame.image.load(f"../data/assets/sprites/{self.name}_Combat_2.png"),
            pygame.image.load(f"../data/assets/sprites/{self.name}_Combat_3.png"),
            pygame.image.load(f"../data/assets/sprites/{self.name}_Combat_4.png"),
            pygame.image.load(f"../data/assets/sprites/{self.name}_Combat_5.png"),
            pygame.image.load(f"../data/assets/sprites/{self.name}_Combat_6.png"),
            pygame.image.load(f"../data/assets/sprites/{self.name}_Combat_7.png"),
            pygame.image.load(f"../data/assets/sprites/{self.name}_Combat_8.png"),
            pygame.image.load(f"../data/assets/sprites/{self.name}_Combat_9.png"),
            pygame.image.load(f"../data/assets/sprites/{self.name}_Combat_10.png"),
            sprite
        ] #Tous les sprites présents lors de l'animation d'attaque

    @property
    def current_damage(self):return self._base_damage+self.weapon.weapon_damage
    
    def level_up (self):
        self.level+=1
        self.pv_max=round(self.pv_max*1.1,0)
        self.base_damage=round(self._base_damage*1.1,0)
    
    def change_weapon (self,weapon):
        self.weapon=weapon

    def draw(self, destination: tuple):
        """
        Affiche le personnage à une position donnée.
        """
        screen.blit(self.image, destination) #Affichage du personnage choisi
    
    def draw_animations(self,attaque_choisi:str,ennemi_position:tuple,orientation:str):

        image_base = BaseGameDisplay(screen, fond, attaque_frontale_box, attaque_special_box,potion_image, HAUTEUR_TOTALE, PANEL_HEIGHT, barres_vie, persos_combat,affichage_display)
        self.animations_attaques = [
            pygame.image.load(f"../data/assets/sprites/{attaque_choisi}_1_V1.png"),
            pygame.image.load(f"../data/assets/sprites/{attaque_choisi}_2_V1.png"),
            pygame.image.load(f"../data/assets/sprites/{attaque_choisi}_3_V1.png"),
            pygame.image.load(f"../data/assets/sprites/{attaque_choisi}_4_V1.png"),
            pygame.image.load(f"../data/assets/sprites/{attaque_choisi}_5_V1.png"),
            pygame.image.load(f"../data/assets/sprites/{attaque_choisi}_6_V1.png"),
            pygame.image.load(f"../data/assets/sprites/{attaque_choisi}_7_V1.png"),
            pygame.image.load(f"../data/assets/sprites/{attaque_choisi}_8_V1.png"),
            pygame.image.load(f"../data/assets/sprites/{attaque_choisi}_9_V1.png")
        ]


        for i in range(len(self.animations_combat)): #Parcourt les animations correspondant au personnage choisi

            image_base.draw_prepare_animations(self,action)
            self.image = pygame.transform.scale(self.animations_combat[i], (200,200))
            if orientation == "gauche":
                self.image = pygame.transform.flip(self.image, True, False)
            screen.blit(self.image,(self.x,self.y))
            
            if i >= 2:
                image_attaque = pygame.transform.scale(self.animations_attaques[i-2],(200,200))
                screen.blit(image_attaque, ennemi_position)

            pygame.display.update()
            pygame.time.delay(40) #Pause d'intervalle entre les différents animations

        image_base.draw_normal(action)

class Ennemy(Perso):
    def __init__ (self,name, pv_max, weapon, nouvelle_taille: tuple,level):
        Perso.__init__(self,name, 0, 0, pv_max, weapon, nouvelle_taille,level)

class BarreVie: #Définit la barre de vie des personnages
    """
    Classe pour afficher la barre de vie d'un personnage.
    """
    def __init__(self, x, y, pv, pv_max): #Les proprités nécessaires pour la création d'une barre de vie
        self.x = x #La position x de la barre de vie, à ajuster au cours de son réutilisation
        self.y = y #La position y de la barre de vie, à ajuster au cours de son réutilisation
        self.pv = pv #Définit les pv de tel personnage
        self.pv_max = pv_max #Définit les pv maximum de tel personnage

    def draw(self, pv):
        """
        Met à jour et dessine la barre de vie en fonction des PV restants.
        """
        self.pv = pv #Différence entre les pvs 
        ratio = self.pv / self.pv_max #Différence entre les pvs actuel et les pv maxs
        pygame.draw.rect(screen, ROUGE, (self.x, self.y, 300, 25)) #Les pvs qui ont été enlevé dans la barre d'hp
        pygame.draw.rect(screen, VERT_VIE, (self.x, self.y, 300 * ratio, 25))

class Degats(pygame.sprite.Sprite):
    """
    Classe pour afficher les dégâts infligés sous forme de texte.
    """

    def update(self):
        """
        Met à jour l'affichage des dégâts et supprime l'objet après un certain temps.
        """
        self.counter += 1
        if self.counter > 100:
            self.kill()

    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.font = police_degats
        self.image = self.font.render(str(damage), True, color)
        self.rect = self.image.get_rect(center=(x, y))
        self.counter = 0
        screen.blit(self.image, self.rect)
        pygame.display.update()
        self.update()

# -----------------------------
# 8. Création des Personnages et des Barres de Vie
# -----------------------------

no_weapon = Weapon(name="no_weapon",weapon_damage=0)
op_weapon = Weapon(name='op_weapon',weapon_damage=10)


Musashi = Perso(f"Musashi",400,350,100,op_weapon,(200,200))
guerrier_takahiro = Perso('Musashi', 700, 350, 70,no_weapon,(200, 200))
guerrier_takahiro.image = changer_orientation_sprite(guerrier_takahiro.image)
guerrier_takahiro2 = Perso('Musashi', 850, 350, 70,no_weapon,(200, 200))
guerrier_takahiro2.image = changer_orientation_sprite(guerrier_takahiro2.image)
# -----------------------------
# 9. Boucle Principale du Jeu
# -----------------------------
def main(perso_player:Perso,allies:List[Perso],persos_ennemy:List[Perso]):
    nombre_ennemi=len(persos_ennemy)
    nombre_joueurs=len(allies)+1
    modifieur_dégats = 5

    #On va ici reprendre les barres de vie de sorte à ce qu'on puisse les intégrer dans l'interface du parchemin
    barres_vie = []

    perso_player_barrevie = BarreVie(100, HAUTEUR_TOTALE - PANEL_HEIGHT + 100, persos_player.pv, persos_player.pv_max)
    barres_vie.append(perso_player_barrevie)

    y = 150
    for allie in allies:
        allie_barre_vie = BarreVie(100, HAUTEUR_TOTALE - PANEL_HEIGHT +y, allie.pv, allie.pv_max)
        barres_vie.append(allie_barre_vie)
        y += 20

    for ennemi in persos_ennemy:
        ennemy_barre_vie = BarreVie(700, HAUTEUR_TOTALE - PANEL_HEIGHT + 100, ennemy.pv, ennemy.pv_max)

    global action, potion, attaque_frontale_compteur, attaque_frontale, attaque_special,persos_combat,image_base
    global dernier_temps_attaque, ennemi_peut_attaquer,tour

    continuer = True
    click_cooldown = False

    # Création de l'affichage de base
    image_base = BaseGameDisplay(screen, fond, attaque_frontale_box, attaque_special_box,potion_image, HAUTEUR_TOTALE, PANEL_HEIGHT, barres_vie, persos_combat,affichage_display,action)

    while continuer:
        # Redessine l'affichage de base
        image_base.draw_normal(action)
        clock.tick(FPS)
       
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False

            # Si le joueur peut agir
            if action == 1:
                if event.type == pygame.MOUSEBUTTONUP and click_cooldown == False:
                    click_cooldown = True

                    #Utilisation de la potion
                    if potion_hitbox.collidepoint(event.pos) and potion > 0:
                        if perso_player.pv < 80:
                            soins_necessaire = 30
                            perso_player.pv += soins_necessaire
                            Degats(perso_player.x + 30, perso_player.y+50, soins_necessaire, VERT_VIE) #Affichage des dégâts
                            potion -= 1
                            action = 0
                            perso_player.draw(perso_player.pv)
                        else: #Si le pv du joueur est au-dessus des pv données par la potion
                            soins_necessaire = 100 - perso_player.pv
                            perso_player.pv += soins_necessaire
                            Degats(perso_player.x+30, perso_player.y+50, soins_necessaire, VERT_VIE) #Affichage des dégâts
                            potion -= 1
                            action = 0
                            perso_player.draw(perso_player.pv)
                        ennemi_peut_attaquer = False

                    # Attaque frontale
                    if attaque_frontale_hitbox.collidepoint(event.pos) and ennemi_peut_attaquer:
                        if persos_ennemy[0].pv > 0: #Il doit forcément y avoir un ennemi à affronter
                            perso_player.draw_animations("Attaque_Frontale",(guerrier_takahiro.x,guerrier_takahiro.y),"droite")
                            attaque_frontale = random.randint(perso_player.current_damage-modifieur_dégats,perso_player.current_damage+modifieur_dégats)
                            Degats(guerrier_takahiro.x+30, guerrier_takahiro.y+50, attaque_frontale, ROUGE) #Affichage des dégâts
                            guerrier_takahiro.pv -= attaque_frontale
                            barres_vie[len()].draw(guerrier_takahiro.pv)
                            attaque_frontale_compteur += 1
                            action = 0
                        elif len(persos_ennemy) == 2:
                            if persos_ennemy[1].pv > 0:
                                perso_player.draw_animations("Attaque_Frontale",(guerrier_takahiro2.x,guerrier_takahiro2.y),"droite")
                                attaque_frontale = random.randint(perso_player.current_damage-modifieur_dégats,perso_player.current_damage+modifieur_dégats)
                                Degats(guerrier_takahiro2.x+30, guerrier_takahiro2.y+50, attaque_frontale, ROUGE)
                                guerrier_takahiro2.pv -= attaque_frontale
                                guerrier_takahiro2_barre_vie.draw(guerrier_takahiro2.pv)
                                attaque_frontale_compteur += 1
                                action = 0
                                nombre_ennemi = 1
                        dernier_temps_attaque = pygame.time.get_ticks()
                        ennemi_peut_attaquer = False

                    # Attaque spéciale (se déclenche après 4 attaques de base)
                    if attaque_special_hitbox.collidepoint(event.pos) and attaque_frontale_compteur >= 4 and ennemi_peut_attaquer:
                        if guerrier_takahiro.pv > 0:
                            perso_player.draw_animations("Attaque_Speciale", (guerrier_takahiro.x,guerrier_takahiro.y),"droite")
                            attaque_special = random.randint(10, 30)
                            Degats(guerrier_takahiro.x+30, guerrier_takahiro.y+50, attaque_special, ROUGE)
                            guerrier_takahiro.pv -= attaque_special
                            guerrier_takahiro_barre_vie.draw(guerrier_takahiro.pv)
                            attaque_frontale_compteur = 0
                            action = 0
                        else:
                            perso_player.draw_animations("Attaque_Speciale", (guerrier_takahiro2.x,guerrier_takahiro2.y),"droite")
                            attaque_special = random.randint(10, 30)
                            Degats(guerrier_takahiro2.x+30, guerrier_takahiro2.y+50, attaque_special, ROUGE)
                            guerrier_takahiro2.pv -= attaque_special
                            guerrier_takahiro2_barre_vie.draw(guerrier_takahiro2.pv)
                            attaque_frontale_compteur = 0
                            action = 0
                            nombre_ennemi = 1
                        ennemi_peut_attaquer = False
            
            for ennemy in persos_ennemy:
                if ennemy.pv < 0:
                    ennemy.pv = 0 #Pour éviter les pv négatifs
                    image_base.draw_normal(action)

                

            # Attaque des ennemis (s'exécute lorsque le joueur n'a plus d'action)
            if ennemi_peut_attaquer == False:
                ennemi_peut_attaquer = True  # Les ennemis peuvent attaquer après le cooldown
                debounce(0.3)
            if action == 0 and ennemi_peut_attaquer:
                degats_total = 0
                for ennemy in persos_ennemy:

                    if ennemy.pv > 0:
                        ennemy.draw_animations("Attaque_Frontale", (perso_player.x,perso_player.y), "gauche")
                        attaque_ennemis = random.randint(5,10)
                        degats_total += attaque_ennemis
                        perso_player.pv -= attaque_ennemis
                        Degats(perso_player.x+30, perso_player.y+50, degats_total, ROUGE)
                        Musashi_barre_vie.draw(ennemy.pv)
                        image_base.draw_normal
                        debounce(0.3)
                    else:
                        image_base.draw_normal(action)
                action = 1
                tour += 1

            # Fin du combat : victoire ou défaite
            compteur_ennemi_mort = 0
            for i in range(nombre_ennemi):
                ennemy=persos_ennemy[i]
                if ennemy.pv <= 0 :
                    compteur_ennemi_mort+=1
            if compteur_ennemi_mort==nombre_ennemi:
                print('WIN')
                pygame.time.delay(4000)
                continuer = False
            elif perso_player.pv < 1:
                print('LOSE')
                pygame.time.delay(4000)
                continuer = False

        pygame.display.flip()

        click_cooldown = False

    pygame.quit()

if __name__ == '__main__':
    main(Musashi,[],)
