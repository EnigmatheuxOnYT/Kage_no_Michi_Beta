#Projet : Kage no Michi
#Auteurs : Alptan Korkmaz, Clément Roux--Bénabou, Maxime Rousseaux, Ahmed-Adam Rezkallah, Cyril Zhao


# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 18:55:37 2025

@author: clementroux--benabou
"""


import pygame
from Cinematics import Cinematics

class Dialogs(Cinematics):
    def __init__ (self):
        Cinematics.__init__(self)
    
    def dialog_example (self,screen,saved):
        # Tu peux utiliser les foncions de la même façon que dans cinematics (exemple :)
        self.cinematic_frame(screen,"azw1",0,"Exemple")
        output1,output2 = self.choice_frame(screen,"azw1",[0,2],["choix 1","choix 2"])
        if output1=="choice":
            print("Tu as choisi le choix", output2)

if __name__ =="__main__":
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    pygame.display.set_caption("Kage no Michi - Dialogues")
    Dialogs().dialog_example (screen,"KM")
    pygame.quit()