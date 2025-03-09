
'''
Persos pouvant être utilisées dans le Combat TPT et fonctions
'''

import pygame
from dataclasses import dataclass

@dataclass
class Weapon:
    name : str
    weapon_damage : int
    special_damage : int
    crit_chance : float

class Perso:
    """
    Classe représentant un personnage du jeu.
    """
    def __init__(self, name:str, pv_max:int, weapon:Weapon,level:int=1,instance:int=0): #Toutes les variables nécessaires pour la création d'un personnage
        self.name = name+str(instance) #Son nom, ATTENTION LE NOM DEFINIT LE SPRITE CHOISI !!
        self.sprite_name = name
        self.pv_max = pv_max #Ses hp max
        self.pv = pv_max #Ses pv, qui vont prendre tout simplement la valeur de ses pvs
        self._base_damage = 2
        self.weapon = weapon
        self.level = 1 #niveau du personnage
        self.set_level(level)
        sprite = pygame.image.load(f"../data/assets/tpt/sprites/{self.sprite_name}_Idle.png") #Le spirte quand il reste immobile
        self.image = pygame.transform.scale(sprite, (200,200)) #On redimensionne le sprite de sorte à ce que ça soit cohérent avec le fond
        self.rect = self.image.get_rect()
        self.rect.width = 100
        self.atk_frame_lengh = 80
        self.debut_frame = 0
        self.orientation="gauche"
        self.pos=(0,0)
        self.attacking=False
        self.animations_combat = [
            pygame.image.load(f"../data/assets/tpt/sprites/{self.sprite_name}_Combat_1.png"),
            pygame.image.load(f"../data/assets/tpt/sprites/{self.sprite_name}_Combat_2.png"),
            pygame.image.load(f"../data/assets/tpt/sprites/{self.sprite_name}_Combat_3.png"),
            pygame.image.load(f"../data/assets/tpt/sprites/{self.sprite_name}_Combat_4.png"),
            pygame.image.load(f"../data/assets/tpt/sprites/{self.sprite_name}_Combat_5.png"),
            pygame.image.load(f"../data/assets/tpt/sprites/{self.sprite_name}_Combat_6.png"),
            pygame.image.load(f"../data/assets/tpt/sprites/{self.sprite_name}_Combat_7.png"),
            pygame.image.load(f"../data/assets/tpt/sprites/{self.sprite_name}_Combat_8.png"),
            pygame.image.load(f"../data/assets/tpt/sprites/{self.sprite_name}_Combat_9.png"),
            pygame.image.load(f"../data/assets/tpt/sprites/{self.sprite_name}_Combat_10.png"),
            sprite
        ] #Tous les sprites présents lors de l'animation d'attaque

        self.index = 0
        self.max_index = 10

    @property
    def current_damage(self):return max(self._base_damage+self.weapon.weapon_damage,0)
    @property
    def is_ko (self):return False if self.pv>0 else True
    
    def level_up (self):
        self.level+=1
        self.pv_max=int(round(self.pv_max*1.1,0))
        self._base_damage=max(int(round(self._base_damage*1.1,0)),self._base_damage+1)
        self.pv = self.pv_max
    
    def set_level (self,level):
        diff = max(level-self.level,0)
        for i in range(diff):
            self.level_up()
    
    def hit (self,damage):
        self.pv = max(self.pv-damage,0)
    
    def change_weapon (self,weapon):self.weapon=weapon
    
    def set_orientation(self,new_orientation):self.orientation=new_orientation

    def set_pos(self,pos):
        self.pos=pos
        self.rect.midtop = pos[0]+100,pos[1]

    def set_attacking(self,val):self.attacking=val

    def draw_static(self,screen):
        """
        Affiche le personnage à une position donnée.
        """
        if self.orientation == 'gauche':
            image = pygame.transform.flip(self.image,True,False)
        else:
            image=self.image
        screen.blit(image, self.pos) #Affichage du personnage choisi
    
    def draw_atk(self,screen,attaque_choisie:str,ennemi_position:tuple):
        self.animations_attaque = [
            pygame.image.load(f"../data/assets/tpt/sprites/{attaque_choisie}_1_V1.png"),
            pygame.image.load(f"../data/assets/tpt/sprites/{attaque_choisie}_2_V1.png"),
            pygame.image.load(f"../data/assets/tpt/sprites/{attaque_choisie}_3_V1.png"),
            pygame.image.load(f"../data/assets/tpt/sprites/{attaque_choisie}_4_V1.png"),
            pygame.image.load(f"../data/assets/tpt/sprites/{attaque_choisie}_5_V1.png"),
            pygame.image.load(f"../data/assets/tpt/sprites/{attaque_choisie}_6_V1.png"),
            pygame.image.load(f"../data/assets/tpt/sprites/{attaque_choisie}_7_V1.png"),
            pygame.image.load(f"../data/assets/tpt/sprites/{attaque_choisie}_8_V1.png"),
            pygame.image.load(f"../data/assets/tpt/sprites/{attaque_choisie}_9_V1.png")
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
                image = pygame.transform.flip(image, True, False)
            screen.blit(image,(self.pos))
            if self.index >= 2:
                image_attaque = pygame.transform.scale(self.animations_attaque[self.index-2],(200,200))
                if self.orientation == "gauche":
                    image_attaque = pygame.transform.flip(image_attaque, True, False)
                screen.blit(image_attaque, ennemi_position)
        else:
            self.draw_static(screen)

class Ennemy(Perso):
    def __init__ (self,name, pv_max, weapon, nouvelle_taille: tuple,level):
        Perso.__init__(self,name, 0, 0, pv_max, weapon, nouvelle_taille,level)

class Fight_assets:
    def __init__(self):
        #Armes à disposition
        self.tengoku_no_ikari = Weapon(name = 'Tengoku No Ikari', weapon_damage = 20,special_damage=10,crit_chance=0.1)
        self.wood_katana = Weapon(name="wood_katana",weapon_damage=5,special_damage=5,crit_chance=0.05)
        self.no_weapon = Weapon(name="no_weapon",weapon_damage=0,special_damage=0,crit_chance=0)
        self.op_weapon = Weapon(name='op_weapon',weapon_damage=10,special_damage=15,crit_chance=0.25)
        self.Musashi = Perso("Musashi",10,self.op_weapon,level = 10)
        self.guerrier_takahiro = Perso('Soldat1',70,self.no_weapon)
        self.guerrier_takahiro2 = Perso('Soldat1', 70,self.no_weapon)
        #self.ma_Juzo = Perso('Ma_Juzo',200, self.tengoku_no_ikari,level=10)

if __name__ == "__main__":
        fight_assets = Fight_assets()
        print(fight_assets.ma_Juzo.level)