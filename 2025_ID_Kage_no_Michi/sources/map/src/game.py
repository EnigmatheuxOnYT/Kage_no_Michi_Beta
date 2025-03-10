#Projet : Kage no Michi
#Auteurs : Alptan Korkmaz, Maxime Rousseaux, Ahmed-Adam Rezkallah, Clément Roux--Bénabou, Cyril Zhao


import Loading
import pygame
import pytmx
import pyscroll
from map.src.player2 import Player,Follower
from map.src.map import MapManager

class Game_map:

    def __init__(self,screen,load_only=[False]):

        self.screen = screen
        
        self.clock = pygame.time.Clock()
        
        # Générer le joeur
        if not load_only[0]:
            Loading.display_loading(screen, 68,"Chargement du joueur")
        self.player = Player()
        self.followers = {"KM":Follower("Keiko"),"KT":Follower("Takeshi"),'none':None}
        self.current_follower = self.followers["none"]
        if not load_only[0]:
            Loading.display_loading(screen, 69,"Chargement des cartes")
        self.map_manager = MapManager(self.screen, self.player,load_only=load_only)
        if not load_only[0]:
            Loading.display_loading(screen, 79,"Finalisation")
        self.sprinting = False
    
    def reload (self):
        for map in list(self.map_manager.maps.values()):
            layer = map.default_layer
            map_data = pyscroll.data.TiledMapData(map.tmx_data)
            map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
            map_layer.zoom = 2
            group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=layer)
            group.add(self.player)
            group.change_layer(self.player,layer)

            #recuperer tous les npcs pour les ajouter au groupe
            for npc in map.npcs:
                npc.reload()
                group.add(npc)
                group.change_layer(npc, layer-1)
                npc.give_layer(layer-1)
            
            for displayzone in map.display_zones:
                group.add(displayzone)
            map.group = group

            for sprite in map.group.sprites():
                sprite.direction = ""
        self.map_manager.teleport_player_spawn()
        self.map_manager.teleport_npcs()

    def set_follower(self,name):
        self.current_follower=self.followers[name]
        if self.current_follower!=None:
            self.current_follower.init_pos(self.player.position,self.player.speed)
            for map in list(self.map_manager.maps.values()):
                if map.has_follower:
                    map.group.add(self.current_follower)
                    map.group.change_layer(self.current_follower,map.default_layer-1)

    def handle_input(self,running=True,from_game=False):
        
        if not from_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
        
        pressed = pygame.key.get_pressed()
        
        if self.sprinting and not (pressed[pygame.K_RSHIFT] or pressed[pygame.K_LSHIFT]):
            self.player.sprint(False)
            self.sprinting = False
        elif not self.sprinting and (pressed[pygame.K_RSHIFT] or pressed[pygame.K_LSHIFT]):
            self.player.sprint(True)
            self.sprinting = True
        
        direction = ""
        
        if pressed[pygame.K_UP]:
            direction += 'up'
        elif pressed[pygame.K_DOWN]:
            direction += 'down'
        if pressed[pygame.K_RIGHT]:
            direction += 'right'
        elif pressed[pygame.K_LEFT]:
            direction += 'left'
        
        if direction != "":
            self.player.set_dir(direction)
            self.player.move_dir(direction,step=1)
            self.map_manager.update()
            self.player.save_location()
            self.player.move_dir(direction,step=2)
        
        
        
        #if pressed[pygame.K_F11]:
        #    pygame.display.toggle_fullscreen()
        #    self.clock.tick(5)


        if not from_game:
            return running


    def update(self):
        self.map_manager.update()
        if self.map_manager.get_map().has_follower and self.current_follower!=None:
            self.current_follower.update_move(self.player.position,self.player.speed)


    def run(self):

        #boucle du jeu
        running = True

        # Clock
        while running:

            self.player.save_location()
            running = self.handle_input(running)
            self.update()
            self.map_manager.draw()
            #pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()
