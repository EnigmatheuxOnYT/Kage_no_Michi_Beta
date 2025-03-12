
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
    def __init__(self, name:str,spritename:str,nouvelle_taille:tuple, pv_max:int, weapon:Weapon,attaque_frames:int,level:int=1,instance:int=0): #Toutes les variables nécessaires pour la création d'un personnage
        self.name = name #Son nom
        self.sprite_name = spritename
        self.pv_max = pv_max #Ses hp max
        self.pv = pv_max #Ses pv, qui vont prendre tout simplement la valeur de ses pvs
        self._base_damage = 2
        self.weapon = weapon
        self.do_attacks = True
        self.level = 1 #niveau du personnage
        self.level_xp = 5
        self.xp = 0
        self.nouvelle_taille = nouvelle_taille
        self.set_level(level)
        sprite = pygame.image.load(f"../data/assets/tpt/sprites/{self.sprite_name}_Idle.png") #Le spirte quand il reste immobile
        self.image = pygame.transform.scale(sprite, nouvelle_taille) #On redimensionne le sprite de sorte à ce que ça soit cohérent avec le fond
        self.rect = self.image.get_rect()
        self.rect.width = 100
        self.atk_frame_lengh = 80
        self.debut_frame = 0
        self.orientation="gauche"
        self.pos=(0,0)
        self.attacking=False
        self.animations_combat = []
        for i in range(attaque_frames):
            self.animations_combat.append(pygame.image.load(f"../data/assets/tpt/sprites/{self.sprite_name}_Combat_{i+1}.png"))
        
        self.index = 0
        self.max_index = attaque_frames-1
        self.fin_attaque = False

    @property
    def current_damage(self):return self._base_damage+self.weapon.weapon_damage
    @property
    def is_ko (self):return False if self.pv>0 else True
    
    def level_up (self):
        self.level+=1
        self.pv_max=int(round(self.pv_max*1.1,0))+2
        self._base_damage=int(round(self._base_damage*1.1,0))+2
        self.pv = self.pv_max
        self.level_xp = int(self.level_xp*1.1)+2
    
    def give_xp (self,xp):
        self.xp += xp
        if self.xp >= self.level_xp:
            self.xp-=self.level_xp
            self.level_up()
    
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
        self.rect.midtop = pos[0]+100,pos[1]

    def set_attacking(self,val):self.attacking=val

    def set_do_attaks (self,val):self.do_attacks = val

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

        if self.index == 0 or self.atk_frame_lengh-pygame.time.get_ticks()+self.debut_frame<=0 and self.attacking:
            self.index +=1

            if self.index>self.max_index:
                self.index=0
                self.attacking=False

            self.debut_frame = pygame.time.get_ticks()

        if self.index!=0 and self.attacking:
            image = pygame.transform.scale(self.animations_combat[self.index], self.nouvelle_taille)
            if self.orientation == "gauche":
                image = pygame.transform.flip(image, True, False)
            screen.blit(image,(self.pos))

            if self.index >= 2 and self.fin_attaque == False and self.attacking: #Début de l'apparition de l'attaque choisie
                index_attaque = min(self.index - 2, len(self.animations_attaque) - 1)
                image_attaque = pygame.transform.scale(self.animations_attaque[index_attaque],(200,200))
                if self.orientation == "gauche":
                    image_attaque = pygame.transform.flip(image_attaque, True, False)
                screen.blit(image_attaque, ennemi_position)
                if image_attaque == self.animations_attaque[8]:
                    self.fin_attaque = True
                
        else:
            self.draw_static(screen)

class Ennemy(Perso):
    def __init__ (self,name, pv_max, weapon, nouvelle_taille: tuple,level):
        Perso.__init__(self,name, 0, 0, pv_max, weapon, nouvelle_taille,level)

class Fight_assets:
    def __init__(self):
        #Armes à disposition
        self.tengoku_no_ikari = Weapon(name = 'Tengoku No Ikari', weapon_damage = 20,special_damage=10,crit_chance=0.1)
        self.jigoku_no_shizuka = Weapon(name = "Jigoku no Shizuka", weapon_damage=20,special_damage=10, crit_chance=0.1)
        self.wood_katana = Weapon(name="wood_katana",weapon_damage=5,special_damage=5,crit_chance=0.05)
        self.training_katana = Weapon(name="wood_katana",weapon_damage=0,special_damage=5)
        self.katana_guerriers = Weapon(name="katana",weapon_damage=10,special_damage=5,crit_chance=0.05)
        self.zero = Weapon(name="no_weapon",weapon_damage=-100,)
        self.no_weapon = Weapon(name="no_weapon",weapon_damage=0,special_damage=0,crit_chance=0)
        self.op_weapon = Weapon(name='op_weapon',weapon_damage=10,special_damage=15,crit_chance=0.25)
        self.Musashi = Perso("Musashi","Musashi",(200,200),100,self.op_weapon,9,level = 30)
        self.Musashi_Tengoku = Perso("Musashi","Musashi_Tengoku", (250,250),50,self.tengoku_no_ikari, 9, 30)
        self.Musashi_jeune = Perso("Musashi","Musashi_Jeune",(200,200),5,self.training_katana,0)
        self.pantin_de_combat = Perso("Pantin de combat", "Pantin",(200,200),30,self.zero,0)
        self.pantin_de_combat.set_do_attaks(False)
        self.guerrier_takahiro = Perso('Soldat1', "Soldat1",(250,250),70,self.no_weapon,11)
        self.guerrier_takahiro2 = Perso('Soldat2', "Soldat1",(250,250), 70,self.no_weapon,11)
        self.Takahiro = Perso("Kojiro Takahiro", "Takahiro", (250,250), 200, self.op_weapon,12, 30)
        self.Senshi = Perso("Senshi Akuma", "Senshi",(250,250), 50, self.jigoku_no_shizuka,12, 30)
        self.guerrier_ch1_e4_1_1 = Perso("Soldat","Soldat1",(250,250),5,self.katana_guerriers,11,5)
        self.guerrier_ch1_e4_1_2 = Perso("Soldat","Soldat1",(250,250),5,self.katana_guerriers,11,5)
        #self.ma_Juzo = Perso('Ma_Juzo',200, self.tengoku_no_ikari,level=10)

if __name__ == "__main__":
        fight_assets = Fight_assets()
        print(fight_assets.ma_Juzo.level)