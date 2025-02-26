#Projet : Kage no Michi
#Auteurs : Alptan Korkmaz, Clément Roux--Bénabou, Maxime Rousseaux, Ahmed-Adam Rezkallah, Cyril Zhao


# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 20:06:16 2025

@author: clementroux--benabou
"""

import pygame
from map.src.game import Game_map



if __name__ == "__main__":
     pygame.init()
     icon = pygame.image.load("../data/assets/common/Icone_LOGO_V12.ico")
     pygame.display.set_icon(icon)
     cursor = pygame.image.load("../data/assets/common/Souris_V4.png")
     pygame.mouse.set_cursor((5, 5), cursor)
     screen = pygame.display.set_mode((1280, 720))
     pygame.display.set_caption("Kage no michi - Carte")
     game_map = Game_map(screen)
     game_map.run()
     pygame.quit()