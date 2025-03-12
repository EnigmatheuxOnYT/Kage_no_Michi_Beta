#Projet : Kage no Michi
#Auteurs : Alptan Korkmaz, Maxime Rousseaux, Ahmed-Adam Rezkallah, Clément Roux--Bénabou, Cyril Zhao


import pygame

from map.src.Map_objects import *
from map.src.animation import AnimateSprite
from map.src.Interactions import *
from typing import List
from dataclasses import dataclass
import copy


class Entity(AnimateSprite):

    def __init__(self, name, x, y):
        super().__init__(name)
        self.name = name
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.85, 12)
        self.old_position = self.position.copy()
        self.direction = ""
        self.allow_sprint=True
        self.is_moving_object=True
        self.collidable = True

    def get(self):
        self.image = self.images["down"]
        self.image.set_colorkey([0, 0, 0])
        return self.image

    def give_layer(self,layer):
        self.base_layer=layer

    def save_location(self): self.old_position = self.position.copy()
    
    def move_dir (self,direction,step=0):
        if step in [0,1]:
            self.change_animation(direction)
        
            if  'u' in direction:
                self.position[1] -= self.speed
            elif 'd' in direction:
                self.position[1] += self.speed
        
        if step in [0,2]:
            if 'r' in direction:
                self.position[0] += self.speed
            elif 'f' in direction:
                self.position[0] -= self.speed
    
    
    def add_dir (self,direction):
        self.direction += direction
    
    def set_dir (self,direction):
        self.direction = direction

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.update()
    
    def change_speed (self,speed) :
        self.speed = speed
    
    def set_allow_sprint (self,state):
        self.allow_sprint= state
    
    def sprint(self,state):
        if self.allow_sprint:
            if state:
                self.speed *= 2
            else:
                self.speed /= 2
        
    def __teleport (self,coords):
        self.position=coords
        self.update()
        self.save_location()

class Player(Entity):

    def __init__(self):
        super().__init__("Player",0,0)
        
        
class NPC(Entity,Interactible):
    
    def __init__(self, name,start_pos=[0,0], nb_points=0,speed=1,instance:int=0):
        Entity.__init__(self,name,start_pos[0],start_pos[1])
        self.instance=instance
        interractions=self._get_interractions()
        is_interractible=len(interractions)!=0
        Interactible.__init__(self,is_interractible,interractions)
        self.instance_name=self.name+str(self.instance)
        self.start_pos=start_pos
        self.nb_points = nb_points
        self.points= []
        self.speed=speed
        self.current_point=0
        self.allow_sprint=False
    
    @property
    def collision_rect(self):
        rect=pygame.Rect(0,0,34,10)
        rect.midbottom = self.rect.midbottom
        return rect
    
    @property
    def interaction_rect(self):
        if self.is_interactible:
            rect=pygame.Rect(0,0,50,50)
        else:
            rect=pygame.Rect(0,0,0,0)
        rect.center=self.rect.midbottom
        return rect
    
    def reload (self):
        name = self.name
        start_pos = self.start_pos
        nb_points = self.nb_points
        speed = self.speed
        instance = self.instance
        self.__init__(name,start_pos,nb_points,speed,instance)

    def move_points(self):
        if self.nb_points !=0:
            current_point = self.current_point
            target_point = self.current_point+1
            
            if target_point >= self.nb_points:
                target_point = 0

            current_rect = self.points[current_point]
            target_rect = self.points[target_point]
        
            self.direction = ""
        
            if current_rect.y < target_rect.y and abs(current_rect.x - target_rect.x) < 3:
                self.direction = "down"
            elif current_rect.y > target_rect.y and abs(current_rect.x - target_rect.x) < 3:
                self.direction = "up"
            elif current_rect.x > target_rect.x and abs(current_rect.y - target_rect.y) < 3:
                self.direction = "left"
            elif current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y) < 3:
                self.direction = "right"
        
            if self.direction != "":
                self.move_dir(self.direction)

            if self.rect.colliderect(target_rect):
                self.current_point = target_point
        
    def _get_interractions(self):
        try:
            return CharactersInteractions[self.name+str(self.instance)]
        except:
            return []


    def teleport_spawn(self):
        self.position[0] = self.start_pos[0]
        self.position[1] = self.start_pos[1]
        self.save_location()
    
    def teleport_coords(self,coords):
        self.__teleport(coords)

    def load_points(self,tmx_data):
        for num in range(1,self.nb_points+1):
            point=tmx_data.get_object_by_name(f"{self.name}_path{num}")
            rect=pygame.Rect(0, 0, 16, 16)
            rect.center = (point.x,point.y)
            self.points.append(rect)
    
    def change_dialog(self,new_dialog:NPCDialog):
        self.dialog=new_dialog

    def interract(self):pass

class StaticEntity(pygame.sprite.Sprite):
    def __init__(self, name, x, y,direction):
        super().__init__()
        self.name = name
        self.nb_points = 0
        self.position = (x, y)
        self.sprite_sheet = pygame.image.load(f"../data/assets/sprites/{name}.png")
        sprite_height = self.get_sprite_height(direction)
        self.image = pygame.Surface([34, 44])
        self.image.blit(self.sprite_sheet, (0, 0), (34, sprite_height, 34, 44))
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.rect.center=self.position
        self.direction = direction
        self.is_moving_object=False
        self.collidable = False
    
    def get_sprite_height(self,direction):
        if direction=='down':
            return 44
    
    def give_layer(self,layer):
        self.base_layer=layer

    
class StaticNPC(StaticEntity,Interactible):
    def __init__(self, name,pos=[0,0],direction="down",instance:int=0):
        StaticEntity.__init__(self,name,pos[0],pos[1],direction)
        self.instance=instance
        interactions = self._get_interactions()
        is_interactible=len(interactions)!=0
        Interactible.__init__(self,is_interactible,interactions)
        self.instance_name=self.name+str(self.instance)
        self.collision_rect = pygame.Rect(0,0,34,10)
        self.collision_rect.bottomright=self.rect.bottomright
    
    @property
    def interaction_rect(self):
        if self.is_interactible:
            rect=pygame.Rect(0,0,50,50)
        else:
            rect=pygame.Rect(0,0,0,0)
        rect.center=self.rect.midbottom
        return rect
    
    def reload (self):pass

    def _get_interactions(self):
        try:
            if self.instance==0:
                return CharactersInteractions[self.name]
            else:
                return CharactersInteractions[self.name+str(self.instance)]
        except:
            return []
    
    def teleport_coords(self,coords):
        self.position=coords
        self.rect.center=self.position
        self.collision_rect.bottomright = self.rect.bottomright
    
    def change_dialog(self,new_dialog:NPCDialog):
        self.dialog=new_dialog
    
    def interract(self):pass
        
    
class Follower(Entity):
    def __init__(self,name):
        super().__init__(name,0,0)
        self.collidable = False
        self.active = False
    
    def reload (self):
        name = self.name
        self.__init__(name)
    
    def init_pos (self,pos,speed):
        self.position = pos
        self.speed = speed
        self.movment_queue = [pos for _ in range(30)]
        self.speed_queue = [speed for _ in range(30)]
        self.save_location()

    
    def update_move(self,pos,speed):
        self.speed_queue.append(copy.deepcopy(speed))
        self.speed = self.speed_queue.pop(0)
        self.movment_queue.append(copy.deepcopy(pos))
        position = self.movment_queue.pop(0)

        direct = ""
        if position[1] > self.position[1]:
            direct += "down"
        elif position[1] < self.position[1]:
            direct += "up"
        if position[0] < self.position[0]:
            direct += "left"
        elif position[0] > self.position[0]:
            direct += "right"

        if direct != "":
            self.move_dir(direct)
        self.position = position
        self.update()
        self.save_location()
        self.direction = direct
    
    def set_active(self,state):self.active = state
