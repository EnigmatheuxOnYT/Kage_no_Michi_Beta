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
        self.found = "Music_Found_Takahiro_Planque.mp3"
        self.choice = "Music_Choice_Aizu.mp3"
        self.zen = "Music_Zen.mp3"
        self.epic = "Music_Epic.mp3"
        self.calmpacific = "Music_CalmPacific_1.mp3"
        self.arrivedine = "Music_ArrivedIne_1.mp3"
        self.retourmagome = "Music_RetourMagome_1.mp3"
        self.stressfull = "Music_BMG_6.mp3"

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
        self.achievement = self.sound("SFX_Achievement_1")
        self.swoosh1 = self.sound("SFX_Swoosh_Bamboo_Katana_1")
        self.swoosh2 = self.sound("SFX_Swoosh_Bamboo_Katana_2")
        self.swoosh3 = self.sound("SFX_Swoosh_Bamboo_Katana_3")
        self.swoosh4 = self.sound("SFX_Swoosh_Bamboo_Katana_4")
        self.scary_effect = self.sound("SFX_ScarryEffect_1")
        self.impact1 = self.sound("SFX_Impact_1")
        self.heartbeat = self.sound("SFX_Heartbeat_1")
        self.struggle = self.sound("SFX_Struggle_1")
        self.anxiety = self.sound("SFX_Anxiety_1")
        self.arbre = self.sound("SFX_arbre")
        self.H_Essoufle = self.sound("SFX_Essoufle")
        self.F_Essoufle = self.sound("SFX_F_Essoufle")
        self.confused = self.sound('SFX_Confused_1')
        self.confused2 = self.sound('SFX_Confused_2')
        self.crowdpanic = self.sound('SFX_CrowdPanic_1')
        self.crowdagony = self.sound('SFX_AgonyCrowd_1')
        self.bodyfalling = self.sound('SFX_BodyFalling_1')
        self.ahah = self.sound('SFX_CrazyLaugh_1')
        self.gasp = self.sound('SFX_Gasp_1')
        self.sigh = self.sound('SFX_Sigh_1')
        self.cough = self.sound('SFX_CoughingMan_1')
        self.oof = self.sound('SFX_Oof_1')
        self.flamme = self.sound("SFX_Flamme")
        self.building = self.sound("SFX_BuildingDestroyed_1.mp3")
        self.galop = self.sound("SFX_galop.mp3")
        self.brise = self.sound("SFX_vent.mp3")
        self.Dialogue_H_1 = self.sound("Homme_Dialogue_1")
        self.Dialogue_H_2 = self.sound("Homme_Dialogue_2")
        self.Dialogue_H_3 = self.sound("Homme_Dialogue_3")
        self.Dialogue_H_4 = self.sound("Homme_Dialogue_4")
        self.Dialogue_F_1 = self.sound("Femme_Dialogue_1")
        self.Dialogue_F_2 = self.sound("Femme_Dialogue_2")
        self.Dialogue_F_3 = self.sound("Femme_Dialogue_3")
    
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
    
