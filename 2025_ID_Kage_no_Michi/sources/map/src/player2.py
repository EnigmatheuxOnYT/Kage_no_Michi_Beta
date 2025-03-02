#Projet : Kage no Michi
#Auteurs : Alptan Korkmaz, Maxime Rousseaux, Ahmed-Adam Rezkallah, Clément Roux--Bénabou, Cyril Zhao


import pygame

from map.src.animation import AnimateSprite
from typing import List
from dataclasses import dataclass

@dataclass
class Event :
    type : str
    data : list

@dataclass
class Event_zone :
    from_world : str
    origin_point : str
    entities : List[str]
    events : List[Event]

class Action:
    def __init__(self,type:str='none'):
        self.action_name=action_name
        if type=='none':
            self.type='none'
            self.in_empty=True
        else:
            self.is_empty=False

class NPCDialog(Action):
    def __init__(self,no:int=0,name:str='none',is_cinematic:bool=False,is_reapeating=False):
        Action.__init__("NPCDialog")
        if no==0:
            self=name = 'none'
            self.in_empty=True
            self.is_cinematic = False
        else:
            self.name=name
            self.is_cinematic=is_cinematic
        self.no=no
        self.event=Event(type="dialog",data=[self.no])

class RepeatInterraction(Action):
    def __init__(self,repetitions:int=-1):
        Action.__init__("RepeatInterraction")
        self.name="RepeatInterraction"
        self.repetitions=repetitions
        self.repetitions_left=repetitions
    
    def read(self):
        if self.repetitions==-1:
            return True
        else:
            if self.repetitions_left==0:
                return False
            else:
                self.repetitions_left-=1
                return True

class Interraction:
    def __init__(self,actions:List[Action]):
        self.types=[]
        for action in actions:
            self.types.append(action.action_name)
        self.actions=actions
        self.current_action_index=0
        self.over=False
    
    @property
    def current_action (self):return self.actions[self.current_action_index-1] if self.current_action_index>=1 else None

    def next_action(self):
        action = self.current_action
        if action is not None:
            self.current_action_index+=1
        else:
            self.over=True
    
    def end(self):
        action = self.current_action
        if action.type=="RepeatInterracttion":
            self.current_action_index=0
            self.over=False
            return action.read()
        else:
            return True


class Interractible:
    def __init__(self,is_interractible:bool=False,interractions:List[Interraction]=[]):
        self.is_interractible=is_interractible
        self.interractions=interractions
        self.current_interraction_index=0
    
    @property
    def current_interraction (self):return self.interractions[self.current_interraction_index-1] if 1<=self.current_interraction_index<=len(self.interractions) else None

    def next_interraction(self):
        interraction = self.current_interraction
        if interraction is not None:
            if self.current_interraction.end():
                self.current_interraction_index+=1

class Entity(AnimateSprite):

    def __init__(self, name, x, y):
        super().__init__(name)
        self.name = name
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()
        self.direction = ""
        self.allow_sprint=True
        self.is_moving_object=True

    def get(self):
        self.image = self.images["down"]
        self.image.set_colorkey([0, 0, 0])
        return self.image

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



class Player(Entity):

    def __init__(self):
        super().__init__("Player",0,0)
        
        
class NPC(Entity,Interractible):
    
    def __init__(self, name,start_pos=[0,0], nb_points=0, interractions:List[Action]=[],speed=1):
        Entity.__init__(name,start_pos[0],start_pos[1])
        is_interractible=len(interractions)!=0
        Interractible.__init__(self,is_interractible,interractions)
        self.start_pos=start_pos
        self.nb_points = nb_points
        self.interractions=interractions
        self.points= []
        self.speed=speed
        self.current_point=0
    
    @property
    def dialog_rect(self):
        if self.is_interractible:
            rect=pygame.Rect(0,0,50,50)
        else:
            rect=pygame.Rect(0,0,0,0)
        rect.center=self.rect.midbottom
        return rect

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
                self.direction += "down"
            elif current_rect.y > target_rect.y and abs(current_rect.x - target_rect.x) < 3:
                self.direction += "up"
            if current_rect.x > target_rect.x and abs(current_rect.y - target_rect.y) < 3:
                self.direction += "left"
            elif current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y) < 3:
                self.direction += "right"
        
            if self.direction != "":
                self.move_dir(self.direction)

            if self.rect.colliderect(target_rect):
                self.current_point = target_point

    def teleport_spawn(self):
        self.position[0] = self.start_pos[0]
        self.position[1] = self.start_pos[1]
        self.save_location()

    def load_points(self,tmx_data):
        for num in range(1,self.nb_points+1):
            point=tmx_data.get_object_by_name(f"{self.name}_path{num}")
            rect=pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)
    
    def change_dialog(self,new_dialog:NPCDialog=NPCDialog()):
        self.dialog=new_dialog

    def interract(self):pass

class StaticEntity(pygame.sprite.Sprite):
    def __init__(self, name, x, y,direction):
        super().__init__()
        self.name = name
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
    
    def get_sprite_height(self,direction):
        if direction=='down':
            return 44
    
class StaticNPC(StaticEntity,Interractible):
    def __init__(self, name,pos=[0,0], interractions:List[Interraction]=[],direction="down"):
        StaticEntity.__init__(name,pos[0],pos[1],direction)
        is_interractible=len(interractions)!=0
        Interractible.__init__(self,is_interractible)
        self.interractions=interractions
        self.collision_rect = pygame.Rect(0,0,34,10)
        self.collision_rect.bottomright=self.rect.bottomright
    
    @property
    def dialog_rect(self):
        if self.is_interractible:
            rect=pygame.Rect(0,0,50,50)
        else:
            rect=pygame.Rect(0,0,0,0)
        rect.center=self.rect.midbottom
        return rect
    
    def teleport_coords(self,coords):
        self.position=coords
        self.rect.center=self.position
        self.collision_rect.bottomright = self.rect.bottomright
    
    def change_dialog(self,new_dialog:NPCDialog=NPCDialog()):
        self.dialog=new_dialog
    
    def interract(self):pass
        
    
