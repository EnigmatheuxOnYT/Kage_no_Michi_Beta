#Projet : Kage no Michi
#Auteurs : Alptan Korkmaz, Clément Roux--Bénabou, Maxime Rousseaux, Ahmed-Adam Rezkallah, Cyril Zhao

#interr
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 00:01:49 2025

@author: clementroux--benabou
"""
import Loading
import pygame
import sys
import random
import math
from Savemgr import Savemgr
from Cinematics import Cinematics
from Commands import Commands
from Mini_jeu_survivants import minigm_survivors
from Mini_jeu_Tuto_Combat import minigm_tutofight
from Mini_jeu_epreuve_combat import minigm_trial1
from Mini_jeu_marchandage import minigm_trade
from Mini_jeu_piege_environnemental import minigm_minesweeper
from Mini_jeu_persuasion import minigm_persuade
from Mini_jeu_filature import minigm_follow
from Mini_jeu_reconstruction import minigm_mastermind
from Mini_jeu_collecte import minigm_collect
from Mini_jeu_sauvetage import minigm_MashingGame
from Audio import Music,Sound
from Gameplay import Story
from map.src.game import Game_map
from map.src.Map_objects import Path,paths_list
from Fight import Fight
from Fight_assets import Fight_assets,Perso,Weapon

class Game:
    
    def __init__ (self,screen):
        self.screen_for_game = screen
        Loading.display_loading(screen, 36,"Lancement des modules secondaires")
        self.cmd = Commands()
        Loading.display_loading(screen, 40,"Lancement des modules mini-jeux")
        self.minigm_01 = minigm_survivors()
        Loading.display_loading(screen, 43,"Lancement des modules mini-jeux")
        self.minigm_02 = minigm_persuade()
        Loading.display_loading(screen, 46,"Lancement des modules mini-jeux")
        self.minigm_03 = minigm_tutofight()
        Loading.display_loading(screen, 49,"Lancement des modules mini-jeux")
        self.minigm_04 = minigm_trial1()
        Loading.display_loading(screen, 52,"Lancement des modules mini-jeux")
        self.minigm_05 = minigm_follow(screen)
        Loading.display_loading(screen, 55,"Lancement des modules mini-jeux")
        self.minigm_06 = minigm_trade()
        Loading.display_loading(screen, 58,"Lancement des modules mini-jeux")
        self.minigm_07 = minigm_minesweeper()
        Loading.display_loading(screen, 61,"Lancement des modules mini-jeux")
        self.minigm_08 = minigm_mastermind()
        Loading.display_loading(screen, 64, "Lancement des modules mini-jeux")
        self.minigm_09 = minigm_collect(screen)
        Loading.display_loading(screen, 67, "Lancement des modules secondaires")
        self.minigm_10 = minigm_MashingGame()
        self.music = Music()
        self.loaded_save = -1
        Loading.display_loading(screen, 67,"Lancement du module de sauvegarde")
        self.savemgr = Savemgr()
        self.story=Story()
        Loading.display_loading(screen, 67,"Lancement du module de cinématiques")
        self.cinematics = Cinematics()
        self.fight = Fight()
        self.fight_assets = Fight_assets()
        self.fighter = self.fight_assets.Musashi
        self.allies = []
        Loading.display_loading(screen, 67,"Lancement du module de la carte")
        self.map_screen_surface = pygame.surface.Surface((1280,720))
        self.map = Game_map(self.map_screen_surface)
        self.paths = self._get_paths(paths_list)
        self.current_path=self.paths[0]
        Loading.display_loading(screen, 80,"Finalisation")
        self.fps_showed = False
        self.passcodes = ["LuneNoire",
                          "FeuDévorant",
                          "Tonnerre",
                          "OmbreProfonde",
                          "Sabre de Minuit",
                          "Aube Sanglante",
                          "Silence de Fer"]
        
        
        self.arrow = pygame.image.load("../data/assets/minigm/Flèche_Directionnelle_Bas.png").convert_alpha()
        self.current_arrow_rect= pygame.Rect(541,380,99,99)
        self.draw_arrow=False
        self.current_arrow_surface = self.arrow
        self.arrow_mode='spawn'

        self.display_fire=False

        self.money_counter_surface=pygame.image.load("../data/assets/minigm/Barre_Reponse.png").convert_alpha()
        self.money_counter_rect=pygame.Rect(1000,0,280,60)
        self.money_rect=pygame.Rect(1020,20,240,20)
        self.fontMFMG20=pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf",20)

        self.devmode=False
        self.in_gameplay=False

        self.current_interaction = {"is":False,"interaction":None}
        self.current_interration = 0

        self.scene=[0,0]
        self.location="wild"
        self.choice1timer = 0

    @property
    def current_playing_scene(self):return self.story.scenes[f'Chapitre {self.scene[0]}'][f'Scene {self.scene[1]}']
    @property
    def current_arrow_point_coordinates(self):
        if self.arrow_mode == 'spawn':
            return self.get_spawn()
        elif self.arrow_mode=='path':
            if self.current_path.over:
                self.draw_arrow=False
            point = self.current_path.get_current_point(self.get_pos())
            return [point.x,point.y]
        elif self.arrow_mode=='target':
            return self.current_arrow_target
    
            



    def get_pos(self): return self.map.player.position
    
    ############### Chargement ###############
    
    def load_save(self, screen, loading_save):
        ########## Récupération des données de sauvegarde pour lancer le jeu ##########
        self.screen_for_game = screen
        if self.loaded_save == 0:
            save_data = self.savemgr.load("../data/saves/save0.json")
        elif self.loaded_save == 1:
            save_data = self.savemgr.load("../data/saves/save1.json")
        elif self.loaded_save == 2:
            save_data = self.savemgr.load("../data/saves/save2.json")
        elif self.loaded_save == 3:
            save_data = self.savemgr.load("../data/saves/save3.json")
        else:
            print("Erreur, sauvegarde inexistante")
        
        self.load_player_data(save_data)
        
        in_game = True

        if self.loaded_save == 0:
            self.blank = False
            self.in_gameplay=True
        
        if self.loaded_save != 0:            
            if self.dead:
                self.death()
                self.in_gameplay = False
                in_game = False
                self.save_savefile()
            elif self.lost:
                self.cinematics.final_loose(screen)
                self.in_gameplay = False
                in_game = False
                self.save_savefile()
        
        
        pygame.mouse.set_visible(False)
        
        loading_save = False
        print(f"Sauvegarde {self.loaded_save} chargée")
        
        
        return loading_save,in_game

    
    def begin (self):
        self.current_passcode = random.choice(self.passcodes)
        self.blank = False
        self.scene=[0,1]
        self.tpt = {'main':self.fight_assets.Musashi,'allies':[]}
        self.fighter=self.fight_assets.Musashi
        self.allies=[]
    
    def get_fps_showed(self): return self.fps_showed
    
    def save_savefile(self):
        ########## Sauvegarde ##########
        tpt = {'main':self.fighter.wrapped(),'allies':[ally.wrapped() for ally in self.allies]}
        self.scene = self.current_playing_scene.id
        self.player_pos = self.get_pos()
        self.inventory={'money':self.money,'weapon':self.current_weapon,'heal_potions':self.heal_potions_count}
        dead = [self.dead,self.lost]
        save_data = self.savemgr.variable_compiler(self.blank,dead,self.scene,tpt,self.player_pos,self.current_map,self.choices,self.genocide_ending_events,self.pacifist_ending_events,self.inventory,self.current_passcode)
        self.savemgr.save(save_data,f"../data/saves/save{self.loaded_save}.json")
        print("Sauvegarde effectuée")
    
    def load_player_data(self,save_data):
        self.blank,dead,self.scene,tpt,self.player_pos,self.current_map,self.choices,self.genocide_ending_events,self.pacifist_ending_events,self.inventory,self.current_passcode = self.savemgr.variable_extractor(save_data)
        self.money,self.current_weapon,self.heal_potions_count=self.inventory['money'],self.inventory['weapon'],self.inventory['heal_potions']
        self.dead,self.lost = dead
        self.map.reload()
        self.map.map_manager.change_map(self.current_map,self.player_pos)
        self.map.set_follower(self.choices[0])
        if tpt!=None:
            self.tpt = {'main':Perso(tpt['main'][0],tpt['main'][1],tpt['main'][2],tpt['main'][3],Weapon(tpt['main'][4][0],tpt['main'][4][1],tpt['main'][4][2],tpt['main'][4][2]),tpt['main'][5],tpt['main'][6]),'allies':[Perso(tpt['allies'][i][0],tpt['allies'][i][1],tpt['allies'][i][2],tpt['allies'][i][3],Weapon(tpt['allies'][i][4][0],tpt['allies'][i][4][1],tpt['allies'][i][4][2],tpt['allies'][i][4][3]),tpt['allies'][i][5],tpt['allies'][i][6]) for i in range(len(tpt['allies']))]}
            self.fighter = self.tpt['main']
            self.allies = self.tpt['allies']
        else:
            self.fighter=None
            self.allies = []

    def handle_zone_events(self,events):
        self.display_fire=False
        self.location='wild'
        self.current_interaction = {"is":False,"interaction":None}
        for i in range(len(events)):
            event = events[i]
            
            if event.type == "choice":
                self.choices[event.data[0]]=event.data[1]
                if event.data[0]==0:
                    self.setup_saved(event.data[1])                    
            
            elif event.type == 'cinematic':
                self.launch_cinematic(cinematic=event.data[0])
            
            elif event.type == "minigm":
                self.launch_minigame(minigame=event.data[0])
            
            elif event.type == "map":
                self.change_map_for_game(event.data[0],event.data[1])
            
            elif event.type == "interaction":
                self.current_interaction = {"is":True,"interaction":event.data[0]}
            
            elif event.type == "gpp_next":
                self.next_gpp(event.data[0])
            
            elif event.type=='on_fire':
                self.display_fire = True
            
            elif event.type=='location':
                self.location = event.data[0]
            
            elif event.type=='gpp':
                self.update_scene(event.data)

    def setup_saved (self,saved):
        self.map.set_follower(saved)
        if saved == "KT":
            self.allies.append(self.fight_assets.Takeshi)



    def handle_interaction (self,interaction):
        for npc in self.map.map_manager.get_map().npcs:
            if npc.instance_name==interaction.npc_name:
                __npc = npc
        for _ in range(len(interaction.actions)):
            self.handle_action(interaction.current_action,__npc)
            interaction.next_action()
        if interaction.end():
            __npc.next_interaction()
        self.temporary_storage=None
    
    def handle_action(self,action,__npc):
        if action.type=="NPCDialog":
            if action.is_cinematic:
                self.launch_cinematic(action.no)
            else :
                self.launch_dialog(action.no)
        elif action.type=='NPCTeleport':
            __npc.teleport_coords(action.position)
        elif action.type=='NPCRemove':
            self.map.map_manager.get_group().remove(__npc)
            self.map.map_manager.get_map().npcs.remove(__npc)
        elif action.type=="NPCEndGPP":
            self.next_gpp(action.output)
        elif action.type=='NPCMinigame':
            self.launch_minigame(action.minigame_no)
        elif action.type =='NPCRepeatInteraction':
            pass
            


            
    def arrow_update (self,point=None,coordinates=None):
        screen_rect = self.map.map_manager.get_map().group._map_layer.view_rect
        if coordinates==None:
            if point==None:
                target_point=[0,0]
            else:
                target_point = self.map.map_manager.get_point_pos(point)
        elif point==None:
            target_point=coordinates
        player_pos = self.map.map_manager.player.rect
        
        diffs = [(target_point[0]-player_pos.centerx),(target_point[1]-player_pos.centery)]
        if diffs[0]==0 and diffs[1]==0:
            angle = 0
        else:
            hypotenuse = math.sqrt((diffs[0]**2)+(diffs[1]**2))
            angle = math.degrees(math.asin(diffs[0]/hypotenuse))
        if diffs[1]<0:
            angle=-angle+180
            
        self.current_arrow_surface = pygame.transform.rotate(self.arrow,angle)
        
        self.current_arrow_rect.top = (player_pos.bottom-screen_rect.top)*2+5
        self.current_arrow_rect.left = (player_pos.left-screen_rect.left)*2+5
        
            

    
    def execute (self,command,args):
        if command == 'cinematic':
            self.launch_cinematic(cinematic=args[0])
        elif command == 'tppos':
            self.map.map_manager.teleport_player_pos(args[0],args[1])
        elif command == 'tploc':
            try:
                self.map.map_manager.teleport_player(args[0])
            except:
                print(f"Le point {args[0]} n'existe pas.")
        elif command == 'spawn':
            self.teleport_spawn()
        elif command == 'minigm':
            self.launch_minigame(minigame=args[0],devmode=self.devmode)
        elif command == 'choice':
            i =args[0]-1
            self.choices[i] = args[1]
        elif command == 'speed':
            self.map.player.change_speed(args[0])
        elif command == 'mapno':
            self.change_map_for_game(False,args[0])
        elif command == 'noclip':
            self.map.map_manager.switch_noclip(args[0])
        elif command == 'fps':
            self.fps_showed = args[0]
        elif command == "arrow":
            subtype = args[0]
            if subtype == "state":
                self.draw_arrow = args[1]
            elif subtype == "point":
                try:
                    self.arrow_mode='target'
                    self.current_arrow_target=self.map.map_manager.get_point_pos(args[1])
                except:
                    print("Le point {args[0]} n'existe pas.")
        elif command == "devmode":
            self.devmode=args[0]
        elif command=='money':
            if args[0]!=-0.1:
                self.money=args[0]
        
        self.music.play(fade=500)
    
    def launch_minigame (self,minigame,choices=None,devmode=False):
        
        pygame.mouse.set_visible(True)
        
        if choices==None:
            choices = self.choices
        
        reward = {'money':0,"heal_potion":0}

        victory_state = -1
        
        if minigame == 1:
            self.running,reward = self.minigm_01.run(self.screen_for_game,choices[0],devmode)
        elif minigame == 2:
            self.running,victory_state = self.minigm_02.run(self.screen_for_game,choices[0],devmode)
        elif minigame == 3:
            self.running = self.minigm_03.run(self.screen_for_game,choices[0],devmode)
        elif minigame == 4:
            self.running = self.minigm_04.run(self.screen_for_game,choices[0],devmode)
        elif minigame == 5:
            self.running,victory_state = self.minigm_05.run(self.screen_for_game,choices[0],self.current_passcode,devmode)
        elif minigame == 6:
            self.running,victory_state = self.minigm_06.run(self.screen_for_game,choices[0],devmode)
        elif minigame == 7:
            self.running,victory_state = self.minigm_07.run(self.screen_for_game,choices[0],devmode)
        elif minigame ==8:
            self.running,victory_state = self.minigm_08.run(self.screen_for_game,choices[0],devmode)
        elif minigame ==9:
            self.running,reward = self.minigm_09.run(self.screen_for_game,choices[0],devmode)
        elif minigame == 10:
            self.running = self.minigm_10.run(self.screen_for_game,choices[0])

        self.handle_minigame_output (minigame,victory_state)
        
        self.money+=reward['money']
        self.heal_potions_count+=reward['heal_potion']
        pygame.mouse.set_visible(False)
        return victory_state
    
    def handle_minigame_output (self,minigame,victory_state):
        
        if victory_state != None:
            if minigame == 2:
                if not victory_state:
                    self.lost = True
                    self.save_savefile()
                    self.in_gameplay = False
            elif minigame == 5:
                if victory_state == 'defeat':
                    self.dead = True
                    self.save_savefile()
                    self.in_gameplay = False
                elif victory_state=="perfect_win2":
                    self.genocide_ending_events+=1
            elif minigame == 6:
                self.choices[2] = str(victory_state[-1])
                if victory_state=='loose2':
                    self.money-=100
                elif victory_state=="win2":
                    self.money-=50
            elif minigame == 7:
                pass
            elif minigame == 8:
                pass
            elif minigame == 9:
                pass
        
    
    def launch_cinematic (self,cinematic,choices=None):
        
        pygame.mouse.set_visible(True)
        
        if choices==None:
            choices = self.choices
        
        
        choice=1
        if cinematic == 1:
            self.cinematics.cinematic_01(self.screen_for_game)
            self.choice1timer = pygame.time.get_ticks()
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
            choice = self.cinematics.cinematic_07(self.screen_for_game,choices[0])
            self.choices[1]=choice
            if choice == 1:
                self.pacifist_ending_events+=1
            elif choice == 3:
                self.genocide_ending_events+=1
            self.fighter.set_level(7)
        elif cinematic == 8:
            choice = self.cinematics.cinematic_08(self.screen_for_game,choices[1])
        elif cinematic == 9:
            self.cinematics.cinematic_09(self.screen_for_game,choices[0])
            self.money+=100
            self.fighter.set_level(15)
            self.heal_potions_count += 5
        elif cinematic == 10:
            choice = self.cinematics.cinematic_10(self.screen_for_game,choices[0])
            self.choices[2] = choice
            if choice == 2:
                self.pacifist_ending_events+=1
            elif choice == 4:
                self.genocide_ending_events+=1
        elif cinematic == 11:
            self.cinematics.cinematic_11(self.screen_for_game,choices[0],choices[2])
            if self.choices[2]==4:
                self.death()
        elif cinematic == 12 :
            choice = self.cinematics.cinematic_12(self.screen_for_game,choices[0])
        elif cinematic == 13 :
            self.cinematics.cinematic_13(self.screen_for_game,choices[0])
        elif cinematic == 14 :
            self.cinematics.cinematic_14(self.screen_for_game,choices[0])
        elif cinematic == 15 :
            choice = self.cinematics.cinematic_15(self.screen_for_game,choices[0],choices[2]==3,self.genocide_ending_events>=4)
        elif cinematic == 16 :
            self.cinematics.cinematic_16(self.screen_for_game,choices[0])
        elif cinematic == 17 :
            self.cinematics.cinematic_17(self.screen_for_game,choices[0])
        elif cinematic == 18 :
            self.cinematics.cinematic_18(self.screen_for_game,choices[0])
        elif cinematic == 19 :
            self.cinematics.cinematic_19(self.screen_for_game,choices[0])
        elif cinematic == 20 :
            if self.genocide_ending_events>=4:
                route='genocide'
            elif self.pacifist_ending_events>=3:
                route='pacifist'
            else:
                route = 'neutral'
            self.cinematics.cinematic_20(self.screen_for_game,choices[0],route)
        elif cinematic == 21 :
            choice = self.cinematics.cinematic_21(self.screen_for_game,choices[0])
            if choice == 1:
                self.pacifist_ending_events+=1
            else:
                self.genocide_ending_events+=1
        elif cinematic == 22 :
            self.cinematics.cinematic_22(self.screen_for_game,choices[0])
        elif cinematic == 23:
            self.cinematics.cinematic_23(self.screen_for_game)
        elif cinematic == 25:
            self.cinematics.cinematic_25(self.screen_for_game,choices[0])
        
        pygame.mouse.set_visible(False)
        return choice
        
        
    
    def launch_dialog(self,dialog,choices=None):
        if choices==None:
            choices = self.choices
        
        self.music.play(fade=500)
    
    def launch_fight(self,bg,ennemies):
        state,self.heal_potions_count = self.fight.run(self.screen_for_game,bg,self.fighter,self.allies,ennemies,self.heal_potions_count)
        self.fighter.set_level(self.fighter.level+5)
        return state
    
    def next_gpp(self,output):
        scene = self.current_playing_scene
        scene.next_gpp(output)
        if scene.over:
            self.scene=scene.next_id
        
        if self.loaded_save!=0:
            self.launch_scene()



    def launch_scene(self):
        if self.blank:
            self.begin()
        
        
                        
        if self.dead:
            self.death()
            self.save_savefile()




        self.in_gameplay=False
        scene=self.current_playing_scene
        gpp=scene.current_gpp
        output=-1
        if gpp==None:
            self.in_gameplay=True
            self.next_gpp(-1)
        else:
            if gpp.type=="GPPCinematic":
                output = self.launch_cinematic(gpp.cinematic_no)
                scene.next_gpp(output)
            elif gpp.type=='GPPMinigame':
                output = self.launch_minigame(gpp.minigame_no)
                scene.next_gpp(output)
            elif gpp.type=='GPPMap':
                self.change_map_for_game(True,gpp.map)
                self.map.map_manager.teleport_player(gpp.spawn)
                if gpp.path!=None:
                    self.start_path(gpp.path)
                else:
                    self.arrow_mode='spawn'
                    self.draw_arrow=False
                self.in_gameplay=True
            elif gpp.type == "GPPFight":
                state = self.launch_fight(gpp.bg,gpp.ennemies)
                if state == 'defeat':
                    self.death()
                else:
                    self.next_gpp(state)
            elif gpp.type=='GPPDeath':
                self.death()
        

    def update_scene (self,data=[]):
        gpp=self.current_playing_scene.current_gpp
        if gpp!=None and gpp.type=='GPPMap':
            for update in gpp.updates:
                if update.condition.type=='location':
                    if self.location==update.condition.data[0]:
                        if update.effect=='next':
                            self.next_gpp(-1)
                        else:
                            self.next_gpp(update.effect)
                elif update.condition.type=='event_zone' and data!=[]:
                    if gpp.name==data[0] and update.condition.data[0]==data[1]:
                        if update.effect=='next':
                            self.next_gpp(-1)
                        else:
                            self.next_gpp(update.effect)
            if gpp.name=='IntroChoice' and 10000-pygame.time.get_ticks()+self.choice1timer<=0:
                self.choices[0] = "none"
                self.genocide_ending_events+=1
                self.next_gpp(-1)
        

    def change_map_for_game(self,by_name,map_info):
        if by_name:
            name=map_info
        else:
            name=self.map.map_manager.maps_keys[map_info]
            
        self.current_map = name
        self.map.map_manager.change_map(name)
        self.player_pos = self.get_pos()
        self.arrow_mode='spawn'
    
    def teleport_spawn (self):
        self.map.map_manager.teleport_player_spawn()
        self.player_pos = self.get_pos()
    
    def get_spawn (self):return self.map.map_manager.get_map().spawn
    
    def death (self):
        self.cinematics.final_death(self.screen_for_game,self.choices[0])
        self.dead = True
    
    def _get_paths(self,paths_list):
        paths=[]
        for i in paths_list:
            sub_paths = []
            for sub_path_name in i['sub_paths_names']:
               for sub_path in self.map.map_manager.get_map().sub_paths:
                   if sub_path.name==sub_path_name:
                       sub_paths.append(sub_path)
            points=[]
            for point_name in i['points_names']:
                if point_name in [str(k) for k in range(1,6)]:
                    points.append(self.map.map_manager.get_object(f'path_cross{point_name}'))
                else:
                    points.append(self.map.map_manager.get_object(point_name))
            
            
            path=Path(i['name'],sub_paths,points,i['order'])
            paths.append(path)
        return paths
    
    def start_path(self,path_name):
        self.arrow_mode='path'
        for path in self.paths:
            if path.name==path_name:
                self.current_path=path
        self.draw_arrow=True


    ############### Partie 1 ###############
    
    def game_events (self,in_game, loading_menu):
        ########## Traitement des imputs du joueur en jeu (partie 1) ##########
        self.pressed_keys = pygame.key.get_pressed()
        
        if self.pressed_keys[pygame.K_ESCAPE]:
            self.save_savefile()
            in_game = False
            self.in_gameplay = False
            loading_menu = True
            pygame.mouse.set_visible(True)
        
        elif self.current_interaction['is'] and self.pressed_keys[pygame.K_e]:
            interaction=self.current_interaction["interaction"]
            self.handle_interaction(interaction)
            self.current_interaction = {"is":False,"interaction":None}
        
        elif self.loaded_save == 0:
            if self.pressed_keys[pygame.K_c]:
                self.screen_for_game.blit(self.cmd.warning_message,pygame.Rect(0,0,200,50))
                pygame.display.flip()
                pygame.mouse.set_visible(True)
                self.cmd.terminal()
                pygame.mouse.set_visible(False)
                command,args = self.cmd.translate()
                self.execute(command,args)
            elif self.pressed_keys[pygame.K_q]:
                pygame.quit()
                sys.exit()
        
        if self.in_gameplay:
            self.map.player.save_location()
            self.map.handle_input(from_game=True)

        return in_game, loading_menu
    
    ############### Partie 2 ###############
    
    def game_update (self):
        ########## Mise à jour des éléments du jeu à afficher (partie 2) ##########
        if self.dead or self.lost:
            pygame.mouse.set_visible(True)
            return False
        elif self.in_gameplay:
            self.map.update()
            current_active_events = self.map.map_manager.get_current_active_events()
            if current_active_events != None:
                self.handle_zone_events(current_active_events)
            self.update_scene()
            self.arrow_update(coordinates=self.current_arrow_point_coordinates)
        elif self.loaded_save !=0:
            self.launch_scene()
        return True
    
    ############### Partie 3 ###############
    
    def game_draw (self,screen):
        ########## Dessin du jeu (partie 3) ##########
        if self.in_gameplay:
            self.map.map_manager.draw()
            screen.blit(self.map_screen_surface,(0,0))
            self.draw_overlap(screen)
            if self.draw_arrow:
                self.screen_for_game.blit(self.current_arrow_surface,self.current_arrow_rect)
            #pygame.display.flip() AAAAAAAAAAAA
            return True
        return False
    
    def draw_overlap (self,screen):
        money_surface=self.fontMFMG20.render(str(self.money),False,"black")

        screen.blit(self.money_counter_surface,self.money_counter_rect)
        screen.blit(money_surface,self.money_rect)
        if self.display_fire:
            surf=pygame.surface.Surface((1280,720))
            surf.fill("red")
            surf.set_alpha(50)
            screen.blit(surf,pygame.Rect(0,0,1280,720))
        pygame.display.flip()


            