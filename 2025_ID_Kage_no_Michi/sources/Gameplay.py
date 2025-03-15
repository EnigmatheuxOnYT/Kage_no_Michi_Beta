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
from Fight_assets import Fight_assets

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
        pass


@dataclass
class Condition:
    type : str
    data : list

@dataclass
class Update:
    condition : Condition
    effect : str

class Direction:
    def __init__(self,no,reasons,dirs):
        self.no = no #Nombre 
        self.reasons = reasons #-1 pour tout
        self.dirs = dirs #next pour la prochaine scène

    @property
    def sender(self):
        res=dict()
        for i in range(self.no):
            res[str(i)] = dict()
            res[str(i)]['reason'] = self.reasons[i]
            res[str(i)]['dir'] = self.dirs[i]
        return res



class GamePlayPhase:
    def __init__(self,name:str,type:str,dirs_data:list):
        self.dirs = Direction(dirs_data[0],dirs_data[1],dirs_data[2])
        self.name = name
        self.type = type

class GPPMap(GamePlayPhase):
    def __init__(self,name:str,map:Map,spawn:str,event_zones:List[DisplayZone]=[],npcs:List[Interactible]=[],display_zones:List[DisplayZone]=[],path:str=None,dirs_data:list=[1,[-1],['next']],updates:List[Update]=[]):
        GamePlayPhase.__init__(self,name,"GPPMap",dirs_data)
        self.map = map
        self.spawn=spawn
        self.event_zones=event_zones
        self.npcs=npcs
        self.display_zones = display_zones
        self.path=path
        self.updates = updates
    
    def setup (self):pass



class GPPCinematic(GamePlayPhase):
    def __init__(self,name:str,cinematic_no:int,dirs_data:list=[1,[-1],['next']]):
        GamePlayPhase.__init__(self,name,"GPPCinematic",dirs_data)
        self.cinematic_no = cinematic_no

class GPPDialog(GamePlayPhase):
    def __init__(self,name:str,dialog_no:int,dirs_data:list):
        GamePlayPhase.__init__(self,name,"GPPDialog",dirs_data)
        self.dialog_no = dialog_no

class GPPMinigame(GamePlayPhase):
    def __init__(self,name:str,minigame_no:int,dirs_data:list):
        GamePlayPhase.__init__(self,name,"GPPMinigame",dirs_data)
        self.minigame_no = minigame_no

class GPPFight(GamePlayPhase):
    def __init__(self,name,bg,ennemies:List[Any],dirs_data:list):
        GamePlayPhase.__init__(self,name,"GPPFight",dirs_data)
        self.ennemies=ennemies
        self.bg = bg

class GPPDeath(GamePlayPhase):
    def __init__(self,name):
        GamePlayPhase.__init__(self,name,"GPPDeath",[])

class Scene:
    def __init__(self,id:List[int],next_id:List[int],gpps:List[GamePlayPhase]):
        self.id=id
        self.chapter=id[0]
        self.episode=id[1]
        self.next_id=next_id
        self.name=f"Chapitre {id[0]}, épisode {id[1]}"
        self.gpps=gpps
        self.gppindex=0
    @property
    def over (self):return self.gppindex >= len(self.gpps)
    @property
    def current_gpp(self):return self.gpps[self.gppindex] if not self.over else None
    
    def next_gpp(self,output):
        if not self.over:
            ressearch=False
            dirs=self.gpps[self.gppindex].dirs
            for i in range(dirs.no):
                if dirs.reasons[i] in [output,-1]:
                    ressearch=dirs.dirs[i]
            if not ressearch:
                raise IndexError(f"Incompatible output ({output} not in {dirs.reasons})")
            else:
                if ressearch=='next':
                    self.gppindex+=1
                elif ressearch == 'next_scene':
                    self.gppindex=len(self.gpps)
                elif ressearch == 'death':
                    self.current_gpp = GPPDeath("death")
                else:
                    for i in range(len(self.gpps)):
                        gpp=self.gpps[i]
                        if gpp.name==ressearch:
                            self.gppindex=i
                            return
                    raise IndexError(f"Dir not existant ({ressearch} not in {[gpp.name for gpp in self.gpps]})")

class Story:
    def __init__ (self):
        self.fa=Fight_assets()
        self.scenes = {'Chapitre 0': {"Scene 0":Scene(id=[0,0],
                                                      next_id=[0,1],
                                                      gpps=[]),
                                      'Scene 1':Scene(id=[0,1],
                                                      next_id=[0,2],
                                                      gpps=[GPPCinematic(name='Intro',
                                                                         cinematic_no=1,
                                                                         dirs_data=[1,[-1],['next']]
                                                                         ),
                                                            GPPMap(name='IntroChoice',
                                                                   map='intro',
                                                                   spawn='Spawn_Magome_cinematic',
                                                                   event_zones="all",
                                                                   npcs=[],
                                                                   display_zones=[],
                                                                   path=None,
                                                                   dirs_data=[1,[-1],['next']]
                                                                   ),
                                                            GPPCinematic(name='Intro2',
                                                                         cinematic_no=2,
                                                                         dirs_data=[1,[-1],['next']]
                                                                         )
                                                            ]
                                                      ),
                                      'Scene 2':Scene(id=[0,2],
                                                      next_id=[1,1],
                                                      gpps=[GPPMinigame(name='mimigm_01',
                                                                        minigame_no=1,
                                                                        dirs_data=[1,[-1],['next']]
                                                                        ),
                                                            GPPCinematic(name='Intro3',
                                                                         cinematic_no=3,
                                                                         dirs_data=[1,[-1],['next']]
                                                                         )
                                                            ]
                                                      )
                                      },
                       'Chapitre 1': {'Scene 1':Scene(id=[1,1],
                                                      next_id=[1,2],
                                                      gpps=[GPPMap(name='Chap1_e1_map',
                                                                   map="main",
                                                                   spawn='spawn_Magome',
                                                                   path="mgm_ine",
                                                                   dirs_data=[1,[-1],['next']],
                                                                   updates=[Update(condition=Condition(type="location",data=['ine']),effect='next')]
                                                                   ),
                                                            GPPCinematic(name="Cinématique 4",
                                                                         cinematic_no=4,
                                                                         dirs_data=[1,[-1],['next']]
                                                                         ),
                                                            ]
                                                      ),
                                      'Scene 2':Scene(id=[1,2],
                                                      next_id=[1,3],
                                                      gpps=[GPPMap(name='Chap1_e2_map',
                                                                   map="main",
                                                                   spawn='spawn_Ine',
                                                                   dirs_data=[1,[-1],['next']]
                                                                   ),
                                                            GPPCinematic(name="Cinématique 5",
                                                                         cinematic_no=5,
                                                                         dirs_data=[1,[-1],['next']]
                                                                         ),
                                                            ]
                                                      ),
                                      'Scene 3':Scene(id=[1,3],
                                                      next_id=[1,4],
                                                      gpps=[GPPMap(name='Chap1_e3_map',
                                                                   map="main",
                                                                   spawn='spawn_ch1_e3_1',
                                                                   dirs_data=[1,[-1],['next']],
                                                                   updates=[Update(condition=Condition(type="event_zone",data=['dojo_ine']),effect='next')]
                                                                   ),
                                                            GPPMinigame(name="mimigm_02",
                                                                        minigame_no=2,
                                                                        dirs_data=[1,[-1],['next']]
                                                                        ),
                                                            GPPMinigame(name="minigm_03",
                                                                        minigame_no=3,
                                                                        dirs_data=[1,[-1],['next']])
                                                            ]
                                                      ),
                                       'Scene 4':Scene(id=[1,4],
                                                       next_id=[2,1],
                                                       gpps=[GPPCinematic(name="cinematic_06",
                                                                          cinematic_no=6,
                                                                          dirs_data=[1,[-1],['next']]),
                                                            GPPMinigame(name="minigm_04",
                                                                        minigame_no=4,
                                                                        dirs_data=[1,[-1],['next']]),
                                                            GPPCinematic(name="cinematic_07",
                                                                         cinematic_no=7,
                                                                         dirs_data=[3,[1,2,3],["cinematic_08","cinematic_08","cinematic_08"]]),
                                                            GPPCinematic(name = "cinematic_08",
                                                                         cinematic_no=8,
                                                                         dirs_data=[3,[1,2,3],["cinematic_09","minigm_05","fight_ch1_e4_1"]]),
                                                            GPPCinematic(name="cinematic_09",
                                                                         cinematic_no=9,
                                                                         dirs_data=[1,[-1],["next_scene"]]),
                                                            GPPMinigame(name="minigm_05",
                                                                        minigame_no=5,
                                                                        dirs_data=[3,["win","perfect_win1","perfect_win2"],["cinematic_09","fight_ch1_e4_2","cinematic_09"]]),
                                                            GPPFight(name="fight_ch1_e4_1",
                                                                     bg='ine1',
                                                                     ennemies=[self.fa.ch1_e4_1,self.fa.ch1_e4_2],
                                                                     dirs_data=[1,[-1],['cinematic_23']]),
                                                            GPPFight(name="fight_ch1_e4_2",
                                                                     bg='ine1',
                                                                     ennemies=[self.fa.ch1_e4_3,self.fa.ch1_e4_4],
                                                                     dirs_data=[1,[-1],['cinematic_23']]),
                                                            GPPCinematic(name='cinematic_23',
                                                                         cinematic_no=23,
                                                                         dirs_data=[1,[-1],['cinematic_09']])
                                                            ]
                                                       ),
                                                                
                                      },
                       'Chapitre 2': {"Scene 1":Scene(id=[2,1],
                                                      next_id=[2,2],
                                                      gpps=[GPPMap(name='Chap2_e1_map',
                                                                   map='main',
                                                                   spawn='spawn_chap2_e1',
                                                                   path='ine_forest',
                                                                   dirs_data=[1,[-1],['next']],
                                                                   updates=[Update(condition=Condition(type="location",data=['forest']),effect='next')]),
                                                            GPPCinematic(name='cinematic_10',
                                                                         cinematic_no=10,
                                                                         dirs_data=[4,[1,2,3,4],['minigm_06',"cinematic_11","cinematic_11","cinematic_11"]]),
                                                            GPPCinematic(name='cinematic_11',
                                                                         cinematic_no=11,
                                                                         dirs_data=[1,[-1],["next_scene"]]),
                                                            GPPMinigame(name='minigm_06',
                                                                        minigame_no=6,
                                                                        dirs_data=[1,[-1],["cinematic_11"]]),]
                                                      ),
                                      "Scene 2":Scene(id=[2,2],
                                                      next_id=[2,3],
                                                      gpps=[GPPCinematic(name='cinematic_21',
                                                                         cinematic_no=21,
                                                                         dirs_data=[3,[1,2,3],["cinematic_22","fight_ch2_e2_1","minigm_07"]]),
                                                            GPPCinematic(name='cinematic_22',
                                                                         cinematic_no=22,
                                                                         dirs_data=[1,[-1],['next_scene']]),
                                                            GPPMinigame(name='minigm_07',
                                                                        minigame_no=7,
                                                                        dirs_data=[2,["win","loose"],["fight_ch2_e2_2","next_scene"]]),
                                                            GPPFight(name='fight_ch2_e2_1',
                                                                     bg='bamboo3',
                                                                     ennemies = [self.fa.ch2_e2_1,self.fa.ch2_e2_2],
                                                                     dirs_data=[1,[-1],['cinematic_25']]),
                                                            GPPFight(name='fight_ch2_e2_2',
                                                                     bg='bamboo3',
                                                                     ennemies = [self.fa.ch2_e2_1],
                                                                     dirs_data=[1,[-1],['cinematic_25']]),
                                                            GPPCinematic(name="cinematic_25",
                                                                         cinematic_no=25,
                                                                         dirs_data=[1,-1,["next_scene"]])
                                                            ]
                                                      ),
                                      "Scene 3":Scene(id=[2,3],
                                                      next_id=[3,1],
                                                      gpps=[GPPMap(name='Chap2_e3_map',
                                                                   map='main',
                                                                   spawn="path_forest_ine1",
                                                                   path='forest_azw',
                                                                   dirs_data=[1,[-1],['next']],
                                                                   updates=[Update(condition=Condition(type="event_zone",data=['entrance_azw_destroyed']),effect='next')])
                                                            ]
                                                      ),
                                      },
                       'Chapitre 3': {"Scene 1":Scene(id=[3,1],
                                                      next_id=[3,2],
                                                      gpps=[GPPMap(name='Chap3_e1_map',
                                                                   map='azw1',
                                                                   spawn='spawn',
                                                                   dirs_data=[1,[-1],['cinematic_12']],
                                                                   updates=[Update(condition=Condition(type="event_zone",data=['exit']),effect='next')]),
                                                            GPPCinematic(name='cinematic_12',
                                                                         cinematic_no=12,
                                                                         dirs_data=[2,[1,2],['next','Chap3_e1_map']]),
                                                            GPPMap(name='Chap3_e2_map',
                                                                   map="main",
                                                                   spawn='path_cross5',
                                                                   path='azw_mgm',
                                                                   dirs_data=[2,[1,2],['Chap3_e1_map','next']],
                                                                   updates=[Update(condition=Condition(type="event_zone",data=['entrance_azw_destroyed']),effect=1),
                                                                            Update(condition=Condition(type="location",data=['mgm']),effect=2)]
                                                                   )
                                                            ]
                                                      ),
                                      "Scene 2":Scene(id=[3,2],
                                                      next_id=[3,3],
                                                      gpps=[GPPCinematic(name='cinematic_13',
                                                                         cinematic_no=13,
                                                                         dirs_data=[1,[-1],['next']]),
                                                            GPPCinematic(name='cinematic_14',
                                                                         cinematic_no=14,
                                                                         dirs_data=[1,[-1],['next']]),
                                                            ]
                                                      ),
                                      "Scene 3":Scene(id=[3,3],
                                                      next_id=[3,4],
                                                      gpps=[GPPMap(name='Chap3_e3_map',
                                                                   map='main',
                                                                   spawn='spawn_Magome',
                                                                   path='mgm_tkh',
                                                                   updates=[Update(condition=Condition(type="location",data=['Takahiro']),effect='next')]
                                                                   ),
                                                            GPPCinematic(name='cinematic_15',
                                                                         cinematic_no=15,
                                                                         dirs_data=[2,[1,2],['next','cinematic_16']]),
                                                            GPPFight(name='',
                                                                     bg='bamboo5',
                                                                     ennemies=[self.fa.Senshi],
                                                                     dirs_data=[1,[-1],['cinematic_16']]),
                                                            GPPCinematic(name='cinematic_16',
                                                                         cinematic_no=16,
                                                                         dirs_data=[1,[-1],['next']]),
                                                            ]
                                                      ),
                                      "Scene 4":Scene(id=[3,4],
                                                      next_id=[3,5],
                                                      gpps=[GPPMap(name="Chap3_e4_map",
                                                                   map='main',
                                                                   spawn='spawn_Boss',
                                                                   updates=[Update(condition=Condition(type="event_zone",data=['tkh_end']),effect='next')]
                                                                   ),
                                                            GPPFight(name='Chap3_e4_fight',
                                                                     bg='tkh2',
                                                                     ennemies=[self.fa.guerrier_takahiro,self.fa.guerrier_takahiro2],
                                                                     dirs_data=[1,[-1],['next']]
                                                                     ),
                                                            GPPCinematic(name="cinematic_17",
                                                                         cinematic_no=17,
                                                                         ),
                                                            GPPCinematic(name="cinematic_18",
                                                                         cinematic_no=18,
                                                                         ),
                                                            ]
                                                      ),
                                      "Scene 5":Scene(id=[3,5],
                                                      next_id=[0,0],
                                                      gpps=[GPPFight(name='final_fight',
                                                                     bg="tkh1",
                                                                     ennemies=[self.fa.Takahiro],
                                                                     dirs_data=[1,[-1],['next']]
                                                                     ),
                                                            GPPCinematic(name='cinematic_19',
                                                                         cinematic_no=19,
                                                                         ),
                                                            GPPCinematic(name='cinematic_20',
                                                                         cinematic_no=20,
                                                                         ),
                                                            GPPMap(name='end',
                                                                   map='main',
                                                                   spawn='spawn_Magome',
                                                                   )
                                                            ]
                                                      )
                                      },
                       }
