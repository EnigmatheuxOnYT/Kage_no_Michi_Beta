
'''
Persos pouvant être utilisées dans le Combat TPT et fonctions
'''

import pygame
import Mini_jeu_TPT_Créateur

class Weapon:
    name : str
    weapon_damage : int

class Perso:
    """
    Classe représentant un personnage du jeu.
    """
    def __init__(self, name, pv_max, weapon, nouvelle_taille: tuple,level=1): #Toutes les variables nécessaires pour la création d'un personnage
        self.name = name #Son nom, ATTENTION LE NOM DEFINIT LE SPRITE CHOISI !!
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

    from Mini_jeu_TPT_Créateur import BaseGameDisplay, image_base,screen

    def draw(self, destination: tuple):
        """
        Affiche le personnage à une position donnée.
        """
        screen.blit(self.image, destination) #Affichage du personnage choisi
    
    def draw_animations(self,attaque_choisi:str,ennemi_position:tuple,orientation:str):

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

            image_base.draw_prepare_animations(self)
            self.image = pygame.transform.scale(self.animations_combat[i], (200,200))
            if orientation == "gauche":
                self.image = pygame.transform.flip(self.image, True, False)
            screen.blit(self.image,(self.x,self.y))
            
            if i >= 2:
                image_attaque = pygame.transform.scale(self.animations_attaques[i-2],(200,200))
                screen.blit(image_attaque, ennemi_position)

            pygame.display.update()
            pygame.time.delay(40) #Pause d'intervalle entre les différents animations

        image_base.draw_normal()

class Ennemy(Perso):
    def __init__ (self,name, pv_max, weapon, nouvelle_taille: tuple,level):
        Perso.__init__(self,name, 0, 0, pv_max, weapon, nouvelle_taille,level)


#Armes à disposition
no_weapon = Weapon(name = "weapon_modification", weapon_damage = 0)
op_weapon = Weapon(name='op_weapon',weapon_damage=100)
tengoku_no_ikari = Weapon(name = 'Tengoku No Ikari', weapon_damage = 20)
wood_katana = Weapon(name="wood_katana",weapon_damage=5)

#Personnages qui peuvent combattre
Musashi = Perso(f"Musashi",100,op_weapon,(200,200)) #Coordonnées x et y de Musashi: 400,350
guerrier_takahiro = Perso('Musashi', 70,no_weapon,(200, 200)) #Coordonnées x et y de guerrier takahiro: 700, 350
guerrier_takahiro2 = Perso('Musashi', 70,no_weapon,(200, 200)) #Coordonnées x et y de guerrier takahiro 2: 850, 350
ma_Juzo = Perso('Ma_Juzo',200, 150, tengoku_no_ikari,10)

print(ma_Juzo.level)