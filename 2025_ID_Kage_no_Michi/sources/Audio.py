#Projet : Kage no Michi
#Auteurs : Alptan Korkmaz, Clément Roux--Bénabou, Maxime Rousseaux, Ahmed-Adam Rezkallah, Cyril Zhao


# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 17:38:30 2025

@author: clementroux--benabou
"""

import pygame

pygame.mixer.init()
pygame.mixer.music.set_endevent(100)

class Music:
    def __init__ (self):
        self.volume = 0.35
    
        self.placeholder = "Musique_Placeholder.mp3"
        self.menu = "japanese-traditional-festival-164421.mp3"
        self.intro = "Prologue_Theme_V1.mp3"
        self.jeu1 = "Music_Game_1.mp3"
        self.jeu2 = "Music_Game_2.mp3"
        self.mg7 = "Music_BMG_4.mp3"
        self.mg9 = "Musique_Placeholder.mp3"
        self.menu3 = "Music_Menu_3.mp3"
        self.dialog1 = "Music_Dialogue_1.mp3"
        self.exploration = "Music_Exploration_1.mp3"

        #Thèmes :
        self.theme_tkh1 = "Takahiro_Theme_V1.mp3"
    
    def play (self,file="Musique_Placeholder.mp3",fade=500,offset=0):
        if file == "Musique_Placeholder.mp3":
            pass
            #print("musique inconnue")
        is_playing = pygame.mixer.music.get_busy()
        if is_playing:
            pygame.mixer.music.fadeout(fade)
            pygame.mixer.music.queue(f"../data/assets/musics/{file}",loops=-1)
        else:
            pygame.mixer.music.load(f"../data/assets/musics/{file}")
            pygame.mixer.music.play(loops=-1,start=offset,fade_ms=fade)
            pygame.mixer.music.set_pos(offset)
        pygame.mixer.music.set_volume(self.volume)
    
    def set_volume (self,volume):
        self.volume=volume


class Sound:
    
    def __init__(self):
        self.volume=0.35

        self.click = self.sound("SFX_ClickSound_2")
        self.win = self.sound("SFX_Achievement_1")
        self.lose = self.sound("SFX_ClickSound_1")
        self.click1 = self.sound("SFX_ClickSound_1")
        self.error = self.sound("SFX_Wrong_1")
        self.correct1 = self.sound("SFX_Cash_1")
        self.incorrect1 = self.sound("SFX_Wrong_1")
        self.swoosh1 = self.sound("SFX_Swoosh_Bamboo_Katana_1")
        self.swoosh2 = self.sound("SFX_Swoosh_Bamboo_Katana_2")
        self.swoosh3 = self.sound("SFX_Swoosh_Bamboo_Katana_3")
        self.swoosh4 = self.sound("SFX_Swoosh_Bamboo_Katana_4")
        self.scary_effect = self.sound("SFX_ScarryEffect_1")
        self.impact1 = self.sound("SFX_Impact_1")
    
    
    def sound (self,file):
        sound = pygame.mixer.Sound(f"../data/assets/sounds/{file}.mp3")
        sound.set_volume(self.volume)
        return sound
    
    def play (self,sound):
        sound.play()

if __name__ == '__main__':
    music=Music()
    sound=Sound()
    music.play(music.intro)
    sound.play(sound.incorrect2)
    