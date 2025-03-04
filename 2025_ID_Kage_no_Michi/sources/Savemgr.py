#Projet : Kage no Michi
#Auteurs : Alptan Korkmaz, Maxime Rousseaux, Ahmed-Adam Rezkallah, Clément Roux--Bénabou, Cyril Zhao


# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 23:15:19 2025

@author: clementroux--benabou
"""

import os
import json

class Savemgr :
    def __init__ (self):
        self.generic_blank_file ={"blank" : True,
                                  "dead" : False,
                                  "scene" : [0,0],
                                  "level" : 0,
                                  "player_pos" : [13000,9000],
                                  "map" : "main",
                                  "choices" : ['none',0,0,0],
                                  "genocide_ending_events" : 0,
                                  "pacifist_ending_events" : 0,
                                  "inventory" : {'money':0,'weapon':'no_weapon','heal_potions':0},
                                  "hideout_passcode" : "jaimelecoucoustajine"
                                  }
    
    def load (self,savefile):
        ########## Importation des données de sauvegarde ##########
        file = open(os.path.join(savefile),"r+")
        save_data = json.load(file)
        return save_data
    
    def save (self,data, savefile):
        ########## Écriture des données de sauvegarde ##########
        file = open(os.path.join(savefile),"w")
        json.dump(data,file)
        #Pour voir ce qui est sauvegardé :
        #print(data,savefile,file)
    
    def check_saves (self):
        is_folder = os.path.isdir("../data/saves")
        if is_folder == True:
            is_file0 = os.path.isfile("../data/saves/save0.json")
            is_file1 = os.path.isfile("../data/saves/save1.json")
            is_file2 = os.path.isfile("../data/saves/save2.json")
            is_file3 = os.path.isfile("../data/saves/save3.json")
            return True, is_file0, is_file1, is_file2, is_file3
        else:
            return False,False,False,False,False
    
    def rebuild_folder(self):
        os.makedirs("../data/saves")
        self.rebuild_saves([False,False,False,False])
    
    def rebuild_saves (self,saves_states):
        for save in range(4):
            if not saves_states[save]:
                self.save(self.generic_blank_file,f'../data/saves/save{save}.json')
        print("Réparation terminée, veuillez redémarrer le jeu.")
        
    
    def variable_extractor (self, save_data):
        ########## Transformation des données de sauvegarde en variables ##########
        blank = save_data["blank"]
        dead = save_data["dead"]
        scene = save_data["scene"]
        level = save_data["level"]
        player_pos = save_data["player_pos"]
        map = save_data["map"]
        choices = save_data["choices"]
        genocide_ending_events = save_data["genocide_ending_events"]
        pacifist_ending_events = save_data["pacifist_ending_events"]
        inventory = save_data["inventory"]
        hideout_passcode = save_data["hideout_passcode"]
        return blank,dead,scene,level,player_pos,map,choices,genocide_ending_events,pacifist_ending_events,inventory,hideout_passcode

    def variable_compiler (self,blank,dead,scene,level,player_pos,map,choices,genocide_ending_events,pacifist_ending_events,inventory,hideout_passcode):
        ########## Transformation des variables en données de sauvegarde ##########
        save_data = {"blank" : blank,
                     "dead" : dead,
                     "scene" : scene,
                     "level" : level,
                     "player_pos" : player_pos,
                     "map" : map,
                     "choices" : choices,
                     "genocide_ending_events" : genocide_ending_events,
                     "pacifist_ending_events" : pacifist_ending_events,
                     "inventory" : inventory,
                     "hideout_passcode" : hideout_passcode
                     }
        return save_data
        
