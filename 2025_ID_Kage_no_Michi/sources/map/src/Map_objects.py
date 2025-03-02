#Projet : Kage no Michi
#Auteurs : Alptan Korkmaz, Maxime Rousseaux, Ahmed-Adam Rezkallah, Clément Roux--Bénabou, Cyril Zhao

# -*- coding: utf-8 -*-
"""
Created on Sun Mar 02 14:54:52 2025

@author: clementroux--benabou
"""
import pygame
import pytmx
import pytmx.util_pygame
import pyscroll
import random
import copy
from dataclasses import dataclass
from typing import List,overload

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

class CompatibleObject:
    """ 
    Classe pour les objets gérés par le jeu hors map mais qui sont affichés par la carte.
    Pour le moment, cet objet est générable à l'enregistrement de la carte.
    En test,aussi implémentable depuis n'importe où d'autre, mais ça peut ne pas marher
    """
    @overload
    def __init__(self,object:pygame.Rect,group_object:pytmx.TiledObject,map_manager)->None:...
    @overload
    def __init__(self,object:pygame.Rect,map_manager)->None:...

    def __init__ (self,rect:pygame.Rect,map_manager):
        self.map_manager=map_manager
        self.map_rect=rect
        self.rect=rect
        self.screen_width = rect.width*2
        self.screen_height = rect.height*2
        self.assigned_surface = pygame.surface.Surface((rect.width,rect.height)).convert_alpha()
        self.hidden=False
        self.map_manager.get_map().group.add(self)
        self.group_object=self


    def __init__(self,object:pygame.Rect,group_object:pytmx.TiledObject,map_manager):
        self.map_manager=map_manager
        self.group_object=group_object
        self.map_rect=object
        self.rect=self.map_rect
        self.screen_width = object.width*2
        self.screen_height = object.height*2
        self.assigned_surface = pygame.surface.Surface((object.width,object.height)).convert_alpha()
        self.hidden=False

    @property
    def image(self):return self.current_image
    @property
    def current_image(self):
        if self.hidden:
            self.assigned_surface.set_alpha(0)
        return self.assigned_surface
    @property
    def is_on_screen (self):return self._get_screen().colliderect(object)
    @property
    def is_fully_on_screen (self):return self._get_screen().top<self.map_rect.top and self._get_screen().bottom>self.map_rect.bottom and self.get_screen().left<self.map_rect.left and self.get_screen().right>self.map_rect.right
    @property
    def screen_x (self):return self.map_rect.x-self._get_screen().x
    @property
    def screen_y (self):return self.map_rect.y-self._get_screen().y
    @property
    def screen_rect (self):return pygame.Rect(self.screen_x,self.screen_y,self.screen_width,self.screen_height)

    def _get_screen(self):return self.map_manager.get_map().group.view()

    def set_assigned_surface (self,surf:pygame.surface.Surface):
        self.assigned_surface=surf
    
    def set_hidden (self,value:bool):
        self.hidden=value

    def draw (self,screen):
        screen.blit(self.image,self.screen_rect)
        
    def change_layer(self,layer):
        self.map_manager.get_map().group.change_layer(self.group_object,layer)

class SubPath:
    def __init__(self,name:str,point_objects:List[pytmx.TiledObject],rect_objects:pytmx.TiledObject):
        self.name=name
        self.point_objects=point_objects
        self.rect_objects=rect_objects
        self.raw_points= list()
        self.raw_rects = list()
        self.points_rects_dict = dict()
        self.order()

    def order(self):
        self.order_points()
        self.order_rects()

    def order_points(self):
        points=dict()
        for i in range(1,len(self.point_objects)+1):
            for object in self.point_objects:
                if str(i) in object.name:
                    points[object.name]={'point':(object.x,object.y)}
        self.points_rects_dict = points
        raw_points = list()
        for i in list(points.values()):
            raw_points.append(i['point'])
        self.raw_points = raw_points
    
    def order_rects(self):
        for i in range(1,len(self.rect_objects)+1):
            for object in self.rect_objects:
                if str(i) in object.name:
                    self.points_rects_dict[object.name]['rect']=pygame.Rect(object.x,object.y,object.width,object.height)
        raw_rects = list()
        for i in list(self.points_rects_dict.values()):
            raw_rects.append(i['rect'])
        self.raw_rects=raw_rects


    
    def get_raw_points(self,reversed:bool=False):
        points=self.raw_points
        if reversed:
            reversed_points=[]
            for i in range(1,len(points)):
                reversed_points=points[-i]
            points=reversed_points
        return points




@dataclass
class Portal :
    from_world : str
    origin_point : str
    target_world : str
    teleport_point : str


class DisplayZone(CompatibleObject,pygame.sprite.Sprite):
    def __init__ (self,object_class:str,name:str,object:pygame.Rect,group_object:pytmx.TiledObject,map_manager):
        CompatibleObject.__init__(self,object,group_object,map_manager)
        pygame.sprite.Sprite.__init__(self)
        self.name=name
        self.object_class=object_class
        self.is_moving_object=False
        self.map_manager=map_manager