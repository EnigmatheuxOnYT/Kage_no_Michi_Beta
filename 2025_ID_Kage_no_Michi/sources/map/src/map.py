#Projet : Kage no Michi
#Auteurs : Alptan Korkmaz, Maxime Rousseaux, Ahmed-Adam Rezkallah, Clément Roux--Bénabou, Cyril Zhao


from dataclasses import dataclass

import pytmx.util_pygame
import Loading
import pygame
import pytmx
import pyscroll
import random
import copy

from map.src.Map_objects import *
from map.src.player2 import *
from map.src.Interactions import *
from typing import List,overload


#,[Portal(from_world="Magome cinemaitc", origin_point="Keiko", target_world="MAP PROJET NSI 2025 500x500", teleport_point="spawn_Magome"),
#                             Portal(from_world="Magome cinemaitc", origin_point="Takeshi", target_world="MAP PROJET NSI 2025 500x500", teleport_point="spawn_Magome")]
#         ]

    
        



@dataclass
class Map:
    name : str
    walls : List[pygame.Rect]
    group : pyscroll.PyscrollGroup
    tmx_data : pytmx.TiledMap
    spawn : List[int]
    portals : List[Portal]
    event_zones : List[Event_zone]
    display_zones : List[DisplayZone]
    sub_paths : List[SubPath]
    npcs : List[NPC]
    has_follower : bool
    default_layer : int

class MapManager :

    def __init__(self,screen,player,load_only=[False]):
        self.maps = dict()
        self.screen = screen
        self.player = player
        self.maps_names = {"main":"MAP PROJET NSI 2025 500x500",
                           "intro":"Magome cinematic",
                           "mg5": "Ine_filature",
                           "mg8": "Aizu_collecte",
                           "azw1":"Aizu_detruite"
                           }
        
        self.maps_shortcut = {"MAP PROJET NSI 2025 500x500":"main",
                              "Magome cinematic":"intro",
                              "Ine_filature": "mg5",
                              "Aizu_collecte": "mg8",
                              "Aizu_detruite": "azw1"
                              }
        self.current_active_events = []
        self.maps_keys = list(self.maps_names.keys())
        self.current_map = self.maps_names["main"]
        self.no_clip = False
        if load_only[0]:
            if load_only[1] == "mg5":
                self.register_map("Ine_filature",
                                  spawn_name="spawn",
                                  event_zones=[Event_zone(from_world="Ine_filature", origin_point="Fin", entities=["Player"], events=[Event(type="mgm_end",data=[])]),
                                               Event_zone(from_world="Ine_filature", origin_point="in_sight_1", entities=["Player"], events=[Event(type="mgm_in_sight",data=[1])]),
                                               Event_zone(from_world="Ine_filature", origin_point="in_sight_1b", entities=["Player"], events=[Event(type="mgm_in_sight",data=[1])]),
                                               Event_zone(from_world="Ine_filature", origin_point="in_sight_2", entities=["Player"], events=[Event(type="mgm_in_sight",data=[2])]),
                                               Event_zone(from_world="Ine_filature", origin_point="in_sight_3", entities=["Player"], events=[Event(type="mgm_in_sight",data=[3])]),
                                               Event_zone(from_world="Ine_filature", origin_point="in_sight_2b_3b", entities=["Player"], events=[Event(type="mgm_in_sight",data=[2]),Event(type="mgm_in_sight",data=[3])]),
                                               Event_zone(from_world="Ine_filature", origin_point="in_sight_4", entities=["Player"], events=[Event(type="mgm_in_sight",data=[4])]),
                                               Event_zone(from_world="Ine_filature", origin_point="in_sight_4b", entities=["Player"], events=[Event(type="mgm_in_sight",data=[4])]),
                                               Event_zone(from_world="Ine_filature", origin_point="in_sight_4c", entities=["Player"], events=[Event(type="mgm_in_sight",data=[4])]),
                                               Event_zone(from_world="Ine_filature", origin_point="in_sight_5", entities=["Player"], events=[Event(type="mgm_in_sight",data=[5])]),
                                               Event_zone(from_world="Ine_filature", origin_point="mgm_stop_npc1", entities=["Karasu","Hayato"], events=[Event(type="mgm_stop_npc",data=[1])]),
                                               Event_zone(from_world="Ine_filature", origin_point="mgm_stop_npc2", entities=["Karasu","Hayato"], events=[Event(type="mgm_stop_npc",data=[2])]),
                                               Event_zone(from_world="Ine_filature", origin_point="mgm_stop_npc3", entities=["Karasu","Hayato"], events=[Event(type="mgm_stop_npc",data=[3])]),
                                               Event_zone(from_world="Ine_filature", origin_point="mgm_stop_npc4", entities=["Karasu","Hayato"], events=[Event(type="mgm_stop_npc",data=[4])]),
                                               Event_zone(from_world="Ine_filature", origin_point="mgm_stop_npc5", entities=["Karasu","Hayato"], events=[Event(type="mgm_stop_npc",data=[5])])
                                               ],
                                  npcs=[NPC(name="Karasu", start_pos=[350,158],speed=1.5),
                                        NPC(name="Hayato", start_pos=[414,158],speed=1.5)
                                        ],
                                  layer=3
                                  )
                self.current_map = self.maps_names["mg5"]
            elif load_only[1]== "mg8":
                self.register_map("Aizu_collecte",
                                  spawn_name="spawn",
                                  event_zones=[Event_zone(from_world="Aizu_collecte", origin_point="mgm_leave", entities=["Player"], events=[Event(type="mgm_leave",data=[])]),
                                               Event_zone(from_world="Aizu_collecte", origin_point="mgm_collect_1", entities=["Player"], events=[Event(type="mgm_hotspot",data=[1])]),
                                               Event_zone(from_world="Aizu_collecte", origin_point="mgm_collect_2", entities=["Player"], events=[Event(type="mgm_hotspot",data=[2])]),
                                               Event_zone(from_world="Aizu_collecte", origin_point="mgm_collect_3", entities=["Player"], events=[Event(type="mgm_hotspot",data=[3])]),
                                               Event_zone(from_world="Aizu_collecte", origin_point="mgm_collect_4", entities=["Player"], events=[Event(type="mgm_hotspot",data=[4])]),
                                               Event_zone(from_world="Aizu_collecte", origin_point="mgm_collect_5", entities=["Player"], events=[Event(type="mgm_hotspot",data=[5])]),
                                               Event_zone(from_world="Aizu_collecte", origin_point="mgm_collect_6", entities=["Player"], events=[Event(type="mgm_hotspot",data=[6])]),
                                               Event_zone(from_world="Aizu_collecte", origin_point="mgm_collect_7", entities=["Player"], events=[Event(type="mgm_hotspot",data=[7])]),
                                               Event_zone(from_world="Aizu_collecte", origin_point="mgm_collect_8", entities=["Player"], events=[Event(type="mgm_hotspot",data=[8])]),
                                               Event_zone(from_world="Aizu_collecte", origin_point="mgm_collect_9", entities=["Player"], events=[Event(type="mgm_hotspot",data=[9])]),
                                               Event_zone(from_world="Aizu_collecte", origin_point="mgm_collect_10", entities=["Player"], events=[Event(type="mgm_hotspot",data=[10])])
                                               ],
                                  npcs=[],
                                  layer=2,
                                  placed_correctly=True,
                                  has_follower=True
                                  )
                self.current_map = self.maps_names["mg8"]
        else:
            Loading.display_loading(screen, 69,"Chargement de la carte principale")
            self.register_map("MAP PROJET NSI 2025 500x500",
                              spawn_name="spawn_Magome",
                              event_zones=[Event_zone(from_world="MAP PROJET NSI 2025 500x500",origin_point="entrance_dojo_ine",entities=["Player"], events=[Event(type="gpp",data=["Chap1_e3_map","dojo_ine"])]),
                                           Event_zone(from_world="MAP PROJET NSI 2025 500x500",origin_point="entrance_azw_destroyed",entities=["Player"], events=[Event(type="gpp",data=["Chap2_e3_map","entrance_azw_destroyed"])]),
                                           Event_zone(from_world="MAP PROJET NSI 2025 500x500",origin_point="Ine",entities=["Player"], events=[Event(type="location",data=["ine"])]),
                                           Event_zone(from_world="MAP PROJET NSI 2025 500x500",origin_point="Magome",entities=["Player"], events=[Event(type="location",data=["mgm"])]),
                                           Event_zone(from_world="MAP PROJET NSI 2025 500x500",origin_point="Takahiro",entities=["Player"], events=[Event(type="location",data=["Takahiro"])]),
                                           Event_zone(from_world="MAP PROJET NSI 2025 500x500",origin_point='forest',entities=["Player"],events=[Event(type='location',data=["forest"])]),
                                           Event_zone(from_world="MAP PROJET NSI 2025 500x500",origin_point='Takahiro',entities=["Player"],events=[Event(type='location',data=["Takahiro"])])
                                           ],
                              npcs=[StaticNPC("Hoshida",[96,576],instance=1)],
                              sub_paths=[{'name':'mgm','lengh':3},
                                         {'name':"ine",'lengh':3},
                                         {'name':'river','lengh':2},
                                         {"name":"forest_ine","lengh":3},
                                         {'name':"forest_azw","lengh":3}],
                              layer=8,
                              has_follower=True
                              )
            Loading.display_loading(screen, 77,"Chargement des cartes secondaires")
            self.register_map("Magome cinematic",
                              spawn_name="Spawn_Magome_cinematic",
                              event_zones=[Event_zone(from_world="Magome cinematic", origin_point="Keiko", entities=["Player"], events=[Event(type='choice',data=[0,"KM"]),Event(type='gpp_next',data=[-1])]),
                                           Event_zone(from_world="Magome cinematic", origin_point="Takeshi", entities=["Player"], events=[Event(type='choice',data=[0,"KT"]),Event(type='gpp_next',data=[-1])])
                                           ],
                            npcs=[StaticNPC("Keiko",[352,192]),
                                  StaticNPC("Takeshi",[896,224])
                                  ],
                              layer=7
                              )
            self.register_map("Ine_filature",
                              spawn_name="spawn",
                              event_zones=[Event_zone(from_world="Ine_filature", origin_point="Fin", entities=["Player"], events=[Event(type="mgm_end",data=[])]),
                                           Event_zone(from_world="Ine_filature", origin_point="in_sight_1", entities=["Player"], events=[Event(type="mgm_in_sight",data=[1])]),
                                           Event_zone(from_world="Ine_filature", origin_point="in_sight_1b", entities=["Player"], events=[Event(type="mgm_in_sight",data=[1])]),
                                           Event_zone(from_world="Ine_filature", origin_point="in_sight_2", entities=["Player"], events=[Event(type="mgm_in_sight",data=[2])]),
                                           Event_zone(from_world="Ine_filature", origin_point="in_sight_3", entities=["Player"], events=[Event(type="mgm_in_sight",data=[3])]),
                                           Event_zone(from_world="Ine_filature", origin_point="in_sight_2b_3b", entities=["Player"], events=[Event(type="mgm_in_sight",data=[2]),Event(type="mgm_in_sight",data=[3])]),
                                           Event_zone(from_world="Ine_filature", origin_point="in_sight_4", entities=["Player"], events=[Event(type="mgm_in_sight",data=[4])]),
                                           Event_zone(from_world="Ine_filature", origin_point="in_sight_4b", entities=["Player"], events=[Event(type="mgm_in_sight",data=[4])]),
                                           Event_zone(from_world="Ine_filature", origin_point="in_sight_4c", entities=["Player"], events=[Event(type="mgm_in_sight",data=[4])]),
                                           Event_zone(from_world="Ine_filature", origin_point="in_sight_5", entities=["Player"], events=[Event(type="mgm_in_sight",data=[5])]),
                                           Event_zone(from_world="Ine_filature", origin_point="mgm_stop_npc1", entities=["Karasu","Hayato"], events=[Event(type="mgm_stop_npc",data=[1])]),
                                           Event_zone(from_world="Ine_filature", origin_point="mgm_stop_npc2", entities=["Karasu","Hayato"], events=[Event(type="mgm_stop_npc",data=[2])]),
                                           Event_zone(from_world="Ine_filature", origin_point="mgm_stop_npc3", entities=["Karasu","Hayato"], events=[Event(type="mgm_stop_npc",data=[3])]),
                                           Event_zone(from_world="Ine_filature", origin_point="mgm_stop_npc4", entities=["Karasu","Hayato"], events=[Event(type="mgm_stop_npc",data=[4])]),
                                           Event_zone(from_world="Ine_filature", origin_point="mgm_stop_npc5", entities=["Karasu","Hayato"], events=[Event(type="mgm_stop_npc",data=[5])])
                                           ],
                              npcs=[NPC(name="Karasu", start_pos=[350,158],speed=1.5),
                                    NPC(name="Hayato", start_pos=[414,158],speed=1.5)
                                    ],
                              layer=3
                              )
            self.register_map("Aizu_collecte",
                              spawn_name="spawn",
                              event_zones=[Event_zone(from_world="Aizu_collecte", origin_point="mgm_leave", entities=["Player"], events=[Event(type="mgm_leave",data=[])]),
                                           Event_zone(from_world="Aizu_collecte", origin_point="mgm_collect_1", entities=["Player"], events=[Event(type="mgm_hotspot",data=[1])]),
                                           Event_zone(from_world="Aizu_collecte", origin_point="mgm_collect_2", entities=["Player"], events=[Event(type="mgm_hotspot",data=[2])]),
                                           Event_zone(from_world="Aizu_collecte", origin_point="mgm_collect_3", entities=["Player"], events=[Event(type="mgm_hotspot",data=[3])]),
                                           Event_zone(from_world="Aizu_collecte", origin_point="mgm_collect_4", entities=["Player"], events=[Event(type="mgm_hotspot",data=[4])]),
                                           Event_zone(from_world="Aizu_collecte", origin_point="mgm_collect_5", entities=["Player"], events=[Event(type="mgm_hotspot",data=[5])]),
                                           Event_zone(from_world="Aizu_collecte", origin_point="mgm_collect_6", entities=["Player"], events=[Event(type="mgm_hotspot",data=[6])]),
                                           Event_zone(from_world="Aizu_collecte", origin_point="mgm_collect_7", entities=["Player"], events=[Event(type="mgm_hotspot",data=[7])]),
                                           Event_zone(from_world="Aizu_collecte", origin_point="mgm_collect_8", entities=["Player"], events=[Event(type="mgm_hotspot",data=[8])]),
                                           Event_zone(from_world="Aizu_collecte", origin_point="mgm_collect_9", entities=["Player"], events=[Event(type="mgm_hotspot",data=[9])]),
                                           Event_zone(from_world="Aizu_collecte", origin_point="mgm_collect_10", entities=["Player"], events=[Event(type="mgm_hotspot",data=[10])])
                                           ],
                              npcs=[],
                              layer=2,
                              placed_correctly=True,
                              has_follower=True
                              )
            self.register_map(name="Aizu_detruite",
                              spawn_name="spawn",
                              portals=[],
                              npcs=[NPC(name="Villager1", start_pos=[320,512],nb_points=6,speed=1),
                                    NPC(name="Villager2", start_pos=[1632,1408],nb_points=4,speed=1),
                                    NPC(name="Villager3", start_pos=[1184,1152],nb_points=5,speed=1)
                                    ],
                              event_zones=[Event_zone("Aizu_detruite","exit",["Player"],[Event(type="gpp",data=["Chap3_e1_map","exit"])])],
                              sub_paths=[],
                              layer=8,
                              placed_correctly=True,
                              has_follower=True
                              )
        self.teleport_player_spawn()
        self.teleport_npcs()

    def check_collisions(self):
        if not self.no_clip:
            #portails
            for portal in self.get_map().portals:
                if portal.from_world == self.current_map :
                    point = self.get_object(portal.origin_point)
                    rect = pygame.Rect(point.x,point.y,point.width,point.height)

                    if self.player.feet.colliderect(rect):
                        copy_portal = portal
                        self.current_map = portal.target_world
                        self.teleport_player(copy_portal.teleport_point)
            
            for event_zone in self.get_map().event_zones:
                point = self.get_object(event_zone.origin_point)
                rect = pygame.Rect(point.x,point.y,point.width,point.height)
                if self.player.feet.colliderect(rect) and "Player" in event_zone.entities:
                    self.current_active_events+=event_zone.events
                    
                for npc in self.get_map().npcs:
                    if npc.name in event_zone.entities and npc.feet.colliderect(rect):
                        self.current_active_events+=event_zone.events
            
            for npc in self.get_map().npcs:
                if npc.is_interactible and self.player.feet.colliderect(npc.interaction_rect) and npc.current_interaction is not None:
                    self.current_active_events.append(npc.current_interaction.event)
                if self.player.feet.colliderect(npc.collision_rect):
                    if not npc.is_moving_object:
                        self.player.move_back()
                    #else:
                    #    npc.move_back()
                    #    self.player.move_back()
                
            #collisions
            for sprite in self.get_group().sprites():
                if sprite.is_moving_object and sprite.collidable:
                    if sprite.feet.collidelist(self.get_walls()) > -1 :
                        sprite.move_back()
            
            for object in self.get_map().tmx_data.objects:
                if object.type=="fire":
                    rect=pygame.Rect(object.x,object.y,object.width,object.height)
                    if self.player.feet.colliderect(rect):
                        self.current_active_events.append(Event(type='on_fire',data=[]))
        

    def teleport_player(self,name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()
    
    def teleport_player_pos(self,x,y):
        self.player.position[0] = x
        self.player.position[1] = y
        self.player.save_location()
    
    def teleport_player_spawn(self):
        point=self.get_map().spawn
        self.teleport_player_pos(point[0], point[1])
    
    def change_map(self,name,pos=[0,0]):
        self.current_map = self.maps_names[name]
        if pos == [0,0]:
            pos = self.get_map().spawn
        self.teleport_player_pos(pos[0],pos[1])
        self.teleport_npcs()
         

    def register_map(self,name,spawn_name,portals=[],npcs=[],event_zones=[],sub_paths=[],layer="",placed_correctly=False,has_follower=False):

        # Charger la map tmx
        if placed_correctly:
            tmx_data = pytmx.util_pygame.load_pygame(f"../data/map/map/Cartes/{name}.tmx")
        else:
            tmx_data = pytmx.util_pygame.load_pygame(f"../data/map/map/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # Les collisions
        walls = []

        for obj in tmx_data.objects:
            if obj.type == "collisions":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        
        display_zones=[]

        for layer_name,layer_objects in tmx_data.layernames.items():
            if layer_name== "DisplayZones":
                for object in layer_objects:
                    object_rect = pygame.Rect(object.x,object.y,object.width,object.height)
                    display_zone = DisplayZone(object.type,object.name,object_rect,object,self)
                    display_zones.append(display_zone)
        
        sub_paths_list= self.get_map_subpaths(tmx_data,sub_paths)
                
        #Le point de spawn
        spawn_point = tmx_data.get_object_by_name(spawn_name)
        spawn = [spawn_point.x,spawn_point.y]
        
        # Dessiner les différents calques
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=layer)
        group.add(self.player)
        group.change_layer(self.player,layer)

        #recuperer tous les npcs pour les ajouter au groupe
        for npc in npcs:
            group.add(npc)
            group.change_layer(npc, layer-1)
            npc.give_layer(layer-1)
        
        for displayzone in display_zones:
            group.add(displayzone)

        #Enregistrement de la nouvelle map chargée
        self.maps[name] = Map(name,walls,group,tmx_data,spawn,portals,event_zones,display_zones,sub_paths_list,npcs,has_follower,layer)
    
    def get_map_subpaths(self,tmx_data,sub_paths:list):
        sub_paths_list=[]
        for sub_path in sub_paths:
            sub_path_object = SubPath(name=sub_path['name'])
            sub_path_object._set_points(tmx_data.objects,sub_path['lengh'])
            sub_paths_list.append(sub_path_object)
        return sub_paths_list


    def get_current_map (self): return self.current_map
    
    def get_current_map_shortcut_name (self): return self.maps_shortcut[self.current_map]
    
    def get_pos (self): return self.player.position
    
    def get_point_pos(self,point_name): return [self.get_object(point_name).x,self.get_object(point_name).y]
    
    def get_map(self): return self.maps[self.current_map]

    def get_group(self): return self.get_map().group

    def get_walls(self): return self.get_map().walls

    def get_object(self,name): return self.get_map().tmx_data.get_object_by_name(name)
    
    def get_current_active_events(self):
        events = copy.deepcopy(self.current_active_events)
        self.current_active_events = []
        return events
    
    def switch_noclip(self,state=None):
        if state == None:
            self.no_clip = True if self.no_clip == False else False
        else:
            self.no_clip = state
        print("Noclip activé" if self.no_clip else "Noclip désactivé")

    def teleport_npcs(self):
        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npcs

            for npc in npcs:
                if npc.is_moving_object:
                    npc.load_points(map_data.tmx_data)
                    npc.teleport_spawn()



    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)


    def update(self):
        self.get_group().update()
        self.check_collisions()

        for npc in self.get_map().npcs:
            if npc.is_moving_object:
                npc.move_points()
        self.update_npcs()
    
    def update_npcs(self):
        player_rect = self.player.rect
        for npc in self.get_map().npcs:
            if player_rect.colliderect(npc.rect):
                if npc.rect.centery>=player_rect.centery:
                    self.get_group().change_layer(npc,npc.base_layer+2)
                else:
                    self.get_group().change_layer(npc,npc.base_layer)