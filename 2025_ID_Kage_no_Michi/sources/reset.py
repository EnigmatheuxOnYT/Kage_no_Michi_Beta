#Projet : Kage no Michi
#Auteurs : Alptan Korkmaz, Clément Roux--Bénabou, Maxime Rousseaux, Ahmed-Adam Rezkallah, Cyril Zhao


# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 16:50:48 2025

@author: clementroux--benabou
"""

import os
import json

# EXÉCUTER INDÉPENDAMMENT DU SCRIPT PRINCIPAL

########## les fonctions load et save sont identiques à celles de Savemgr
def load (savefile):
    file = open(os.path.join(savefile),"r+")
    save_data = json.load(file)
    return save_data

def save ( data, savefile):
    file = open(os.path.join(savefile),"w")
    json.dump(data,file)

def set_save (savefile,dead=False, blank=True, scene=[0,0], level=0, player_pos=[0,0],map="main", choices=[0,0,0,0], genocide_ending_events=0, pacifist_ending_events=0, inventory={},hideout_passcode="jaimelecouscoustajine"):
    ########## Pour modifier une sauvegarde : précisez les infos à mettre à jour en arguments, le reste sera identique à une sauvegarde vide ##########
    data = {"blank" : blank,
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
    save(data,f"../data/saves/save{savefile}.json")

def set_all ():
    ########## Pour définir les données de sauvegarde telles qu'elles sont ci dessous de save0 à save3 (ici, vides) ##########
    save(save0,"../data/saves/save0.json")
    save(save1,"../data/saves/save1.json")
    save(save2,"../data/saves/save2.json")
    save(save3,"../data/saves/save3.json")



generic_blank_file ={"blank" : True,
                     "dead" : False,
                     "scene" : [0,0],
                     "level" : 0,
                     "player_pos" : [0,0],
                     "map" : "main",
#                     "money" : 0,
                     "choices" : ['none',0,0,0],
                     "genocide_ending_events" : 0,
                     "pacifist_ending_events" : 0,
                     "inventory" : {},
                     "hideout_passcode" : "jaimelecouscoustajine"
                     }
    
save0 ={"blank" : False,
        "dead" : False,
       "scene" : [0,0],
       "level" : 0,
       "player_pos" : [0,0],
       "map" : "main",
       "choices" : ['none',0,0,0],
       "genocide_ending_events" : 0,
       "pacifist_ending_events" : 0,
       "inventory" : {},
       "hideout_passcode" : "jaimelecouscoustajine"
       }

save1 ={"blank" : True,
        "dead" : False,
       "scene" : [0,0],
       "level" : 0,
       "player_pos" : [0,0],
       "map" : "main",
       "choices" : ['none',0,0,0],
       "genocide_ending_events" : 0,
       "pacifist_ending_events" : 0,
       "inventory" : {},
       "hideout_passcode" : "jaimelecouscoustajine"
       }

save2 ={"blank" : True,
        "dead" : False,
       "scene" : [0,0],
       "level" : 0,
       "player_pos" : [0,0],
       "map" : "main",
       "choices" : ['KM',0,0,0],
       "genocide_ending_events" : 0,
       "pacifist_ending_events" : 0,
       "inventory" : {},
       "hideout_passcode" : "jaimelecouscoustajine"
       }

save3 ={"blank" : True,
        "dead" : False,
       "scene" : [0,0],
       "level" : 0,
       "player_pos" : [0,0],
       "map" : "main",
       "choices" : ['KT',0,0,0],
       "genocide_ending_events" : 0,
       "pacifist_ending_events" : 0,
       "inventory" : {},
       "hideout_passcode" : "jaimelecouscoustajine"
       }

########## Fonctions à executer (ici réinitialiser) ##########
if __name__ == '__main__':
    set_all()
    #set_save(1,dead=True)