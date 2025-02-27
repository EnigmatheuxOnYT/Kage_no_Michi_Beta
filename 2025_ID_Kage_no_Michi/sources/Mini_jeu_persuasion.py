#Projet : Kage no Michi
#Auteurs : Alptan Korkmaz, Clément Roux--Bénabou, Maxime Rousseaux, Ahmed-Adam Rezkallah, Cyril Zhao

# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 09:21:06 2025

@author: ahmed-adamrezkallah & alptankorkmaz
"""

import pygame
import random
from Cinematics import Cinematics
from Audio import Music,Sound

#########################################
# Classe Particle (pour les effets visuels)
#########################################
class Particle:
    def __init__(self, pos):
        self.pos = [pos[0], pos[1]]
        self.vel = [random.uniform(-1.5, 1.5), random.uniform(-3, -1)]
        self.lifetime = random.uniform(0.5, 1.0)
        self.timer = 0
        self.size = random.randint(3, 6)
        self.color = (255, 255, 0)  # Jaune

    def update(self, dt):
        self.timer += dt
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

    def draw(self, surface):
        alpha = max(0, 255 * (1 - self.timer / self.lifetime))
        surf = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
        pygame.draw.circle(surf, self.color + (int(alpha),), (self.size, self.size), self.size)
        surface.blit(surf, (self.pos[0]-self.size, self.pos[1]-self.size))

#########################################
# Classe minigm
#########################################
class minigm_persuade:
    
    def __init__(self):
        ### Etats du mini-jeu ###
        self.running = True      # Le jeu tourne
        self.playing = False     # Le mini-jeu est lancé
        self.in_minigm = False   # La phase de gameplay est passive
        
        ### Appel de la classe Cinematics ###
        self.cin = Cinematics()
        self.music = Music()
        
        ### Importation de la police d'écriture pour les dialogues
        self.font_MFMG30 = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf", 30)
        
        ### Paramètres de la fenêtre ###
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720
        
        # Pour appliquer des effets sur l'ensemble de l'affichage
        self.game_surface = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
        ### Horloge pour le delta time ###
        self.clock = pygame.time.Clock()
        
        ### Variables de jeu ###
        self.question_number = 0
        self.bonnes_reponses = 0
        self.state = "question"      # états possibles : "question", "feedback", "fade_out", "fade_in", "result"
        self.feedback_timer = 0
        self.fade_alpha = 0
        self.fade_duration = 0.5
        self.flash_timer = 0
        self.flash_color = (0, 0, 0)
        self.screen_shake_timer = 0
        self.shake_intensity = 5
        self.particles = []
        
        # Variables pour stocker la réponse saisie lors d'un tour
        self.answer_chosen = None
        self.button_index = None
        
        # Rectangle pour le bandeau d'explications
        self.explications_rect = pygame.Rect(0, 670, 1280, 50)
        
        ### Chargement des ressources et des données du jeu ###
        self.load_assets()
    
    ########## Démarrage du mini-jeu ##########
    def load(self):
        self.playing = True
        self.music.play(self.music.intro)
        # Les ressources ont déjà été chargées dans __init__
    
    def load_assets(self):
        # --- Chargement des images ---
        self.fond_dojo = pygame.image.load('../data/assets/bgs/Ine_Dojo_1.png').convert()
        
        self.boutons_reponses = [
            pygame.image.load('../data/assets/minigm/Bouton_Cercle.png').convert_alpha(),
            pygame.image.load('../data/assets/minigm/Bouton_Carre.png').convert_alpha(),
            pygame.image.load('../data/assets/minigm/Bouton_Triangle.png').convert_alpha(),
            pygame.image.load('../data/assets/minigm/Bouton_Croix.png').convert_alpha()
        ]
        
        self.boutons_pressed = [
            pygame.image.load('../data/assets/minigm/Bouton_Cercle_Appuye.png').convert_alpha(),
            pygame.image.load('../data/assets/minigm/Bouton_Carre_Appuye.png').convert_alpha(),
            pygame.image.load('../data/assets/minigm/Bouton_Triangle_Appuye.png').convert_alpha(),
            pygame.image.load('../data/assets/minigm/Bouton_Croix_Appuye.png').convert_alpha()
        ]
        
        self.reponses_parchemin = pygame.image.load('../data/assets/minigm/Parchemin_Reponses.png').convert_alpha()
        self.parchemin_question_UI = pygame.image.load('../data/assets/minigm/Parchemin_Question.png').convert_alpha()
        
        # --- Chargement des sprites des personnages ---
        sprite_shikisha_musashi = pygame.image.load('../data/assets/cinematics/characters/Shikisha_16bit_Gauche_SansArme_V1.png').convert_alpha()
        sprite_sensei_hoshida = pygame.image.load('../data/assets/cinematics/characters/Hoshida_16bit_Droite_SansArme_V1.png').convert_alpha()
        self.new_sprite_musashi = pygame.transform.scale(sprite_shikisha_musashi, (235, 550))
        self.new_sprite_hoshida = pygame.transform.scale(sprite_sensei_hoshida, (255, 550))
        
        # --- Chargement des sons ---
        self.sound_button = pygame.mixer.Sound('../data/assets/sounds/SFX_ClickSound_2.mp3')
        self.sound_correct = pygame.mixer.Sound('../data/assets/sounds/SFX_Correct_1.mp3')
        self.sound_incorrect = pygame.mixer.Sound('../data/assets/sounds/SFX_ClickSound_1.mp3')
        
        
        # --- Chargement des polices ---
        self.font_question = pygame.font.Font('../data/assets/fonts/MadouFutoMaruGothic.ttf', 52)
        self.font_reponse = pygame.font.Font('../data/assets/fonts/MadouFutoMaruGothic.ttf', 20)
        self.font_explications = pygame.font.Font('../data/assets/fonts/MadouFutoMaruGothic.ttf', 24)
        self.font_qcm = pygame.font.Font('../data/assets/fonts/MadouFutoMaruGothic.ttf', 54)
        self.font_resultats = pygame.font.Font('../data/assets/fonts/MadouFutoMaruGothic.ttf', 100)
        
        # --- Données du jeu ---
        self.texte_explications = "Appuyer sur les touches &, é, \", ' ou clic gauche sur l'un des 4 boutons pour répondre!"
        
        self.questions = [
            "Comment se nomme le village dont tu proviens?",
            "Quels sont les trois valeurs principales du \ncode Bushido?",
            "Quelle est la signification du mot 'Bushido'?",
            "Quel est le principal rôle des samouraïs \ndans la société japonaise?",
            "Quelle est l'arme traditionnelle \nla plus associée aux samouraïs?",
            "Quelle pratique était couramment utilisée \npar les samouraïs pour cultiver \nla concentration et la paix intérieure?",
            "Quelle forme d'art était pratiquée par \nles samouraïs en plus de leur \nformation martiale?",
            "Comment appelle-t-on le rituel d'exécution \nhonorifique des samouraïs s'ils s'avèrent\n infidèles au code 'Bushido' ?",
            "Quelle est la signification profonde \ndu concept de 'Mushin' (無心) dans la \npratique des arts martiaux samouraïs ?",
            "Dans la philosophie du Bushido, \ncomment un samouraï doit-il traiter \nses ennemis vaincus ?"
        ]
        
        self.reponses = [
            ["Ine", "Saitama", "Magome", "Hokkaido"],
            ["Rectitude, \nCourage et \nHonneur", "Liberté, \négalité, \nfraternité", "Père, \nFils, \nSaint-Esprit", "Loyauté, \nBravoure et \nRespect"],
            ["La voie \nde la sagesse", "La voie \nde la guerre", "La voie \nde l'épée", "La voie \ndu guerrier"],
            ["Artisans", "Marchands", "Guerriers", "Paysans"],
            ["Nunchaku", "Katana", "Arc", "Lance"],
            ["Méditation \nZen", "Yoga", "Tai Chi", "Pilates"],
            ["Peinture", "Caligraphie", "Musique", "Danse"],
            ["Seppuku", "Harakiri", "Kamikaze", "Hara"],
            ["La maîtrise \nparfaite des \ntechniques \nde combat", "L'état de \nnon-esprit, \noù l'esprit \nest libre de\ntoute pensée \nconsciente", "L'importance \nde l'honneur \net de la \nréputation", "Le respect \nabsolu \nenvers les \nmaîtres"],
            ["Les exécuter \npour montrer \nsa force", "Les humilier \npubliquement \npour\nrenforcer sa \nréputation", "Les traiter \navec respect \net compassion", "Les réduire \nen esclavage \npour servir \nde leçon"]
        ]
        
        self.reponses_admises = ["C", "A", "D", "C", "B", "A", "B", "A", "C", "C"]
        self.lettres_qcm = ["A", "B", "C", "D"]
        
        self.button_coords = [
            (290, 455),  # Bouton A
            (490, 455),  # Bouton B
            (690, 455),  # Bouton C
            (890, 455)   # Bouton D
        ]
    
    ########## Intro / Fin ##########
    def intro(self, screen, saved):
        # Appel de la cinématique d'intro
        if saved=='none':
            self.cin.cinematic_frame(screen, 'mgm1', 2, "Sensei Hoshida... Je suis prêt à tout pour devenir un véritable samourai.", "Dites-moi ce que je dois faire !", kind_info=[["SM","no_weapon"],["SH", "no_weapon"], 1], running=self.running)
            self.cin.cinematic_frame(screen, 'mgm1', 2, "Bien. Sache qu'un entraînement rigoureux t'attend. Mais avant de commencer,", "prouve-moi ta détermination.", "Pourquoi devrais-je consacrer mon temps à t'enseigner l'art du sabre ?", kind_info=[["SM","no_weapon"],["SH", "no_weapon"], 2], running=self.running)
            self.cin.cinematic_frame(screen, 'mgm1', 2, "Parce que sans votre aide, je ne pourrai jamais protéger ceux qui me sont", "chers... ni honorer la mémoire de mon village.", "Je vous en supplie, laissez-moi prouver ma valeur !", kind_info=[["SM","no_weapon"],["SH", "no_weapon"], 1], running=self.running)
            self.cin.cinematic_frame(screen, 'mgm1', 2, "Hmph. Ton ambition est certaine, mais elle n'est rien sans discipline.", "Je vais te poser une série de questions pour jauger ta sincérité et ta", "capacité à réfléchir sous pression.", kind_info=[["SM","no_weapon"],["SH", "no_weapon"], 2], running=self.running)
            self.cin.cinematic_frame(screen, 'mgm1', 2, "Réponds correctement, et je t'enseignerai tout ce que je sais.", "Échoue... et je te renverrai à ta vie d'avant.", kind_info=[["SM","no_weapon"],["SH", "no_weapon"], 2], running=self.running)
            self.cin.cinematic_frame(screen, 'mgm1', 2, "Shikisha Musashi se tient droit, le regard empli de détermination.", "Sensei Hoshida esquisse un léger sourire, amusé par la fougue du jeune homme.", kind_info=[["SM","no_weapon"],["SH", "no_weapon"], 0], running=self.running)
            #self.cin.cinematic_frame(screen, 'mgm1', 2, "Shikisha Musashi rencontre ainsi Sensei Hoshida, maître samouraï à la retraite", "qui est devenu pêcheur.", kind_info=[["SM","no_weapon"],["SH", "no_weapon"], 0], running=self.running)
            #self.cin.cinematic_frame(screen, 'mgm1', 2, "Après avoir écouté l'histoire de notre héros, il est prêt à enseigner de", "nouveau, à condition qu'il réussisse son épreuve.", kind_info=[["SM","no_weapon"],["SH", "no_weapon"], 0], running=self.running)
            #self.cin.cinematic_frame(screen, 'mgm1', 2, "Pourra-t-il devenir un véritable samouraï ?", "Ce sera à lui de faire ses preuves !", kind_info=[["SM","no_weapon"],["SH", "no_weapon"], 0], running=self.running)
            self.cin.cinematic_frame(screen, 'mgm1', 2, "Bien. Approche. Commençons ton épreuve. ", "Tu veux devenir plus fort, mais la force seule ne suffit pas.", "Montre-moi que tu possèdes l'esprit d'un samouraï.", kind_info=[["SM","no_weapon"],["SH", "no_weapon"], 2], running=self.running)
        elif saved=='KM':
            self.cin.cinematic_frame(screen, 'mgm1', 3, "Sensei Hoshida... Je suis prêt à tout pour devenir un véritable samourai.", "Dites-moi ce que je dois faire !", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 1], running=self.running)
            self.cin.cinematic_frame(screen, 'mgm1', 3, "Bien. Sache qu'un entraînement rigoureux t'attend. Mais avant de commencer,", "prouve-moi ta détermination.", "Pourquoi devrais-je consacrer mon temps à t'enseigner l'art du sabre ?", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 3], running=self.running)
            self.cin.cinematic_frame(screen, 'mgm1', 3, "Parce que sans votre aide, je ne pourrai jamais protéger ceux qui me sont", "chers... ni honorer la mémoire de mon village.", "Je vous en supplie, laissez-moi prouver ma valeur !", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 1], running=self.running)
            self.cin.cinematic_frame(screen, 'mgm1', 3, "Hmph. Ton ambition est certaine, mais elle n'est rien sans discipline.", "Je vais te poser une série de questions pour jauger ta sincérité et ta", "capacité à réfléchir sous pression.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 3], running=self.running)
            self.cin.cinematic_frame(screen, 'mgm1', 3, "Réponds correctement, et je t'enseignerai tout ce que je sais.", "Échoue... et je te renverrai à ta vie d'avant.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 3], running=self.running)
            self.cin.cinematic_frame(screen, 'mgm1', 3, "Shikisha Musashi se tient droit, le regard empli de détermination.", "Sensei Hoshida esquisse un léger sourire, amusé par la fougue du jeune homme.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 0], running=self.running)
            #self.cin.cinematic_frame(screen, 'mgm1', 3, "Shikisha Musashi rencontre ainsi Sensei Hoshida, maître samouraï à la retraite", "qui est devenu pêcheur.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 0], running=self.running)
            #self.cin.cinematic_frame(screen, 'mgm1', 3, "Après avoir écouté l'histoire de notre héros, il est prêt à enseigner de", "nouveau, à condition qu'il réussisse son épreuve.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 0], running=self.running)
            #self.cin.cinematic_frame(screen, 'mgm1', 3, "Pourra-t-il devenir un véritable samouraï ?", "Ce sera à lui de faire ses preuves !", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 0], running=self.running)
            self.cin.cinematic_frame(screen, 'mgm1', 3, "Bien. Approche. Commençons ton épreuve. ", "Tu veux devenir plus fort, mais la force seule ne suffit pas.", "Montre-moi que tu possèdes l'esprit d'un samouraï.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 3], running=self.running)
        elif saved=='KT':
            self.cin.cinematic_frame(screen, 'mgm1', 3, "Sensei Hoshida... Je suis prêt à tout pour devenir un véritable samourai.", "Dites-moi ce que je dois faire !", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["SH", "no_weapon"], 1], running=self.running)
            self.cin.cinematic_frame(screen, 'mgm1', 3, "Bien. Sache qu'un entraînement rigoureux t'attend. Mais avant de commencer,", "prouve-moi ta détermination.", "Pourquoi devrais-je consacrer mon temps à t'enseigner l'art du sabre ?", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["SH", "no_weapon"], 3], running=self.running)
            self.cin.cinematic_frame(screen, 'mgm1', 3, "Parce que sans votre aide, je ne pourrai jamais protéger ceux qui me sont", "chers... ni honorer la mémoire de mon village.", "Je vous en supplie, laissez-moi prouver ma valeur !", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["SH", "no_weapon"], 1], running=self.running)
            self.cin.cinematic_frame(screen, 'mgm1', 3, "Hmph. Ton ambition est certaine, mais elle n'est rien sans discipline.", "Je vais te poser une série de questions pour jauger ta sincérité et ta", "capacité à réfléchir sous pression.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["SH", "no_weapon"], 3], running=self.running)
            self.cin.cinematic_frame(screen, 'mgm1', 3, "Réponds correctement, et je t'enseignerai tout ce que je sais.", "Échoue... et je te renverrai à ta vie d'avant.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["SH", "no_weapon"], 3], running=self.running)
            self.cin.cinematic_frame(screen, 'mgm1', 3, "Shikisha Musashi se tient droit, le regard empli de détermination.", "Sensei Hoshida esquisse un léger sourire, amusé par la fougue du jeune homme.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["SH", "no_weapon"], 0], running=self.running)
            #self.cin.cinematic_frame(screen, 'mgm1', 3, "Shikisha Musashi rencontre ainsi Sensei Hoshida, maître samouraï à la retraite", "qui est devenu pêcheur.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["SH", "no_weapon"], 0], running=self.running)
            #self.cin.cinematic_frame(screen, 'mgm1', 3, "Après avoir écouté l'histoire de notre héros, il est prêt à enseigner de", "nouveau, à condition qu'il réussisse son épreuve.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["SH", "no_weapon"], 0], running=self.running)
            #self.cin.cinematic_frame(screen, 'mgm1', 3, "Pourra-t-il devenir un véritable samouraï ?", "Ce sera à lui de faire ses preuves !", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["SH", "no_weapon"], 0], running=self.running)
            self.cin.cinematic_frame(screen, 'mgm1', 3, "Bien. Approche. Commençons ton épreuve. ", "Tu veux devenir plus fort, mais la force seule ne suffit pas.", "Montre-moi que tu possèdes l'esprit d'un samouraï.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["SH", "no_weapon"], 3], running=self.running)
        
        self.in_minigm = True
    
    def end(self, screen, saved):
        # Appel de la cinématique de fin (à personnaliser)
        if self.bonnes_reponses >= 5:
            if saved=='none' :
                self.cin.cinematic_frame(screen, 'mgm1', 2, "Sensei Hoshida...  j'ai répondu à vos questions avec toute la", "sincérité dont j'étais capable.", kind_info=[["SM","no_weapon"],["SH", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'mgm1', 2, "(légèrement souriant)", "Tes réponses révèlent la force et la détermination d'un véritable samouraï.", " Tu as réussi, Musashi.", kind_info=[["SM","no_weapon"],["SH", "no_weapon"], 2], running=self.running)
                self.cin.cinematic_frame(screen, 'mgm1', 2, "Merci, Sensei !", "Vous ne pouvez pas imaginer combien ces mots me rendent heureux !", "Je ferai tout ce qu'il faut pour honorer cette chance.", kind_info=[["SM","no_weapon"],["SH", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'mgm1', 2, "Tu as réussi cette première épreuve, Musashi.", "Mais souviens-toi : ce n'est que le début.  Reviens demain,", "prêt à débuter cet entraînement sans relâche.", kind_info=[["SM","no_weapon"],["SH", "no_weapon"], 2], running=self.running)
            elif saved=='KM':
                self.cin.cinematic_frame(screen, 'mgm1', 3, "Sensei Hoshida...  j'ai répondu à vos questions avec toute la sincérité", "dont j'étais capable.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'mgm1', 3, "(légèrement souriant)", "Tes réponses révèlent la force et la détermination d'un véritable samouraï.", "Tu as réussi, Musashi.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 3], running=self.running)
                self.cin.cinematic_frame(screen, 'mgm1', 3, "Merci, Sensei !", "Vous ne pouvez pas imaginer combien ces mots me rendent heureux !", "Je ferai tout ce qu'il faut pour honorer cette chance.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'mgm1', 3, "Grand frère, je suis tellement fière de toi !", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 2], running=self.running)
                self.cin.cinematic_frame(screen, 'mgm1', 3, "Tu as réussi cette première épreuve, Musashi.", "Mais souviens-toi : ce n'est que le début.  Reviens demain, prêt à débuter", "cet entraînement sans relâche.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 3], running=self.running)
            elif saved=='KT':
                self.cin.cinematic_frame(screen, 'mgm1', 3, "Sensei Hoshida...  j'ai répondu à vos questions avec toute la sincérité", "dont j'étais capable.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["SH", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'mgm1', 3, "(légèrement souriant)", "Tes réponses révèlent la force et la détermination d'un véritable samouraï.", "Tu as réussi, Musashi.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["SH", "no_weapon"], 3], running=self.running)
                self.cin.cinematic_frame(screen, 'mgm1', 3, "Merci, Sensei !", "Vous ne pouvez pas imaginer combien ces mots me rendent heureux !", "Je ferai tout ce qu'il faut pour honorer cette chance.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["SH", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'mgm1', 3, "Je savais que tu pouvais le faire, mon ami !", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["SH", "no_weapon"], 2], running=self.running)
                self.cin.cinematic_frame(screen, 'mgm1', 3, "Tu as réussi cette première épreuve, Musashi.", "Mais souviens-toi : ce n'est que le début.  Reviens demain, prêt à débuter", "cet entraînement sans relâche.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["SH", "no_weapon"], 3], running=self.running)
        
        else :
            if saved=='none' :
                self.cin.cinematic_frame(screen, 'mgm1', 2, "(Silence) Hmph. Ce n'est pas concluant. Tu n'es pas prêt pour cet", "entraînement. Rentre chez toi, je ne t'entraînerai pas si c'est ce que tu", "penses des samouraïs.", kind_info=[["SM","no_weapon"],["SH", "no_weapon"], 2], running=self.running)
                self.cin.cinematic_frame(screen, 'mgm1', 2, "Je... Je ne pourrai pas venger mon village ?", kind_info=[["SM","no_weapon"],["SH", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'mgm1', 2, "Avoir des objectifs est une bonne chose, mais tu n'as pas compris comment", "s'y prendre. Retourne à ton village.", "Occupe-toi des habitants, ils ont besoin de toi.", kind_info=[["SM","no_weapon"],["SH", "no_weapon"], 2], running=self.running)
                self.cin.cinematic_frame(screen, 'mgm1', 2, "Shikisha Musashi quitte le dojo, l'esprit troublé.", "Il retourne au village, mais le souvenir de ses échecs le hantera", "pour le restant de ses jours.", kind_info=[["SM","no_weapon"],["SH", "no_weapon"], 0], running=self.running)
            elif saved=='KM':
                self.cin.cinematic_frame(screen, 'mgm1', 3, "(Silence) Hmph. Ce n'est pas concluant. Tu n'es pas prêt pour cet", "entraînement. Rentre chez toi, je ne t'entraînerai pas si c'est ce que tu", "penses des samouraïs.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 3], running=self.running)
                self.cin.cinematic_frame(screen, 'mgm1', 3, "Je... Je ne pourrai pas venger mon village ?", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'mgm1', 3, "Avoir des objectifs est une bonne chose, mais tu n'as pas compris comment", "s'y prendre. Retourne à ton village.", "Occupe-toi des habitants, ils ont besoin de toi.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 3], running=self.running)
                self.cin.cinematic_frame(screen, 'mgm1', 3, "Shikisha Musashi quitte le dojo, l'esprit troublé.", "Il retourne au village, mais le souvenir de ses échecs le hantera", "pour le restant de ses jours.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 0], running=self.running)
            elif saved=='KT':
                self.cin.cinematic_frame(screen, 'mgm1', 3, "(Silence) Hmph. Ce n'est pas concluant. Tu n'es pas prêt pour cet", "entraînement. Rentre chez toi, je ne t'entraînerai pas si c'est ce que tu", "penses des samouraïs.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 3], running=self.running)
                self.cin.cinematic_frame(screen, 'mgm1', 3, "Je... Je ne pourrai pas venger mon village ?", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'mgm1', 3, "Avoir des objectifs est une bonne chose, mais tu n'as pas compris comment", "s'y prendre. Retourne à ton village.", "Occupe-toi des habitants, ils ont besoin de toi.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 3], running=self.running)
                self.cin.cinematic_frame(screen, 'mgm1', 3, "Shikisha Musashi quitte le dojo, l'esprit troublé.", "Il retourne au village, mais le souvenir de ses échecs le hantera", "pour le restant de ses jours.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 0], running=self.running)
                
        self.playing= False
    ########## Partie 1 : Évènements ##########
    def minigm_events(self):
        self.answer_chosen = None
        self.button_index = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.event.post(event)
            
            if self.state in ["question", "feedback"]:
                if event.type == pygame.KEYDOWN:
                    if event.unicode == '&':
                        self.answer_chosen = "A"
                        self.button_index = 0
                    elif event.unicode == 'é':
                        self.answer_chosen = "B"
                        self.button_index = 1
                    elif event.unicode == '"':
                        self.answer_chosen = "C"
                        self.button_index = 2
                    elif event.unicode == "'":
                        self.answer_chosen = "D"
                        self.button_index = 3
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        mouse_pos = event.pos
                        for i, coord in enumerate(self.button_coords):
                            btn_rect = self.boutons_reponses[i].get_rect(topleft=coord)
                            if btn_rect.collidepoint(mouse_pos):
                                self.answer_chosen = self.lettres_qcm[i]
                                self.button_index = i
                                self.sound_button.play()
                                break
        
        # Permettre le plein écran avec F11
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_F11]:
            pygame.display.toggle_fullscreen()
            self.clock.tick(5)
    
    ########## Partie 2 : Mise à jour ##########
    def minigm_update(self):
        dt = self.clock.get_time() / 1000.0  # delta time en secondes
        
        # Traitement de la réponse si en phase "question"
        if self.state == "question" and self.answer_chosen is not None:
            if self.answer_chosen == self.reponses_admises[self.question_number]:
                self.bonnes_reponses += 1
                self.flash_color = (0, 255, 0)
                self.sound_correct.play()
                # Générer des particules autour du bouton cliqué
                bx, by = self.button_coords[self.button_index]
                for _ in range(15):
                    self.particles.append(Particle((bx + 50, by + 50)))
            else:
                self.flash_color = (255, 0, 0)
                self.sound_incorrect.play()
                self.screen_shake_timer = 0.3
            self.flash_timer = 0.3
            self.feedback_timer = 0.3
            self.state = "feedback"
            # Réinitialiser la réponse saisie
            self.answer_chosen = None
        
        # Mise à jour des particules
        for p in self.particles[:]:
            p.update(dt)
            if p.timer >= p.lifetime:
                self.particles.remove(p)
        
        # Mise à jour du flash visuel
        if self.flash_timer > 0:
            self.flash_timer -= dt
        
        # Gestion de la machine à états
        if self.state == "feedback":
            self.feedback_timer -= dt
            if self.feedback_timer <= 0:
                self.state = "fade_out"
                self.fade_alpha = 0
        elif self.state == "fade_out":
            self.fade_alpha += 255 * (dt / self.fade_duration)
            if self.fade_alpha >= 255:
                self.fade_alpha = 255
                self.question_number += 1
                if self.question_number >= len(self.questions):
                    self.state = "result"
                else:
                    self.state = "fade_in"
        elif self.state == "fade_in":
            self.fade_alpha -= 255 * (dt / self.fade_duration)
            if self.fade_alpha <= 0:
                self.fade_alpha = 0
                self.state = "question"
    
    ########## Partie 3 : Affichage ##########
    
    def draw_multiline_text(self, surface, text, font, color, rect):
        lines = text.split('\n')
        line_height = font.get_linesize()
        total_height = len(lines) * line_height
        y_offset = rect.y + (rect.height - total_height) // 2
        for line in lines:
            rendered = font.render(line, True, color)
            text_rect = rendered.get_rect(center=(rect.centerx, y_offset + line_height // 2))
            surface.blit(rendered, text_rect)
            y_offset += line_height

    def minigm_draw(self, screen, saved):
        # Réinitialiser la surface de jeu avec le fond
        self.game_surface.blit(self.fond_dojo, (0, 0))
        
        if self.state != "result":
            # Affichage des personnages
            self.game_surface.blit(self.new_sprite_musashi, (8, 350))
            self.game_surface.blit(self.new_sprite_hoshida, (1037, 320))
            
            # Affichage du parchemin de la question et de la question
            self.game_surface.blit(self.parchemin_question_UI, (0, -20))
            question_area = pygame.Rect(0, -20, self.parchemin_question_UI.get_width(), self.parchemin_question_UI.get_height())
            self.draw_multiline_text(self.game_surface, self.questions[self.question_number], self.font_question, (0, 0, 0), question_area)
            
            # Affichage des réponses et de leurs parchemins
            answer_x, answer_y = 250, 235
            for i in range(4):
                self.game_surface.blit(self.reponses_parchemin, (answer_x, answer_y))
                # Lettre QCM
                letter = self.font_qcm.render(self.lettres_qcm[i], True, (0, 0, 0))
                self.game_surface.blit(letter, (answer_x + 70, answer_y + 30))
                # Texte de la réponse (possibilité de multi-ligne)
                lines = self.reponses[self.question_number][i].split('\n')
                line_y = answer_y + 100
                for line in lines:
                    line_render = self.font_reponse.render(line, True, (0, 0, 0))
                    self.game_surface.blit(line_render, (answer_x + 35, line_y))
                    line_y += 20
                answer_x += 200
            
            # Affichage des boutons (avec effet survol / sélection)
            current_mouse_pos = pygame.mouse.get_pos()
            for idx, coord in enumerate(self.button_coords):
                btn_rect = self.boutons_reponses[idx].get_rect(topleft=coord)
                if self.answer_chosen is not None and idx == self.button_index:
                    self.game_surface.blit(self.boutons_pressed[idx], coord)
                elif btn_rect.collidepoint(current_mouse_pos) and self.state == "question":
                    self.game_surface.blit(self.boutons_pressed[idx], coord)
                else:
                    self.game_surface.blit(self.boutons_reponses[idx], coord)
            
            # Affichage du bandeau d'explications
            pygame.draw.rect(self.game_surface, (0, 0, 0), self.explications_rect)
            explications_text = self.font_explications.render(self.texte_explications, True, (255, 255, 255))
            self.game_surface.blit(explications_text, (10, 680))
        else:
            '''# Écran de résultat                                                             #ANCIENS ECRANS DE RESULTATS REMPLACES PAR LES DIALOGUES
            result_rect = self.parchemin_question_UI.get_rect()
            if self.bonnes_reponses >= 5:
                result_text = self.font_resultats.render("Tu es admis!", True, (0, 0, 0))
                
            else:
                result_text = self.font_resultats.render("Tu n'es pas admis!", True, (0, 0, 0))
            result_pos = result_text.get_rect(center=result_rect.center)
            self.game_surface.blit(result_text, result_pos)'''
            
            self.end(screen, saved)
        
        # Affichage des particules
        for p in self.particles:
            p.draw(self.game_surface)
        
        # Affichage du flash de feedback (par-dessus tout)
        if self.flash_timer > 0:
            flash_overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            flash_overlay.set_alpha(int(255 * (self.flash_timer / 0.3)))
            flash_overlay.fill(self.flash_color)
            self.game_surface.blit(flash_overlay, (0, 0))
        
        # Affichage du fondu lors des transitions
        if self.state in ["fade_out", "fade_in"]:
            fade_overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            fade_overlay.fill((0, 0, 0))
            fade_overlay.set_alpha(int(self.fade_alpha))
            self.game_surface.blit(fade_overlay, (0, 0))
        
        # Effet de secousse en cas d'erreur
        shake_offset = [0, 0]
        if self.screen_shake_timer > 0:
            shake_offset[0] = random.randint(-self.shake_intensity, self.shake_intensity)
            shake_offset[1] = random.randint(-self.shake_intensity, self.shake_intensity)
            self.screen_shake_timer -= self.clock.get_time() / 1000.0
        
        # Blit final sur l'écran avec l'offset de secousse
        screen.fill((0, 0, 0))
        screen.blit(self.game_surface, (shake_offset[0], shake_offset[1]))
        pygame.display.flip()
        
    ########## Boucle mini-jeu ##########
    def run(self, screen, saved,devmode=False):
        if devmode:
            print(self.reponses_admises)
        self.load()
        self.intro(screen, saved)
        
        while self.playing and self.running and self.in_minigm:
            self.minigm_events()
            self.minigm_update()
            self.minigm_draw(screen, saved)
            self.clock.tick(60)  # Limite à 60 FPS
        
        if self.playing and self.running:
            self.end(screen, saved)
        
        return self.running

#########################################
# Lancement du mini-jeu
#########################################
if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    
    icon = pygame.image.load("../data/assets/common/Icone_LOGO_V12.ico")
    pygame.display.set_icon(icon)
    cursor = pygame.image.load("../data/assets/common/Souris_V4.png")
    pygame.mouse.set_cursor((5,5), cursor)
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Kage no michi")
    
    mini_game = minigm_persuade()
    mini_game.run(screen, 'KT')
    pygame.quit()
