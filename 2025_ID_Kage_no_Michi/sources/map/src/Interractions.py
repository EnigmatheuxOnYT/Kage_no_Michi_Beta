#Projet : Kage no Michi
#Auteurs : Alptan Korkmaz, Maxime Rousseaux, Ahmed-Adam Rezkallah, Clément Roux--Bénabou, Cyril Zhao

# -*- coding: utf-8 -*-
"""
Created on Sun Mar 02 14:54:49 2025

@author: clementroux--benabou
"""

import pygame
from typing import List
from dataclasses import dataclass
from map.src.Map_objects import Event_zone,Event

class Action:
    def __init__(self,type:str='none'):
        self.type=type
        if type=='none':
            self.type='none'
            self.in_empty=True
        else:
            self.is_empty=False

class NPCDialog(Action):
    def __init__(self,no:int=0,name:str='none',is_cinematic:bool=False):
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

class NPCTeleport(Action):
    def __init__(self,new_map:str="main",new_position:str=(0,0)):
        Action.__init__("NPCTeleport")
        self.map=new_map
        self.position=new_position

class NPCRemove(Action):
    def __init__(self):
        Action.__init__("NPCRemove")

class NPCRepeatInterraction(Action):
    def __init__(self,repetitions:int=-1):
        Action.__init__("NPCRepeatInterraction")
        self.name="NPCRepeatInterraction"
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
    def __init__(self,actions:List[Action]=[]):
        self.types=[]
        for action in actions:
            self.types.append(action.action_name)
        self.is_empty=len(self.types)!=0
        self.actions=actions
        self.current_action_index=0
        self.over=False
    
    @property
    def current_action (self):return self.actions[self.current_action_index] if self.current_action_index>=1 else None

    @property
    def event(self):return Event(type='interraction',data=[self])

    def next_action(self):
        action = self.current_action
        if action is not None:
            self.current_action_index+=1
        else:
            self.over=True
    
    def end(self):
        action = self.current_action
        if action.type=="NPCRepeatInterraction":
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
    def current_interraction(self):return self.interractions[self.current_interraction_index] if 1<=self.current_interraction_index<=len(self.interractions) else None


    def next_interraction(self):
        interraction = self.current_interraction
        if interraction is not None:
            if self.current_interraction.end():
                self.current_interraction_index+=1


CharactersInterractions = {"Hoshida1":[Interraction(actions=[NPCDialog(no=5,
                                                                       name="Hoshida1",
                                                                       is_cinematic=True
                                                                       ),
                                                             NPCRemove()
                                                             ]
                                                    ),
                                       ]
                           }