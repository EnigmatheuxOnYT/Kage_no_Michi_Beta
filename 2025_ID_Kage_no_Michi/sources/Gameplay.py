#Projet : Kage no Michi
#Auteurs : Alptan Korkmaz, Clément Roux--Bénabou, Maxime Rousseaux, Ahmed-Adam Rezkallah, Cyril Zhao


# -*- coding: utf-8 -*-
"""
Created on Tue Mar 04 09:31:37 2025

@author: clementroux--benabou
"""
import pygame
from typing import List,Any,overload
from dataclasses import dataclass
import Loading
from Mini_jeu_survivants import minigm_survivors
from Mini_jeu_epreuve_combat import minigm_trial1
from Mini_jeu_marchandage import minigm_trade
from Mini_jeu_piege_environnemental import minigm_minesweeper
from Mini_jeu_persuasion import minigm_persuade
from Mini_jeu_filature import minigm_follow
from Mini_jeu_reconstruction import minigm_mastermind
from Mini_jeu_collecte import minigm_collect
from Audio import Music,Sound
from map.src.game import Game_map
from Savemgr import Savemgr
from Cinematics import Cinematics
from map.src.Map_objects import *
from map.src.player2 import *
from map.src.map import Map

class Launcher:
    def __init__(self,screen):
        Loading.display_loading(screen, 40,"Lancement des modules mini-jeux")
        self.minigm_01 = minigm_survivors()
        Loading.display_loading(screen, 43,"Lancement des modules mini-jeux")
        self.minigm_02 = minigm_persuade()
        Loading.display_loading(screen, 46,"Lancement des modules mini-jeux")
        self.minigm_04 = minigm_trial1()
        Loading.display_loading(screen, 49,"Lancement des modules mini-jeux")
        self.minigm_05 = minigm_follow(screen)
        Loading.display_loading(screen, 52,"Lancement des modules mini-jeux")
        self.minigm_06 = minigm_trade()
        Loading.display_loading(screen, 55,"Lancement des modules mini-jeux")
        self.minigm_07 = minigm_minesweeper()
        Loading.display_loading(screen, 58,"Lancement des modules mini-jeux")
        self.minigm_08 = minigm_mastermind()
        Loading.display_loading(screen, 61,"Lancement des modules mini-jeux")
        self.minigm_09 = minigm_collect(screen)
        Loading.display_loading(screen, 64,"Lancement des modules secondaires")
        self.music = Music()
        self.loaded_save = -1
        Loading.display_loading(screen, 65,"Lancement du module de sauvegarde")
        self.savemgr = Savemgr()
        Loading.display_loading(screen, 66,"Lancement du module de cinématiques")
        self.cinematics = Cinematics()
        Loading.display_loading(screen, 67,"Lancement du module de la carte")
        self.map = Game_map(screen)

    def launch_minigame (self,minigame,choices,devmode=False):
        
        pygame.mouse.set_visible(True)
        
        
        self.music.play(fade=500)
        
        if minigame == 1:
            self.running = self.minigm_01.run(self.screen_for_game,choices[0],devmode)
        elif minigame == 2:
            self.running = self.minigm_02.run(self.screen_for_game,choices[0],devmode)
        elif minigame == 3:
            print("Mini-jeu de tuto combat tour par tour non implémenté")
        elif minigame == 4:
            self.running = self.minigm_04.run(self.screen_for_game,choices[0],devmode)
        elif minigame == 5:
            self.running = self.minigm_05.run(self.screen_for_game,choices[0],self.current_passcode,devmode)
        elif minigame == 6:
            self.running = self.minigm_06.run(self.screen_for_game,choices[0],devmode)
        elif minigame == 7:
            self.running = self.minigm_07.run(self.screen_for_game,choices[0],devmode)
        elif minigame ==8:
            self.running = self.minigm_08.run(self.screen_for_game,choices[0],devmode)
        elif minigame ==9:
            self.running = self.minigm_09.run(self.screen_for_game,choices[0],devmode)
        
        pygame.mouse.set_visible(False)
        
    
    def launch_cinematic (self,cinematic,choices):
        
        pygame.mouse.set_visible(True)
        
        
        self.music.play(fade=500)
        
        if cinematic == 1:
            self.cinematics.cinematic_01(self.screen_for_game)
        elif cinematic == 2:
            self.cinematics.cinematic_02(self.screen_for_game,choices[0])
        elif cinematic == 3:
            self.cinematics.cinematic_03(self.screen_for_game,choices[0])
        elif cinematic == 4:
            self.cinematics.cinematic_04(self.screen_for_game,choices[0])
        elif cinematic == 5:
            self.cinematics.cinematic_05(self.screen_for_game,choices[0])
        elif cinematic == 6:
            self.cinematics.cinematic_06(self.screen_for_game,choices[0])
        elif cinematic == 7:
            self.cinematics.cinematic_07(self.screen_for_game,choices[0])
        elif cinematic == 8:
            self.cinematics.cinematic_08(self.screen_for_game,choices[1])
        elif cinematic == 9:
            self.cinematics.cinematic_09(self.screen_for_game,choices[0])
        elif cinematic == 10:
            self.choices[2] = self.cinematics.cinematic_10(self.screen_for_game,choices[0])
        elif cinematic == 11:
            self.cinematics.cinematic_11(self.screen_for_game,choices[0],choices[2])
        
        
        pygame.mouse.set_visible(False)
    
    def launch_dialog(self,dialog,choices=None):
        
        
        self.music.play(fade=500)

class Direction:
    def __init__(self,no,reasons,dirs):
        self.no = no
        self.reasons = reasons
        self.dirs = dirs

    @property
    def sender(self):
        res=dict()
        for i in range(self.no):
            res[str(i)] = dict()
            res[str(i)]['reason'] = self.reasons[i]
            res[str(i)]['dir'] = self.dirs[i]
        return res



class GamePlayPhase:
    def __init__(self,name:str,type:str,dirs_data):
        self.dirs = Direction(dirs_data[0],dirs_data[1],dirs_data[2])
        self.name = name
        self.type = type

class GPPMap(GamePlayPhase):
    def __init__(self,name:str,map:Map,event_zones:List[DisplayZone],npcs:List[NPC|StaticNPC],display_zones:List[DisplayZone],path:SubPath,dirs_data:List[List[str|int]|int]):
        GamePlayPhase.__init__(self,name,"GPFMap",dirs_data)
        self.map = map
        self.event_zones=event_zones
        self.npcs=npcs
        self.display_zones = display_zones
        self.path=path


class GPPCinematic(GamePlayPhase):
    def __init__(self,name:str,cinematic_no:int,dirs_data:List[List[str|int]|int]):
        GamePlayPhase.__init__(self,name,"GPPCinematic",dirs_data)
        self.cinematic_no = cinematic_no

class GPPDialog(GamePlayPhase):
    def __init__(self,name:str,dialog_no:int,dirs_data:List[List[str|int]|int]):
        GamePlayPhase.__init__(self,name,"GPPDialog",dirs_data)
        self.dialog_no = dialog_no

class GPPMinigame(GamePlayPhase):
    def __init__(self,name:str,minigame_no:int,dirs_data:List[List[str|int]|int]):
        GamePlayPhase.__init__(self,name,"GPPMinigame",dirs_data)
        self.minigame_no = minigame_no

class GPPFight(GamePlayPhase):
    def __init__(self,name,ennemies:List[Any],dirs_data:List[List[str|int]|int]):
        GamePlayPhase.__init__(self,name,"GPPFight",dirs_data)
        self.ennemies=ennemies

class Scene:
    def __init__(self,id:List[int],gpps:List[GamePlayPhase]):
        self.id=id
        self.chapter=id[0]
        self.episode=id[1]
        self.name=f"Chapitre {id[0]}, épisode {id[1]}"
        self.gpps=gpps

