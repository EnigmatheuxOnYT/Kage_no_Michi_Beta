
#Projet : Kage no Michi
#Auteurs : Alptan Korkmaz, Maxime Rousseaux, Ahmed-Adam Rezkallah, Clément Roux--Bénabou, Cyril Zhao


'''
Persos pouvant être utilisées dans le Combat TPT et fonctions
'''

import pygame
from dataclasses import dataclass

@dataclass
class Weapon:
    name : str
    weapon_damage : int
    special_damage : int = 0
    crit_chance : float = 0

class Perso:
    """
    Classe représentant un personnage du jeu.
    """
    def __init__(self, name:str,spritename:str,atk_length:int, pv_max:int, weapon:Weapon,level:int=1,instance:int=0): #Toutes les variables nécessaires pour la création d'un personnage
        self.name = name #Son nom
        self.sprite_name = spritename
        self.pv_max = pv_max #Ses hp max
        self.__base_pv_max = pv_max
        self.pv = pv_max #Ses pv, qui vont prendre tout simplement la valeur de ses pvs
        self._base_damage = 2
        self.weapon = weapon
        self.level = 1 #niveau du personnage
        self.set_level(level)
        self.size=200
        sprite = pygame.image.load(f"../data/assets/tpt/sprites/{self.sprite_name}_Idle.png") #Le spirte quand il reste immobile
        self.image = pygame.transform.scale(sprite, (200,200)) #On redimensionne le sprite de sorte à ce que ça soit cohérent avec le fond
        self.rect = self.image.get_rect()
        self.sprite_rect = self.image.get_rect()
        self.rect.width = 100
        self.atk_frame_lengh = 80
        self.debut_frame = 0
        self.orientation="gauche"
        self.pos=(0,0)
        self.attacking=False
        self.atk_length = atk_length
        if self.atk_length==0:
            self.do_attacks=False
        else:
            self.do_attacks=True
        self.animations_combat=list()
        for i in range(self.atk_length):
            self.animations_combat.append(pygame.image.load(f"../data/assets/tpt/sprites/{self.sprite_name}_Combat_{i+1}.png"))
     
        self.index = 0
        self.max_index = self.atk_length
        self.instance = instance

    @property
    def current_damage(self):return self._base_damage+self.weapon.weapon_damage
    @property
    def is_ko (self):return False if self.pv>0 else True

    def wrapped (self):return [self.name,self.sprite_name,self.atk_length,self.__base_pv_max,[self.weapon.name,self.weapon.weapon_damage,self.weapon.special_damage,self.weapon.crit_chance],self.level,self.instance]

    def set_taille(self,size):
        self.size=size
        sprite = pygame.image.load(f"../data/assets/tpt/sprites/{self.sprite_name}_Idle.png") #Le spirte quand il reste immobile
        self.image = pygame.transform.scale(sprite, (size,size)) #On redimensionne le sprite de sorte à ce que ça soit cohérent avec le fond
        self.sprite_rect = self.image.get_rect()
        self.sprite_rect.center=self.pos
    
    def level_up (self):
        self.level+=1
        self.pv_max=int(round(self.pv_max*1.1,0))
        self._base_damage=max(int(round(self._base_damage*1.1,0)),self._base_damage+1)
        self.pv = self.pv_max
    
    def set_level (self,level):
        diff = max(level-self.level,0)
        for i in range(diff):
            self.level_up()
    
    def hit (self,damage:int):
        self.pv = max(self.pv-damage,0)
    
    def change_weapon (self,weapon):self.weapon=weapon
    
    def set_orientation(self,new_orientation):self.orientation=new_orientation

    def set_pos(self,pos):
        self.pos=pos
        self.rect.center = pos
        self.sprite_rect.center=pos

    def set_attacking(self,val):self.attacking=val

    def draw_static(self,screen):
        """
        Affiche le personnage à une position donnée.
        """
        if self.orientation == 'gauche':
            image = pygame.transform.flip(self.image,True,False)
        else:
            image=self.image
        screen.blit(image, self.sprite_rect) #Affichage du personnage choisi
    
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

        ennemy_rect = pygame.Rect(0,0,200,200)
        ennemy_rect.center = ennemi_position

        if self.index == 0 or self.atk_frame_lengh-pygame.time.get_ticks()+self.debut_frame<=0:
            self.index +=1
            if self.index>self.max_index:
                self.index=0
                self.attacking=False
            self.debut_frame = pygame.time.get_ticks()
        if self.index!=0:
            image = pygame.transform.scale(self.animations_combat[self.index-1], (self.size,self.size))
            if self.orientation == "gauche":
                image = pygame.transform.flip(image, True, False)
            screen.blit(image,self.sprite_rect)
            if 10>=self.index>= 2:
                image_attaque = pygame.transform.scale(self.animations_attaque[self.index-2],(200,200))
                if self.orientation == "gauche":
                    image_attaque = pygame.transform.flip(image_attaque, True, False)
                screen.blit(image_attaque, ennemy_rect)
        else:
            self.draw_static(screen)

class Ennemy(Perso):
    def __init__ (self,name, pv_max, weapon, nouvelle_taille: tuple,level):
        Perso.__init__(self,name, 0, 0, pv_max, weapon, nouvelle_taille,level)

class Fight_assets:
    def __init__(self):
        #Armes à disposition
        self.tengoku_no_ikari = Weapon(name = 'Tengoku No Ikari', weapon_damage = 30,special_damage=100,crit_chance=0.2)
        self.jigoku_no_shizuka = Weapon(name = "Jigoku no Shizuka", weapon_damage=20,special_damage=10, crit_chance=0.1)
        self.wood_katana = Weapon(name="wood_katana",weapon_damage=5,special_damage=5,crit_chance=0.05)
        self.training_katana = Weapon(name="wood_katana",weapon_damage=0,special_damage=5)
        self.katana_guerriers = Weapon(name="katana",weapon_damage=10,special_damage=5,crit_chance=0.05)
        self.zero = Weapon(name="no_weapon",weapon_damage=-100,)
        self.no_weapon = Weapon(name="no_weapon",weapon_damage=0,special_damage=0,crit_chance=0)
        self.op_weapon = Weapon(name='op_weapon',weapon_damage=10,special_damage=15,crit_chance=0.25)


        self.Musashi = Perso("Musashi","Musashi",10,10,self.wood_katana,level = 40)
        self.Musashi_jeune = Perso("Musashi","Musashi_Jeune",9,5,self.training_katana)
        self.Musashi_Tengoku = Perso("Musashi","Musashi_Tengoku",9,80,self.tengoku_no_ikari, 35)
        self.Takeshi = Perso("Takeshi","Musashi",0,30,self.wood_katana)


        self.pantin_de_combat = Perso("Pantin de combat", "Pantin",0,15,self.zero)
        self.guerrier_takahiro = Perso('Guerrier', "Soldat1",11,70,self.katana_guerriers,25)
        self.guerrier_takahiro2 = Perso('Guerrier', "Soldat2",10, 70,self.katana_guerriers,25)

        self.Takahiro = Perso("Kojiro Takahiro", "Takahiro",12, 130, self.katana_guerriers, 25)
        self.Senshi = Perso("Senshi Akuma", "Senshi",12, 50, self.jigoku_no_shizuka, 30)

        self.ch1_e4_1 = Perso("Soldat1","Soldat1",11,50,self.wood_katana,5)
        self.ch1_e4_2 = Perso("Soldat2","Soldat2",10,50,self.wood_katana,5)
        self.ch1_e4_3 = Perso("Soldat1","Soldat1",11,50,self.wood_katana,5)
        self.ch1_e4_4 = Perso("Soldat2","Soldat2",10,50,self.wood_katana,5)
        self.ch1_e4_3.hit(self.ch1_e4_3.pv_max//2)
        self.ch1_e4_4.hit(self.ch1_e4_4.pv_max//2)

        self.ch2_e2_1 = Perso("Soldat1","Soldat1",11,70,self.katana_guerriers,10)
        self.ch2_e2_2 = Perso("Soldat2","Soldat2",10,70,self.katana_guerriers,10)


        self.set_sizes()
        
    def set_sizes(self):
        self.Musashi_Tengoku.set_taille(250)
        self.Musashi.set_taille(225)
        self.guerrier_takahiro.set_taille(250)
        self.guerrier_takahiro2.set_taille(300)
        self.Takahiro.set_taille(300)
        self.Senshi.set_taille(350)
        self.ch1_e4_1.set_taille(250)
        self.ch1_e4_3.set_taille(250)
        self.ch2_e2_1.set_taille(250)
        self.ch1_e4_2.set_taille(300)
        self.ch1_e4_4.set_taille(300)
        self.ch2_e2_2.set_taille(300)

if __name__ == "__main__":
        fight_assets = Fight_assets()
        print(fight_assets.ma_Juzo.level)