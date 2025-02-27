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
                  "money_bag":pygame.image.load("../data/assets/map/32x32_placeholder.png"),
                  "heal_potion":pygame.image.load("../data/assets/map/32x32_placeholder.png"),
                  "food1":pygame.image.load("../data/assets/map/32x32_placeholder.png"),
                  "food2":pygame.image.load("../data/assets/map/32x32_placeholder.png"),
                  "food3":pygame.image.load("../data/assets/map/32x32_placeholder.png"),
                  "food4":pygame.image.load("../data/assets/map/32x32_placeholder.png"),
                  "food5":pygame.image.load("../data/assets/map/32x32_placeholder.png"),
                  }