#Projet : Kage no Michi
#Auteurs : Alptan Korkmaz, Maxime Rousseaux, Ahmed-Adam Rezkallah, Clément Roux--Bénabou, Cyril Zhao


import Loading
import pygame
import pytmx
import pyscroll
from map.src.player2 import Player
from map.src.map import MapManager

class Game_map:

    def __init__(self,screen,load_only=[False]):

        self.screen = screen
        
        self.clock = pygame.time.Clock()
        
        # Générer le joeur
        if not load_only[0]:
            Loading.display_loading(screen, 68,"Chargement du joueur")
        self.player = Player()
        if not load_only[0]:
            Loading.display_loading(screen, 69,"Chargement des cartes")
        self.map_manager = MapManager(self.screen, self.player,load_only=load_only)
        if not load_only[0]:
            Loading.display_loading(screen, 79,"Finalisation")
        self.sprinting = False

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
