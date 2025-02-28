#Projet : Kage no Michi
#Auteurs : Alptan Korkmaz, Maxime Rousseaux, Ahmed-Adam Rezkallah, Clément Roux--Bénabou, Cyril Zhao


# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 23:18:15 2025

@author: clementroux--benabou
"""

import pygame

surfaces_32x32 = {"none":pygame.surface.Surface((32,32)),
                  "placeholder":pygame.image.load("../data/assets/map/32x32_placeholder.png"),
                  "money10":pygame.image.load("../data/assets/map/Pièce_10Y_1.png"),
                  "money20":pygame.image.load("../data/assets/map/Pièce_20Y_1.png"),
                  "money30":pygame.image.load("../data/assets/map/Pièce_30Y_1.png"),
                  "money100":pygame.image.load("../data/assets/map/Pièce_100Y_1.png"),
                  "heal_potion":pygame.image.load("../data/assets/map/Potion_Soin_1.png"),
                  "food1":pygame.image.load("../data/assets/map/Café_1.png"),
                  "food2":pygame.image.load("../data/assets/map/Cerises_1.png"),
                  "food3":pygame.image.load("../data/assets/map/Champignon_1.png"),
                  "food4":pygame.image.load("../data/assets/map/Patate_1.png"),
                  "food5":pygame.image.load("../data/assets/map/Sushi_1.png"),
                  }
