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
        Action.__init__(self,"NPCDialog")
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
    def __init__(self,new_position:str=(0,0)):
        Action.__init__(self,"NPCTeleport")
        self.position=new_position

class NPCRemove(Action):
    def __init__(self):
        Action.__init__(self,"NPCRemove")

class NPCEndGPP(Action):
    def __init__(self,output):
        Action.__init__(self,"NPCEndGPP")
        self.output=output

class NPCRepeatInteraction(Action):
    def __init__(self,repetitions:int=-1):
        Action.__init__(self,"NPCRepeatInteraction")
        self.name="NPCRepeatInteraction"
        self.repetitions=repetitions
        self.repetitions_left=repetitions

class NPCMinigame(Action):
    def __init__(self,minigame_no):
        Action.__init__(self,"NPCMinigame")
        self.minigame_no = minigame_no
    
    def read(self):
        if self.repetitions==-1:
            return True
        else:
            if self.repetitions_left==0:
                return False
            else:
                self.repetitions_left-=1
                return True

class Interaction:
    def __init__(self,npc_name:str,actions:List[Action]=[]):
        self.npc_name=npc_name
        self.types=[]
        for action in actions:
            self.types.append(action.type)
        self.is_empty=len(self.types)!=0
        self.actions=actions
        self.current_action_index=0
        self.over=False
    
    @property
    def current_action (self):return self.actions[self.current_action_index] if 0<=self.current_action_index<=len(self.actions)-1 else None

    @property
    def event(self):return Event(type='interaction',data=[self])

    def next_action(self):
        action = self.current_action
        if action is not None:
            self.current_action_index+=1
        else:
            self.over=True
    
    def end(self):
        action = self.current_action
        if action is not None and action.type=="NPCRepeatInteraction":
            self.current_action_index=0
            self.over=False
            return action.read()
        else:
            return True


class Interactible:
    def __init__(self,is_interactible:bool=False,interactions:List[Interaction]=[]):
        self.is_interactible=is_interactible
        self.interactions=interactions
        self.current_interaction_index=0
    
    @property
    def current_interaction(self):return self.interactions[self.current_interaction_index] if 0<=self.current_interaction_index<=len(self.interactions)-1 else None


    def next_interaction(self):
        interaction = self.current_interaction
        if interaction is not None:
            self.current_interaction_index+=1


CharactersInteractions = {"Hoshida1":[Interaction(npc_name="Hoshida1",
                                                    actions=[NPCEndGPP(output=-1),
                                                             NPCRemove()
                                                             ]
                                                    ),
                                       ],
                           "Villager10":[Interaction(npc_name="Villager10",
                                                    actions=[NPCMinigame(minigame_no=9),
                                                             NPCRepeatInteraction()
                                                             ]
                                                     )
                                        ],
                           "Villager20":[Interaction(npc_name="Villager20",
                                                   actions=[NPCMinigame(minigame_no=10),
                                                            NPCRepeatInteraction()
                                                            ]
                                                    )
                                       ],
                           "Villager30":[Interaction(npc_name="Villager30",
                                                   actions=[NPCMinigame(minigame_no=8),
                                                            NPCRepeatInteraction()
                                                            ]
                                                    )
                                       ],
                           }