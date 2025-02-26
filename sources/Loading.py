# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 17:31:53 2025

@author: clementroux--benabou
"""
import pygame

pygame.init()
police = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf",70)
dots = "..."
index = 0
        
def display_loading (screen,percent,text=""):
    global index
    loading_text = police.render(f"Chargement{dots[:index]}",False,"white")
    loading_text_rect = loading_text.get_rect()
    loading_text_rect.center=(640,150)
    percent_text = police.render(f"{percent}%",False,"white")
    percent_text_rect = percent_text.get_rect()
    percent_text_rect.center=(640,350)
    text_text = police.render(text,False,"white")
    text_text_rect = text_text.get_rect()
    text_text_rect.center=(640,550)
    screen.fill("black")
    screen.blit(loading_text,loading_text_rect)
    screen.blit(percent_text,percent_text_rect)
    screen.blit(text_text,text_text_rect)
    pygame.display.flip()
    if index==3:
        index=0
    else:
        index+=1